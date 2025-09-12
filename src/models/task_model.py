from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class TaskModel:
    """Data model for a task."""

    name: str
    priority_level: str = "low"
    completed: bool = False
    id: Optional[int] = None
    deadline: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
