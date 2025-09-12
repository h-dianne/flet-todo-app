"""Utility functions for the todo app."""


def get_priority_emoji(priority_level: str) -> str:
    """Get the fire emoji representation for priority level."""
    priority_emojis = {"low": "🔥", "medium": "🔥🔥", "high": "🔥🔥🔥"}
    return priority_emojis.get(priority_level.lower(), "🔥")


def get_priority_levels() -> list[str]:
    """Get list of available priority levels."""
    return ["low", "medium", "high"]
