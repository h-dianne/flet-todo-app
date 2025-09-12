"""Application entrypoint for Flet runtime."""

import flet as ft

from src.todo import TodoApp


def main(page: ft.Page) -> None:
    page.title = "ToDo App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE

    # Set window dimensions
    page.window.width = 1600
    page.window.height = 900
    page.window.min_width = 1280
    page.window.min_height = 720

    # Main App Component
    todo_app = TodoApp()
    todo_app.width = 900
    page.add(todo_app)


if __name__ == "__main__":
    ft.app(main)
