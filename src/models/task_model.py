from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class TaskModel:
    """Data model for a task."""

    name: str
    completed: bool = False
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
