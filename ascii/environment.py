"""
ASCII Design System — Environment Detection

Detects terminal type and adapts rendering for:
- Terminal (full ANSI colors)
- IDE chat (Cursor, Claude Code - markdown)
- Mobile chat (simplified)
- Plain (NO_COLOR mode)
"""

import os
import sys
from enum import Enum


class RenderMode(Enum):
    """Rendering mode for terminal output"""

    TERMINAL = "terminal"  # Full terminal with ANSI colors
    IDE_CHAT = "ide-chat"  # Desktop agent chat (Cursor, Claude)
    MOBILE_CHAT = "mobile-chat"  # Mobile agent chat
    PLAIN = "plain"  # No colors, minimal formatting


def get_render_mode() -> RenderMode:
    """
    Detect the current rendering environment.

    Priority:
    1. ASCII_RENDER_MODE env var (explicit override)
    2. NO_COLOR env var (force plain mode)
    3. TTY detection + environment hints
    """

    # Explicit override
    mode_override = os.environ.get("ASCII_RENDER_MODE")
    if mode_override:
        mode_map = {
            "terminal": RenderMode.TERMINAL,
            "ide-chat": RenderMode.IDE_CHAT,
            "mobile-chat": RenderMode.MOBILE_CHAT,
            "plain": RenderMode.PLAIN,
        }
        return mode_map.get(mode_override.lower(), RenderMode.TERMINAL)

    # NO_COLOR forces plain mode
    if os.environ.get("NO_COLOR"):
        return RenderMode.PLAIN

    # Detect IDE chat environments
    cursor_agent = os.environ.get("CURSOR_AGENT")
    cloud_agent = os.environ.get("CLOUD_AGENT")
    if cursor_agent or cloud_agent:
        return RenderMode.IDE_CHAT

    # Detect mobile
    term_program = os.environ.get("TERM_PROGRAM", "").lower()
    if "mobile" in term_program:
        return RenderMode.MOBILE_CHAT

    # Check if it's a TTY (interactive terminal)
    if sys.stdout.isatty():
        return RenderMode.TERMINAL

    # Default to IDE chat for non-TTY (piped output)
    return RenderMode.IDE_CHAT


def is_plain_ascii_mode() -> bool:
    """Check if plain ASCII mode is active (no colors)"""
    mode = get_render_mode()
    return mode in (RenderMode.PLAIN, RenderMode.MOBILE_CHAT, RenderMode.IDE_CHAT)


def should_use_minimal_logo() -> bool:
    """Check if minimal logo should be used (mobile or narrow)"""
    mode = get_render_mode()
    if mode == RenderMode.MOBILE_CHAT:
        return True

    # Check terminal width
    try:
        columns = os.get_terminal_size().columns
        return columns < 60
    except (OSError, AttributeError):
        return False


def should_use_vertical_tables() -> bool:
    """Check if tables should be rendered vertically (mobile or narrow)"""
    mode = get_render_mode()
    if mode == RenderMode.MOBILE_CHAT:
        return True

    # Check terminal width
    try:
        columns = os.get_terminal_size().columns
        return columns < 60
    except (OSError, AttributeError):
        return False


def get_terminal_width() -> int:
    """Get current terminal width (or default)"""
    try:
        return os.get_terminal_size().columns
    except (OSError, AttributeError):
        # Default widths by mode
        mode = get_render_mode()
        return {
            RenderMode.TERMINAL: 80,
            RenderMode.IDE_CHAT: 120,
            RenderMode.MOBILE_CHAT: 60,
            RenderMode.PLAIN: 80,
        }.get(mode, 80)


def get_layout_classification() -> str:
    """
    Get layout classification based on terminal width.

    Returns: 'narrow', 'compact', 'standard', or 'wide'
    """
    width = get_terminal_width()

    if width < 40:
        return "narrow"
    elif width < 80:
        return "compact"
    elif width < 120:
        return "standard"
    else:
        return "wide"
