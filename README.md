# Flet Todo App

A modern, feature-rich todo application built with Python and [Flet](https://flet.dev/). This app provides a clean, intuitive interface for managing your tasks with advanced features like priority levels, deadlines, and smart filtering.

![Python](https://img.shields.io/badge/python-v3.13+-blue.svg) ![Flet](https://img.shields.io/badge/flet-v0.28.3+-green.svg) ![SQLite](https://img.shields.io/badge/sqlite-database-orange.svg)

## ✨ Features

### Core Task Management

- ✅ **Add Tasks** - Quick task creation with intuitive input
- ✅ **Edit Tasks** - In-place editing of task name, priority, and deadline
- ✅ **Delete Tasks** - Remove tasks with a single click
- ✅ **Mark Complete** - Toggle task completion status with checkboxes

### Advanced Features

- 🔥 **Priority Levels** - Three priority levels (Low, Medium, High) with visual indicators
- 📅 **Deadlines** - Set optional deadlines for tasks (date-only format)
- 🎯 **Smart Filtering** - Filter tasks by status (All, Active, Completed)
- 📊 **Task Counter** - Real-time count of remaining active tasks
- 💾 **Persistent Storage** - SQLite database for reliable data storage

## 🚀 Quick Start

### Prerequisites

- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) package manager

### Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/h-dianne/flet-todo-app.git
   cd flet-todo-app
   ```

2. **Install dependencies**

   ```bash
   uv sync
   ```

3. **Run the application**

   ```bash
   # Desktop application
   uv run python src/main.py

   # Web application with hot reload
   uv run flet run --web --port 8080 src/main.py
   ```

## 📱 How to Use

### Adding Tasks

1. Enter your task description in the main input field
2. Select a priority level
3. Optionally set a deadline using YYYY-MM-DD format (e.g., 2025-12-31)
4. Click the ➕ button or press Enter to add the task

### Managing Tasks

- **Complete**: Click the checkbox to mark tasks as done
- **Edit**: Click the ✏️ edit icon to modify task details
- **Delete**: Click the 🗑️ delete icon to remove tasks
- **Filter**: Use the tabs (All/Active/Completed) to view specific task sets

### Priority System

Tasks are automatically sorted by priority:

- 🔥🔥🔥 **High** priority tasks appear first
- 🔥🔥 **Medium** priority tasks appear second
- 🔥 **Low** priority tasks appear last

### Deadline Management

- Set deadlines in YYYY-MM-DD format (e.g., 2025-09-15)
- Tasks with deadlines show a 📅 calendar icon
- Tasks are sorted by deadline within each priority level

## 🏗️ Project Structure

```text
flet-todo-app/
├── src/
│   ├── main.py                 # Application entry point
│   ├── todo.py                 # Main todo app component
│   ├── utils.py                # Utility functions
│   ├── components/             # UI components
│   │   ├── __init__.py
│   │   ├── add_bar.py         # Task input component
│   │   ├── buttons.py         # Reusable button components
│   │   ├── filter_tabs.py     # Filter tabs component
│   │   ├── footer.py          # Footer with task counter
│   │   ├── header.py          # Application header
│   │   └── task.py            # Individual task component
│   ├── data/                   # Data layer
│   │   ├── __init__.py
│   │   ├── database.py        # SQLite database handler
│   │   └── task_repo.py       # Task repository
│   └── models/                 # Data models
│       ├── __init__.py
│       └── task_model.py      # Task data model
├── data/                       # Database storage
│   └── todos.db               # SQLite database file
├── pyproject.toml             # Project configuration
└── README.md                  # This file
```

## 🔧 Technical Details

### Built With

- **[Flet](https://flet.dev/)** - Python framework for building multi-platform apps
- **SQLite** - Lightweight database for task storage
- **Python 3.13+** - Modern Python with latest features

### Architecture

- **Component-Based Design** - Modular UI components for maintainability
- **Repository Pattern** - Clean separation between data access and business logic
- **MVC Pattern** - Model-View-Controller architecture for organized code

### Database Schema

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    priority_level TEXT DEFAULT 'low',
    deadline TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🛠️ Development

### Development Mode with Hot Reload

For the best development experience, use the web version with hot reload:

```bash
uv run flet run --web --port 8080 src/main.py
```

This will:

- Start the app in your web browser
- Automatically reload when you save changes
- Preserve app state during most code changes

### Building for Distribution

Create a standalone executable for easy distribution:

```bash
# Install PyInstaller
uv add pyinstaller

# Build standalone executable
uv run pyinstaller --onefile --name "TodoApp" src/main.py
```

The executable will be created in the `dist/` directory.

#### Data Storage in Executable

When running as an executable, the app automatically stores data in the user's AppData directory:

- **Windows**: `C:\Users\{username}\AppData\Local\FletTodoApp\todos.db`
- **Development**: `{project-directory}\data\todos.db`

This ensures:

- ✅ Data persists between app updates
- ✅ Each user has their own tasks
- ✅ No admin permissions required
- ✅ Data survives app reinstallation

#### Building Options

```bash
# Basic executable
uv run pyinstaller --onefile src/main.py

# With custom name and icon
uv run pyinstaller --onefile --name "TodoApp" --icon="icon.ico" src/main.py

# Console-free (no command prompt window)
uv run pyinstaller --onefile --windowed --name "TodoApp" src/main.py
```

## 📊 Data Management

### Task Storage

- All tasks stored in SQLite database
- Automatic timestamp tracking (created_at, updated_at)
- Efficient querying with optimized indexes
- Handles concurrent access safely

### Sorting Logic

1. **Priority Level**: High → Medium → Low
2. **Deadline**: Earliest first (within same priority)
3. **Creation Date**: Newest first (for tasks without deadlines)

This ensures your most important and urgent tasks are always visible at the top.
