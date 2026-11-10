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
	home, npm, skills := t.TempDir(), t.TempDir(), t.TempDir()
	writeFile(t, filepath.Join(home, ".agents", ".skill-lock.json"), `{"version":3,"skills":{"via-lock":{"source":"vercel-labs/skills"}}}`)
	writeFile(t, filepath.Join(npm, "rea-agents", "skills", "via-rea", "SKILL.md"), "---\nname: via-rea\n---\n")
	writeFile(t, filepath.Join(skills, "via-licenca", "LICENSE.txt"), "Apache-2.0")

	cases := map[string]struct {
		dir      string
		metadata map[string]any
		want     string
	}{
		"lock":    {filepath.Join(skills, "via-lock"), nil, "npx skills (vercel-labs/skills)"},
		"rea":     {filepath.Join(skills, "via-rea"), nil, "rea-agents"},
		"autor":   {filepath.Join(skills, "android-cli"), map[string]any{"author": "Google LLC"}, "autor externo (Google LLC)"},
		"licença": {filepath.Join(skills, "via-licenca"), nil, "licença de terceiro"},
	}
	for name, c := range cases {
		if got := thirdPartySource(c.dir, c.metadata, "", home, npm); got != c.want {
			t.Errorf("%s: got %q, want %q", name, got, c.want)
		}
	}
}

// Adversarial: a isenção não pode engolir skills próprias, mesmo com LICENSE ou sem metadados.
func TestThirdPartySourceNaoIsentaSkillsProprias(t *testing.T) {
	home, npm, skills := t.TempDir(), t.TempDir(), t.TempDir()
	propriaComLicenca := filepath.Join(skills, "obsidian-vault")
	writeFile(t, filepath.Join(propriaComLicenca, "LICENSE.txt"), "MIT")
	if got := thirdPartySource(propriaComLicenca, map[string]any{"author": "Melki Donadon"}, "MIT", home, npm); got != "" {
		t.Errorf("skill própria com LICENSE marcada como terceiro: %q", got)
	}
	if got := thirdPartySource(filepath.Join(skills, "sem-metadados"), nil, "", home, npm); got != "" {
		t.Errorf("skill sem autor nem licença marcada como terceiro: %q", got)
	}
	writeFile(t, filepath.Join(home, ".agents", ".skill-lock.json"), `{corrompido`)
	if got := thirdPartySource(filepath.Join(skills, "qualquer"), nil, "", home, npm); got != "" {
		t.Errorf("lock corrompido não pode isentar: %q", got)
	}
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
