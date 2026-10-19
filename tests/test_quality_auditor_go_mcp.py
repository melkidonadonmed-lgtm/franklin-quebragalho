"""
test_quality_auditor_go_mcp.py
Suíte de testes determinísticos (Nível 4) para os módulos Go (*_test.go) e MCP (JSON-RPC 2.0 / FastMCP)
da skill test-quality-auditor (v1.1.0).
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
AUDITOR_SCRIPTS_DIR = ROOT_DIR / "skills" / "test-quality-auditor" / "scripts"
if str(AUDITOR_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(AUDITOR_SCRIPTS_DIR))

from go_test_auditor import audit_go_test_file
from mcp_test_auditor import audit_mcp_test_file
from test_quality_auditor import audit_test_file


def test_go_auditor_detects_silenced_error_and_nil_only() -> None:
    """Valida se o módulo Go reprova testes que descartam erro com '_' e checam apenas nil (Nível 1)."""
    go_code = """package domain_test
import "testing"

func TestSilencedAndNilOnly(t *testing.T) {
	res, _ := store.AnalyzeIssue("ISS-101")
	if res == nil {
		t.Fatal("nil result")
	}
}
"""
    report = audit_go_test_file(go_code, "silenced_test.go")
    assert report.aprovado is False
    assert report.language == "go"
    issue_ids = {iss.id for iss in report.issues}
    assert "SILENCED_ERROR_IN_TEST" in issue_ids
    assert "WEAK_NIL_ONLY_ASSERT" in issue_ids
    assert report.score_medio <= 25.0
    assert report.nivel_espectro == "NÍVEL 1: ILUSÓRIO / PLACEBO"


def test_go_auditor_detects_goroutine_fatal_and_setenv_leakage() -> None:
    """Valida detecção de t.Fatalf dentro de goroutine e os.Setenv sem t.Cleanup (Nível 2)."""
    go_code = """package agents_test
import (
	"os"
	"testing"
)

func TestGoroutineAndEnvLeak(t *testing.T) {
	os.Setenv("ADK_ENV", "prod")
	go func() {
		t.Fatalf("illegal fatal in child goroutine")
	}()
	if got := 42; got != 42 {
		t.Errorf("unexpected %d", got)
	}
}
"""
    report = audit_go_test_file(go_code, "concurrency_test.go")
    assert report.aprovado is False
    issue_ids = {iss.id for iss in report.issues}
    assert "UNSAFE_GOROUTINE_FATAL" in issue_ids
    assert "GLOBAL_STATE_LEAKAGE" in issue_ids
    assert report.nivel_espectro == "NÍVEL 2: SUPERFICIAL / FRÁGIL"


def test_go_auditor_approves_level4_deterministic_test() -> None:
    """Valida aprovação 100/100 (Nível 4) de teste Go com t.TempDir(), errors.Is e asserções de negócio."""
    go_code = """package agents_test
import (
	"errors"
	"testing"
)

func TestStoreAnalyzeSLADeterministic(t *testing.T) {
	vault := t.TempDir()
	triage, err := store.AnalyzeIssue("ISS-101")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if !triage.SLABreached || triage.ImpactScore < 90 || vault == "" {
		t.Errorf("expected SLA breach and score >= 90, got %+v", triage)
	}
	_, err = store.AnalyzeIssue("ISS-999")
	if !errors.Is(err, ErrIssueNotFound) {
		t.Fatalf("expected ErrIssueNotFound, got %v", err)
	}
}
"""
    report = audit_go_test_file(go_code, "reviewer_test.go")
    assert report.aprovado is True
    assert report.total_inconformidades == 0
    assert report.score_medio == 100.0
    assert report.nivel_espectro == "NÍVEL 4: DETERMINÍSTICO & RESILIENTE"


def test_mcp_auditor_detects_missing_handshake_and_error_code() -> None:
    """Valida se o módulo MCP detecta ausência de handshake initialize e falta de código -32601."""
    mcp_go_code = """package mcpserver_test
import "testing"

func TestMCPBrokenStdio(t *testing.T) {
	req := `{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"nonexistent_tool"}}`
	resp := runStdioServer(req)
	if len(resp) == 0 {
		t.Fatalf("empty response")
	}
}
"""
    report = audit_mcp_test_file(mcp_go_code, "stdio_server_test.go")
    assert report.aprovado is False
    issue_ids = {iss.id for iss in report.issues}
    assert "MCP_INCOMPLETE_STDIO_HANDSHAKE" in issue_ids
    assert "MCP_UNVERIFIED_ERROR_CODE_CONTRACT" in issue_ids


def test_mcp_auditor_detects_unparsed_json_and_weak_security_guard() -> None:
    """Valida detecção de resposta JSON MCP sem json.loads e falta de asserção Zero-Trust."""
    mcp_py_code = """def test_mcp_weak_json_and_security():
    res = server.franklin_execute_dag("../secrets.json")
    assert len(res) > 0
"""
    report = audit_mcp_test_file(mcp_py_code, "test_mcp_security.py")
    assert report.aprovado is False
    issue_ids = {iss.id for iss in report.issues}
    assert "MCP_TAUTOLOGICAL_RAW_RESPONSE" in issue_ids
    assert "MCP_WEAK_SECURITY_GUARD_ASSERT" in issue_ids


def test_mcp_auditor_approves_level4_stdio_handshake() -> None:
    """Valida aprovação 100/100 (Nível 4) de teste MCP com initialize, tools/list e erro -32601."""
    mcp_go_code = """package mcpserver_test
import (
	"encoding/json"
	"strings"
	"testing"
)

func TestMCPStdioComplete(t *testing.T) {
	reqs := []string{
		`{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}`,
		`{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}`,
		`{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}`,
		`{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"nonexistent_tool"}}`,
	}
	out := serveMCP(t.TempDir(), reqs)
	var errResp JSONRPCResponse
	if err := json.Unmarshal([]byte(out[2]), &errResp); err != nil {
		t.Fatalf("unmarshal failed: %v", err)
	}
	if !strings.Contains(out[1], "go_fast_dispatch") || errResp.Error.Code != -32601 {
		t.Errorf("invalid mcp contract: %+v", errResp)
	}
}
"""
    report = audit_test_file(mcp_go_code, "stdio_server_test.go", domain="auto")
    assert report.aprovado is True
    assert report.total_inconformidades == 0
    assert report.score_medio == 100.0
    assert report.dossiers[0].domain == "mcp/go"
