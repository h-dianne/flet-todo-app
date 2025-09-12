import sqlite3
from datetime import datetime
from typing import List, Optional

from ..models.task_model import TaskModel
from .database import Database


class TaskRepository:
    """Repository for task data operations"""

    def __init__(self, database: Database):
        self.db = database

    def create_task(
        self,
        name: str,
        priority_level: str = "low",
        deadline: Optional[datetime] = None,
    ) -> TaskModel:
        """Create a new task."""
        with self.db.connection() as conn:
            cursor = conn.execute(
                "INSERT INTO tasks (name, priority_level, deadline) VALUES (?, ?, ?)",
                (name, priority_level, deadline.isoformat() if deadline else None),
            )
            conn.commit()

            # Get the created task
            row = conn.execute(
                "SELECT * FROM tasks WHERE id = ?", (cursor.lastrowid,)
            ).fetchone()
            return self._row_to_task(row)

    def get_all_tasks(self) -> List[TaskModel]:
        """Get all tasks ordered by priority and deadline."""
        with self.db.connection() as conn:
            rows = conn.execute("""
                SELECT * FROM tasks
                ORDER BY
                    CASE priority_level
                        WHEN 'high' THEN 1
                        WHEN 'medium' THEN 2
                        WHEN 'low' THEN 3
                        ELSE 4
                    END,
                    deadline ASC NULLS LAST,
                    created_at DESC
            """).fetchall()
        return [self._row_to_task(row) for row in rows]

    def update_task(
        self,
        task_id: int,
        name: Optional[str] = None,
        completed: Optional[bool] = None,
        priority_level: Optional[str] = None,
        deadline: Optional[datetime] = None,
    ) -> Optional[TaskModel]:
        """Update a task"""
        updates = []
        params = []

        if name is not None:
            updates.append("name = ? ")
            params.append(name)

        if completed is not None:
            updates.append("completed = ? ")
            params.append(completed)

        if priority_level is not None:
            updates.append("priority_level = ? ")
            params.append(priority_level)

        if deadline is not None:
            updates.append("deadline = ? ")
            params.append(deadline.isoformat())

        updates.append("updated_at = CURRENT_TIMESTAMP")
        params.append(task_id)

        with self.db.connection() as conn:
            conn.execute(f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?", params)
            conn.commit()

            # Get the updated task
            row = conn.execute(
                "SELECT * FROM tasks WHERE id = ?", (task_id,)
            ).fetchone()

            return self._row_to_task(row) if row else None

    def delete_task(self, task_id: int) -> bool:
        """Delete a task"""
        with self.db.connection() as conn:
            cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
            return cursor.rowcount > 0

    def _row_to_task(self, row: sqlite3.Row) -> TaskModel:
        """Convert a database row to a TaskModel."""
        deadline = None
        if "deadline" in row.keys() and row["deadline"]:
            try:
                deadline = datetime.fromisoformat(row["deadline"])
            except (ValueError, TypeError):
                deadline = None

        # Handle priority_level with fallback for older records
        priority_level = "low"
        if "priority_level" in row.keys() and row["priority_level"]:
            priority_level = row["priority_level"]

        return TaskModel(
            id=row["id"],
            name=row["name"],
            completed=bool(row["completed"]),
            priority_level=priority_level,
            deadline=deadline,
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )
