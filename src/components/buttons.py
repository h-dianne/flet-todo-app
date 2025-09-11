"""Reusable button factory helpers for the app UI.

These small helpers centralize icon, color, and tooltip choices so
buttons look consistent across components.
"""

from typing import Callable, Optional

import flet as ft


def edit_icon_button(on_click: Optional[Callable[[ft.ControlEvent], None]] = None) -> ft.IconButton:
    """Create the edit icon button used by task items."""
    return ft.IconButton(
        icon=ft.Icons.CREATE_OUTLINED,
        tooltip="Edit To-Do",
        on_click=on_click,
    )


def delete_icon_button(on_click: Optional[Callable[[ft.ControlEvent], None]] = None) -> ft.IconButton:
    """Create the delete icon button used by task items."""
    return ft.IconButton(
        icon=ft.Icons.DELETE_OUTLINE,
        tooltip="Delete To-Do",
        on_click=on_click,
    )


def save_icon_button(on_click: Optional[Callable[[ft.ControlEvent], None]] = None) -> ft.IconButton:
    """Create the save icon button used by task items while editing."""
    return ft.IconButton(
        icon=ft.Icons.DONE_OUTLINE_OUTLINED,
        icon_color=ft.Colors.GREEN,
        tooltip="Update To-Do",
        on_click=on_click,
    )


def add_fab(on_click: Optional[Callable[[ft.ControlEvent], None]] = None) -> ft.FloatingActionButton:
    """Create the floating action button for adding tasks."""
    return ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=on_click)


def clear_completed_button(on_click: Optional[Callable[[ft.ControlEvent], None]] = None) -> ft.OutlinedButton:
    """Create the footer button for clearing completed tasks."""
    return ft.OutlinedButton(text="Clear completed", on_click=on_click)
