"""
ASCII Design System for Python

Terminal-first UI design system for CLI tools using Rich library.
Adapts to terminal (ANSI), desktop agent chat (Cursor, Claude), and mobile.

Usage:
    from ascii import Tokens, Symbols, get_render_mode

    # Get colors
    primary = Tokens.get('primary')
    success = Tokens.get('success')

    # Use symbols
    print(f"{Symbols.CHECKMARK} Done")
    print(f"{Symbols.SKENE_LOGO} Skene Skills")

    # Check environment
    mode = get_render_mode()
"""

from .design_tokens import (
    RISK_COLORS,
    BoxChars,
    SkeneColors,
    Symbols,
    Tokens,
    get_risk_color_hex,
    should_use_color,
)
from .environment import (
    RenderMode,
    get_layout_classification,
    get_render_mode,
    get_terminal_width,
    is_plain_ascii_mode,
    should_use_minimal_logo,
    should_use_vertical_tables,
)

__all__ = [
    # Colors & Tokens
    "SkeneColors",
    "Tokens",
    "Symbols",
    "BoxChars",
    "RISK_COLORS",
    "should_use_color",
    "get_risk_color_hex",
    # Environment
    "RenderMode",
    "get_render_mode",
    "is_plain_ascii_mode",
    "should_use_minimal_logo",
    "should_use_vertical_tables",
    "get_terminal_width",
    "get_layout_classification",
]
