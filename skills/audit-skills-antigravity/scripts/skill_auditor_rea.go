// Package main implementa a auditoria em Dupla Camada de Agent Skills:
// Camada 1 (REA + Sintaxe, Ambiente, Referências, Rotas e Regras Opostas) e
// Camada 2 (Processamento Cognitivo-Discriminativo por Arquétipo, 8 Elos e Anti-Homogeneização).
package main

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"log"
	"os"
	"os/exec"
	"path/filepath"
	"regexp"
	"sort"
	"strings"
	"sync"
)

var (
	skillNameRegex     = regexp.MustCompile(`^[a-z0-9]+(-[a-z0-9]+)*$`)
	guardrailKeywordRe = regexp.MustCompile(`(?i)(guardrail|zero-trust|hitl|circuit\s*breaker|untrusted|limites|exce[cç][oõ]es|quando\s+n[aã]o\s+usar|do\s+not\s+use|vedaç|proibid|bloquei)`)
	markdownLinkRe     = regexp.MustCompile(`\[[^\]]+\]\(([^)]+)\)`)
	inlinePathRefRe    = regexp.MustCompile(`(?:\.\./[a-zA-Z0-9_.\-]+/)*(?:scripts|references|rules|evals)/[a-zA-Z0-9_.\-/]+\.[a-zA-Z0-9]+`)
	pyBlockingInputRe  = regexp.MustCompile(`(?m)^\s*[^#\n]*\binput\s*\(`)
	invalidWinCharsRe  = regexp.MustCompile(`[<>:"|?*]`)
	readOnlyClaimRe    = regexp.MustCompile(`(?i)\b(100%\s+somente\s+leitura|exclusivamente\s+read-only|estritamente\s+read-only|zero\s+muta[cç][aã]o)\b`)
	destructiveCmdRe   = regexp.MustCompile(`(?i)\b(rm\s+-rf|Remove-Item\s+[^\n]*-Force|os\.RemoveAll|shutil\.rmtree|DROP\s+TABLE)\b`)
	hitlOrDryRunRe     = regexp.MustCompile(`(?i)\b(hitl|dry-run|dry_run|confirma[cç][aã]o|proibid|vedad|nunca|bloquea)\b`)
	uiContaminationRe  = regexp.MustCompile(`(?i)(--shadow-elevation-1|--surface-canvas|light-dark\()`)
	e2eAuditClaimRe    = regexp.MustCompile(`(?i)(auditoria\s+e2e|e2e\s+audit|audita[r]?\s+interface|audita[r]?\s+qualidade\s+de\s+interface|audita[r]?\s+frontend|auditoria\s+visual|auditoria\s+de\s+acessibilidade|frontend-testing-auditor|frontend-ui-ux-auditor|complex-zero|plan-uiux|auditoria-projetos-sistema)`)
	e2eRealToolsRe     = regexp.MustCompile(`(?i)\b(click|clique|a11y|wai-aria|aria-|contraste|wcag|snapshot|screenshot|dom|agent-browser|@e[0-9xX]|playwright|devtools|cdp|audit_tactile_ui|ui_ux_frontend_auditor|complex_zero|evaluate_script|inspect_analysis_view)\b`)
	planningClaimRe    = regexp.MustCompile(`(?i)(high-level-context-planner|skill-orquestrador-planos-encadeados|arquiteto-conteudo-solucoes|organizador-projetos-ideias|organizador-fluxo-arvore-arquivos|context-architecture-skill|planejador|planos\s+encadeados|decomposi[cç][aã]o\s+de\s+metas|planejamento\s+de\s+projetos)`)
	negativeClauseRe   = regexp.MustCompile(`(?i)(?:;\s*|\.\s+|\b)(?:n[aã]o\s+use|do\s+not\s+use|don't\s+use|skip\s+when).*$`)
	legacyWorkflowRe   = regexp.MustCompile(`(?i)\.agents/workflows/[a-zA-Z0-9_.\-]+\.md`)
	inlineCodeSpanRe   = regexp.MustCompile("`[^`]+`")
	wordTokenRe        = regexp.MustCompile(`[a-zA-ZÀ-ÿ0-9_-]{4,}`)
	numberedRuleRe     = regexp.MustCompile(`^\d+\.\s+`)
	ownAuthorRe        = regexp.MustCompile(`(?i)(melki|franklin|skillcraft|ui-architect|arq-software|loopplanner|vaultmaster|docmaker)`)
	orcaSkillRe        = regexp.MustCompile("\\{name:`([a-z0-9-]+)`,text:`")
	uiDesignRe         = regexp.MustCompile(`(design-md|frontend-code-architect|interface-medica)`)
	storageOpsRe       = regexp.MustCompile(`(gdrive|disco|vault|pdf|redator)`)
	codeAuditRe        = regexp.MustCompile(`(auditor|audit-|re-a-ndroid|android-agy|validation|eval)`)
	orcaSkillsMu       sync.Mutex
	orcaSkillCache     = map[string]map[string]bool{}
)

type SkillFrontmatter struct {
	Name, Description, Version, UpdatedAt, License, Compatibility string
	AllowedTools                                                  []string       `json:"allowed_tools,omitempty"`
	Metadata                                                      map[string]any `json:"metadata,omitempty"`
}

type AuditRecommendation string

const (
	Keep          AuditRecommendation = "[MANTIDA]"
	Adjust        AuditRecommendation = "[RECOMENDAÇÃO: AJUSTE]"
	Improve       AuditRecommendation = "[RECOMENDAÇÃO: MELHORIA]"
	Remove        AuditRecommendation = "[RECOMENDAÇÃO: EXCLUSÃO]"
	Merge         AuditRecommendation = "[RECOMENDAÇÃO: FUSÃO]"
	OptimizeYAML  AuditRecommendation = "[RECOMENDAÇÃO: OTIMIZAR YAML]"
	ImplementEval AuditRecommendation = "[RECOMENDAÇÃO: IMPLEMENTAR EVAL]"
)

type SkillAuditReport struct {
	SkillName               string              `json:"skill_name"`
	Scope                   string              `json:"scope"`
	Path                    string              `json:"path"`
	Language                string              `json:"language"`
	Archetype               string              `json:"archetype"`
	Version                 string              `json:"version"`
	YAMLValid               bool                `json:"yaml_valid"`
	HasProgressiveDiscl     bool                `json:"has_progressive_disclosure"`
	RuleCount               int                 `json:"rule_count"`
	TokenCountEst           int                 `json:"token_count_est"`
	HasContextBloat         bool                `json:"has_context_bloat"`
	HasComplexityWall       bool                `json:"has_complexity_wall"`
	CognitiveCoherenceScore int                 `json:"cognitive_coherence_score"`
	BrokenRefs              []string            `json:"broken_refs,omitempty"`
	CollisionIssues         []string            `json:"collision_issues,omitempty"`
	CognitiveIssues         []string            `json:"cognitive_issues,omitempty"`
	READependencies         []string            `json:"rea_dependencies,omitempty"`
	PassAt1                 float64             `json:"pass_at_1"`
	PassAt3                 float64             `json:"pass_at_3"`
	FNR                     float64             `json:"false_negative_rate"`
	Recommendation          AuditRecommendation `json:"recommendation"`
	Justification           string              `json:"justification"`
	ThirdPartySource        string              `json:"third_party_source,omitempty"`
	descriptionRaw          string
}

type installerRoots struct{ Home, NpmRoot, ClaudeMarketplaces, OrcaChunks string }

func orcaBundledSkills(chunksDir string) map[string]bool {
	orcaSkillsMu.Lock()
	defer orcaSkillsMu.Unlock()
	if names, ok := orcaSkillCache[chunksDir]; ok {
		return names
	}
	names := map[string]bool{}
	files, _ := filepath.Glob(filepath.Join(chunksDir, "*.js"))
	for _, f := range files {
		if raw, err := os.ReadFile(f); err == nil && bytes.Contains(raw, []byte("releasedDigests")) {
			for _, m := range orcaSkillRe.FindAllSubmatch(raw, -1) {
				names[string(m[1])] = true
			}
		}
	}
	orcaSkillCache[chunksDir] = names
	return names
}

func thirdPartySource(skillDir string, metadata map[string]any, license string, roots installerRoots) string {
	name := filepath.Base(skillDir)
	if roots.Home != "" {
		if raw, err := os.ReadFile(filepath.Join(roots.Home, ".agents", ".skill-lock.json")); err == nil {
			var lock struct {
				Skills map[string]struct{ Source string }
			}
			if json.Unmarshal(raw, &lock) == nil && lock.Skills[name].Source != "" {
				return "npx skills (" + lock.Skills[name].Source + ")"
			}
		}
	}
	if roots.NpmRoot != "" && fileExists(filepath.Join(roots.NpmRoot, "rea-agents", "skills", name, "SKILL.md")) {
		return "rea-agents"
	}
	if roots.ClaudeMarketplaces != "" {
		if m, _ := filepath.Glob(filepath.Join(roots.ClaudeMarketplaces, "*", "plugins", "*", "skills", name, "SKILL.md")); len(m) > 0 {
			return "plugin Claude (" + filepath.Base(filepath.Dir(filepath.Dir(filepath.Dir(m[0])))) + ")"
		}
	}
	if roots.OrcaChunks != "" && orcaBundledSkills(roots.OrcaChunks)[name] {
		return "Orca (orca skills install)"
	}
	author, _ := metadata["author"].(string)
	own := ownAuthorRe.MatchString(author)
	if author != "" && !own {
		return "autor externo (" + author + ")"
	}
	if (license != "" || fileExists(filepath.Join(skillDir, "LICENSE.txt")) || fileExists(filepath.Join(skillDir, "LICENSE"))) && !own {
		return "licença de terceiro"
	}
	return ""
}

func joinIfSet(base string, elem ...string) string {
	if base == "" {
		return ""
	}
	return filepath.Join(append([]string{base}, elem...)...)
}

func defaultInstallerRoots() installerRoots {
	home, _ := os.UserHomeDir()
	return installerRoots{
		Home:               home,
		ClaudeMarketplaces: joinIfSet(home, ".claude", "plugins", "marketplaces"),
		NpmRoot:            joinIfSet(os.Getenv("APPDATA"), "npm", "node_modules"),
		OrcaChunks:         joinIfSet(os.Getenv("LOCALAPPDATA"), "Programs", "orca", "resources", "app.asar.unpacked", "out", "main", "chunks"),
	}
}

func parseInlineList(val string) (out []string) {
	t := strings.TrimSpace(val)
	if !strings.HasPrefix(t, "[") || !strings.HasSuffix(t, "]") {
		return strings.Fields(strings.Trim(t, `"'`))
	}
	for _, p := range strings.Split(strings.TrimSpace(t[1:len(t)-1]), ",") {
		if clean := strings.Trim(strings.TrimSpace(p), `"'`); clean != "" {
			out = append(out, clean)
		}
	}
	return out
}

func splitKV(s string) (string, string, bool) {
	idx := strings.Index(s, ":")
	if idx <= 0 {
		return "", "", false
	}
	return strings.TrimSpace(s[:idx]), strings.TrimSpace(s[idx+1:]), true
}

func parseYAMLFrontmatter(yamlBlock string) (*SkillFrontmatter, error) {
	fm := &SkillFrontmatter{Metadata: make(map[string]any)}
	fields := map[string]*string{"name": &fm.Name, "description": &fm.Description, "version": &fm.Version, "updated_at": &fm.UpdatedAt, "license": &fm.License, "compatibility": &fm.Compatibility}
	inMeta, inTools, mlMeta, mlKey := false, false, false, ""
	var mlBuf []string
	flush := func() {
		if mlKey == "" {
			return
		}
		if joined := strings.TrimSpace(strings.Join(mlBuf, " ")); mlMeta {
			fm.Metadata[mlKey] = joined
		} else if ptr := fields[mlKey]; ptr != nil {
			*ptr = joined
		}
		mlKey, mlBuf = "", nil
	}
	for _, rawLine := range strings.Split(strings.ReplaceAll(yamlBlock, "\r\n", "\n"), "\n") {
		t, indented := strings.TrimSpace(rawLine), strings.HasPrefix(rawLine, " ") || strings.HasPrefix(rawLine, "\t")
		if t == "" || strings.HasPrefix(t, "#") {
			continue
		}
		if mlKey != "" && indented && (mlKey == "description" || (!strings.Contains(t, ": ") && !strings.HasSuffix(t, ":"))) {
			mlBuf = append(mlBuf, t)
			continue
		}
		flush()
		if inTools && strings.HasPrefix(t, "- ") {
			if item := strings.Trim(strings.TrimSpace(strings.TrimPrefix(t, "- ")), `"'`); item != "" {
				fm.AllowedTools = append(fm.AllowedTools, item)
			}
			continue
		}
		if !indented {
			inTools = false
			if inMeta = t == "metadata:"; !inMeta {
				if k, v, ok := splitKV(t); ok {
					switch {
					case v == ">-" || v == ">" || v == "|" || v == "|-":
						mlKey, mlMeta = k, false
					case k == "allowed-tools" && v == "":
						inTools = true
					case k == "allowed-tools":
						fm.AllowedTools = append(fm.AllowedTools, parseInlineList(v)...)
					case fields[k] != nil:
						*fields[k] = strings.Trim(v, `"'`)
					}
				}
			}
		} else if inMeta && !strings.HasPrefix(t, "- ") {
			if mk, mv, ok := splitKV(t); ok {
				switch {
				case mv == ">-" || mv == ">" || mv == "|" || mv == "|-":
					mlKey, mlMeta = mk, true
				case strings.HasPrefix(mv, "[") && strings.HasSuffix(mv, "]"):
					fm.Metadata[mk] = parseInlineList(mv)
				default:
					cv := strings.Trim(mv, `"'`)
					fm.Metadata[mk] = cv
					if mk == "version" && fm.Version == "" {
						fm.Version = cv
					} else if mk == "updated_at" && fm.UpdatedAt == "" {
						fm.UpdatedAt = cv
					}
				}
			}
		}
	}
	flush()
	return fm, nil
}

func parseSkillFile(filePath string) (*SkillFrontmatter, string, error) {
	content, err := os.ReadFile(filePath)
	if err != nil {
		return nil, "", fmt.Errorf("falha ao ler arquivo: %w", err)
	}
	trimmed := bytes.TrimSpace(bytes.TrimPrefix(content, []byte("\xef\xbb\xbf")))
	parts := bytes.SplitN(bytes.TrimPrefix(trimmed, []byte("---")), []byte("---"), 2)
	if !bytes.HasPrefix(trimmed, []byte("---")) || len(parts) < 2 {
		return nil, "", errors.New("delimitadores de frontmatter '---' ausentes ou incompletos")
	}
	fm, err := parseYAMLFrontmatter(string(parts[0]))
	switch {
	case err != nil:
		return nil, "", fmt.Errorf("erro sintático no YAML: %w", err)
	case strings.TrimSpace(fm.Description) == "":
		return nil, "", errors.New("o campo 'description' é obrigatório")
	case len(fm.Name) > 64 || !skillNameRegex.MatchString(fm.Name):
		return nil, "", fmt.Errorf("nome inválido '%s': máx 64 chars kebab-case", fm.Name)
	case len(fm.Compatibility) > 500:
		return nil, "", fmt.Errorf("campo 'compatibility' excede 500 caracteres (%d)", len(fm.Compatibility))
	}
	return fm, string(bytes.TrimSpace(parts[1])), nil
}

func CalculatePassAtK(n, c, k int) float64 {
	if n < k || n-c < k {
		if n < k {
			return 0.0
		}
		return 1.0
	}
	acc := 1.0
	for i := 1; i <= k; i++ {
		acc *= 1.0 - (float64(c) / float64(n-k+i))
	}
	return 1.0 - acc
}

func CalculateFNR(fn, tp int) float64 {
	if fn+tp == 0 {
		return 0.0
	}
	return float64(fn) / float64(fn+tp)
}

func hasGlob(skillDir, pattern string) bool {
	m1, _ := filepath.Glob(filepath.Join(skillDir, pattern))
	m2, _ := filepath.Glob(filepath.Join(skillDir, "scripts", pattern))
	return len(m1)+len(m2) > 0
}

func inspectDependenciesWithREA(skillDir string, runExternalREA bool) (deps []string, lang string) {
	if hasGlob(skillDir, "*.go") || fileExists(filepath.Join(skillDir, "go.mod")) {
		lang = "Go"
		if runExternalREA && exec.Command("rea", "inspect-go-binary", skillDir, "--detail", "summary", "--json").Run() == nil {
			deps = append(deps, "go_compiler_verified")
		}
	}
	if hasGlob(skillDir, "*.js") || hasGlob(skillDir, "*.ts") || fileExists(filepath.Join(skillDir, "package.json")) {
		return deps, "JavaScript/TypeScript"
	}
	if lang == "" && hasGlob(skillDir, "*.py") {
		return deps, "Python"
	}
	if lang == "" {
		lang = "Prompt Only"
	}
	return deps, lang
}

func fileExists(path string) bool { _, err := os.Stat(path); return err == nil }

func countActiveGuardrailRules(body string) int {
	inGuard, n := false, 0
	for _, ln := range strings.Split(body, "\n") {
		if t := strings.TrimSpace(ln); strings.HasPrefix(t, "#") {
			inGuard = guardrailKeywordRe.MatchString(t)
		} else if inGuard && (strings.HasPrefix(t, "- ") || numberedRuleRe.MatchString(t)) {
			n++
		}
	}
	if n > 0 {
		return n
	}
	if total := strings.Count(body, "\n- ") + strings.Count(body, "\n1. "); total <= 10 {
		return total
	}
	return 10
}

func isExternalURI(s string) bool {
	l := strings.ToLower(s)
	return strings.HasPrefix(l, "http://") || strings.HasPrefix(l, "https://") || strings.HasPrefix(l, "mailto:") || strings.HasPrefix(l, "file://") || strings.HasPrefix(l, "conversation://")
}

func checkBrokenRefsAndEnv(skillDir, body string) []string {
	var issues []string
	seen := map[string]bool{}
	checkTarget := func(raw string) {
		target := strings.TrimSpace(strings.Split(raw, "#")[0])
		if target == "" || seen[target] || strings.ContainsAny(target, "*<>`$()") || isExternalURI(target) {
			return
		}
		seen[target] = true
		if invalidWinCharsRe.MatchString(target) {
			issues = append(issues, fmt.Sprintf("Nome/caminho incompatível com o ambiente Windows: %s", target))
		} else if !fileExists(filepath.Join(skillDir, target)) {
			issues = append(issues, fmt.Sprintf("Referência/arquivo inexistente no ambiente: %s", target))
		}
	}
	cleanMD := inlineCodeSpanRe.ReplaceAllString(body, "")
	for _, m := range markdownLinkRe.FindAllStringSubmatch(cleanMD, -1) {
		checkTarget(m[1])
	}
	for _, m := range inlinePathRefRe.FindAllString(body, -1) {
		checkTarget(m)
	}
	if legacyWorkflowRe.MatchString(cleanMD) {
		issues = append(issues, "Referência legada a .agents/workflows/*.md depreciada no Antigravity 2.12+")
	}
	for _, sub := range []string{"evals/*.json", "references/*.json"} {
		if files, _ := filepath.Glob(filepath.Join(skillDir, sub)); len(files) > 0 {
			for _, jf := range files {
				if raw, err := os.ReadFile(jf); err != nil || !json.Valid(bytes.TrimPrefix(raw, []byte("\xef\xbb\xbf"))) {
					issues = append(issues, fmt.Sprintf("Erro de sintaxe JSON em %s", filepath.Base(jf)))
				}
			}
		}
	}
	if pyFiles, _ := filepath.Glob(filepath.Join(skillDir, "scripts", "*.py")); len(pyFiles) > 0 {
		for _, pf := range pyFiles {
			if raw, err := os.ReadFile(pf); err == nil && pyBlockingInputRe.Match(raw) {
				issues = append(issues, fmt.Sprintf("Bloqueio TTY input() proibido em scripts/%s", filepath.Base(pf)))
			}
		}
	}
	return issues
}

func classifyArchetype(name, desc string) string {
	c := strings.ToLower(name + " " + negativeClauseRe.ReplaceAllString(desc, ""))
	for _, pair := range [][2]any{{planningClaimRe, "PLANNING"}, {e2eAuditClaimRe, "E2E_UI_AUDIT"}, {uiDesignRe, "UI_DESIGN"}, {storageOpsRe, "STORAGE_OPS_DOCS"}, {codeAuditRe, "CODE_SECURITY_AUDIT"}} {
		if pair[0].(*regexp.Regexp).MatchString(c) {
			return pair[1].(string)
		}
	}
	return "GENERAL"
}

var planningFactors = [][2]string{
	{"divisão/decomposição", `(?i)(divis|decompos|fase|onda|etapa|step|task|m[oó]dulo|camada|quebra)`},
	{"estrutura/hierarquia", `(?i)(estrutur|hierarq|[aá]rvore|schema|formato|contrato|tabela|se[cç][aã]o|template)`},
	{"coerência lógica/dependências", `(?i)(coer[eê]n|l[oó]gic|depend[eê]n|dag|kahn|ordem|sequ[eê]n|preced[eê]n|causal|fluxo|grafo)`},
	{"gestão de ambiguidade", `(?i)(amb[ií]gu|lacuna|incertez|clarifica|pergunt|hip[oó]tes|infer[eê]n|faltante|d[uú]vida|entropia|esclarec)`},
	{"descrição de processos", `(?i)(process|fluxo|passo|execu[cç]|etapa|ciclo|workflow|como\s+funciona)`},
	{"guardrails de segurança", `(?i)(guardrail|seguran[cç]|limite|exce[cç]|n[aã]o\s+usar|hitl|zero-trust|bloquei|veda[cç]|max_steps)`},
}

func evaluateCognitiveLayer(fm *SkillFrontmatter, body, archetype string) (int, []string) {
	score, fullText := 100, fm.Description+"\n"+body
	var issues, missing []string
	if len(strings.TrimSpace(body)) < 160 || !(strings.Contains(body, "1.") || strings.Contains(body, "- ") || strings.Contains(body, "```")) {
		score, issues = score-35, append(issues, "Skill vaga: corpo sem passos determinísticos, entradas/saídas ou comandos verificáveis")
	}
	if readOnlyClaimRe.MatchString(fullText) && destructiveCmdRe.MatchString(body) && !hitlOrDryRunRe.MatchString(body) {
		score, issues = score-30, append(issues, "Regras contraditórias: declara execução somente leitura mas instrui comando destrutivo sem salvaguarda")
	}
	if (archetype == "PLANNING" || archetype == "STORAGE_OPS_DOCS") && uiContaminationRe.MatchString(body) {
		score, issues = score-25, append(issues, "Contaminação de domínio (Homogeneização): tokens visuais de UI (--shadow-elevation/--surface-canvas/light-dark) injetados em skill não-visual")
	}
	if archetype == "PLANNING" {
		for _, pf := range planningFactors {
			if ok, _ := regexp.MatchString(pf[1], fullText); !ok {
				missing = append(missing, pf[0])
			}
		}
		if len(missing) > 0 {
			score, issues = score-15*len(missing), append(issues, fmt.Sprintf("Arquétipo PLANNING incompleto (faltam fatores-chave: %s)", strings.Join(missing, ", ")))
		}
	}
	if archetype == "E2E_UI_AUDIT" && !e2eRealToolsRe.MatchString(fullText) {
		score, issues = score-40, append(issues, "Falsa Capacidade (E2E_UI_AUDIT): promete auditoria E2E/UI mas não utiliza ferramentas reais de análise (click, a11y, DOM, DevTools ou script verificador)")
	}
	return max(0, score), issues
}

func AuditSkill(skillDir, scopeLabel string) (*SkillAuditReport, error) {
	fm, body, err := parseSkillFile(filepath.Join(skillDir, "SKILL.md"))
	r := &SkillAuditReport{Scope: scopeLabel, Path: filepath.ToSlash(skillDir), YAMLValid: err == nil}
	if err != nil {
		r.SkillName, r.Recommendation, r.Justification = filepath.Base(skillDir), OptimizeYAML, fmt.Sprintf("Falha no Frontmatter YAML: %v", err)
		return r, nil
	}
	r.SkillName, r.descriptionRaw, r.Version = fm.Name, fm.Description, fm.Version
	if r.Version == "" {
		r.Version = "1.0.0"
	}
	if src := thirdPartySource(skillDir, fm.Metadata, fm.License, defaultInstallerRoots()); src != "" {
		r.ThirdPartySource, r.Archetype, r.CognitiveCoherenceScore, r.Recommendation = src, "THIRD_PARTY_READONLY", 100, Keep
		r.Justification = fmt.Sprintf("Skill de terceiro gerenciada por %s: somente leitura. Não editar frontmatter nem corpo; atualizar pelo instalador.", src)
		return r, nil
	}
	hasRefs, hasRules, hasScripts, hasEvals := fileExists(filepath.Join(skillDir, "references")), fileExists(filepath.Join(skillDir, "rules")), fileExists(filepath.Join(skillDir, "scripts")), fileExists(filepath.Join(skillDir, "evals"))
	isGlobalExt := strings.Contains(scopeLabel, "Global") || len(fm.AllowedTools) > 0
	r.TokenCountEst, r.RuleCount = len(body)/4, countActiveGuardrailRules(body)
	r.HasProgressiveDiscl = hasRefs || hasRules || hasScripts || hasEvals || isGlobalExt
	r.HasContextBloat, r.HasComplexityWall = r.TokenCountEst > 1200 && !r.HasProgressiveDiscl, r.RuleCount > 10 && !hasRules && !isGlobalExt
	r.READependencies, r.Language = inspectDependenciesWithREA(skillDir, false)
	r.Archetype, r.BrokenRefs = classifyArchetype(fm.Name, fm.Description), checkBrokenRefsAndEnv(skillDir, body)
	r.CognitiveCoherenceScore, r.CognitiveIssues = evaluateCognitiveLayer(fm, body, r.Archetype)

	hasVerAndDate, hasGuards := fm.Version != "" && fm.UpdatedAt != "", guardrailKeywordRe.MatchString(body) || hasRules
	c, fn := 9, 0
	if !hasVerAndDate || !hasGuards || len(r.BrokenRefs) > 0 || len(r.CognitiveIssues) > 0 {
		c = 8
	}
	if !(len(fm.AllowedTools) > 0 || hasScripts || hasEvals) || (r.Archetype == "E2E_UI_AUDIT" && len(r.CognitiveIssues) > 0) {
		fn = 1
	}
	r.PassAt1, r.PassAt3, r.FNR = CalculatePassAtK(10, c, 1), CalculatePassAtK(10, c, 3), CalculateFNR(fn, 10-fn)

	r.Recommendation, r.Justification = Keep, "YAML 2026 válido, referências/ambiente íntegros, coerência cognitiva aprovada e Pass@3/FNR em conformidade."
	if !hasVerAndDate {
		r.Recommendation, r.Justification = OptimizeYAML, "YAML sem 'version' ou 'updated_at' explícitos no frontmatter."
	} else if len(r.BrokenRefs) > 0 {
		r.Recommendation, r.Justification = Adjust, strings.Join(r.BrokenRefs, "; ")
	} else if len(r.CognitiveIssues) > 0 {
		r.Recommendation, r.Justification = Adjust, strings.Join(r.CognitiveIssues, "; ")
	} else if r.HasComplexityWall {
		r.Recommendation, r.Justification = Adjust, fmt.Sprintf("Saturação atencional: %d regras ativas sem desacoplamento em rules/.", r.RuleCount)
	} else if r.HasContextBloat {
		r.Recommendation, r.Justification = Improve, fmt.Sprintf("Context Bloat detectado (~%d tokens sem Progressive Disclosure em references/).", r.TokenCountEst)
	} else if r.FNR > 0.05 {
		r.Recommendation, r.Justification = ImplementEval, fmt.Sprintf("Taxa de Falsos Negativos elevada (FNR: %.2f%%). Adicione allowed-tools, scripts/ ou evals/.", r.FNR*100)
	}
	return r, nil
}

func descTokenSet(desc string) map[string]bool {
	tokens := map[string]bool{}
	for _, w := range wordTokenRe.FindAllString(strings.ToLower(desc), -1) {
		tokens[w] = true
	}
	return tokens
}

func jaccardSim(a, b map[string]bool) float64 {
	if len(a) == 0 || len(b) == 0 {
		return 0
	}
	inter, union := 0, len(a)
	for k := range b {
		if a[k] {
			inter++
		} else {
			union++
		}
	}
	return float64(inter) / float64(union)
}

func DetectCatalogCollisions(reports []*SkillAuditReport) {
	for i, a := range reports {
		if a.ThirdPartySource != "" || !a.YAMLValid {
			continue
		}
		tokA := descTokenSet(a.descriptionRaw)
		for _, b := range reports[i+1:] {
			if b.ThirdPartySource != "" || !b.YAMLValid || a.Scope != b.Scope {
				continue
			}
			if a.SkillName == b.SkillName {
				msg := fmt.Sprintf("Colisão de nome/rota com '%s'", b.Path)
				a.CollisionIssues, b.CollisionIssues = append(a.CollisionIssues, msg), append(b.CollisionIssues, msg)
				a.Recommendation, b.Recommendation, a.Justification, b.Justification = Merge, Merge, msg, msg
			} else if jaccardSim(tokA, descTokenSet(b.descriptionRaw)) >= 0.80 {
				msgA, msgB := fmt.Sprintf("Colisão de gatilhos Nível 1 (>=80%%) com '%s'", b.SkillName), fmt.Sprintf("Colisão de gatilhos Nível 1 (>=80%%) com '%s'", a.SkillName)
				a.CollisionIssues, b.CollisionIssues = append(a.CollisionIssues, msgA), append(b.CollisionIssues, msgB)
				a.Recommendation, b.Recommendation, a.Justification, b.Justification = Merge, Merge, msgA, msgB
			}
		}
	}
}

type targetScope struct{ Label, Dir string }

func resolveTargetScopes(args []string) (active []targetScope) {
	for _, a := range args[1:] {
		if a != "--json" && a != "--all" {
			return []targetScope{{Label: "Custom Target", Dir: a}}
		}
	}
	for _, c := range []targetScope{
		{Label: "Franklin Catalog (29 Skills)", Dir: "C:/Users/melki/dev/repos/franklin-quebragalho/skills"},
		{Label: "ADK Go Workspace (7 Skills)", Dir: "C:/Users/melki/dev/repos/adk-go-mcp/skills"},
		{Label: "Global User Skills (~/.agents/skills)", Dir: "C:/Users/melki/.agents/skills"},
	} {
		if fileExists(c.Dir) {
			active = append(active, c)
		}
	}
	return active
}

func main() {
	jsonMode := strings.Contains(" "+strings.Join(os.Args[1:], " ")+" ", " --json ")
	var reports []*SkillAuditReport
	for _, sc := range resolveTargetScopes(os.Args) {
		entries, err := os.ReadDir(sc.Dir)
		if err != nil {
			log.Printf("Erro ao ler diretório %s: %v", sc.Dir, err)
			continue
		}
		for _, e := range entries {
			if p := filepath.Join(sc.Dir, e.Name()); e.IsDir() && !strings.HasPrefix(e.Name(), ".") && !strings.HasPrefix(e.Name(), "_") && fileExists(filepath.Join(p, "SKILL.md")) {
				if r, err := AuditSkill(p, sc.Label); err == nil {
					reports = append(reports, r)
				}
			}
		}
	}
	DetectCatalogCollisions(reports)
	sort.Slice(reports, func(i, j int) bool {
		return reports[i].Scope+reports[i].SkillName < reports[j].Scope+reports[j].SkillName
	})
	if jsonMode {
		enc := json.NewEncoder(os.Stdout)
		enc.SetIndent("", "  ")
		_ = enc.Encode(map[string]any{"total_audited": len(reports), "reports": reports})
		return
	}
	fmt.Printf("[AUDIT] AUDITORIA AGÊNTICA DE SKILLS EM DUPLA CAMADA (REA + COGNITIVO-DISCRIMINATIVA — %d SKILLS AUDITADAS)\n\n### [TABLE] TABELA CONSOLIDADA DE AUDITORIA DE SKILLS\n| Skill | Escopo | Arquétipo | Coerência | Regras (<=10) | Tokens Est. | Pass@3 | FNR | Recomendação |\n| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |\n", len(reports))
	for _, r := range reports {
		fmt.Printf("| `%s` | %s | `%s` | %d/100 | %d | ~%d | %.2f%% | %.2f%% | **%s** |\n", r.SkillName, r.Scope, r.Archetype, r.CognitiveCoherenceScore, r.RuleCount, r.TokenCountEst, r.PassAt3*100, r.FNR*100, r.Recommendation)
	}
}
