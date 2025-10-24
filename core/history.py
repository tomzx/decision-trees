"""
Decision history tracking and analytics.

This module provides persistent storage and analysis of decision history,
enabling learning, pattern recognition, and optimization over time.
"""

import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Any
from dataclasses import asdict
from core.context import DecisionOutcome


class DecisionHistory:
    """
    Persistent storage and retrieval of decision outcomes.

    Uses SQLite for lightweight, local storage of decision history.
    Supports querying, analytics, and pattern recognition.
    """

    def __init__(self, db_path: str = "decision_history.db"):
        """
        Initialize the decision history tracker.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """Create database tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS decisions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                decision_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                choice_made TEXT,
                duration_seconds REAL,
                satisfaction_rating INTEGER,
                energy_cost INTEGER,
                notes TEXT,
                completion_time TEXT,
                interruptions INTEGER DEFAULT 0,
                context_switches INTEGER DEFAULT 0,
                tags TEXT,
                goal_progress TEXT,
                metadata TEXT
            )
        """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_decision_id
            ON decisions(decision_id)
        """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_timestamp
            ON decisions(timestamp)
        """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_tags
            ON decisions(tags)
        """
        )

        conn.commit()
        conn.close()

    def record(self, outcome: DecisionOutcome) -> int:
        """
        Record a decision outcome.

        Args:
            outcome: The decision outcome to record

        Returns:
            The ID of the recorded decision
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO decisions (
                decision_id, timestamp, choice_made, duration_seconds,
                satisfaction_rating, energy_cost, notes, completion_time,
                interruptions, context_switches, tags, goal_progress, metadata
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                outcome.decision_id,
                outcome.timestamp.isoformat(),
                json.dumps(outcome.choice_made),
                outcome.duration.total_seconds() if outcome.duration else None,
                outcome.satisfaction_rating,
                outcome.energy_cost.value if outcome.energy_cost else None,
                outcome.notes,
                outcome.completion_time.isoformat() if outcome.completion_time else None,
                outcome.interruptions,
                outcome.context_switches,
                json.dumps(outcome.tags),
                json.dumps(outcome.goal_progress),
                json.dumps({}),  # Reserved for future metadata
            ),
        )

        decision_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return decision_id

    def get_recent(
        self, decision_id: Optional[str] = None, limit: int = 100
    ) -> list[dict[str, Any]]:
        """
        Get recent decision history.

        Args:
            decision_id: Filter by specific decision ID (optional)
            limit: Maximum number of records to return

        Returns:
            List of decision records as dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        if decision_id:
            cursor.execute(
                """
                SELECT * FROM decisions
                WHERE decision_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """,
                (decision_id, limit),
            )
        else:
            cursor.execute(
                """
                SELECT * FROM decisions
                ORDER BY timestamp DESC
                LIMIT ?
            """,
                (limit,),
            )

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def get_by_date_range(
        self, start_date: datetime, end_date: datetime, decision_id: Optional[str] = None
    ) -> list[dict[str, Any]]:
        """
        Get decisions within a date range.

        Args:
            start_date: Start of date range
            end_date: End of date range
            decision_id: Filter by specific decision ID (optional)

        Returns:
            List of decision records
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        if decision_id:
            cursor.execute(
                """
                SELECT * FROM decisions
                WHERE decision_id = ?
                  AND timestamp >= ?
                  AND timestamp <= ?
                ORDER BY timestamp
            """,
                (decision_id, start_date.isoformat(), end_date.isoformat()),
            )
        else:
            cursor.execute(
                """
                SELECT * FROM decisions
                WHERE timestamp >= ?
                  AND timestamp <= ?
                ORDER BY timestamp
            """,
                (start_date.isoformat(), end_date.isoformat()),
            )

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def get_statistics(self, decision_id: str, days: int = 30) -> dict[str, Any]:
        """
        Get statistics for a specific decision over recent history.

        Args:
            decision_id: The decision to analyze
            days: Number of days to look back

        Returns:
            Dictionary with statistics (count, avg_duration, avg_satisfaction, etc.)
        """
        cutoff_date = datetime.now() - timedelta(days=days)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                COUNT(*) as count,
                AVG(duration_seconds) as avg_duration,
                AVG(satisfaction_rating) as avg_satisfaction,
                AVG(energy_cost) as avg_energy,
                AVG(interruptions) as avg_interruptions,
                AVG(context_switches) as avg_context_switches,
                MIN(timestamp) as first_occurrence,
                MAX(timestamp) as last_occurrence
            FROM decisions
            WHERE decision_id = ?
              AND timestamp >= ?
        """,
            (decision_id, cutoff_date.isoformat()),
        )

        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                "decision_id": decision_id,
                "days_analyzed": days,
                "count": row[0],
                "avg_duration_seconds": row[1],
                "avg_satisfaction": row[2],
                "avg_energy_cost": row[3],
                "avg_interruptions": row[4],
                "avg_context_switches": row[5],
                "first_occurrence": row[6],
                "last_occurrence": row[7],
            }
        else:
            return {
                "decision_id": decision_id,
                "days_analyzed": days,
                "count": 0,
            }

    def get_most_frequent(self, days: int = 30, limit: int = 10) -> list[dict[str, Any]]:
        """
        Get the most frequently made decisions.

        Args:
            days: Number of days to look back
            limit: Maximum number of decisions to return

        Returns:
            List of decisions with frequency counts
        """
        cutoff_date = datetime.now() - timedelta(days=days)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                decision_id,
                COUNT(*) as frequency,
                AVG(satisfaction_rating) as avg_satisfaction
            FROM decisions
            WHERE timestamp >= ?
            GROUP BY decision_id
            ORDER BY frequency DESC
            LIMIT ?
        """,
            (cutoff_date.isoformat(), limit),
        )

        rows = cursor.fetchall()
        conn.close()

        return [
            {
                "decision_id": row[0],
                "frequency": row[1],
                "avg_satisfaction": row[2],
            }
            for row in rows
        ]

    def find_patterns(self, decision_id: str, days: int = 30) -> dict[str, Any]:
        """
        Find patterns in decision-making for a specific decision.

        Args:
            decision_id: The decision to analyze
            days: Number of days to look back

        Returns:
            Dictionary with pattern insights
        """
        records = self.get_by_date_range(
            datetime.now() - timedelta(days=days), datetime.now(), decision_id
        )

        if not records:
            return {"decision_id": decision_id, "patterns_found": False}

        # Analyze day of week patterns
        day_of_week_counts = {}
        hour_of_day_counts = {}

        for record in records:
            timestamp = datetime.fromisoformat(record["timestamp"])
            day_name = timestamp.strftime("%A")
            hour = timestamp.hour

            day_of_week_counts[day_name] = day_of_week_counts.get(day_name, 0) + 1
            hour_of_day_counts[hour] = hour_of_day_counts.get(hour, 0) + 1

        return {
            "decision_id": decision_id,
            "patterns_found": True,
            "total_occurrences": len(records),
            "day_of_week_distribution": day_of_week_counts,
            "hour_of_day_distribution": hour_of_day_counts,
            "most_common_day": max(day_of_week_counts, key=day_of_week_counts.get)
            if day_of_week_counts
            else None,
            "most_common_hour": max(hour_of_day_counts, key=hour_of_day_counts.get)
            if hour_of_day_counts
            else None,
        }

    def get_learning_defaults(self, decision_id: str, days: int = 30) -> Optional[Any]:
        """
        Learn the most common choice for a decision based on history.

        This enables smart defaults that improve over time.

        Args:
            decision_id: The decision to learn from
            days: Number of days of history to consider

        Returns:
            The most common choice, or None if no history
        """
        records = self.get_by_date_range(
            datetime.now() - timedelta(days=days), datetime.now(), decision_id
        )

        if not records:
            return None

        # Count frequency of each choice
        choice_counts = {}
        for record in records:
            choice = record["choice_made"]
            if choice:
                choice_counts[choice] = choice_counts.get(choice, 0) + 1

        if not choice_counts:
            return None

        # Return most common choice
        most_common = max(choice_counts, key=choice_counts.get)

        try:
            return json.loads(most_common)
        except json.JSONDecodeError:
            return most_common
