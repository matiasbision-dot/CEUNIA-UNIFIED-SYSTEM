"""CEUNIA Ω MIP: integrated, auditable orchestration core.

This module deliberately does not claim autonomous learning. It provides:
- deterministic routing to explicitly registered executors,
- a minimal output validator,
- meta-observation and non-mutating evolution recommendations,
- SQLite event storage with a SHA-256 hash chain,
- explicit approval gating for actions marked as requiring approval.

No model provider is called unless the caller registers an executor.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Optional
import hashlib
import json
import sqlite3

Executor = Callable[[str], str]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"), default=str)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


@dataclass
class Route:
    executor_name: str
    task_type: str
    reason: str


class CEUNIARouter:
    """Routes tasks deterministically; never randomly invents provider availability."""

    def __init__(self, default_executor: str = "default") -> None:
        self.default_executor = default_executor
        self._routes: dict[str, str] = {}

    def set_route(self, task_type: str, executor_name: str) -> None:
        self._routes[task_type.strip().lower()] = executor_name

    def select(self, task_type: str, available_executors: set[str]) -> Route:
        requested = self._routes.get(task_type.strip().lower(), self.default_executor)
        if requested in available_executors:
            return Route(requested, task_type, "configured_route" if requested != self.default_executor else "default_route")
        if self.default_executor in available_executors:
            return Route(self.default_executor, task_type, "fallback_to_default")
        raise RuntimeError("No registered executor is available for this task.")


class CEUNIAValidator:
    """Minimal structural validation, not semantic truth verification."""

    def evaluate(self, output: Any) -> dict[str, Any]:
        nonempty = isinstance(output, str) and bool(output.strip())
        return {
            "status": "PASS" if nonempty else "FAIL",
            "nonempty_output": nonempty,
            "score": 1.0 if nonempty else 0.0,
            "scope": "structural_only",
            "limitations": ["Does not verify factual correctness, safety, or task success."],
        }


class CEUNIAMetaObserver:
    def observe(self, task_type: str, route: Route, validation: dict[str, Any],
                approval_required: bool, approval_granted: bool) -> dict[str, Any]:
        return {
            "timestamp": utc_now(),
            "task_type": task_type,
            "executor": route.executor_name,
            "route_reason": route.reason,
            "validation_status": validation["status"],
            "approval_required": approval_required,
            "approval_granted": approval_granted,
            "observation_scope": "execution_metadata",
        }


class CEUNIAEvolution:
    """Produces recommendations only; it does not alter its own policies."""

    def recommend(self, validation: dict[str, Any], approval_blocked: bool = False) -> dict[str, str]:
        if approval_blocked:
            recommendation = "Request explicit authorization before retrying."
            trend = "blocked_by_policy"
        elif validation.get("status") != "PASS":
            recommendation = "Inspect failure and correct the executor or input before retrying."
            trend = "degraded"
        else:
            recommendation = "Keep current configuration; require benchmark evidence before changing policy."
            trend = "unassessed"
        return {"trend": trend, "recommendation": recommendation, "self_modification": "disabled"}


class CEUNIAEventStore:
    """SQLite append-only event log with a verifiable SHA-256 chain."""

    def __init__(self, path: str | Path = "ceunia_events.sqlite3") -> None:
        self.path = str(path)
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    event_json TEXT NOT NULL,
                    previous_hash TEXT NOT NULL,
                    event_hash TEXT NOT NULL UNIQUE
                )
            """)

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.path)

    def append(self, event: dict[str, Any]) -> dict[str, Any]:
        timestamp = utc_now()
        event_json = canonical_json(event)
        with self._connect() as conn:
            row = conn.execute("SELECT event_hash FROM events ORDER BY id DESC LIMIT 1").fetchone()
            previous_hash = row[0] if row else "GENESIS"
            material = canonical_json({
                "timestamp": timestamp,
                "event": json.loads(event_json),
                "previous_hash": previous_hash,
            })
            event_hash = sha256_text(material)
            conn.execute(
                "INSERT INTO events(timestamp, event_json, previous_hash, event_hash) VALUES (?, ?, ?, ?)",
                (timestamp, event_json, previous_hash, event_hash),
            )
        return {"timestamp": timestamp, "previous_hash": previous_hash, "event_hash": event_hash}

    def verify_chain(self) -> dict[str, Any]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT timestamp, event_json, previous_hash, event_hash FROM events ORDER BY id"
            ).fetchall()
        previous = "GENESIS"
        for index, (timestamp, event_json, previous_hash, stored_hash) in enumerate(rows, start=1):
            if previous_hash != previous:
                return {"valid": False, "events_checked": index, "failed_at": index, "reason": "previous_hash_mismatch"}
            material = canonical_json({
                "timestamp": timestamp,
                "event": json.loads(event_json),
                "previous_hash": previous_hash,
            })
            calculated = sha256_text(material)
            if calculated != stored_hash:
                return {"valid": False, "events_checked": index, "failed_at": index, "reason": "event_hash_mismatch"}
            previous = stored_hash
        return {"valid": True, "events_checked": len(rows), "head_hash": previous}


class CEUNIAEngine:
    """Integrated CEUNIA core. Inject the actual model/API executor from outside."""

    def __init__(self, store_path: str | Path = "ceunia_events.sqlite3") -> None:
        self.router = CEUNIARouter()
        self.validator = CEUNIAValidator()
        self.meta_observer = CEUNIAMetaObserver()
        self.evolution = CEUNIAEvolution()
        self.store = CEUNIAEventStore(store_path)
        self._executors: dict[str, Executor] = {}

    def register_executor(self, name: str, executor: Executor) -> None:
        if not name.strip() or not callable(executor):
            raise ValueError("Executor requires a non-empty name and callable.")
        self._executors[name] = executor

    def run(self, task: str, task_type: str = "general", *,
            requires_approval: bool = False, approval_granted: bool = False) -> dict[str, Any]:
        if not isinstance(task, str) or not task.strip():
            raise ValueError("task must be a non-empty string")

        route = self.router.select(task_type, set(self._executors))
        blocked = requires_approval and not approval_granted
        if blocked:
            output: Optional[str] = None
            validation = {
                "status": "BLOCKED",
                "nonempty_output": False,
                "score": 0.0,
                "scope": "approval_gate",
                "limitations": ["Execution was not performed because required approval was not granted."],
            }
        else:
            output = self._executors[route.executor_name](task)
            validation = self.validator.evaluate(output)

        observation = self.meta_observer.observe(
            task_type, route, validation, requires_approval, approval_granted
        )
        evolution = self.evolution.recommend(validation, approval_blocked=blocked)
        event = {
            "schema": "ceunia.event.v1",
            "task_type": task_type,
            "task_sha256": sha256_text(task),
            "executor": route.executor_name,
            "route_reason": route.reason,
            "validation": validation,
            "observation": observation,
            "evolution": evolution,
            "output_sha256": sha256_text(output) if output is not None else None,
        }
        provenance = self.store.append(event)
        return {
            "output": output,
            "route": asdict(route),
            "validation": validation,
            "observation": observation,
            "evolution": evolution,
            "provenance": provenance,
        }

    def verify_provenance(self) -> dict[str, Any]:
        return self.store.verify_chain()
