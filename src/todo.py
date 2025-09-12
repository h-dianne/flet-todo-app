"""Todo application root control composed of reusable components."""

from typing import Dict

import flet as ft

from .components import AddTaskRow, FilterTabs, FooterBar, Header, Task
from .data import Database, TaskRepository


class TodoApp(ft.Column):
    """Main todo application component."""

    def __init__(self) -> None:
        super().__init__()

        # Initialize database and repository
        self.db = Database()
        self.task_repo = TaskRepository(self.db)

        # Load existing tasks
        self.tasks: Dict[int, Task] = {}
        self._load_tasks()

        # UI Components
        self.new_task = AddTaskRow(on_submit=self.add_clicked)
        self.tasks_views = ft.Column()
        self.filter_tabs = FilterTabs(on_change=self.tabs_changed)
        self.items_left = ft.Text("0 items left")

        # Update tasks view
        self._update_tasks_view()

        # Build the UI
        self.width = 600
        self.controls = [
            Header(),
            self.new_task,
            ft.Column(
                spacing=25,
                controls=[
                    self.filter_tabs,
                    self.tasks_views,
                    FooterBar(self.items_left),
                ],
            ),
        ]

    def _load_tasks(self) -> None:
        """Load tasks from database."""
        task_models = self.task_repo.get_all_tasks()
        self.tasks = {
            model.id: Task(
                task_model=model,
                task_status_change=self.task_status_change,
                task_delete=self.task_delete,
                task_edit=self.task_edit,
            )
            for model in task_models
        }

    def add_clicked(self, e: ft.ControlEvent | None) -> None:
        """Handle adding a new task"""
        task_data = self.new_task.get_task_data()
        task_name = task_data["name"].strip()
        if not task_name:
            return

        # Create task in database
        task_model = self.task_repo.create_task(
            name=task_name,
            priority_level=task_data["priority_level"],
            deadline=task_data["deadline"],
        )

        # Create UI Component
        task_component = Task(
            task_model=task_model,
            task_status_change=self.task_status_change,
            task_delete=self.task_delete,
            task_edit=self.task_edit,
        )

        # Add to tasks dict
        self.tasks[task_model.id] = task_component

        # Clear input and update view
        self.new_task.clear_inputs()
        self._update_tasks_view()
        self.new_task.input.focus()
        self.update()

    def task_status_change(self, task: Task) -> None:
        """Handle task status change."""
        # Update in database
        self.task_repo.update_task(task.task_model.id, completed=task.completed)
        self._update_tasks_view()
        self.update()

    def task_edit(self, task: Task) -> None:
        """Handle task edit."""
        # Update in database
        self.task_repo.update_task(
            task.task_model.id,
            name=task.task_model.name,
            priority_level=task.task_model.priority_level,
            deadline=task.task_model.deadline,
        )
        self._update_tasks_view()
        self.update()

    def task_delete(self, task: Task) -> None:
        """Handle task deletion."""
        # Delete from database
        self.task_repo.delete_task(task.task_model.id)

        # Remove from tasks dictionary
        del self.tasks[task.task_model.id]

        self._update_tasks_view()
        self.update()

    def tabs_changed(self, e: ft.ControlEvent) -> None:
        """Handle filter tab change."""
        self._update_tasks_view()

    def _update_tasks_view(self) -> None:
        """Update the tasks view based on current filter."""
        # Get current filter
        status = (
            self.filter_tabs.selected_tab
            if hasattr(self.filter_tabs, "selected_tab")
            else "all"
        )

        # Filter tasks
        if status == "all":
            filtered_tasks = list(self.tasks.values())
        elif status == "active":
            filtered_tasks = [
                task for task in self.tasks.values() if not task.completed
            ]
        elif status == "completed":
            filtered_tasks = [task for task in self.tasks.values() if task.completed]
        else:
            filtered_tasks = list(self.tasks.values())

        # Update tasks view
        self.tasks_views.controls = filtered_tasks

        # Update items left counter
        active_count = len([task for task in self.tasks.values() if not task.completed])
        self.items_left.value = (
            f"{active_count} item{'s' if active_count != 1 else ''} left"
        )
