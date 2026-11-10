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
