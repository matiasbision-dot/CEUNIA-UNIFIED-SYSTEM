"""SQLite-backed idempotency ledger for a single-node deployment.

For multi-instance production, replace with a transactional shared database.
"""
import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from .execution import ExecutionReceipt

class SQLiteExecutionLedger:
    def __init__(self, database_path: str = "ceunia-execution.sqlite3"):
        self.database_path = str(database_path)
        Path(self.database_path).parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as db:
            db.execute("""
                CREATE TABLE IF NOT EXISTS execution_ledger (
                    idempotency_key TEXT PRIMARY KEY,
                    fingerprint TEXT NOT NULL,
                    status TEXT NOT NULL CHECK(status IN ('RESERVED', 'RECORDED')),
                    receipt_json TEXT
                )
            """)

    @contextmanager
    def _connect(self):
        db = sqlite3.connect(self.database_path, timeout=10, isolation_level=None)
        try:
            db.execute("PRAGMA journal_mode=WAL")
            db.execute("PRAGMA busy_timeout=10000")
            yield db
        finally:
            db.close()

    def reserve(self, key: str, fingerprint: str) -> bool:
        if not key or not key.strip() or not fingerprint:
            raise ValueError("key and fingerprint are required")
        with self._connect() as db:
            db.execute("BEGIN IMMEDIATE")
            try:
                db.execute(
                    "INSERT INTO execution_ledger VALUES (?, ?, 'RESERVED', NULL)",
                    (key, fingerprint),
                )
                db.execute("COMMIT")
                return True
            except sqlite3.IntegrityError:
                db.execute("ROLLBACK")
                return False
            except Exception:
                db.execute("ROLLBACK")
                raise

    def record(self, receipt: ExecutionReceipt) -> None:
        payload = json.dumps({
            "provider": receipt.provider,
            "idempotency_key": receipt.idempotency_key,
            "status": receipt.status,
            "external_reference": receipt.external_reference,
        }, sort_keys=True)
        with self._connect() as db:
            db.execute("BEGIN IMMEDIATE")
            try:
                cursor = db.execute(
                    """UPDATE execution_ledger SET status='RECORDED', receipt_json=?
                       WHERE idempotency_key=? AND status='RESERVED'""",
                    (payload, receipt.idempotency_key),
                )
                if cursor.rowcount != 1:
                    raise ValueError("no reserved ledger entry for receipt")
                db.execute("COMMIT")
            except Exception:
                db.execute("ROLLBACK")
                raise

    def get(self, key: str) -> dict | None:
        with self._connect() as db:
            row = db.execute(
                "SELECT fingerprint, status, receipt_json FROM execution_ledger WHERE idempotency_key=?",
                (key,),
            ).fetchone()
        if row is None:
            return None
        return {"fingerprint": row[0], "status": row[1],
                "receipt": json.loads(row[2]) if row[2] else None}
