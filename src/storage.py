import json
import sqlite3
from datetime import datetime, timedelta

from src.models import LogEntry


class LogStorage:
    def __init__(self, db_path: str = "logs.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    source_ip TEXT,
                    message TEXT,
                    status_code INTEGER,
                    service_name TEXT,
                    metadata TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def save_log(self, entry: LogEntry):
        with self._get_connection() as conn:
            conn.execute(
                """
                INSERT INTO logs (timestamp, source_ip, message, status_code, service_name, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    entry.timestamp.isoformat(),
                    entry.source_ip,
                    entry.message,
                    entry.status_code,
                    entry.service_name,
                    json.dumps(entry.metadata),
                ),
            )
            conn.commit()

    def save_batch(self, entries: list[LogEntry]):
        with self._get_connection() as conn:
            conn.executemany(
                """
                INSERT INTO logs (timestamp, source_ip, message, status_code, service_name, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        e.timestamp.isoformat(),
                        e.source_ip,
                        e.message,
                        e.status_code,
                        e.service_name,
                        json.dumps(e.metadata),
                    )
                    for e in entries
                ],
            )
            conn.commit()

    def get_logs(self, limit: int = 100, offset: int = 0, service_name: str | None = None) -> list[dict]:
        query = "SELECT timestamp, source_ip, message, status_code, service_name, metadata FROM logs"
        params = []
        if service_name:
            query += " WHERE service_name = ?"
            params.append(service_name)

        query += " ORDER BY timestamp DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(query, params)
            rows = cursor.fetchall()

            logs = []
            for row in rows:
                log = dict(row)
                log["metadata"] = json.loads(log["metadata"])
                logs.append(log)
            return logs

    def get_stats(self) -> dict:
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row

            # Total logs
            total = conn.execute("SELECT COUNT(*) as count FROM logs").fetchone()["count"]

            # Logs per service
            service_counts = conn.execute(
                "SELECT service_name, COUNT(*) as count FROM logs GROUP BY service_name"
            ).fetchall()

            # Recent volume (last 24h)
            since = (datetime.now() - timedelta(days=1)).isoformat()
            recent = conn.execute(
                "SELECT COUNT(*) as count FROM logs WHERE timestamp > ?", (since,)
            ).fetchone()["count"]

            return {
                "total_logs": total,
                "services": {row["service_name"]: row["count"] for row in service_counts},
                "recent_24h": recent,
            }
