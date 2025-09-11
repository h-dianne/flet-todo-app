"""Filter tabs (all/active/completed) component."""

from typing import Callable, Optional

import flet as ft


class FilterTabs(ft.Tabs):
    """Tabs for filtering tasks by status."""

    def __init__(
        self,
        on_change: Optional[Callable[[ft.ControlEvent], None]] = None,
        selected_index: int = 0,
    ) -> None:
        super().__init__(
            scrollable=False,
            selected_index=selected_index,
            on_change=on_change,
            tabs=[ft.Tab(text="all"), ft.Tab(text="active"), ft.Tab(text="completed")],
        )
