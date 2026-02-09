"""
ASCII Design System — Color Tokens & Symbols (Python)

Skene Design System tokens for terminal UI with Rich library.
Provides consistent branding across CLI tools.

Features:
- TrueColor (24-bit) colors via Rich hex
- Semantic tokens for status indicators
- NO_COLOR environment variable support
- Adaptive rendering for terminal/IDE/mobile
"""

import os
from typing import Dict


# Skene Design System — Base Colors
class SkeneColors:
    """Hex color values from Skene Design System"""

    # Brand colors
    PRIMARY = "#EDC29C"  # Skene peach (headers, borders)
    PRIMARY_HOVER = "#EBDCCF"
    PRIMARY_GOLD = "#E8C260"  # Accent, highlights, logo
    PRIMARY_BRONZE = "#8C6B47"  # Secondary emphasis

    # Backgrounds
    BLACK = "#060606"  # Deep black
    DARK_GREY = "#161616"  # Card backgrounds
    WHITE = "#FAF1E9"  # Cream (body text)

    # Text
    TEXT = "#2C2C2C"
    TEXT_ON_DARK = "#EBDCCF"
    LIGHT_GREY = "#A1A1A1"

    # Semantic
    SUCCESS = "#9CEDC7"  # Green teal (completed)
    ALERT = "#EDC29C"  # Same as primary
    ERROR = "#ED9C9C"  # Soft red (failed)
    WARNING = "#FFAA00"  # Orange (attention)

    # Beacon states (progress indicators)
    BEACON_ACTIVE = "#00FFC2"  # Skene teal (active CTA)
    BEACON_PULSE = "#F0ABFC"  # Lilac (scanning)
    BEACON_WARN = "#FFAA00"  # Warning/attention

    # Dim/secondary
    DIM = "#9ca3af"  # Gray for less emphasis


def should_use_color() -> bool:
    """Check if colors should be enabled (respects NO_COLOR env var)"""
    return os.environ.get('NO_COLOR') is None


def get_rich_color(hex_color: str) -> str:
    """Convert hex to Rich color format"""
    if not should_use_color():
        return "white"  # Fallback to default
    return hex_color


# Rich-compatible color tokens
# These return Rich color strings that can be used in markup like [primary]text[/primary]
class Tokens:
    """Rich library color tokens for terminal output"""

    # Map semantic names to hex colors
    colors: Dict[str, str] = {
        'primary': SkeneColors.PRIMARY,
        'primary_gold': SkeneColors.PRIMARY_GOLD,
        'primary_bronze': SkeneColors.PRIMARY_BRONZE,
        'white': SkeneColors.WHITE,
        'text_on_dark': SkeneColors.TEXT_ON_DARK,
        'secondary': SkeneColors.LIGHT_GREY,
        'success': SkeneColors.SUCCESS,
        'alert': SkeneColors.ALERT,
        'error': SkeneColors.ERROR,
        'warning': SkeneColors.WARNING,
        'beacon_active': SkeneColors.BEACON_ACTIVE,
        'beacon_pulse': SkeneColors.BEACON_PULSE,
        'beacon_warn': SkeneColors.BEACON_WARN,
        'dim': SkeneColors.DIM,
    }

    @classmethod
    def get(cls, name: str) -> str:
        """Get Rich color string by token name"""
        return get_rich_color(cls.colors.get(name, SkeneColors.WHITE))


# Unicode symbols for terminal UI
class Symbols:
    """Unicode characters for terminal rendering"""

    # Brand
    SKENE_LOGO = "[⋯]"
    DIAMOND = "◈"
    BEACON = "◉"
    BEACON_PULSE = "◎"

    # Status
    CHECKMARK = "✓"
    CROSS = "✗"
    BULLET = "•"
    ARROW = "→"
    ARROW_RIGHT = "▸"

    # Progress bar
    PROGRESS_FULL = "█"
    PROGRESS_EMPTY = "░"
    PROGRESS_MID = "▓"

    # Emojis (for Rich terminal)
    FOLDER = "📦"
    GEAR = "⚙️"
    LINK = "🔗"
    CHART = "📈"
    MONEY = "💰"
    TARGET = "🎯"
    LIGHTBULB = "💡"
    ROCKET = "🚀"
    LOCK = "🔐"
    STAR = "⭐"


# Box drawing characters (Rich box styles use these internally)
class BoxChars:
    """Box drawing unicode characters"""

    # Rounded corners
    TOP_LEFT = "╭"
    TOP_RIGHT = "╮"
    BOTTOM_LEFT = "╰"
    BOTTOM_RIGHT = "╯"

    # Lines
    HORIZONTAL = "─"
    VERTICAL = "│"

    # Table separators
    LEFT_T = "├"
    RIGHT_T = "┤"
    TOP_T = "┬"
    BOTTOM_T = "┴"
    CROSS = "┼"

    # Double lines
    DOUBLE_HORIZONTAL = "═"
    DOUBLE_VERTICAL = "║"


# Risk level color mapping (for skills)
RISK_COLORS = {
    'Critical': 'error',  # Maps to Tokens.get('error')
    'High': 'warning',
    'Medium': 'beacon_active',  # Cyan/teal
    'Low': 'success'
}


# Export convenience function
def get_risk_color_hex(risk_level: str) -> str:
    """Get hex color for risk level"""
    token_name = RISK_COLORS.get(risk_level, 'white')
    return Tokens.get(token_name)
