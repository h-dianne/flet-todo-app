import sqlite3
from pathlib import Path


class Database:
    """SQlite database handler for the todo app"""

    def __init__(self, db_path: str = "data/todos.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        self._init_database()

    def _init_database(self) -> None:
        """Create the database and tables if they don't exist"""
        with self.connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        completed BOOLEAN DEFAULT FALSE,
                        priority_level TEXT DEFAULT 'low',
                        deadline TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Add new columns to existing table if they don't exist
            try:
                conn.execute(
                    "ALTER TABLE tasks ADD COLUMN priority_level TEXT DEFAULT 'low'"
                )
            except Exception:
                pass  # Column already exists

            try:
                conn.execute("ALTER TABLE tasks ADD COLUMN deadline TIMESTAMP")
            except Exception:
                pass  # Column already exists

            conn.commit()

    def connection(self) -> sqlite3.Connection:
        """Get a database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # enable column access by name
        return conn
