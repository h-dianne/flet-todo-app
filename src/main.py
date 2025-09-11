"""Application entrypoint for Flet runtime."""

import flet as ft

from src.todo import TodoApp


def main(page: ft.Page) -> None:
    page.title = "ToDo App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE

    # create app control and add it to the page
    page.add(TodoApp())


if __name__ == "__main__":
    ft.app(main)
