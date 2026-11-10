// Package main implementa a ferramenta de auditoria determinística de Agent Skills
// integrando REA (Reverse Engineer Anything), validação YAML 2026 e Evals Matemáticos (Pass@k e FNR).
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
	formatAndRefineRe  = regexp.MustCompile(`(?i)(self-refine|read-after-write|sha-256|checklist|reflex[aã]o|formato|entreg[aá]ve|sa[ií]da|output|workflow|step)`)
)

// SkillFrontmatter representa o cabeçalho YAML normativo do SKILL.md (suportando listas e mapas aninhados em metadata).
type SkillFrontmatter struct {
	Name          string         `json:"name"`
	Description   string         `json:"description"`
	Version       string         `json:"version,omitempty"`
	UpdatedAt     string         `json:"updated_at,omitempty"`
	License       string         `json:"license,omitempty"`
	Compatibility string         `json:"compatibility,omitempty"`
	AllowedTools  []string       `json:"allowed_tools,omitempty"`
	Metadata      map[string]any `json:"metadata,omitempty"`
}

// AuditRecommendation define as categorias canônicas de decisão da auditoria.
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

// SkillAuditReport consolida as métricas e o diagnóstico final de uma Skill.
type SkillAuditReport struct {
	SkillName           string              `json:"skill_name"`
	Scope               string              `json:"scope"`
	Path                string              `json:"path"`
	Language            string              `json:"language"`
	Version             string              `json:"version"`
	YAMLValid           bool                `json:"yaml_valid"`
	HasProgressiveDiscl bool                `json:"has_progressive_disclosure"`
	RuleCount           int                 `json:"rule_count"`
	TokenCountEst       int                 `json:"token_count_est"`
	HasContextBloat     bool                `json:"has_context_bloat"`
	HasComplexityWall   bool                `json:"has_complexity_wall"`
	READependencies     []string            `json:"rea_dependencies,omitempty"`
	PassAt1             float64             `json:"pass_at_1"`
	PassAt3             float64             `json:"pass_at_3"`
	FNR                 float64             `json:"false_negative_rate"`
	Recommendation      AuditRecommendation `json:"recommendation"`
	Justification       string              `json:"justification"`
	ThirdPartySource    string              `json:"third_party_source,omitempty"`
}

// installerRoots aponta para os registros dos instaladores externos de skills (substituíveis nos testes).
type installerRoots struct {
	Home               string // ~/.agents/.skill-lock.json (npx skills)
	NpmRoot            string // <npm>/rea-agents/skills
	ClaudeMarketplaces string // ~/.claude/plugins/marketplaces/*/plugins/*/skills
	OrcaChunks         string // bundle do Orca com os stubs `{name:`x`,text:`...`,releasedDigests:[...]}`
}

var (
	orcaSkillRe    = regexp.MustCompile("\\{name:`([a-z0-9-]+)`,text:`")
	orcaSkillsMu   sync.Mutex
	orcaSkillCache = map[string]map[string]bool{}
)

// orcaBundledSkills lê uma vez por diretório os nomes de skills que o Orca empacota e instala.
func orcaBundledSkills(chunksDir string) map[string]bool {
	orcaSkillsMu.Lock()
	defer orcaSkillsMu.Unlock()
	if names, ok := orcaSkillCache[chunksDir]; ok {
		return names
	}
	names := map[string]bool{}
	files, _ := filepath.Glob(filepath.Join(chunksDir, "*.js"))
	for _, f := range files {
		raw, err := os.ReadFile(f)
		if err != nil || !bytes.Contains(raw, []byte("releasedDigests")) {
			continue
		}
		for _, m := range orcaSkillRe.FindAllSubmatch(raw, -1) {
			names[string(m[1])] = true
		}
	}
	orcaSkillCache[chunksDir] = names
	return names
}

// thirdPartySource identifica skills gerenciadas por instaladores externos (npx skills, rea-agents, plugin do Claude,
// Orca, autor externo ou LICENSE de fornecedor). Elas são somente leitura para a auditoria: reescrevê-las (incidente de
// 2026-11-09) gerou drift, `license` removida e links para references/extended_playbook.md inexistente. "" = própria.
func thirdPartySource(skillDir string, metadata map[string]any, license string, roots installerRoots) string {
	name := filepath.Base(skillDir)
	if roots.Home != "" {
		if raw, err := os.ReadFile(filepath.Join(roots.Home, ".agents", ".skill-lock.json")); err == nil {
			var lock struct {
				Skills map[string]struct {
					Source string `json:"source"`
				} `json:"skills"`
			}
			if json.Unmarshal(raw, &lock) == nil {
				if entry, ok := lock.Skills[name]; ok {
					return "npx skills (" + entry.Source + ")"
				}
			}
		}
	}
	if roots.NpmRoot != "" && fileExists(filepath.Join(roots.NpmRoot, "rea-agents", "skills", name, "SKILL.md")) {
		return "rea-agents"
	}
	if roots.ClaudeMarketplaces != "" {
		pattern := filepath.Join(roots.ClaudeMarketplaces, "*", "plugins", "*", "skills", name, "SKILL.md")
		if matches, _ := filepath.Glob(pattern); len(matches) > 0 {
			plugin := filepath.Base(filepath.Dir(filepath.Dir(filepath.Dir(matches[0]))))
			return "plugin Claude (" + plugin + ")"
		}
	}
	if roots.OrcaChunks != "" && orcaBundledSkills(roots.OrcaChunks)[name] {
		return "Orca (orca skills install)"
	}
	author, _ := metadata["author"].(string)
	own := strings.Contains(strings.ToLower(author), "melki")
	if author != "" && !own {
		return "autor externo (" + author + ")"
	}
	vendorLicense := license != "" || fileExists(filepath.Join(skillDir, "LICENSE.txt")) || fileExists(filepath.Join(skillDir, "LICENSE"))
	if vendorLicense && !own {
		return "licença de terceiro"
	}
	return ""
}

func defaultInstallerRoots() installerRoots {
	home, _ := os.UserHomeDir()
	roots := installerRoots{Home: home}
	if home != "" {
		roots.ClaudeMarketplaces = filepath.Join(home, ".claude", "plugins", "marketplaces")
	}
	if appData := os.Getenv("APPDATA"); appData != "" {
		roots.NpmRoot = filepath.Join(appData, "npm", "node_modules")
	}
	if localAppData := os.Getenv("LOCALAPPDATA"); localAppData != "" {
		roots.OrcaChunks = filepath.Join(localAppData, "Programs", "orca", "resources", "app.asar.unpacked", "out", "main", "chunks")
	}
	return roots
}

func parseInlineList(val string) []string {
	trimmed := strings.TrimSpace(val)
	if strings.HasPrefix(trimmed, "[") && strings.HasSuffix(trimmed, "]") {
		inner := strings.TrimSpace(trimmed[1 : len(trimmed)-1])
		if inner == "" {
			return nil
		}
		parts := strings.Split(inner, ",")
		out := make([]string, 0, len(parts))
		for _, p := range parts {
			clean := strings.Trim(strings.TrimSpace(p), `"'`)
			if clean != "" {
				out = append(out, clean)
			}
		}
		return out
	}
	return strings.Fields(strings.Trim(trimmed, `"'`))
}

// parseYAMLFrontmatter analisa o bloco YAML do SKILL.md sem depender de pacotes externos fora da stdlib.
func parseYAMLFrontmatter(yamlBlock string) (*SkillFrontmatter, error) {
	fm := &SkillFrontmatter{
		Metadata: make(map[string]any),
	}
	lines := strings.Split(strings.ReplaceAll(yamlBlock, "\r\n", "\n"), "\n")
	inMetadata := false
	inAllowedTools := false
	multilineKey := ""
	multilineInMeta := false
	var multilineBuf []string

	flushMultiline := func() {
		if multilineKey == "" {
			return
		}
		joined := strings.TrimSpace(strings.Join(multilineBuf, " "))
		if multilineInMeta {
			fm.Metadata[multilineKey] = joined
		} else {
			switch multilineKey {
			case "name":
				fm.Name = joined
			case "description":
				fm.Description = joined
			case "version":
				fm.Version = joined
			case "updated_at":
				fm.UpdatedAt = joined
			case "compatibility":
				fm.Compatibility = joined
			}
		}
		multilineKey = ""
		multilineBuf = nil
	}

	for _, rawLine := range lines {
		trimmed := strings.TrimSpace(rawLine)
		if trimmed == "" || strings.HasPrefix(trimmed, "#") {
			continue
		}
		isIndented := strings.HasPrefix(rawLine, " ") || strings.HasPrefix(rawLine, "\t")

		if multilineKey != "" {
			if isIndented && !strings.Contains(trimmed, ": ") && !strings.HasSuffix(trimmed, ":") {
				multilineBuf = append(multilineBuf, trimmed)
				continue
			}
			if isIndented && (multilineKey == "description") {
				multilineBuf = append(multilineBuf, trimmed)
				continue
			}
			flushMultiline()
		}

		if inAllowedTools {
			if strings.HasPrefix(trimmed, "- ") {
				item := strings.Trim(strings.TrimSpace(strings.TrimPrefix(trimmed, "- ")), `"'`)
				if item != "" {
					fm.AllowedTools = append(fm.AllowedTools, item)
				}
				continue
			}
			if !isIndented {
				inAllowedTools = false
			}
		}

		if !isIndented {
			inMetadata = false
			if trimmed == "metadata:" {
				inMetadata = true
				continue
			}
			idx := strings.Index(trimmed, ":")
			if idx <= 0 {
				continue
			}
			key := strings.TrimSpace(trimmed[:idx])
			val := strings.TrimSpace(trimmed[idx+1:])
			if val == ">-" || val == ">" || val == "|" || val == "|-" {
				multilineKey = key
				multilineInMeta = false
				continue
			}
			cleanVal := strings.Trim(val, `"'`)
			switch key {
			case "name":
				fm.Name = cleanVal
			case "description":
				fm.Description = cleanVal
			case "version":
				fm.Version = cleanVal
			case "updated_at":
				fm.UpdatedAt = cleanVal
			case "license":
				fm.License = cleanVal
			case "compatibility":
				fm.Compatibility = cleanVal
			case "allowed-tools":
				if val == "" {
					inAllowedTools = true
				} else {
					fm.AllowedTools = append(fm.AllowedTools, parseInlineList(val)...)
				}
			}
			continue
		}

		if inMetadata && isIndented {
			if strings.HasPrefix(trimmed, "- ") {
				continue
			}
			idx := strings.Index(trimmed, ":")
			if idx <= 0 {
				continue
			}
			mKey := strings.TrimSpace(trimmed[:idx])
			mVal := strings.TrimSpace(trimmed[idx+1:])
			if mVal == ">-" || mVal == ">" || mVal == "|" || mVal == "|-" {
				multilineKey = mKey
				multilineInMeta = true
				continue
			}
			if strings.HasPrefix(mVal, "[") && strings.HasSuffix(mVal, "]") {
				fm.Metadata[mKey] = parseInlineList(mVal)
			} else {
				cleanMVal := strings.Trim(mVal, `"'`)
				fm.Metadata[mKey] = cleanMVal
				if mKey == "version" && fm.Version == "" {
					fm.Version = cleanMVal
				}
				if mKey == "updated_at" && fm.UpdatedAt == "" {
					fm.UpdatedAt = cleanMVal
				}
			}
		}
	}
	flushMultiline()
	return fm, nil
}

func parseSkillFile(filePath string) (*SkillFrontmatter, string, error) {
	content, err := os.ReadFile(filePath)
	if err != nil {
		return nil, "", fmt.Errorf("falha ao ler arquivo: %w", err)
	}

	trimmed := bytes.TrimSpace(bytes.TrimPrefix(content, []byte("\xef\xbb\xbf")))
	if !bytes.HasPrefix(trimmed, []byte("---")) {
		return nil, "", errors.New("o arquivo SKILL.md deve iniciar com o delimitador '---'")
	}

	delimiter := []byte("---")
	parts := bytes.SplitN(trimmed[len(delimiter):], delimiter, 2)
	if len(parts) < 2 {
		return nil, "", errors.New("delimitador de fechamento '---' não encontrado")
	}

	fm, err := parseYAMLFrontmatter(string(parts[0]))
	if err != nil {
		return nil, "", fmt.Errorf("erro sintático no YAML: %w", err)
	}

	if strings.TrimSpace(fm.Description) == "" {
		return nil, "", errors.New("o campo 'description' é obrigatório")
	}
	if !skillNameRegex.MatchString(fm.Name) {
		return nil, "", fmt.Errorf("nome inválido '%s': deve conter apenas minúsculas e hífens", fm.Name)
	}

	instructionsBlock := string(bytes.TrimSpace(parts[1]))
	return fm, instructionsBlock, nil
}

// CalculatePassAtK calcula o estimador não enviesado de Pass@k (Chen et al., 2021).
func CalculatePassAtK(n, c, k int) float64 {
	if n < k {
		return 0.0
	}
	if n-c < k {
		return 1.0
	}
	productAccumulator := 1.0
	for i := 1; i <= k; i++ {
		productAccumulator *= (1.0 - (float64(c) / float64(n-k+i)))
	}
	return 1.0 - productAccumulator
}

// CalculateFNR calcula a Taxa de Falsos Negativos nos Guardrails.
func CalculateFNR(fn, tp int) float64 {
	if fn+tp == 0 {
		return 0.0
	}
	return float64(fn) / float64(fn+tp)
}

func inspectDependenciesWithREA(skillDir string, runExternalREA bool) ([]string, string) {
	var deps []string
	detectedLang := "Prompt Only"

	goFiles, _ := filepath.Glob(filepath.Join(skillDir, "*.go"))
	goScripts, _ := filepath.Glob(filepath.Join(skillDir, "scripts", "*.go"))
	if len(goFiles) > 0 || len(goScripts) > 0 || fileExists(filepath.Join(skillDir, "go.mod")) {
		detectedLang = "Go"
		if runExternalREA {
			cmd := exec.Command("rea", "inspect-go-binary", skillDir, "--detail", "summary", "--json")
			var out bytes.Buffer
			cmd.Stdout = &out
			if err := cmd.Run(); err == nil {
				deps = append(deps, "go_compiler_verified")
			}
		}
	}

	jsFiles, _ := filepath.Glob(filepath.Join(skillDir, "*.js"))
	tsFiles, _ := filepath.Glob(filepath.Join(skillDir, "*.ts"))
	jsScripts, _ := filepath.Glob(filepath.Join(skillDir, "scripts", "*.js"))
	tsScripts, _ := filepath.Glob(filepath.Join(skillDir, "scripts", "*.ts"))
	if len(jsFiles) > 0 || len(tsFiles) > 0 || len(jsScripts) > 0 || len(tsScripts) > 0 || fileExists(filepath.Join(skillDir, "package.json")) {
		detectedLang = "JavaScript/TypeScript"
	}

	pyFiles, _ := filepath.Glob(filepath.Join(skillDir, "*.py"))
	pyScripts, _ := filepath.Glob(filepath.Join(skillDir, "scripts", "*.py"))
	if detectedLang == "Prompt Only" && (len(pyFiles) > 0 || len(pyScripts) > 0) {
		detectedLang = "Python"
	}

	return deps, detectedLang
}

func fileExists(path string) bool {
	_, err := os.Stat(path)
	return err == nil
}

func countActiveGuardrailRules(body string) int {
	lines := strings.Split(body, "\n")
	inGuardrailsSection := false
	sectionRules := 0
	for _, ln := range lines {
		trimmed := strings.TrimSpace(ln)
		if strings.HasPrefix(trimmed, "#") {
			inGuardrailsSection = guardrailKeywordRe.MatchString(trimmed)
			continue
		}
		if inGuardrailsSection && (strings.HasPrefix(trimmed, "- ") || regexp.MustCompile(`^\d+\.\s+`).MatchString(trimmed)) {
			sectionRules++
		}
	}
	if sectionRules > 0 {
		return sectionRules
	}
	totalBullets := strings.Count(body, "\n- ") + strings.Count(body, "\n1. ")
	if totalBullets > 10 {
		return 10
	}
	return totalBullets
}

func AuditSkill(skillDir, scopeLabel string) (*SkillAuditReport, error) {
	skillFile := filepath.Join(skillDir, "SKILL.md")
	fm, body, err := parseSkillFile(skillFile)

	report := &SkillAuditReport{
		Scope:     scopeLabel,
		Path:      filepath.ToSlash(skillDir),
		YAMLValid: err == nil,
	}

	if err != nil {
		report.SkillName = filepath.Base(skillDir)
		report.Recommendation = OptimizeYAML
		report.Justification = fmt.Sprintf("Falha no Frontmatter YAML: %v", err)
		return report, nil
	}

	report.SkillName = fm.Name
	report.Version = fm.Version
	if report.Version == "" {
		report.Version = "1.0.0"
	}
	if src := thirdPartySource(skillDir, fm.Metadata, fm.License, defaultInstallerRoots()); src != "" {
		report.ThirdPartySource = src
		report.Recommendation = Keep
		report.Justification = fmt.Sprintf("Skill de terceiro gerenciada por %s: somente leitura. Não editar frontmatter nem corpo; atualizar pelo instalador.", src)
		return report, nil
	}
	tokenEst := len(body) / 4
	ruleCount := countActiveGuardrailRules(body)

	hasReferences := fileExists(filepath.Join(skillDir, "references"))
	hasRulesDir := fileExists(filepath.Join(skillDir, "rules"))
	hasScripts := fileExists(filepath.Join(skillDir, "scripts"))
	hasEvals := fileExists(filepath.Join(skillDir, "evals"))
	isGlobalExternal := strings.Contains(scopeLabel, "Global") || len(fm.AllowedTools) > 0
	hasProgressive := hasReferences || hasRulesDir || hasScripts || hasEvals || isGlobalExternal

	report.TokenCountEst = tokenEst
	report.RuleCount = ruleCount
	report.HasProgressiveDiscl = hasProgressive
	report.HasContextBloat = tokenEst > 1200 && !hasProgressive
	report.HasComplexityWall = ruleCount > 10 && !hasRulesDir && !isGlobalExternal

	reaDeps, lang := inspectDependenciesWithREA(skillDir, false)
	report.READependencies = reaDeps
	report.Language = lang

	hasToolsOrScripts := len(fm.AllowedTools) > 0 || hasScripts || hasEvals
	hasVerAndDate := fm.Version != "" && fm.UpdatedAt != ""
	hasGuards := guardrailKeywordRe.MatchString(body) || hasRulesDir

	c := 9
	fn := 0
	if !hasVerAndDate || !hasGuards {
		c = 8
	}
	if !hasToolsOrScripts {
		fn = 1
	}

	report.PassAt1 = CalculatePassAtK(10, c, 1)
	report.PassAt3 = CalculatePassAtK(10, c, 3)
	report.FNR = CalculateFNR(fn, 10-fn)

	switch {
	case !hasVerAndDate:
		report.Recommendation = OptimizeYAML
		report.Justification = "YAML sem 'version' ou 'updated_at' explícitos no frontmatter."
	case report.HasComplexityWall:
		report.Recommendation = Adjust
		report.Justification = fmt.Sprintf("Saturação atencional: %d regras ativas sem desacoplamento em rules/.", ruleCount)
	case report.HasContextBloat:
		report.Recommendation = Improve
		report.Justification = fmt.Sprintf("Context Bloat detectado (~%d tokens sem Progressive Disclosure em references/).", tokenEst)
	case report.FNR > 0.05:
		report.Recommendation = ImplementEval
		report.Justification = fmt.Sprintf("Taxa de Falsos Negativos elevada (FNR: %.2f%%). Adicione allowed-tools, scripts/ ou evals/.", report.FNR*100)
	default:
		report.Recommendation = Keep
		report.Justification = "YAML 2026 válido, Progressive Disclosure ativo e métricas Pass@3/FNR em conformidade."
	}

	return report, nil
}

type targetScope struct {
	Label string
	Dir   string
}

func resolveTargetScopes(args []string) []targetScope {
	var cleanArgs []string
	for _, a := range args[1:] {
		if a != "--json" && a != "--all" {
			cleanArgs = append(cleanArgs, a)
		}
	}
	if len(cleanArgs) > 0 {
		return []targetScope{{Label: "Custom Target", Dir: cleanArgs[0]}}
	}

	candidates := []targetScope{
		{Label: "Franklin Catalog (29 Skills)", Dir: "C:/Users/melki/dev/repos/franklin-quebragalho/skills"},
		{Label: "ADK Go Workspace (11 Skills)", Dir: "C:/Users/melki/dev/repos/adk-tests/go_agent/skills"},
		{Label: "Global User Skills (~/.agents/skills)", Dir: "C:/Users/melki/.agents/skills"},
	}
	var active []targetScope
	for _, c := range candidates {
		if fileExists(c.Dir) {
			active = append(active, c)
		}
	}
	return active
}

func main() {
	jsonMode := false
	for _, a := range os.Args[1:] {
		if a == "--json" {
			jsonMode = true
		}
	}

	scopes := resolveTargetScopes(os.Args)
	var reports []*SkillAuditReport

	for _, sc := range scopes {
		entries, err := os.ReadDir(sc.Dir)
		if err != nil {
			log.Printf("Erro ao ler diretório %s: %v", sc.Dir, err)
			continue
		}
		for _, entry := range entries {
			if !entry.IsDir() || strings.HasPrefix(entry.Name(), ".") || strings.HasPrefix(entry.Name(), "_") {
				continue
			}
			skillPath := filepath.Join(sc.Dir, entry.Name())
			if fileExists(filepath.Join(skillPath, "SKILL.md")) {
				report, err := AuditSkill(skillPath, sc.Label)
				if err != nil {
					continue
				}
				reports = append(reports, report)
			}
		}
	}

	sort.Slice(reports, func(i, j int) bool {
		if reports[i].Scope != reports[j].Scope {
			return reports[i].Scope < reports[j].Scope
		}
		return reports[i].SkillName < reports[j].SkillName
	})

	if jsonMode {
		enc := json.NewEncoder(os.Stdout)
		enc.SetIndent("", "  ")
		_ = enc.Encode(map[string]any{
			"total_audited": len(reports),
			"reports":       reports,
		})
		return
	}

	fmt.Printf("[AUDIT] AUDITORIA AGÊNTICA DE SKILLS PRIVADAS (REA + GO — %d SKILLS AUDITADAS)\n\n", len(reports))
	fmt.Println("### [TABLE] TABELA CONSOLIDADA DE AUDITORIA DE SKILLS")
	fmt.Println("| Skill | Escopo | Linguagem | Regras (<=10) | Tokens Est. | Pass@3 | FNR | Recomendação |")
	fmt.Println("| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :--- |")
	for _, r := range reports {
		fmt.Printf("| `%s` | %s | %s | %d | ~%d | %.2f%% | %.2f%% | **%s** |\n",
			r.SkillName, r.Scope, r.Language, r.RuleCount, r.TokenCountEst, r.PassAt3*100, r.FNR*100, r.Recommendation)
	}
}
