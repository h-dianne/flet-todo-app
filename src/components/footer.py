"""Footer component showing active count and a clear-completed button."""

from typing import Callable, Optional

import flet as ft
from .buttons import clear_completed_button


class FooterBar(ft.Row):
    """Row displaying items-left text and a clear-completed action."""

    def __init__(
        self, on_clear: Optional[Callable[[ft.ControlEvent], None]] = None
    ) -> None:
        self.items_left: ft.Text = ft.Text("0 items left")
        self.clear_btn: ft.OutlinedButton = clear_completed_button(on_clear)
        self.clear_btn.visible = False
        super().__init__(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[self.items_left, self.clear_btn],
        )

    def set_count(self, count: int) -> None:
        plural = "s" if count != 1 else ""
        self.items_left.value = f"{count} item{plural} left"

    def set_clear_visible(self, visible: bool) -> None:
        self.clear_btn.visible = visible
