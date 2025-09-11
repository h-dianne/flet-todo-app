"""Todo application root control composed of reusable components."""

import flet as ft

from src.components import AddTaskRow, FilterTabs, FooterBar, Header, Task


class TodoApp(ft.Column):
    """Main app layout and orchestration for tasks and filters."""

    def __init__(self) -> None:
        super().__init__()

        self.add_bar = AddTaskRow(
            on_submit=self.add_clicked, on_add_click=self.add_clicked
        )
        self.tasks = ft.Column()

        self.filter = FilterTabs(on_change=self.tabs_changed, selected_index=0)

        self.footer = FooterBar(on_clear=self.clear_clicked)

        self.width = 600
        self.controls = [
            Header("Todos"),
            self.add_bar,
            ft.Column(
                spacing=25,
                controls=[
                    self.filter,
                    self.tasks,
                    self.footer,
                ],
            ),
        ]

    def add_clicked(self, e: ft.ControlEvent | None) -> None:
        """Add a new task from the input field."""
        value = self.add_bar.input.value
        if value:
            task = Task(value, self.task_status_change, self.task_delete)
            self.tasks.controls.append(task)
            self.add_bar.input.value = ""
            self.add_bar.input.focus()
            self.update()

    def task_status_change(self, task: Task) -> None:
        """Handle task status change."""
        self.update()

    def task_delete(self, task: Task) -> None:
        """Handle task deletion."""
        self.tasks.controls.remove(task)
        self.update()

    def tabs_changed(self, e: ft.ControlEvent | None) -> None:
        """Handle filter tab change."""
        self.update()

    def clear_clicked(self, e: ft.ControlEvent | None) -> None:
        """Clear all completed tasks."""
        for task in list(self.tasks.controls):
            if task.completed:
                self.task_delete(task)

    def before_update(self) -> None:
        """Update task visibility based on selected filter before rendering."""
        status: str = self.filter.tabs[self.filter.selected_index].text
        count: int = 0
        for task in self.tasks.controls:
            task.visible = (
                status == "all"
                or (status == "active" and not task.completed)
                or (status == "completed" and task.completed)
            )
            if not task.completed:
                count += 1
        self.footer.set_count(count)
