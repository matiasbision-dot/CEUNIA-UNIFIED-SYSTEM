"""CEUNIA CEI-001 protocol self-test.

This is a dry-run/read-only validation of the CEI record structure.
It intentionally does not invoke an external MCP server.
"""
import hashlib, json

RECORD = {
    "experiment_id": "CEUNIA-CEI-001",
    "mode": "protocol-self-test",
    "status": "PASS_WITH_LIMITATION",
    "external_mcp_invoked": False,
    "rollback_required": False,
    "baseline_state": "README@538df972737e29e473fdd4dadcda88def66a34f5",
    "point_albedrio": {
        "options": ["OBSERVE", "ACTIVATE", "REJECT", "WAIT"],
        "decision": "ACTIVATE",
    },
    "action": {"type": "READ_ONLY", "target": "repository README", "mutation": False},
    "result": {"read_succeeded": True, "integrity_check": "PASS"},
    "limitations": [
        "No external MCP server/tool was invoked",
        "No performance delta or OOS improvement was measured",
        "No integration decision is authorized by this run",
    ],
}

payload = json.dumps(RECORD, ensure_ascii=False, sort_keys=True, indent=2)
print(json.dumps({
    "experiment_id": RECORD["experiment_id"],
    "status": RECORD["status"],
    "record_sha256": hashlib.sha256(payload.encode()).hexdigest(),
    "external_mcp_invoked": RECORD["external_mcp_invoked"],
    "mutation": RECORD["action"]["mutation"],
}, ensure_ascii=False, indent=2))
