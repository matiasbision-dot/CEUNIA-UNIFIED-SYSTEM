#!/usr/bin/env python3
"""CEUNIA Ω triad registry bridge. Safe by default: validates and plans, never pretends to run agents."""
from __future__ import annotations
import argparse, csv, hashlib, json, sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

REQUIRED = {
    "numero", "id_ceunia", "nombre_triada", "personalidad_1", "personalidad_2",
    "personalidad_3", "perfil_conocimiento", "mision", "entregable",
    "criterio_evolutivo", "criterio_integracion", "estado"
}

def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()

def load_registry(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        missing = REQUIRED - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Registro incompleto. Faltan columnas: {sorted(missing)}")
        rows = list(reader)
    if len(rows) != 99:
        raise ValueError(f"Se esperaban 99 tríadas; se encontraron {len(rows)}")
    ids = [r["id_ceunia"].strip() for r in rows]
    if len(set(ids)) != 99 or set(ids) != {f"T{i:03d}" for i in range(1, 100)}:
        raise ValueError("Los IDs deben ser únicos y cubrir T001..T099")
    for r in rows:
        for k in REQUIRED:
            if not (r.get(k) or "").strip():
                raise ValueError(f"Campo vacío '{k}' en {r.get('id_ceunia', '?')}")
        if len({r[f"personalidad_{i}"].strip() for i in range(1, 4)}) != 3:
            raise ValueError(f"La tríada {r['id_ceunia']} repite una personalidad dentro de la tríada")
    return sorted(rows, key=lambda r: r["id_ceunia"])

def mission_payload(row: dict[str, str]) -> dict[str, Any]:
    return {
        "triad_id": row["id_ceunia"], "number": int(row["numero"]),
        "triad_name": row["nombre_triada"],
        "perspectives": [row[f"personalidad_{i}"] for i in range(1, 4)],
        "knowledge_profile": row["perfil_conocimiento"], "mission": row["mision"],
        "deliverable": row["entregable"], "acceptance_criteria": row["criterio_evolutivo"],
        "integration_rule": row["criterio_integracion"],
        "execution_status": "PLANNED_NOT_EXECUTED", "requires_human_review": True,
    }

def build_plan(rows: list[dict[str, str]], limit: int | None = None) -> list[dict[str, Any]]:
    return [mission_payload(r) for r in (rows if limit is None else rows[:max(0, limit)])]

def write_plan(plan: list[dict[str, Any]], output: str | Path) -> dict[str, Any]:
    out = Path(output)
    out.parent.mkdir(parents=True, exist_ok=True)
    body = "\n".join(json.dumps(item, ensure_ascii=False, sort_keys=True) for item in plan)
    body += "\n" if body else ""
    out.write_text(body, encoding="utf-8")
    report = {
        "system": "CEUNIA Ω / 99 Triads Runtime Bridge",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "planned_missions": len(plan), "executed_missions": 0,
        "status": "PLAN_CREATED_NOT_EXECUTED", "plan_sha256": sha256_text(body),
        "plan_path": str(out),
        "safety": "No model/API/agent was called. Execution requires an explicit executor adapter and review policy."
    }
    out.with_suffix(out.suffix + ".report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report

def execute_with_adapter(plan: list[dict[str, Any]], executor: Callable[[dict[str, Any]], dict[str, Any]]) -> list[dict[str, Any]]:
    """Run only with an explicitly supplied executor. Never infer success from a missing result."""
    results = []
    for item in plan:
        raw = executor(item)
        if not isinstance(raw, dict) or "status" not in raw:
            raise ValueError(f"Executor debe devolver un dict con 'status' para {item['triad_id']}")
        results.append({"triad_id": item["triad_id"], "status": raw["status"], "result": raw,
                        "recorded_at_utc": datetime.now(timezone.utc).isoformat()})
    return results

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", required=True, help="Ruta al CSV CEUNIA_99_Triadas_Nombradas.csv")
    parser.add_argument("--output", default="artifacts/ceunia_triads_dispatch.jsonl")
    parser.add_argument("--limit", type=int, default=None, help="Limita la planificación a las primeras N tríadas")
    args = parser.parse_args(argv)
    try:
        rows = load_registry(args.registry)
        report = write_plan(build_plan(rows, args.limit), args.output)
        print(json.dumps({"validation": "PASS", "registry_triads": len(rows), **report}, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(json.dumps({"validation": "FAIL", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
