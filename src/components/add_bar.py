"""Add-task input row component."""

from typing import Callable, Optional

import flet as ft
from .buttons import add_fab


class AddTaskRow(ft.Row):
    """A row containing a task input field and an add button."""

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
        add_btn: ft.FloatingActionButton = add_fab(on_add_click or on_submit)
        super().__init__(controls=[self.input, add_btn])
