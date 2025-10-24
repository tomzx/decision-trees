"""
Goal tracking and management system.

This module provides functionality for defining, tracking, and analyzing
goals that guide decision-making.
"""

import sqlite3
import json
from datetime import datetime
from typing import Optional
from core.context import Goal, DecisionPriority


class GoalTracker:
    """
    Persistent storage and management of goals.

    Goals provide the "why" behind decisions, enabling the system to
    suggest choices aligned with user objectives and track progress over time.
    """

    def __init__(self, db_path: str = "goals.db"):
        """
        Initialize the goal tracker.

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
            CREATE TABLE IF NOT EXISTS goals (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                target_value REAL NOT NULL,
                current_value REAL DEFAULT 0.0,
                deadline TEXT,
                priority INTEGER,
                tags TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                completed_at TEXT,
                is_active INTEGER DEFAULT 1
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS goal_updates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                goal_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                previous_value REAL,
                new_value REAL,
                delta REAL,
                source TEXT,
                notes TEXT,
                FOREIGN KEY (goal_id) REFERENCES goals(id)
            )
        """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_goal_updates_goal_id
            ON goal_updates(goal_id)
        """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_goal_updates_timestamp
            ON goal_updates(timestamp)
        """
        )

        conn.commit()
        conn.close()

    def create_goal(self, goal: Goal) -> Goal:
        """
        Create a new goal.

        Args:
            goal: The goal to create

        Returns:
            The created goal with timestamps
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        now = datetime.now().isoformat()

        cursor.execute(
            """
            INSERT INTO goals (
                id, name, description, target_value, current_value,
                deadline, priority, tags, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                goal.id,
                goal.name,
                goal.description,
                goal.target_value,
                goal.current_value,
                goal.deadline.isoformat() if goal.deadline else None,
                goal.priority.value,
                json.dumps(goal.tags),
                now,
                now,
            ),
        )

        conn.commit()
        conn.close()

        return goal

    def get_goal(self, goal_id: str) -> Optional[Goal]:
        """
        Retrieve a goal by ID.

        Args:
            goal_id: The goal ID

        Returns:
            The goal, or None if not found
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM goals WHERE id = ?", (goal_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        return self._row_to_goal(dict(row))

    def get_active_goals(self) -> list[Goal]:
        """
        Get all active (not completed) goals.

        Returns:
            List of active goals
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM goals
            WHERE is_active = 1
            ORDER BY priority DESC, created_at
        """
        )

        rows = cursor.fetchall()
        conn.close()

        return [self._row_to_goal(dict(row)) for row in rows]

    def update_progress(
        self, goal_id: str, delta: float, source: str = "", notes: str = ""
    ) -> Optional[Goal]:
        """
        Update progress toward a goal.

        Args:
            goal_id: The goal to update
            delta: Change in progress (positive or negative)
            source: What caused this update (e.g., decision module name)
            notes: Additional notes

        Returns:
            Updated goal, or None if not found
        """
        goal = self.get_goal(goal_id)
        if not goal:
            return None

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        previous_value = goal.current_value
        new_value = previous_value + delta
        now = datetime.now().isoformat()

        # Update goal
        cursor.execute(
            """
            UPDATE goals
            SET current_value = ?,
                updated_at = ?,
                completed_at = CASE
                    WHEN ? >= target_value AND completed_at IS NULL THEN ?
                    ELSE completed_at
                END
            WHERE id = ?
        """,
            (new_value, now, new_value, now, goal_id),
        )

        # Record update
        cursor.execute(
            """
            INSERT INTO goal_updates (
                goal_id, timestamp, previous_value, new_value, delta, source, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (goal_id, now, previous_value, new_value, delta, source, notes),
        )

        conn.commit()
        conn.close()

        # Return updated goal
        goal.current_value = new_value
        return goal

    def set_progress(
        self, goal_id: str, value: float, source: str = "", notes: str = ""
    ) -> Optional[Goal]:
        """
        Set progress to an absolute value.

        Args:
            goal_id: The goal to update
            value: New progress value
            source: What caused this update
            notes: Additional notes

        Returns:
            Updated goal, or None if not found
        """
        goal = self.get_goal(goal_id)
        if not goal:
            return None

        delta = value - goal.current_value
        return self.update_progress(goal_id, delta, source, notes)

    def complete_goal(self, goal_id: str) -> Optional[Goal]:
        """
        Mark a goal as completed.

        Args:
            goal_id: The goal to complete

        Returns:
            Updated goal, or None if not found
        """
        goal = self.get_goal(goal_id)
        if not goal:
            return None

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        now = datetime.now().isoformat()

        cursor.execute(
            """
            UPDATE goals
            SET is_active = 0,
                completed_at = ?,
                updated_at = ?
            WHERE id = ?
        """,
            (now, now, goal_id),
        )

        conn.commit()
        conn.close()

        return self.get_goal(goal_id)

    def get_progress_history(self, goal_id: str, limit: int = 100) -> list[dict]:
        """
        Get history of progress updates for a goal.

        Args:
            goal_id: The goal to query
            limit: Maximum number of updates to return

        Returns:
            List of update records
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM goal_updates
            WHERE goal_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """,
            (goal_id, limit),
        )

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def get_goals_by_tag(self, tag: str) -> list[Goal]:
        """
        Get all goals with a specific tag.

        Args:
            tag: The tag to filter by

        Returns:
            List of goals with the tag
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # SQLite doesn't have native JSON array search, so we use LIKE
        cursor.execute(
            """
            SELECT * FROM goals
            WHERE tags LIKE ?
            AND is_active = 1
            ORDER BY priority DESC
        """,
            (f'%"{tag}"%',),
        )

        rows = cursor.fetchall()
        conn.close()

        return [self._row_to_goal(dict(row)) for row in rows]

    def get_statistics(self, goal_id: str) -> dict:
        """
        Get statistics for a goal's progress.

        Args:
            goal_id: The goal to analyze

        Returns:
            Dictionary with statistics
        """
        goal = self.get_goal(goal_id)
        if not goal:
            return {}

        updates = self.get_progress_history(goal_id)

        if not updates:
            return {
                "goal_id": goal_id,
                "total_updates": 0,
                "progress": goal.progress,
            }

        total_positive = sum(u["delta"] for u in updates if u["delta"] > 0)
        total_negative = sum(u["delta"] for u in updates if u["delta"] < 0)

        return {
            "goal_id": goal_id,
            "goal_name": goal.name,
            "total_updates": len(updates),
            "progress": goal.progress,
            "current_value": goal.current_value,
            "target_value": goal.target_value,
            "remaining": goal.target_value - goal.current_value,
            "is_complete": goal.is_complete,
            "total_positive_progress": total_positive,
            "total_negative_progress": total_negative,
            "net_progress": total_positive + total_negative,
            "first_update": updates[-1]["timestamp"] if updates else None,
            "last_update": updates[0]["timestamp"] if updates else None,
        }

    def _row_to_goal(self, row: dict) -> Goal:
        """Convert database row to Goal object"""
        return Goal(
            id=row["id"],
            name=row["name"],
            description=row["description"] or "",
            target_value=row["target_value"],
            current_value=row["current_value"],
            deadline=datetime.fromisoformat(row["deadline"]) if row["deadline"] else None,
            priority=DecisionPriority(row["priority"]),
            tags=json.loads(row["tags"]) if row["tags"] else [],
        )
