"""Task item component.

Represents a single to-do item with the ability to toggle completion,
edit its label, and delete it. The parent provides callbacks to react
to status changes and deletions.
"""

from typing import Callable

import flet as ft

from .buttons import delete_icon_button, edit_icon_button, save_icon_button


class Task(ft.Column):
    """A reusable to-do item widget."""

    def __init__(
        self,
        task_name: str,
        task_status_change: Callable[["Task"], None],
        task_delete: Callable[["Task"], None],
    ) -> None:
        super().__init__()
        self.completed: bool = False
        self.task_name: str = task_name
        self.task_status_change = task_status_change
        self.task_delete = task_delete
        self.display_task = ft.Checkbox(
            value=False, label=self.task_name, on_change=self.status_changed
        )
        self.edit_name = ft.TextField(expand=1)

        self.display_view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.display_task,
                ft.Row(
                    spacing=0,
                    controls=[
                        edit_icon_button(self.edit_clicked),
                        delete_icon_button(self.delete_clicked),
                    ],
                ),
            ],
        )

        self.edit_view = ft.Row(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.edit_name,
                save_icon_button(self.save_clicked),
            ],
        )
        self.controls = [self.display_view, self.edit_view]

    def edit_clicked(self, e: ft.ControlEvent | None) -> None:
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def save_clicked(self, e: ft.ControlEvent | None) -> None:
        self.display_task.label = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()

    def status_changed(self, e: ft.ControlEvent | None) -> None:
        self.completed = self.display_task.value
        self.task_status_change(self)

    def delete_clicked(self, e: ft.ControlEvent | None) -> None:
        self.task_delete(self)
