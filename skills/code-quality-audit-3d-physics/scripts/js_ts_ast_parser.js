/**
 * js_ts_ast_parser.js
 * Analisador estático estrutural para código JavaScript e TypeScript em motores 3D / WebGL / Three.js.
 *
 * Cobre os Módulos 1, 2 e 3 do Dossiê Técnico:
 * - Módulo 1 (static-sanitization-auditor, w1 = 20%):
 *     ALLOC_IN_LOOP (-30), DUPLICATE_FUNCTION (-20), DEAD_CODE_FUNCTION (-10), UNUSED_VARIABLE (-5)
 * - Módulo 2 (architecture-hardcoded-auditor, w2 = 15%):
 *     PHYSICS_RENDER_COUPLING (-35), RIGID_CONSTRUCTOR (-15), HARDCODED_MAGIC_NUMBER (-10)
 * - Módulo 3 (physics-3d-math-auditor, w3 = 25% + 5 Sub-dimensões S1..S5):
 *     MISSING_DELTA_TIME (-40), UNCHECKED_NORMALIZE (-25), EULER_GIMBAL_LOCK (-20),
 *     STRICT_FLOAT_COMPARE (-15), MISSING_DAMPING (-15)
 */

const fs = require('fs');

function stripCommentsAndStrings(line) {
  return line
    .replace(/\/\/.*$/, '')
    .replace(/'(?:\\.|[^'\\])*'|"(?:\\.|[^"\\])*"|`(?:\\.|[^`\\])*`/g, '""');
}

function computeScores(issues) {
  const penalties = {
    'static-sanitization-auditor': 0,
    'architecture-hardcoded-auditor': 0,
    'physics-3d-math-auditor': 0
  };
  const subdimPenalties = {
    S1_temporal_integration: 0,
    S2_vector_algebra_rotations: 0,
    S3_conservation_stability: 0,
    S4_collision_ccd: 0,
    S5_numerical_robustness: 0
  };

  for (const issue of issues) {
    if (penalties[issue.subskill] !== undefined) {
      penalties[issue.subskill] += issue.penalty || 0;
    }
    if (issue.physics_subdimension && subdimPenalties[issue.physics_subdimension] !== undefined) {
      subdimPenalties[issue.physics_subdimension] += issue.subdimension_penalty || 0;
    }
  }

  const s1 = Math.max(0, 100 - penalties['static-sanitization-auditor']);
  const s2 = Math.max(0, 100 - penalties['architecture-hardcoded-auditor']);
  const s3 = Math.max(0, 100 - penalties['physics-3d-math-auditor']);

  const subdimScores = {
    S1_temporal_integration: Math.max(0, 100 - subdimPenalties.S1_temporal_integration),
    S2_vector_algebra_rotations: Math.max(0, 100 - subdimPenalties.S2_vector_algebra_rotations),
    S3_conservation_stability: Math.max(0, 100 - subdimPenalties.S3_conservation_stability),
    S4_collision_ccd: Math.max(0, 100 - subdimPenalties.S4_collision_ccd),
    S5_numerical_robustness: Math.max(0, 100 - subdimPenalties.S5_numerical_robustness)
  };

  const s3Weighted =
    subdimScores.S1_temporal_integration * 0.25 +
    subdimScores.S2_vector_algebra_rotations * 0.25 +
    subdimScores.S3_conservation_stability * 0.20 +
    subdimScores.S4_collision_ccd * 0.15 +
    subdimScores.S5_numerical_robustness * 0.15;

  return {
    s1_static_sanitization: Number(s1.toFixed(2)),
    s2_architecture_hardcoded: Number(s2.toFixed(2)),
    s3_physics_3d_math: Number(s3.toFixed(2)),
    s3_subdimensions_weighted: Number(s3Weighted.toFixed(2)),
    physics_3d_subdimensions: {
      S1_integracao_temporal_dt: { score: subdimScores.S1_temporal_integration, weight: 0.25 },
      S2_algebra_vetorial_rotacoes: { score: subdimScores.S2_vector_algebra_rotacoes, weight: 0.25 },
      S3_conservacao_estabilidade: { score: subdimScores.S3_conservation_stability, weight: 0.20 },
      S4_colisao_ccd: { score: subdimScores.S4_collision_ccd, weight: 0.15 },
      S5_robustez_numerica_float: { score: subdimScores.S5_numerical_robustness, weight: 0.15 }
    }
  };
}

function analyzeJsTsCode(code, filename = 'script.ts') {
  const issues = [];
  const lines = code.split(/\r?\n/);

  function addIssue({
    id,
    title,
    category,
    subskill,
    severity,
    penalty,
    physics_subdimension = null,
    subdimension_penalty = 0,
    line,
    col,
    description,
    recommendation,
    root_cause = '',
    best_fix_code = '',
    why_best_fix = '',
    expected_result = ''
  }) {
    issues.push({
      id,
      title,
      category,
      subskill,
      severity,
      penalty,
      physics_subdimension,
      subdimension_penalty,
      file: filename,
      line,
      col,
      description,
      recommendation,
      root_cause: root_cause || description,
      best_fix_code,
      why_best_fix: why_best_fix || recommendation,
      expected_result
    });
  }

  let braceDepth = 0;
  let inAnimationLoop = false;
  let loopStartDepth = -1;
  let currentFnName = '';
  let currentFnStartDepth = -1;
  let currentClassName = '';
  let classStartDepth = -1;

  const loopKeywords = ['update', 'render', 'animate', 'tick', 'step', 'requestanimationframe', 'integrate'];
  const allocPattern = /new\s+(THREE\.|BABYLON\.|CANNON\.)?(Vector[234]|Matrix[34]|Quaternion|Euler|Array|Float32Array|Object3D|Box3|Raycaster)\b/g;

  const declaredFunctions = new Map(); // name -> { line, col, bodyLines, exported }
  const functionBodiesNormalized = new Map(); // normalizedBody -> firstFnName
  let activeFnRecord = null;

  lines.forEach((rawLine, index) => {
    const lineNum = index + 1;
    const cleanLine = stripCommentsAndStrings(rawLine);

    // Detectar declaração de classe
    const classMatch = cleanLine.match(/\bclass\s+([A-Za-z0-9_]+)/);
    if (classMatch) {
      currentClassName = classMatch[1];
      classStartDepth = braceDepth;
    }

    // Detectar declaração de função
    const fnDeclMatch =
      cleanLine.match(/\b(?:export\s+)?(?:async\s+)?function\s+([A-Za-z0-9_]+)\s*\(/) ||
      cleanLine.match(/\b(?:export\s+)?(?:const|let|var)\s+([A-Za-z0-9_]+)\s*=\s*(?:async\s*)?\([^)]*\)\s*=>/);

    if (fnDeclMatch) {
      currentFnName = fnDeclMatch[1];
      currentFnStartDepth = braceDepth;
      const isExported = /\bexport\b/.test(cleanLine);
      activeFnRecord = {
        name: currentFnName,
        line: lineNum,
        col: rawLine.indexOf(currentFnName) + 1,
        bodyLines: [],
        exported: isExported
      };
      declaredFunctions.set(currentFnName, activeFnRecord);

      if (loopKeywords.some(kw => currentFnName.toLowerCase().includes(kw))) {
        inAnimationLoop = true;
        loopStartDepth = braceDepth;
      }
    }

    // Detectar laços explícitos ou callbacks de animação
    if (
      /\b(for|while)\s*\(/.test(cleanLine) ||
      cleanLine.includes('requestAnimationFrame') ||
      cleanLine.includes('.setAnimationLoop')
    ) {
      if (!inAnimationLoop) {
        inAnimationLoop = true;
        loopStartDepth = braceDepth;
      }
    }

    if (activeFnRecord && lineNum > activeFnRecord.line) {
      const trimmed = cleanLine.trim();
      if (trimmed && trimmed !== '{' && trimmed !== '}') {
        activeFnRecord.bodyLines.push(trimmed.replace(/\s+/g, ' '));
      }
    }

    // 1. ALLOC_IN_LOOP (Módulo 1)
    if (inAnimationLoop) {
      let match;
      allocPattern.lastIndex = 0;
      while ((match = allocPattern.exec(cleanLine)) !== null) {
        addIssue({
          id: 'ALLOC_IN_LOOP',
          title: 'Alocação de Objeto 3D no Laço de Animação (Garbage Collector Spike)',
          category: 'Sanitização Estática & Memory Cleanup',
          subskill: 'static-sanitization-auditor',
          severity: 'Crítica',
          penalty: 30,
          line: lineNum,
          col: match.index + 1,
          description: `Instanciação '${match[0]}' detectada dentro do laço '${currentFnName || 'render/loop'}'.`,
          recommendation: 'Pré-aloque objetos temporários fora do laço (Scratchpad estático) e reutilize-os com .copy() ou .set().',
          root_cause: 'A criação de instâncias na Heap a cada frame (60-120Hz) pressiona o Garbage Collector da engine JS, causando frame drops e stuttering.',
          best_fix_code: 'const _TEMP_VEC3 = new THREE.Vector3();\nfunction animate(dt) {\n  _TEMP_VEC3.copy(velocity).multiplyScalar(dt);\n  position.add(_TEMP_VEC3);\n}',
          why_best_fix: 'Reduz a taxa de alocação dinâmica para 0 B/s durante a simulação.',
          expected_result: 'Taxa de alocação reduzida para 0 B/s no laço de renderização.'
        });
      }
    }

    // 2. UNCHECKED_NORMALIZE (Módulo 3 / S2)
    if (/\.(normalize|normalized)\s*\(\s*\)/.test(cleanLine)) {
      const prevLine = index > 0 ? lines[index - 1] : '';
      const prev2Line = index > 1 ? lines[index - 2] : '';
      const contextWindow = `${prev2Line} ${prevLine} ${cleanLine}`;
      if (!/length|lengthSq|magnitude|EPSILON|1e-/i.test(contextWindow)) {
        addIssue({
          id: 'UNCHECKED_NORMALIZE',
          title: 'Normalização Sem Checagem de Vetor Nulo',
          category: 'Física 3D & Matemática Numérica',
          subskill: 'physics-3d-math-auditor',
          severity: 'Alta',
          penalty: 25,
          physics_subdimension: 'S2_vector_algebra_rotations',
          subdimension_penalty: 40,
          line: lineNum,
          col: rawLine.indexOf('normalize') + 1,
          description: 'Chamada de .normalize() realizada sem verificar se o comprimento do vetor é maior que EPSILON.',
          recommendation: 'Valide se v.lengthSq() > 1e-12 antes de normalizar para evitar divisão por zero / NaN.',
          root_cause: 'Normalizar um vetor de magnitude zero executa 0 / 0 = NaN, corrompendo as matrizes de transformação da cena 3D.',
          best_fix_code: 'if (dir.lengthSq() > 1e-12) {\n  dir.normalize();\n}',
          why_best_fix: 'Previne divisão por zero usando lengthSq() sem custo extra de raiz quadrada quando o vetor é nulo.',
          expected_result: 'Zero ocorrências de NaN em vetores de direção e velocidade.'
        });
      }
    }

    // 3. MISSING_DELTA_TIME (Módulo 3 / S1)
    if (
      /(pos|position|vel|velocity)\.(x|y|z)\s*\+=/.test(cleanLine) ||
      /(pos|position|vel|velocity)\s*\+=\s*/.test(cleanLine) ||
      /\.(add)\s*\(\s*(vel|velocity)\b/.test(cleanLine)
    ) {
      if (!/dt|delta|deltaTime|fixedDelta|clock\.getDelta|addScaledVector/i.test(cleanLine)) {
        addIssue({
          id: 'MISSING_DELTA_TIME',
          title: 'Atualização Física Sem Delta Time (Dependência de Framerate)',
          category: 'Física 3D & Matemática Numérica',
          subskill: 'physics-3d-math-auditor',
          severity: 'Crítica',
          penalty: 40,
          physics_subdimension: 'S1_temporal_integration',
          subdimension_penalty: 100,
          line: lineNum,
          col: 1,
          description: 'Atribuição aditiva em propriedade física sem multiplicação por dt ou deltaTime.',
          recommendation: 'Multiplique o incremento por delta time (ex: position.addScaledVector(velocity, dt)).',
          root_cause: 'Sem escalar pelo intervalo de tempo real entre quadros, a velocidade física dobra em monitores de 120Hz comparada a 60Hz.',
          best_fix_code: 'entity.position.addScaledVector(entity.velocity, dt);',
          why_best_fix: 'Garante integração cinemática invariante à taxa de quadros e sem alocar vetores intermediários.',
          expected_result: 'Divergência de posição < 0.01m entre 60Hz e 120Hz.'
        });
      }
    }

    // 4. EULER_GIMBAL_LOCK (Módulo 3 / S2)
    if (/rotation\.(x|y|z)\s*\+=/.test(cleanLine)) {
      addIssue({
        id: 'EULER_GIMBAL_LOCK',
        title: 'Acúmulo Contínuo de Rotação via Ângulos de Euler (Gimbal Lock)',
        category: 'Física 3D & Matemática Numérica',
        subskill: 'physics-3d-math-auditor',
        severity: 'Alta',
        penalty: 20,
        physics_subdimension: 'S2_vector_algebra_rotations',
        subdimension_penalty: 50,
        line: lineNum,
        col: rawLine.indexOf('rotation') + 1,
        description: 'Incremento direto em rotation.x/y/z (Euler) detectado.',
        recommendation: 'Utilize Quaternions (quaternion.multiply(deltaQuat).normalize()) para rotações contínuas 3D.',
        root_cause: 'Ângulos de Euler sofrem perda de grau de liberdade (Gimbal Lock) quando o eixo central atinge +-90 graus.',
        best_fix_code: '_DELTA_QUAT.setFromAxisAngle(AXIS_Y, angularSpeed * dt);\nmesh.quaternion.multiply(_DELTA_QUAT).normalize();',
        why_best_fix: 'Garante interpolação e composição rotacional livre de singularidades em SO(3).',
        expected_result: 'Estabilidade rotacional contínua em 3 eixos sem Gimbal Lock.'
      });
    }

    // 5. STRICT_FLOAT_COMPARE (Módulo 3 / S5)
    if (/===?\s*([0-9]+\.[0-9]+)/.test(cleanLine) || /([0-9]+\.[0-9]+)\s*===?/.test(cleanLine)) {
      addIssue({
        id: 'STRICT_FLOAT_COMPARE',
        title: 'Comparação Estrita de Ponto Flutuante (IEEE 754)',
        category: 'Física 3D & Matemática Numérica',
        subskill: 'physics-3d-math-auditor',
        severity: 'Média',
        penalty: 15,
        physics_subdimension: 'S5_numerical_robustness',
        subdimension_penalty: 40,
        line: lineNum,
        col: 1,
        description: "Comparação direta com número de ponto flutuante usando '===' ou '=='.",
        recommendation: 'Utilize tolerância numérica: Math.abs(a - b) < EPSILON.',
        root_cause: 'A representação binária finita IEEE 754 acumula resíduos de arredondamento que impedem igualdade exata.',
        best_fix_code: 'const EPSILON = 1e-6;\nif (Math.abs(a - b) < EPSILON) { /* ... */ }',
        why_best_fix: 'Torna os testes de convergência numérica resilientes a imprecisões de mantissa.',
        expected_result: '100% de confiabilidade em gatilhos numéricos de limite.'
      });
    }

    // 6. PHYSICS_RENDER_COUPLING (Módulo 2)
    if (
      /physics|rigidbody|solver|collider/i.test(currentClassName || currentFnName) &&
      /\b(document\.|window\.|WebGLRenderingContext|THREE\.Mesh|canvas\.getContext)\b/.test(cleanLine)
    ) {
      addIssue({
        id: 'PHYSICS_RENDER_COUPLING',
        title: 'Acoplamento Direto entre Física e DOM/Renderizador 3D',
        category: 'Modularidade & Ausência de Hardcoded',
        subskill: 'architecture-hardcoded-auditor',
        severity: 'Crítica',
        penalty: 35,
        line: lineNum,
        col: 1,
        description: `Rotina física '${currentClassName || currentFnName}' manipula diretamente elementos de DOM/Canvas/Mesh.`,
        recommendation: 'Isole a lógica física em classes puras e sincronize o estado visual em uma camada separada de renderização.',
        root_cause: 'Acoplar física ao DOM impede a execução do motor físico em Web Workers ou testes automatizados Node.js headless.',
        best_fix_code: '// Motor físico puro (sem DOM/Three.Mesh):\nphysicsBody.step(dt);\n// Sincronizador visual:\nmesh.position.copy(physicsBody.position);',
        why_best_fix: 'Habilita offloading da simulação para Web Workers e testes determinísticos fora do browser.',
        expected_result: 'Motor de física 100% desacoplado e testável em ambiente headless.'
      });
    }

    // 7. HARDCODED_MAGIC_NUMBER (Módulo 2)
    const magicMatch = cleanLine.match(/[\*\+\-\/]\s*([3-9]\.[0-9]+|[1-9][0-9]+\.[0-9]+)\b/);
    if (magicMatch && !cleanLine.includes('Math.PI') && !/^\s*(const|let|var)\s+[A-Z0-9_]+\s*=/.test(cleanLine)) {
      addIssue({
        id: 'HARDCODED_MAGIC_NUMBER',
        title: 'Valor Numérico Mágico Hardcoded em Equação',
        category: 'Modularidade & Ausência de Hardcoded',
        subskill: 'architecture-hardcoded-auditor',
        severity: 'Baixa',
        penalty: 10,
        line: lineNum,
        col: rawLine.indexOf(magicMatch[1]) + 1,
        description: `Constante numérica hardcoded '${magicMatch[1]}' encontrada em cálculo físico.`,
        recommendation: 'Extraia o valor para uma constante nomeada (ex: PHYSICS_CONFIG.GRAVITY = 9.81).',
        root_cause: `O literal '${magicMatch[1]}' reduz a legibilidade física da fórmula e dificulta parametrização.`,
        best_fix_code: `const GRAVITY_ACCEL = ${magicMatch[1]};\nvelocity.y -= GRAVITY_ACCEL * dt;`,
        why_best_fix: 'Centraliza constantes físicas e permite injeção de configuração por cena.',
        expected_result: 'Zero números mágicos soltos nas equações do motor.'
      });
    }

    // Atualizar profundidade de chaves {} para controlar escopo de loops e funções com precisão
    const openBraces = (cleanLine.match(/\{/g) || []).length;
    const closeBraces = (cleanLine.match(/\}/g) || []).length;
    braceDepth += openBraces - closeBraces;

    if (inAnimationLoop && braceDepth <= loopStartDepth && closeBraces > 0) {
      inAnimationLoop = false;
      loopStartDepth = -1;
    }

    if (activeFnRecord && braceDepth <= currentFnStartDepth && closeBraces > 0) {
      const normBody = activeFnRecord.bodyLines.join(';');
      if (normBody.length > 20) {
        if (functionBodiesNormalized.has(normBody)) {
          const origName = functionBodiesNormalized.get(normBody);
          addIssue({
            id: 'DUPLICATE_FUNCTION',
            title: 'Função Duplicada Identificada',
            category: 'Sanitização Estática & Memory Cleanup',
            subskill: 'static-sanitization-auditor',
            severity: 'Alta',
            penalty: 20,
            line: activeFnRecord.line,
            col: activeFnRecord.col,
            description: `A função '${activeFnRecord.name}' possui corpo idêntico à função '${origName}'.`,
            recommendation: `Unifique a lógica reutilizando '${origName}'.`
          });
        } else {
          functionBodiesNormalized.set(normBody, activeFnRecord.name);
        }
      }
      activeFnRecord = null;
      currentFnName = '';
      currentFnStartDepth = -1;
    }

    if (currentClassName && braceDepth <= classStartDepth && closeBraces > 0) {
      currentClassName = '';
      classStartDepth = -1;
    }
  });

  // Verificar funções declaradas mas nunca referenciadas (DEAD_CODE_FUNCTION)
  const strippedFullCode = stripCommentsAndStrings(code);
  for (const [fnName, meta] of declaredFunctions.entries()) {
    if (meta.exported || ['main', 'animate', 'render', 'init', 'update'].includes(fnName)) {
      continue;
    }
    const regex = new RegExp(`\\b${fnName}\\b`, 'g');
    const occurrences = (strippedFullCode.match(regex) || []).length;
    if (occurrences <= 1) {
      addIssue({
        id: 'DEAD_CODE_FUNCTION',
        title: 'Função Declarada Não Utilizada (Código Morto)',
        category: 'Sanitização Estática & Memory Cleanup',
        subskill: 'static-sanitization-auditor',
        severity: 'Média',
        penalty: 10,
        line: meta.line,
        col: meta.col,
        description: `A função '${fnName}' foi declarada na linha ${meta.line} mas nunca é invocada no módulo.`,
        recommendation: `Remova '${fnName}' ou exporte-a caso pertença à API pública do módulo.`
      });
    }
  }

  const scores = computeScores(issues);

  return {
    filename,
    language: filename.endsWith('.ts') ? 'typescript' : 'javascript',
    total_issues: issues.length,
    scores,
    issues
  };
}

// Execução CLI
if (require.main === module) {
  const arg = process.argv[2];
  if (!arg || arg === '--self-test') {
    const sampleCode = `
      function animate() {
        const dir = new THREE.Vector3(1, 0, 0);
        dir.normalize();
        mesh.position.x += velocity.x;
        mesh.rotation.y += 0.05;
        if (mesh.position.y === 0.0) {
          velocity.y *= -9.81;
        }
      }
      function helperAfterLoop() {
        // Fora do loop: esta alocação NÃO deve disparar ALLOC_IN_LOOP
        const staticVec = new THREE.Vector3(0, 1, 0);
        return staticVec;
      }
    `;
    const result = analyzeJsTsCode(sampleCode, 'self_test_sample.ts');
    console.log(JSON.stringify(result, null, 2));
    process.exit(0);
  }

  try {
    const code = fs.readFileSync(arg, 'utf-8');
    const result = analyzeJsTsCode(code, arg);
    console.log(JSON.stringify(result, null, 2));
  } catch (err) {
    console.error(JSON.stringify({ error: `Erro ao processar arquivo: ${err.message}`, issues: [] }));
    process.exit(1);
  }
}

module.exports = { analyzeJsTsCode, computeScores };
