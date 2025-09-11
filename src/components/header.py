"""Header component for the app title."""

import flet as ft


class Header(ft.Row):
    """Centered page header with a title text."""

    def __init__(self, title: str = "Todos") -> None:
        super().__init__(
            controls=[ft.Text(value=title, theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM)],
            alignment=ft.MainAxisAlignment.CENTER,
        )
