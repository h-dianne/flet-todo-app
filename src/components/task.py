"""Task item component.

Represents a single to-do item with the ability to toggle completion,
edit its label, priority, deadline, and delete it. The parent provides callbacks to react
to status changes and deletions.
"""

from datetime import datetime
from typing import Callable

import flet as ft

from ..models import TaskModel
from ..utils import get_priority_emoji
from .buttons import delete_icon_button, edit_icon_button, save_icon_button


class Task(ft.Column):
    """A reusable to-do item widget."""

    def __init__(
        self,
        task_model: TaskModel,
        task_status_change: Callable[["Task"], None],
        task_delete: Callable[["Task"], None],
        task_edit: Callable[["Task"], None] = None,
    ) -> None:
        super().__init__()
        self.task_model = task_model
        self.completed: bool = task_model.completed
        self.task_status_change = task_status_change
        self.task_delete = task_delete
        self.task_edit = task_edit

        # Create task info with priority and deadline
        task_info = ft.Column(
            spacing=2,
            controls=[
                ft.Text(
                    value=self.task_model.name,
                    theme_style=ft.TextThemeStyle.BODY_MEDIUM,
                    weight=ft.FontWeight.W_500,
                ),
                ft.Row(
                    spacing=10,
                    controls=[
                        ft.Text(
                            value=f"{get_priority_emoji(self.task_model.priority_level)} {self.task_model.priority_level.title()}",
                            theme_style=ft.TextThemeStyle.BODY_SMALL,
                            color=ft.Colors.ORANGE_600,
                        ),
                        ft.Text(
                            value=f"📅 {self.task_model.deadline.strftime('%Y-%m-%d')}"
                            if self.task_model.deadline
                            else "",
                            theme_style=ft.TextThemeStyle.BODY_SMALL,
                            color=ft.Colors.BLUE_600,
                        )
                        if self.task_model.deadline
                        else ft.Container(),
                    ],
                ),
            ],
        )

        self.display_task = ft.Checkbox(
            value=task_model.completed,
            on_change=self.status_changed,
        )

        self.edit_name = ft.TextField(expand=1, label="Task name")
        self.edit_priority = ft.Dropdown(
            label="Priority",
            width=180,
            options=[
                ft.dropdown.Option("low", "🔥 Low"),
                ft.dropdown.Option("medium", "🔥🔥 Medium"),
                ft.dropdown.Option("high", "🔥🔥🔥 High"),
            ],
            value=self.task_model.priority_level,
        )
        self.edit_deadline = ft.TextField(
            label="Deadline",
            width=180,
            hint_text="YYYY-MM-DD",
        )

        self.display_view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    controls=[
                        self.display_task,
                        task_info,
                    ],
                    spacing=10,
                ),
                ft.Row(
                    spacing=0,
                    controls=[
                        edit_icon_button(self.edit_clicked),
                        delete_icon_button(self.delete_clicked),
                    ],
                ),
            ],
        )

        self.edit_view = ft.Column(
            visible=False,
            spacing=10,
            controls=[
                ft.Row(
                    controls=[
                        self.edit_name,
                        self.edit_priority,
                        self.edit_deadline,
                    ],
                    spacing=10,
                ),
                ft.Row(
                    controls=[
                        save_icon_button(self.save_clicked),
                        ft.TextButton("Cancel", on_click=self.cancel_clicked),
                    ],
                    spacing=10,
                ),
            ],
        )
        self.controls = [self.display_view, self.edit_view]

    def edit_clicked(self, e: ft.ControlEvent | None) -> None:
        """Switch to edit mode."""
        self.edit_name.value = self.task_model.name
        self.edit_priority.value = self.task_model.priority_level
        self.edit_deadline.value = (
            self.task_model.deadline.strftime("%Y-%m-%d")
            if self.task_model.deadline
            else ""
        )

        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def save_clicked(self, e: ft.ControlEvent | None) -> None:
        """Save changes and switch back to display mode."""
        self.task_model.name = self.edit_name.value
        self.task_model.priority_level = self.edit_priority.value

        # Parse deadline
        if self.edit_deadline.value:
            try:
                self.task_model.deadline = datetime.strptime(
                    self.edit_deadline.value, "%Y-%m-%d"
                )
            except ValueError:
                # If parsing fails, keep the original deadline
                pass
        else:
            self.task_model.deadline = None

        self._update_display()
        self.display_view.visible = True
        self.edit_view.visible = False

        # Notify parent about the edit
        if self.task_edit:
            self.task_edit(self)

        self.update()

    def cancel_clicked(self, e: ft.ControlEvent | None) -> None:
        """Cancel editing and switch back to display mode."""
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()

    def _update_display(self) -> None:
        """Update the display view with current task data."""
        # Update the task info display
        task_info = self.display_view.controls[0].controls[1]
        task_info.controls[0].value = self.task_model.name

        # Update priority display
        task_info.controls[1].controls[
            0
        ].value = f"{get_priority_emoji(self.task_model.priority_level)} {self.task_model.priority_level.title()}"

        # Update deadline display
        if self.task_model.deadline:
            deadline_text = f"📅 {self.task_model.deadline.strftime('%Y-%m-%d')}"
            if len(task_info.controls[1].controls) > 1:
                task_info.controls[1].controls[1].value = deadline_text
            else:
                task_info.controls[1].controls.append(
                    ft.Text(
                        value=deadline_text,
                        theme_style=ft.TextThemeStyle.BODY_SMALL,
                        color=ft.Colors.BLUE_600,
                    )
                )
        else:
            if len(task_info.controls[1].controls) > 1:
                task_info.controls[1].controls.pop(1)

    def status_changed(self, e: ft.ControlEvent | None) -> None:
        """Handle checkbox state change."""
        self.completed = self.display_task.value
        self.task_model.completed = self.completed
        self.task_status_change(self)

    def delete_clicked(self, e: ft.ControlEvent | None) -> None:
        """Handle task deletion."""
        self.task_delete(self)
