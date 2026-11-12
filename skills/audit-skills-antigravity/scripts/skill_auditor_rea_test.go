package main

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func writeFile(t *testing.T, path, content string) {
	t.Helper()
	if err := os.MkdirAll(filepath.Dir(path), 0o755); err != nil {
		t.Fatal(err)
	}
	if err := os.WriteFile(path, []byte(content), 0o644); err != nil {
		t.Fatal(err)
	}
}

func TestThirdPartySourceDetectaInstaladoresEFornecedores(t *testing.T) {
	roots := tempRoots(t)
	skills := t.TempDir()
	writeFile(t, filepath.Join(roots.Home, ".agents", ".skill-lock.json"), `{"version":3,"skills":{"via-lock":{"source":"vercel-labs/skills"}}}`)
	writeFile(t, filepath.Join(roots.NpmRoot, "rea-agents", "skills", "via-rea", "SKILL.md"), "---\nname: via-rea\n---\n")
	writeFile(t, filepath.Join(roots.ClaudeMarketplaces, "claude-plugins-official", "plugins", "mcp-server-dev", "skills", "via-plugin", "SKILL.md"), "---\nname: via-plugin\n---\n")
	writeFile(t, filepath.Join(roots.OrcaChunks, "service-abc.js"), "x=[{name:`via-orca`,text:`---\\nname: via-orca\\n---`,releasedDigests:[`00`]}]")
	writeFile(t, filepath.Join(skills, "via-licenca", "LICENSE.txt"), "Apache-2.0")

	cases := map[string]struct {
		dir      string
		metadata map[string]any
		want     string
	}{
		"lock":    {filepath.Join(skills, "via-lock"), nil, "npx skills (vercel-labs/skills)"},
		"rea":     {filepath.Join(skills, "via-rea"), nil, "rea-agents"},
		"plugin":  {filepath.Join(skills, "via-plugin"), nil, "plugin Claude (mcp-server-dev)"},
		"orca":    {filepath.Join(skills, "via-orca"), nil, "Orca (orca skills install)"},
		"autor":   {filepath.Join(skills, "android-cli"), map[string]any{"author": "Google LLC"}, "autor externo (Google LLC)"},
		"licença": {filepath.Join(skills, "via-licenca"), nil, "licença de terceiro"},
	}
	for name, c := range cases {
		if got := thirdPartySource(c.dir, c.metadata, "", roots); got != c.want {
			t.Errorf("%s: got %q, want %q", name, got, c.want)
		}
	}
}

// Adversarial: a isenção não pode engolir skills próprias, mesmo com LICENSE ou sem metadados.
func TestThirdPartySourceNaoIsentaSkillsProprias(t *testing.T) {
	roots := tempRoots(t)
	skills := t.TempDir()
	propriaComLicenca := filepath.Join(skills, "obsidian-vault")
	writeFile(t, filepath.Join(propriaComLicenca, "LICENSE.txt"), "MIT")
	if got := thirdPartySource(propriaComLicenca, map[string]any{"author": "Melki Donadon"}, "MIT", roots); got != "" {
		t.Errorf("skill própria com LICENSE marcada como terceiro: %q", got)
	}
	if got := thirdPartySource(filepath.Join(skills, "sem-metadados"), nil, "", roots); got != "" {
		t.Errorf("skill sem autor nem licença marcada como terceiro: %q", got)
	}
	writeFile(t, filepath.Join(roots.Home, ".agents", ".skill-lock.json"), `{corrompido`)
	if got := thirdPartySource(filepath.Join(skills, "qualquer"), nil, "", roots); got != "" {
		t.Errorf("lock corrompido não pode isentar: %q", got)
	}
	// Um .js do Orca sem releasedDigests (não é o registro de stubs) não pode isentar nomes.
	writeFile(t, filepath.Join(roots.OrcaChunks, "outro.js"), "y={name:`agent-0meia`,text:`x`}")
	if got := thirdPartySource(filepath.Join(skills, "agent-0meia"), nil, "", roots); got != "" {
		t.Errorf("chunk do Orca sem releasedDigests não pode isentar: %q", got)
	}
}

func tempRoots(t *testing.T) installerRoots {
	t.Helper()
	return installerRoots{Home: t.TempDir(), NpmRoot: t.TempDir(), ClaudeMarketplaces: t.TempDir(), OrcaChunks: t.TempDir()}
}

func TestAuditSkillTerceiroFicaSomenteLeitura(t *testing.T) {
	dir := filepath.Join(t.TempDir(), "zz-probe-terceiro")
	writeFile(t, filepath.Join(dir, "SKILL.md"), "---\nname: zz-probe-terceiro\ndescription: x\nmetadata:\n  author: \"Google LLC\"\n---\n"+strings.Repeat("texto longo sem guardrails ", 400))
	rep, err := AuditSkill(dir, "Global User Skills (~/.agents/skills)")
	if err != nil {
		t.Fatal(err)
	}
	if rep.Recommendation != Keep || rep.ThirdPartySource == "" || !strings.Contains(rep.Justification, "somente leitura") {
		t.Fatalf("terceiro deveria ser [MANTIDA] somente leitura, veio %s / %q", rep.Recommendation, rep.Justification)
	}
}

// Adversarial: skill própria sem version/updated_at continua reprovada como antes.
func TestAuditSkillPropriaSemVersaoContinuaReprovada(t *testing.T) {
	dir := filepath.Join(t.TempDir(), "zz-probe-propria")
	writeFile(t, filepath.Join(dir, "SKILL.md"), "---\nname: zz-probe-propria\ndescription: x\nmetadata:\n  author: \"melki\"\n---\ncorpo curto\n")
	rep, err := AuditSkill(dir, "Global User Skills (~/.agents/skills)")
	if err != nil {
		t.Fatal(err)
	}
	if rep.Recommendation != OptimizeYAML || rep.ThirdPartySource != "" {
		t.Fatalf("skill própria sem version deveria seguir em %s, veio %s (%q)", OptimizeYAML, rep.Recommendation, rep.ThirdPartySource)
	}
}

func TestAuditSkillDetectaReferenciasQuebradasEAmbienteInvalido(t *testing.T) {
	dir := filepath.Join(t.TempDir(), "probe-broken-ref")
	body := "## 1. Objetivo\nExecuta validação local.\n1. Consulte [Guia](references/inexistente.md) e `scripts/bloqueante.py`.\n## 5. Guardrails\n- Limites: não usar em produção sem validação.\n"
	writeFile(t, filepath.Join(dir, "SKILL.md"), "---\nname: probe-broken-ref\ndescription: \"Valida referências. Use para teste; não use para UI.\"\nversion: \"1.0.0\"\nupdated_at: \"2026-11-12\"\nallowed-tools: [\"read_file\"]\nmetadata:\n  author: \"melki\"\n---\n"+body)
	writeFile(t, filepath.Join(dir, "scripts", "bloqueante.py"), "x = input('digite: ')\n")
	writeFile(t, filepath.Join(dir, "evals", "evals.json"), "{invalido")

	rep, err := AuditSkill(dir, "Custom Target")
	if err != nil {
		t.Fatal(err)
	}
	if rep.Recommendation != Adjust || len(rep.BrokenRefs) < 3 {
		t.Fatalf("esperava Adjust com >=3 falhas de referência/ambiente, veio %s (%v)", rep.Recommendation, rep.BrokenRefs)
	}
}

func TestAuditSkillPlanningExigeOs6FatoresChave(t *testing.T) {
	dirIncompleto := filepath.Join(t.TempDir(), "planejador-raso")
	bodyIncompleto := "## 1. Objetivo\nPlanejador de projetos que cria passos simples.\n1. Passo 1: escrever lista.\n2. Passo 2: salvar arquivo.\n## 5. Guardrails\n- Quando não usar: não use para CSS.\n"
	writeFile(t, filepath.Join(dirIncompleto, "SKILL.md"), "---\nname: planejador-raso\ndescription: \"Planejador de projetos e decomposição de metas. Use para planejar; não use para UI.\"\nversion: \"1.0.0\"\nupdated_at: \"2026-11-12\"\nallowed-tools: [\"read_file\"]\nmetadata:\n  author: \"melki\"\n---\n"+bodyIncompleto)

	repInc, err := AuditSkill(dirIncompleto, "Custom Target")
	if err != nil {
		t.Fatal(err)
	}
	if repInc.Archetype != "PLANNING" || repInc.Recommendation != Adjust || len(repInc.CognitiveIssues) == 0 {
		t.Fatalf("planejador sem gestão de ambiguidade/coerência lógica deveria ser reprovado em Adjust, veio %s (%v)", repInc.Recommendation, repInc.CognitiveIssues)
	}

	dirCompleto := filepath.Join(t.TempDir(), "planejador-completo")
	bodyCompleto := "## 1. Objetivo\nDecomposição em fases e ondas com estrutura hierárquica em árvore e contrato.\n1. Coerência lógica via grafo DAG (Kahn) e precedência causal.\n2. Gestão de ambiguidade: classificar [LACUNA] e fazer perguntas de clarificação.\n3. Processo de execução passo a passo no workflow.\n## 5. Guardrails\n- Guardrail Zero-Trust e HITL com max_steps = 10.\n"
	writeFile(t, filepath.Join(dirCompleto, "SKILL.md"), "---\nname: planejador-completo\ndescription: \"Planejador de projetos e decomposição de metas. Use para planejar; não use para UI.\"\nversion: \"1.0.0\"\nupdated_at: \"2026-11-12\"\nallowed-tools: [\"read_file\"]\nmetadata:\n  author: \"melki\"\n---\n"+bodyCompleto)

	repComp, err := AuditSkill(dirCompleto, "Custom Target")
	if err != nil {
		t.Fatal(err)
	}
	if repComp.Recommendation != Keep || repComp.CognitiveCoherenceScore != 100 {
		t.Fatalf("planejador completo deveria ser [MANTIDA] 100/100, veio %s (%d: %v)", repComp.Recommendation, repComp.CognitiveCoherenceScore, repComp.CognitiveIssues)
	}
}

func TestAuditSkillE2EReprovaFaltaDeFerramentasDeAnalise(t *testing.T) {
	dir := filepath.Join(t.TempDir(), "auditor-e2e-placebo")
	body := "## 1. Objetivo\nRealiza auditoria E2E de interface frontend lendo apenas textos.\n1. Abrir o texto e dar nota subjetiva para a página.\n2. Emitir relatório em Markdown.\n## 5. Guardrails\n- Limites: quando não usar em backend.\n"
	writeFile(t, filepath.Join(dir, "SKILL.md"), "---\nname: auditor-e2e-placebo\ndescription: \"Executa auditoria E2E e audita interface frontend. Use para auditar UI; não use para Go.\"\nversion: \"1.0.0\"\nupdated_at: \"2026-11-12\"\nallowed-tools: [\"read_file\"]\nmetadata:\n  author: \"melki\"\n---\n"+body)

	rep, err := AuditSkill(dir, "Custom Target")
	if err != nil {
		t.Fatal(err)
	}
	if rep.Archetype != "E2E_UI_AUDIT" || rep.Recommendation != Adjust || !strings.Contains(rep.Justification, "Falsa Capacidade (E2E_UI_AUDIT)") {
		t.Fatalf("E2E sem click/a11y/DOM deveria reprovar por Falsa Capacidade, veio %s (%s)", rep.Recommendation, rep.Justification)
	}
}

func TestAuditSkillReprovaVaguezaContradicaoEHomogeneizacaoUI(t *testing.T) {
	// 1. Skill vaga
	dirVaga := filepath.Join(t.TempDir(), "skill-vaga")
	writeFile(t, filepath.Join(dirVaga, "SKILL.md"), "---\nname: skill-vaga\ndescription: \"Faz coisas gerais. Use sempre; não use nunca.\"\nversion: \"1.0.0\"\nupdated_at: \"2026-11-12\"\nallowed-tools: [\"read_file\"]\nmetadata:\n  author: \"melki\"\n---\nFaça um bom trabalho com qualidade.\n")
	repVaga, _ := AuditSkill(dirVaga, "Custom Target")
	if repVaga.Recommendation != Adjust || !strings.Contains(repVaga.Justification, "Skill vaga") {
		t.Fatalf("skill vaga deveria ser reprovada, veio %s (%s)", repVaga.Recommendation, repVaga.Justification)
	}

	// 2. Regras opostas/contraditórias e contaminação de domínio UI em skill de planejamento
	dirContrad := filepath.Join(t.TempDir(), "planejador-contaminado")
	bodyContrad := "## 1. Objetivo\nOperação 100% somente leitura para decomposição em fases, estrutura em árvore, coerência lógica DAG, gestão de ambiguidade [LACUNA] e processo de workflow.\n1. Execute `rm -rf /tmp/build` imediatamente.\n2. Aplique `--shadow-elevation-1`, `--surface-canvas` e `light-dark()` em todos os planos.\n## 5. Limites\n- Exceções documentadas.\n"
	writeFile(t, filepath.Join(dirContrad, "SKILL.md"), "---\nname: planejador-contaminado\ndescription: \"Planejador de projetos com decomposição de metas. Use para planejar; não use para código.\"\nversion: \"1.0.0\"\nupdated_at: \"2026-11-12\"\nallowed-tools: [\"read_file\"]\nmetadata:\n  author: \"melki\"\n---\n"+bodyContrad)
	repContrad, _ := AuditSkill(dirContrad, "Custom Target")
	if repContrad.Recommendation != Adjust || !strings.Contains(repContrad.Justification, "Regras contraditórias") || !strings.Contains(repContrad.Justification, "Contaminação de domínio") {
		t.Fatalf("esperava detecção de regras contraditórias e contaminação UI, veio %s (%s)", repContrad.Recommendation, repContrad.Justification)
	}
}

func TestDetectCatalogCollisionsDetectaGatilhosDuplicados(t *testing.T) {
	r1 := &SkillAuditReport{SkillName: "skill-a", Scope: "Catalog", YAMLValid: true, Recommendation: Keep, descriptionRaw: "Audita código Python via AST contra eval exec e calcula Quality Score. Use para auditar Python; não use para CSS."}
	r2 := &SkillAuditReport{SkillName: "skill-b", Scope: "Catalog", YAMLValid: true, Recommendation: Keep, descriptionRaw: "Audita código Python via AST contra eval exec e calcula Quality Score. Use para auditar Python; não use para CSS."}
	DetectCatalogCollisions([]*SkillAuditReport{r1, r2})
	if r1.Recommendation != Merge || r2.Recommendation != Merge || len(r1.CollisionIssues) == 0 {
		t.Fatalf("colisão de gatilhos deveria marcar [RECOMENDAÇÃO: FUSÃO], veio %s / %s", r1.Recommendation, r2.Recommendation)
	}
}

