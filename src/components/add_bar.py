"""Add-task input row component."""

from datetime import datetime
from typing import Callable, Optional

import flet as ft

from .buttons import add_fab


class AddTaskRow(ft.Column):
    """A column containing task input fields and an add button."""

    def __init__(
        self,
        on_submit: Optional[Callable[[ft.ControlEvent], None]] = None,
        on_add_click: Optional[Callable[[ft.ControlEvent], None]] = None,
    ) -> None:
        self.input: ft.TextField = ft.TextField(
            hint_text="What needs to be done?",
            on_submit=on_submit,
            expand=True,
        )

        self.priority_dropdown: ft.Dropdown = ft.Dropdown(
            label="Priority",
            width=180,
            options=[
                ft.dropdown.Option("low", "🔥 Low"),
                ft.dropdown.Option("medium", "🔥🔥 Medium"),
                ft.dropdown.Option("high", "🔥🔥🔥 High"),
            ],
            value="low",
        )

        self.deadline_input: ft.TextField = ft.TextField(
            label="Deadline (optional)",
            hint_text="YYYY-MM-DD",
            width=200,
        )

        add_btn: ft.FloatingActionButton = add_fab(on_add_click or on_submit)

        input_row = ft.Row(
            controls=[self.input, self.priority_dropdown, self.deadline_input, add_btn],
            spacing=10,
        )

        super().__init__(controls=[input_row], spacing=10)

    def get_task_data(self) -> dict:
        """Get the task data from input fields."""
        deadline = None
        if self.deadline_input.value:
            try:
                deadline = datetime.strptime(self.deadline_input.value, "%Y-%m-%d")
            except ValueError:
                deadline = None

        return {
            "name": self.input.value,
            "priority_level": self.priority_dropdown.value,
            "deadline": deadline,
        }

    def clear_inputs(self) -> None:
        """Clear all input fields."""
        self.input.value = ""
        self.priority_dropdown.value = "low"
        self.deadline_input.value = ""
        self.update()
