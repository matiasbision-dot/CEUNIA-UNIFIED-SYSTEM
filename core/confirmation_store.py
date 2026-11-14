"""SQLite persistence for ONECLICK proposals, decisions and outcomes.

This store is a local evidence ledger. It does not call merchants, submit orders,
reserve stock, authorize payments or store payment credentials.
"""
from dataclasses import asdict
from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import json
import sqlite3
from pathlib import Path
from .proposal import OrderProposal
from .confirmation import ConfirmationRecord

class ConfirmationStore:
    def __init__(self, database_path: str | Path):
        self.database_path = str(database_path)
        if self.database_path != ":memory:":
            Path(self.database_path).parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self):
        connection = sqlite3.connect(self.database_path, timeout=10)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def _initialize(self):
        with self._connect() as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS proposals (
                    proposal_id TEXT PRIMARY KEY,
                    snapshot_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    valid_until TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS confirmations (
                    confirmation_id TEXT PRIMARY KEY,
                    proposal_id TEXT NOT NULL UNIQUE REFERENCES proposals(proposal_id),
                    decision TEXT NOT NULL CHECK(decision IN ('confirm','decline')),
                    status TEXT NOT NULL,
                    decided_at TEXT NOT NULL,
                    record_json TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS outcomes (
                    outcome_id TEXT PRIMARY KEY,
                    proposal_id TEXT NOT NULL REFERENCES proposals(proposal_id),
                    outcome TEXT NOT NULL,
                    source TEXT NOT NULL,
                    external_reference TEXT,
                    observed_at TEXT NOT NULL,
                    idempotency_key TEXT NOT NULL UNIQUE,
                    details_json TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_outcomes_proposal
                    ON outcomes(proposal_id, observed_at);
            """)

    @staticmethod
    def _proposal_snapshot(proposal: OrderProposal) -> str:
        data = asdict(proposal)
        for key in ("unit_price", "subtotal"):
            data[key] = str(data[key])
        for key in ("catalog_observed_at", "created_at", "valid_until"):
            data[key] = data[key].isoformat()
        data["modifiers"] = list(proposal.modifiers)
        return json.dumps(data, sort_keys=True, separators=(",", ":"))

    def save_proposal(self, proposal: OrderProposal) -> bool:
        if not isinstance(proposal, OrderProposal):
            raise ValueError("valid_order_proposal_required")
        snapshot = self._proposal_snapshot(proposal)
        with self._connect() as db:
            existing = db.execute(
                "SELECT snapshot_json FROM proposals WHERE proposal_id=?",
                (proposal.proposal_id,)).fetchone()
            if existing:
                if existing["snapshot_json"] != snapshot:
                    raise ValueError("proposal_id_snapshot_conflict")
                return False
            db.execute(
                "INSERT INTO proposals VALUES (?, ?, ?, ?)",
                (proposal.proposal_id, snapshot, proposal.created_at.isoformat(),
                 proposal.valid_until.isoformat()))
            return True

    def record_decision(self, record: ConfirmationRecord) -> bool:
        if not isinstance(record, ConfirmationRecord):
            raise ValueError("valid_confirmation_record_required")
        with self._connect() as db:
            if not db.execute("SELECT 1 FROM proposals WHERE proposal_id=?",
                              (record.proposal_id,)).fetchone():
                raise ValueError("proposal_must_be_saved_first")
            existing = db.execute(
                "SELECT confirmation_id, decision, decided_at FROM confirmations WHERE proposal_id=?",
                (record.proposal_id,)).fetchone()
            if existing:
                if (existing["confirmation_id"] == record.confirmation_id
                    and existing["decision"] == record.decision
                    and existing["decided_at"] == record.decided_at.isoformat()):
                    return False
                raise ValueError("proposal_already_has_a_different_decision")
            payload = {
                "confirmation_id": record.confirmation_id,
                "proposal_id": record.proposal_id,
                "decision": record.decision, "status": record.status,
                "decided_at": record.decided_at.isoformat(),
                "execution_authorized": record.execution_authorized,
                "order_submitted": record.order_submitted,
                "payment_taken": record.payment_taken,
            }
            db.execute(
                "INSERT INTO confirmations VALUES (?, ?, ?, ?, ?, ?)",
                (record.confirmation_id, record.proposal_id, record.decision,
                 record.status, record.decided_at.isoformat(),
                 json.dumps(payload, sort_keys=True, separators=(",", ":"))))
            return True

    def record_outcome(self, *, proposal_id: str, outcome: str, source: str,
                       observed_at: datetime, idempotency_key: str,
                       external_reference: str | None = None,
                       details: dict | None = None) -> bool:
        if not all(isinstance(v, str) and v.strip() for v in
                   (proposal_id, outcome, source, idempotency_key)):
            raise ValueError("outcome_identity_and_source_required")
        if observed_at.tzinfo is None or observed_at.utcoffset() is None:
            raise ValueError("outcome_timestamp_must_be_timezone_aware")
        if details is not None and not isinstance(details, dict):
            raise ValueError("outcome_details_must_be_object")
        details_json = json.dumps(details or {}, sort_keys=True,
                                  separators=(",", ":"), default=str)
        payload = json.dumps({
            "proposal_id": proposal_id, "outcome": outcome, "source": source,
            "observed_at": observed_at.isoformat(),
            "external_reference": external_reference, "details": details or {},
        }, sort_keys=True, separators=(",", ":"), default=str)
        outcome_id = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        with self._connect() as db:
            if not db.execute("SELECT 1 FROM proposals WHERE proposal_id=?",
                              (proposal_id,)).fetchone():
                raise ValueError("proposal_must_be_saved_first")
            existing = db.execute(
                "SELECT outcome_id FROM outcomes WHERE idempotency_key=?",
                (idempotency_key,)).fetchone()
            if existing:
                if existing["outcome_id"] == outcome_id:
                    return False
                raise ValueError("outcome_idempotency_conflict")
            db.execute(
                "INSERT INTO outcomes VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (outcome_id, proposal_id, outcome, source, external_reference,
                 observed_at.isoformat(), idempotency_key, details_json))
            return True

    def get_history(self, proposal_id: str) -> dict:
        with self._connect() as db:
            proposal = db.execute(
                "SELECT snapshot_json FROM proposals WHERE proposal_id=?",
                (proposal_id,)).fetchone()
            if not proposal:
                raise ValueError("proposal_not_found")
            decision = db.execute(
                "SELECT record_json FROM confirmations WHERE proposal_id=?",
                (proposal_id,)).fetchone()
            outcomes = db.execute(
                "SELECT outcome_id, outcome, source, external_reference, observed_at, details_json "
                "FROM outcomes WHERE proposal_id=? ORDER BY observed_at, outcome_id",
                (proposal_id,)).fetchall()
            return {
                "proposal": json.loads(proposal["snapshot_json"]),
                "confirmation": json.loads(decision["record_json"]) if decision else None,
                "outcomes": [{
                    "outcome_id": row["outcome_id"], "outcome": row["outcome"],
                    "source": row["source"], "external_reference": row["external_reference"],
                    "observed_at": row["observed_at"],
                    "details": json.loads(row["details_json"]),
                } for row in outcomes],
            }
