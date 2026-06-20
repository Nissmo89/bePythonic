#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRONT_END_DIR = ROOT / "src" / "bepythonic" / "gui" / "front_end"
OUTPUT_PATH = FRONT_END_DIR / "css" / "tailwind-utilities.css"

BREAKPOINTS = {
    "sm": "640px",
    "md": "768px",
    "lg": "1024px",
}

PSEUDO_VARIANTS = {
    "hover": ":hover",
    "focus": ":focus",
    "active": ":active",
}

CUSTOM_CLASSES = {
    "active",
    "ai",
    "blank-opt-btn",
    "btn-tactile-primary",
    "btn-tactile-secondary",
    "chat-bubble",
    "code-block-wrapper",
    "fallback-active",
    "glass-card",
    "glass-nav",
    "lesson-card-btn",
    "light-status-bar",
    "mcq-opt-btn",
    "nav-tab",
    "opt-check-circle",
    "prose",
    "user",
    "welcome-screen",
}

DISPLAY_CLASSES = {
    "absolute": "position: absolute;",
    "block": "display: block;",
    "flex": "display: flex;",
    "grid": "display: grid;",
    "hidden": "display: none;",
    "inline": "display: inline;",
    "inline-block": "display: inline-block;",
    "inline-flex": "display: inline-flex;",
    "relative": "position: relative;",
}

SIMPLE_CLASSES = {
    **DISPLAY_CLASSES,
    "antialiased": (
        "-webkit-font-smoothing: antialiased;\n"
        "  -moz-osx-font-smoothing: grayscale;"
    ),
    "bg-clip-text": "-webkit-background-clip: text;\n  background-clip: text;",
    "border": "border-width: 1px;",
    "border-b": "border-bottom-width: 1px;",
    "border-b-2": "border-bottom-width: 2px;",
    "border-l": "border-left-width: 1px;",
    "border-l-2": "border-left-width: 2px;",
    "border-r": "border-right-width: 1px;",
    "border-t": "border-top-width: 1px;",
    "flex-1": "flex: 1 1 0%;",
    "flex-col": "flex-direction: column;",
    "flex-row": "flex-direction: row;",
    "flex-wrap": "flex-wrap: wrap;",
    "font-bold": "font-weight: 700;",
    "font-medium": "font-weight: 500;",
    "font-mono": (
        "font-family: \"IBM Plex Mono\", ui-monospace, SFMono-Regular, Menlo, monospace;"
    ),
    "font-sans": (
        "font-family: \"Space Grotesk\", \"Segoe UI\", sans-serif;"
    ),
    "font-semibold": "font-weight: 600;",
    "h-full": "height: 100%;",
    "inset-0": "top: 0;\n  right: 0;\n  bottom: 0;\n  left: 0;",
    "inset-y-0": "top: 0;\n  bottom: 0;",
    "items-center": "align-items: center;",
    "items-start": "align-items: flex-start;",
    "justify-between": "justify-content: space-between;",
    "justify-center": "justify-content: center;",
    "leading-normal": "line-height: 1.5;",
    "leading-relaxed": "line-height: 1.625;",
    "left-0": "left: 0;",
    "min-h-0": "min-height: 0;",
    "mx-auto": "margin-left: auto;\n  margin-right: auto;",
    "ml-auto": "margin-left: auto;",
    "mr-auto": "margin-right: auto;",
    "overflow-auto": "overflow: auto;",
    "overflow-hidden": "overflow: hidden;",
    "overflow-y-auto": "overflow-y: auto;",
    "rounded-md": "border-radius: 0.375rem;",
    "rounded-full": "border-radius: 9999px;",
    "rounded-lg": "border-radius: 0.5rem;",
    "rounded-xl": "border-radius: 0.75rem;",
    "rounded-2xl": "border-radius: 1rem;",
    "select-none": (
        "-webkit-user-select: none;\n"
        "  user-select: none;"
    ),
    "select-text": (
        "-webkit-user-select: text;\n"
        "  user-select: text;"
    ),
    "shrink-0": "flex-shrink: 0;",
    "text-center": "text-align: center;",
    "text-left": "text-align: left;",
    "text-transparent": "color: transparent;",
    "tracking-tight": "letter-spacing: -0.025em;",
    "tracking-wide": "letter-spacing: 0.025em;",
    "tracking-wider": "letter-spacing: 0.05em;",
    "tracking-widest": "letter-spacing: 0.1em;",
    "transform": "",
    "transition-all": (
        "transition-property: all;\n"
        "  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);\n"
        "  transition-duration: 150ms;"
    ),
    "transition-colors": (
        "transition-property: color, background-color, border-color, "
        "text-decoration-color, fill, stroke;\n"
        "  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);\n"
        "  transition-duration: 150ms;"
    ),
    "transition-transform": (
        "transition-property: transform;\n"
        "  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);\n"
        "  transition-duration: 150ms;"
    ),
    "transition-opacity": (
        "transition-property: opacity;\n"
        "  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);\n"
        "  transition-duration: 150ms;"
    ),
    "fill-current": "fill: currentColor;",
    "truncate": (
        "overflow: hidden;\n"
        "  text-overflow: ellipsis;\n"
        "  white-space: nowrap;"
    ),
    "uppercase": "text-transform: uppercase;",
    "self-start": "align-self: flex-start;",
    "w-full": "width: 100%;",
}

TEXT_SIZES = {
    "xs": ("0.75rem", "1rem"),
    "sm": ("0.875rem", "1.25rem"),
    "base": ("1rem", "1.5rem"),
    "lg": ("1.125rem", "1.75rem"),
    "xl": ("1.25rem", "1.75rem"),
    "2xl": ("1.5rem", "2rem"),
    "3xl": ("1.875rem", "2.25rem"),
    "4xl": ("2.25rem", "2.5rem"),
}

SPACING_SCALE = {
    "0": "0px",
    "0.5": "0.125rem",
    "1": "0.25rem",
    "1.5": "0.375rem",
    "2": "0.5rem",
    "2.5": "0.625rem",
    "3": "0.75rem",
    "3.5": "0.875rem",
    "4": "1rem",
    "4.5": "1.125rem",
    "5": "1.25rem",
    "6": "1.5rem",
    "8": "2rem",
    "9": "2.25rem",
    "10": "2.5rem",
    "14": "3.5rem",
    "16": "4rem",
    "20": "5rem",
    "40": "10rem",
    "48": "12rem",
    "60": "15rem",
    "64": "16rem",
    "72": "18rem",
    "80": "20rem",
    "px": "1px",
}

MAX_WIDTH_SCALE = {
    "xs": "20rem",
    "sm": "24rem",
    "md": "28rem",
    "lg": "32rem",
    "2xl": "42rem",
    "3xl": "48rem",
    "6xl": "72rem",
}

GRID_COLS = {
    "1": "repeat(1, minmax(0, 1fr))",
    "2": "repeat(2, minmax(0, 1fr))",
    "3": "repeat(3, minmax(0, 1fr))",
    "4": "repeat(4, minmax(0, 1fr))",
}

SHADOWS = {
    "shadow-sm": "0 1px 2px 0 rgb(15 23 42 / 0.08)",
    "shadow-md": "0 4px 6px -1px rgb(15 23 42 / 0.12), 0 2px 4px -2px rgb(15 23 42 / 0.12)",
    "shadow-xl": "0 20px 25px -5px rgb(15 23 42 / 0.12), 0 8px 10px -6px rgb(15 23 42 / 0.12)",
    "shadow-2xl": "0 25px 50px -12px rgb(15 23 42 / 0.25)",
}

BACKDROP_BLUR = {
    "backdrop-blur": "8px",
    "backdrop-blur-md": "12px",
    "backdrop-blur-xl": "24px",
}

COLORS = {
    "amber": {
        "50": "#fffbeb",
        "100": "#fef3c7",
        "500": "#f59e0b",
        "700": "#b45309",
    },
    "emerald": {
        "50": "#ecfdf5",
        "100": "#d1fae5",
        "200": "#a7f3d0",
        "400": "#34d399",
        "500": "#10b981",
        "600": "#059669",
        "800": "#065f46",
    },
    "indigo": {
        "50": "#eef2ff",
        "100": "#e0e7ff",
        "200": "#c7d2fe",
        "300": "#a5b4fc",
        "400": "#818cf8",
        "500": "#6366f1",
        "600": "#4f46e5",
        "700": "#4338ca",
    },
    "rose": {
        "50": "#fff1f2",
        "100": "#ffe4e6",
        "200": "#fecdd3",
        "400": "#fb7185",
        "500": "#f43f5e",
        "600": "#e11d48",
        "800": "#9f1239",
    },
    "yellow": {
        "500": "#eab308",
    },
    "slate": {
        "50": "#f8fafc",
        "100": "#f1f5f9",
        "150": "#e9eff6",
        "200": "#e2e8f0",
        "300": "#cbd5e1",
        "400": "#94a3b8",
        "500": "#64748b",
        "600": "#475569",
        "700": "#334155",
        "800": "#1e293b",
        "900": "#0f172a",
        "950": "#020617",
    },
    "white": {
        "DEFAULT": "#ffffff",
    },
}


def css_escape(token: str) -> str:
    escaped = []
    for char in token:
        if char.isalnum() or char in {"_", "-"}:
            escaped.append(char)
        else:
            escaped.append(f"\\{char}")
    return "".join(escaped)


def parse_opacity(value: str) -> float:
    return int(value) / 100


def hex_to_rgb(hex_value: str) -> tuple[int, int, int]:
    stripped = hex_value.lstrip("#")
    return tuple(int(stripped[index:index + 2], 16) for index in (0, 2, 4))


def resolve_color(color_token: str) -> str:
    if "/" in color_token:
        base, opacity = color_token.split("/", 1)
    else:
        base, opacity = color_token, None

    if base == "white":
        hex_value = COLORS["white"]["DEFAULT"]
    else:
        family, shade = base.rsplit("-", 1)
        hex_value = COLORS[family][shade]

    if opacity is None:
        return hex_value

    red, green, blue = hex_to_rgb(hex_value)
    return f"rgba({red}, {green}, {blue}, {parse_opacity(opacity):g})"


def resolve_spacing(token: str) -> str:
    if token.startswith("[") and token.endswith("]"):
        return token[1:-1]
    return SPACING_SCALE[token]


def extract_candidate_classes() -> list[str]:
    candidates: set[str] = set()
    token_pattern = re.compile(r"^[A-Za-z0-9_:\-\[\]\/\.]+$")
    class_sources = [
        re.compile(r'class\s*=\s*"([^"]+)"'),
        re.compile(r"class\s*=\s*'([^']+)'"),
        re.compile(r'className\s*=\s*"([^"]+)"'),
        re.compile(r"className\s*=\s*'([^']+)'"),
        re.compile(r"className\s*=\s*`([^`]+)`", re.S),
        re.compile(r"classList\.(?:add|remove|toggle)\(([^)]+)\)"),
    ]

    for path in FRONT_END_DIR.rglob("*"):
        if path.suffix not in {".html", ".js"}:
            continue
        text = path.read_text(encoding="utf-8")
        for pattern in class_sources:
            for match in pattern.finditer(text):
                group = match.group(1)
                for token in re.findall(r'"([^"]+)"|\'([^\']+)\'|([^\s,]+)', group):
                    token_text = next(part for part in token if part)
                    for class_name in token_text.split():
                        if class_name in CUSTOM_CLASSES:
                            continue
                        if not token_pattern.fullmatch(class_name):
                            continue
                        if class_name == ":" or not (
                            class_name[0].isalnum() or class_name[0] == "-"
                        ):
                            continue
                        if class_name in SIMPLE_CLASSES or any(
                            char in class_name for char in ("-", ":", "[", "]", "/")
                        ):
                            candidates.add(class_name)

    return sorted(candidates - CUSTOM_CLASSES)


def parse_variants(token: str) -> tuple[str | None, list[str], str]:
    breakpoint: str | None = None
    pseudos: list[str] = []
    utility = token

    while ":" in utility:
        prefix, remainder = utility.split(":", 1)
        if prefix in BREAKPOINTS:
            breakpoint = prefix
        elif prefix in PSEUDO_VARIANTS:
            pseudos.append(prefix)
        else:
            raise ValueError(f"Unsupported class variant: {token}")
        utility = remainder

    return breakpoint, pseudos, utility


def generate_spacing_rule(prefix: str, value: str) -> str:
    resolved = resolve_spacing(value)
    if prefix == "p":
        return f"padding: {resolved};"
    if prefix == "px":
        return f"padding-left: {resolved};\n  padding-right: {resolved};"
    if prefix == "py":
        return f"padding-top: {resolved};\n  padding-bottom: {resolved};"
    if prefix == "pt":
        return f"padding-top: {resolved};"
    if prefix == "pb":
        return f"padding-bottom: {resolved};"
    if prefix == "pl":
        return f"padding-left: {resolved};"
    if prefix == "m":
        return f"margin: {resolved};"
    if prefix == "mx":
        return f"margin-left: {resolved};\n  margin-right: {resolved};"
    if prefix == "my":
        return f"margin-top: {resolved};\n  margin-bottom: {resolved};"
    if prefix == "mt":
        return f"margin-top: {resolved};"
    if prefix == "mb":
        return f"margin-bottom: {resolved};"
    if prefix == "ml":
        return f"margin-left: {resolved};"
    if prefix == "mr":
        return f"margin-right: {resolved};"
    if prefix == "gap":
        return f"gap: {resolved};"
    raise ValueError(f"Unsupported spacing prefix: {prefix}-{value}")


def generate_color_rule(utility: str) -> str | None:
    for prefix, property_name in (
        ("bg-", "background-color"),
        ("border-", "border-color"),
        ("text-", "color"),
    ):
        if utility.startswith(prefix):
            color_token = utility[len(prefix):]
            if color_token in {"clip-text", "transparent"}:
                return None
            return f"{property_name}: {resolve_color(color_token)};"
    return None


def generate_rule_body(utility: str) -> str:
    if utility in SIMPLE_CLASSES:
        body = SIMPLE_CLASSES[utility]
        if body:
            return body
        return (
            "transform: translate(var(--tw-translate-x), var(--tw-translate-y)) "
            "scaleX(var(--tw-scale-x)) scaleY(var(--tw-scale-y));"
        )

    if utility in SHADOWS:
        return f"box-shadow: {SHADOWS[utility]};"

    if utility in BACKDROP_BLUR:
        blur = BACKDROP_BLUR[utility]
        return f"-webkit-backdrop-filter: blur({blur});\n  backdrop-filter: blur({blur});"

    if utility == "bg-gradient-to-r":
        return (
            "background-image: linear-gradient("
            "to right, var(--tw-gradient-from), var(--tw-gradient-to));"
        )
    if utility.startswith("from-"):
        return f"--tw-gradient-from: {resolve_color(utility[len('from-'):])};"
    if utility.startswith("to-"):
        return f"--tw-gradient-to: {resolve_color(utility[len('to-'):])};"

    if utility == "duration-300":
        return "transition-duration: 300ms;"
    if utility == "ease-in-out":
        return "transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);"

    if utility == "outline-none":
        return "outline: 2px solid transparent;\n  outline-offset: 2px;"
    if utility == "ring-1":
        return "box-shadow: 0 0 0 1px var(--tw-ring-color, rgb(99 102 241 / 0.6));"
    if utility == "ring-2":
        return "box-shadow: 0 0 0 2px var(--tw-ring-color, rgb(99 102 241 / 0.6));"
    if utility.startswith("ring-"):
        return f"--tw-ring-color: {resolve_color(utility[len('ring-'):])};"

    if utility == "-translate-x-full":
        return (
            "--tw-translate-x: -100%;\n"
            "  transform: translate(var(--tw-translate-x), var(--tw-translate-y)) "
            "scaleX(var(--tw-scale-x)) scaleY(var(--tw-scale-y));"
        )
    if utility.startswith("scale-[") and utility.endswith("]"):
        scale = utility[7:-1]
        return (
            f"--tw-scale-x: {scale};\n"
            f"  --tw-scale-y: {scale};\n"
            "  transform: translate(var(--tw-translate-x), var(--tw-translate-y)) "
            "scaleX(var(--tw-scale-x)) scaleY(var(--tw-scale-y));"
        )

    if utility == "animate-pulse":
        return "animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;"
    if utility == "animate-fadeIn":
        return "animation: fadeIn 220ms ease-out both;"

    if utility == "sr-only":
        return (
            "position: absolute;\n"
            "  width: 1px;\n"
            "  height: 1px;\n"
            "  padding: 0;\n"
            "  margin: -1px;\n"
            "  overflow: hidden;\n"
            "  clip: rect(0, 0, 0, 0);\n"
            "  white-space: nowrap;\n"
            "  border-width: 0;"
        )

    if utility.startswith("z-"):
        return f"z-index: {utility[2:]};"

    if utility.startswith("opacity-"):
        return f"opacity: {int(utility[8:]) / 100:g};"

    if utility.startswith("text-[") and utility.endswith("]"):
        size = utility[6:-1]
        return f"font-size: {size};"
    if utility.startswith("text-"):
        size_token = utility[5:]
        if size_token in TEXT_SIZES:
            font_size, line_height = TEXT_SIZES[size_token]
            return f"font-size: {font_size};\n  line-height: {line_height};"
        if size_token == "5xl":
            return "font-size: 3rem;\n  line-height: 1;"
        maybe_color = generate_color_rule(utility)
        if maybe_color:
            return maybe_color

    if utility == "w-1/3":
        return "width: 33.333333%;"
    if utility.startswith("w-"):
        value = utility[2:]
        if value == "full":
            return "width: 100%;"
        if value == "px":
            return "width: 1px;"
        return f"width: {resolve_spacing(value)};"
    if utility.startswith("h-"):
        value = utility[2:]
        if value == "full":
            return "height: 100%;"
        return f"height: {resolve_spacing(value)};"
    if utility.startswith("max-h-"):
        return f"max-height: {resolve_spacing(utility[6:])};"
    if utility.startswith("min-h-"):
        return f"min-height: {resolve_spacing(utility[6:])};"
    if utility.startswith("min-w-"):
        return f"min-width: {resolve_spacing(utility[6:])};"
    if utility.startswith("max-w-"):
        value = utility[6:]
        if value.startswith("["):
            return f"max-width: {resolve_spacing(value)};"
        return f"max-width: {MAX_WIDTH_SCALE[value]};"
    for spacing_prefix in (
        "p",
        "px",
        "py",
        "pt",
        "pb",
        "pl",
        "m",
        "mx",
        "my",
        "mt",
        "mb",
        "ml",
        "mr",
        "gap",
    ):
        pattern = f"{spacing_prefix}-"
        if utility.startswith(pattern):
            return generate_spacing_rule(spacing_prefix, utility[len(pattern):])

    if utility.startswith("space-y-"):
        spacing = resolve_spacing(utility[8:])
        return (
            "--tw-space-y-reverse: 0;\n"
            f"  margin-top: calc({spacing} * calc(1 - var(--tw-space-y-reverse)));\n"
            f"  margin-bottom: calc({spacing} * var(--tw-space-y-reverse));"
        )

    if utility.startswith("grid-cols-"):
        return f"grid-template-columns: {GRID_COLS[utility[10:]]};"
    if utility.startswith("col-span-"):
        return f"grid-column: span {utility[9:]} / span {utility[9:]};"

    if utility.startswith("top-"):
        return f"top: {resolve_spacing(utility[4:])};"
    if utility.startswith("right-"):
        return f"right: {resolve_spacing(utility[6:])};"
    if utility.startswith("bottom-"):
        return f"bottom: {resolve_spacing(utility[7:])};"
    if utility.startswith("left-"):
        return f"left: {resolve_spacing(utility[5:])};"
    if utility.startswith("inset-"):
        val = resolve_spacing(utility[6:])
        return f"top: {val};\n  right: {val};\n  bottom: {val};\n  left: {val};"
    if utility.startswith("-left-"):
        return f"left: -{resolve_spacing(utility[6:])};"

    if utility.startswith("bg-"):
        maybe_color = generate_color_rule(utility)
        if maybe_color:
            return maybe_color

    if utility.startswith("border-"):
        maybe_color = generate_color_rule(utility)
        if maybe_color:
            return maybe_color

    if utility == "top-0":
        return "top: 0;"

    raise ValueError(f"Unsupported utility class: {utility}")


def build_selector(token: str, pseudos: list[str], utility: str) -> str:
    escaped = css_escape(token)
    suffix = "".join(PSEUDO_VARIANTS[pseudo] for pseudo in pseudos)
    if utility.startswith("space-y-"):
        return f".{escaped} > :not([hidden]) ~ :not([hidden]){suffix}"
    return f".{escaped}{suffix}"


def render_rule(token: str) -> str:
    breakpoint, pseudos, utility = parse_variants(token)
    selector = build_selector(token, pseudos, utility)
    body = generate_rule_body(utility)
    rule = f"{selector} {{\n  {body}\n}}"
    if breakpoint is not None:
        return f"@media (min-width: {BREAKPOINTS[breakpoint]}) {{\n  {rule}\n}}"
    return rule


def main() -> None:
    classes = extract_candidate_classes()
    rules: list[str] = []
    unsupported: list[str] = []

    for token in classes:
        try:
            rules.append(render_rule(token))
        except Exception:
            unsupported.append(token)

    if unsupported:
        unsupported_list = "\n".join(f" - {token}" for token in unsupported)
        raise SystemExit(f"Unsupported utility classes:\n{unsupported_list}")

    header = """/*
 * Generated by scripts/generate_frontend_utility_css.py
 * This replaces the Tailwind runtime CDN for the embedded desktop frontend.
 */

*, ::before, ::after {
  --tw-translate-x: 0;
  --tw-translate-y: 0;
  --tw-scale-x: 1;
  --tw-scale-y: 1;
  --tw-ring-color: rgb(99 102 241 / 0.6);
  --tw-gradient-from: transparent;
  --tw-gradient-to: transparent;
  box-sizing: border-box;
}

@keyframes pulse {
  50% {
    opacity: 0.5;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(8px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}
"""

    OUTPUT_PATH.write_text(
        header + "\n" + "\n\n".join(sorted(rules)) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
