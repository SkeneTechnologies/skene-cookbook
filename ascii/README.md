# ASCII Design System — Python Edition

Terminal-first UI design system for Python CLI tools using Rich library.
Provides consistent Skene branding across terminal interfaces.

## Features

- **🎨 Skene Color Palette** - Brand colors (#EDC29C, #E8C260, #00FFC2)
- **📐 Unicode Symbols** - Consistent icons (◈, ✓, →, ◉, etc.)
- **🌗 Adaptive Rendering** - Terminal, IDE chat, mobile detection
- **🎭 NO_COLOR Support** - Respects user preferences
- **📦 Rich Integration** - Built for Rich library (tables, panels, prompts)

## Installation

No installation needed - this is a local module.

**Dependencies:**

```bash
pip3 install rich
```

## Usage

### Basic Import

```python
from ascii import Tokens, Symbols, SkeneColors

# Use in Rich markup
console.print(f"[{SkeneColors.PRIMARY}]Header[/{SkeneColors.PRIMARY}]")
console.print(f"[{SkeneColors.SUCCESS}]{Symbols.CHECKMARK} Done[/{SkeneColors.SUCCESS}]")
```

### Color Tokens

```python
from ascii import SkeneColors

# Brand colors
SkeneColors.PRIMARY          # #EDC29C (Skene peach)
SkeneColors.PRIMARY_GOLD     # #E8C260 (Accent gold)
SkeneColors.PRIMARY_BRONZE   # #8C6B47 (Bronze)

# Backgrounds
SkeneColors.BLACK            # #060606 (Deep black)
SkeneColors.WHITE            # #FAF1E9 (Cream)
SkeneColors.DARK_GREY        # #161616 (Card background)

# Semantic
SkeneColors.SUCCESS          # #9CEDC7 (Green teal)
SkeneColors.ERROR            # #ED9C9C (Soft red)
SkeneColors.WARNING          # #FFAA00 (Orange)
SkeneColors.BEACON_ACTIVE    # #00FFC2 (Skene teal - CTA)

# Text
SkeneColors.DIM              # #9ca3af (Secondary text)
```

### Unicode Symbols

```python
from ascii import Symbols

# Brand
Symbols.SKENE_LOGO      # "[⋯]"
Symbols.DIAMOND         # "◈"
Symbols.BEACON          # "◉"
Symbols.BEACON_PULSE    # "◎"

# Status
Symbols.CHECKMARK       # "✓"
Symbols.CROSS           # "✗"
Symbols.BULLET          # "•"
Symbols.ARROW           # "→"
Symbols.ARROW_RIGHT     # "▸"

# Progress
Symbols.PROGRESS_FULL   # "█"
Symbols.PROGRESS_EMPTY  # "░"
Symbols.PROGRESS_MID    # "▓"
```

### Environment Detection

```python
from ascii import get_render_mode, RenderMode, get_terminal_width

# Detect rendering environment
mode = get_render_mode()

if mode == RenderMode.TERMINAL:
    # Full terminal with ANSI colors
    pass
elif mode == RenderMode.IDE_CHAT:
    # Desktop agent chat (Cursor, Claude Code)
    pass
elif mode == RenderMode.MOBILE_CHAT:
    # Mobile agent chat
    pass
elif mode == RenderMode.PLAIN:
    # NO_COLOR mode
    pass

# Get terminal width
width = get_terminal_width()  # Returns: 80, 120, or actual width
```

### Risk Level Colors

```python
from ascii import RISK_COLORS, SkeneColors

# Map risk levels to colors
risk_level = "High"
color = {
    'Critical': SkeneColors.ERROR,
    'High': SkeneColors.WARNING,
    'Medium': SkeneColors.BEACON_ACTIVE,
    'Low': SkeneColors.SUCCESS
}[risk_level]

console.print(f"[{color}]Risk: {risk_level}[/{color}]")
```

## Example: Rich Table with Design System

```python
from rich.console import Console
from rich.table import Table
from rich import box
from ascii import SkeneColors, Symbols

console = Console()

# Create table with Skene branding
table = Table(
    show_header=True,
    box=box.ROUNDED,
    border_style=SkeneColors.PRIMARY  # Skene peach border
)

table.add_column("Status", style=f"bold {SkeneColors.PRIMARY_GOLD}")
table.add_column("Item", style=SkeneColors.WHITE)

table.add_row(
    f"[{SkeneColors.SUCCESS}]{Symbols.CHECKMARK}[/{SkeneColors.SUCCESS}]",
    "Task completed"
)

table.add_row(
    f"[{SkeneColors.WARNING}]{Symbols.BEACON_WARN}[/{SkeneColors.WARNING}]",
    "Needs attention"
)

console.print(table)
```

## Environment Variables

| Variable            | Effect                                                        |
| ------------------- | ------------------------------------------------------------- |
| `ASCII_RENDER_MODE` | Override mode: `terminal`, `ide-chat`, `mobile-chat`, `plain` |
| `NO_COLOR`          | Disable all ANSI colors (falls back to plain mode)            |

**Example:**

```bash
# Force plain mode (no colors)
NO_COLOR=1 python3 skill-loom-cli.py

# Force IDE chat mode
ASCII_RENDER_MODE=ide-chat python3 skill-loom-cli.py
```

## Architecture

```
ascii/
├── __init__.py           # Main exports
├── design_tokens.py      # Colors, symbols, tokens
├── environment.py        # Render mode detection
└── README.md            # This file
```

## Design Philosophy

This system follows the **Skene ASCII Design Spec** from `skene-flow`:

- **Terminal-first**: Designed for CLI, works everywhere
- **Adaptive**: Detects environment and adjusts rendering
- **Consistent**: Same colors/symbols across all Skene tools
- **Accessible**: Respects NO_COLOR and adapts to terminal width

## Related Projects

- **TypeScript version**: `~/skene-prototypes/skene-flow-proto-local-backup/docs/templates/ascii-design-system/`
- **Production use**: `~/skene-primary/skene-dashboard/skene-flow/src/onboarding/design-tokens.ts`
- **Figma Design System**: `~/skene-strategy/projects/design-system/` (web components)

## Color Reference

### Skene Brand Palette

| Token              | Hex       | Usage                          |
| ------------------ | --------- | ------------------------------ |
| **PRIMARY**        | `#EDC29C` | Headers, borders, primary text |
| **PRIMARY_GOLD**   | `#E8C260` | Accents, highlights, logo      |
| **PRIMARY_BRONZE** | `#8C6B47` | Secondary emphasis             |
| **BEACON_ACTIVE**  | `#00FFC2` | Active CTA, links, highlights  |
| **SUCCESS**        | `#9CEDC7` | Success states, completed      |
| **ERROR**          | `#ED9C9C` | Error states, critical alerts  |
| **WARNING**        | `#FFAA00` | Warning states, attention      |
| **WHITE**          | `#FAF1E9` | Body text, light backgrounds   |
| **BLACK**          | `#060606` | Deep backgrounds               |
| **DIM**            | `#9ca3af` | Secondary text, muted          |

## Contributing

When adding new symbols or colors:

1. Add to `design_tokens.py`
2. Update this README
3. Follow existing naming conventions (SCREAMING_SNAKE_CASE)
4. Test with `NO_COLOR=1` to ensure graceful degradation

## License

Part of Skene Technologies design system.
