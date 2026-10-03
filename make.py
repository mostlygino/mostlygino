"""Render the README banner and cards, light and dark, from the mostlygino.com tokens.

    python3 make.py

Colours mirror zeron/src/styles/globals.css. GitHub renders SVG through <img>,
so no web fonts and no links inside: system stack only. The glyph field is the
site's own backdrop in miniature, seeded so a re-render gives the same bytes.
"""

import base64
import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from readme_art import banner as material_banner, palette

HERE = Path(__file__).parent
ART_THEME = json.loads((HERE / "readme-theme.json").read_text())
# the site's repo, next to this one: the tagline and the build come from it,
# so they match mostlygino.com instead of whatever was typed here last
ZERON = Path(os.environ.get("ZERON", HERE.parent / "zeron"))


def icon(name: str) -> str:
    """A picture under assets/, base64 for an SVG <image>."""
    return base64.b64encode((HERE / f"assets/{name}").read_bytes()).decode()


def site_field(field: str, fallback: str) -> str:
    """A field of `site` in zeron/src/lib/config.ts, from the preview branch."""
    try:
        src = subprocess.run(["git", "-C", str(ZERON), "show", "origin/preview:src/lib/config.ts"],
                             capture_output=True, text=True, check=True).stdout
        return re.search(rf'{field}: "([^"]+)"', src).group(1)
    except Exception:
        return fallback


def site_build(fallback: str) -> str:
    """The site's version string, made the way zeron/src/lib/version.ts makes it: 26.9 (20260930.2125)."""
    try:
        ts = subprocess.run(["git", "-C", str(ZERON), "log", "-1", "--format=%ct", "origin/preview"],
                            capture_output=True, text=True, check=True).stdout.strip()
        at = datetime.fromtimestamp(int(ts), tz=timezone.utc)
        return f"{at:%y}.{at.month} ({at:%Y%m%d.%H%M})"
    except Exception:
        return fallback


W, H = 1280, 400
BUILD = site_build("26.9")
TAGLINE = f"{site_field('tagline', 'Security Engineer')} · {site_field('location', 'Behind a VPN')}"
SANS = "-apple-system,BlinkMacSystemFont,'SF Pro Display','Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,'SF Mono',Menlo,Consolas,monospace"

THEMES = {
    "light": {
        "bg0": "#f7f7fb", "bg1": "#eceef8", "dots": "#cfd3f6", "label": "#000000",
        "label2": "rgba(60,60,67,0.88)", "glyph": "#6b6f86", "accent": "#0062cc",
        "badge_bg": "rgba(118,118,128,0.14)", "badge_fg": "rgba(60,60,67,0.88)",
        "shadow": "0.22",
        "card0": "#ffffff", "card1": "#f3f4fa", "line": "rgba(0,0,0,0.09)", "bar": "#1c1c1e",
        "tile": "rgba(0,98,204,0.10)", "red": "#d70015", "muted": "rgba(60,60,67,0.62)",
        # the site's app icon, as every app in the reel wears its own
        "icon": icon("icons/zeron.png"),
    },
    "dark": {
        "bg0": "#0b0f1f", "bg1": "#000000", "dots": "#121865", "label": "#ffffff",
        "label2": "rgba(235,235,245,0.66)", "glyph": "#5a6a9c", "accent": "#4da2ff",
        "badge_bg": "rgba(118,118,128,0.24)", "badge_fg": "rgba(235,235,245,0.66)",
        "shadow": "0.7",
        "card0": "#10131d", "card1": "#05060a", "line": "rgba(255,255,255,0.10)", "bar": "#000000",
        "tile": "rgba(77,162,255,0.14)", "red": "#ff453a", "muted": "rgba(235,235,245,0.52)",
        "icon": icon("icons/zeron.png"),
    },
}

def material_theme(dark: bool, key: str | None = None) -> dict:
    """The same material palette dresses the banner, cards and the showreel."""
    base = THEMES["dark" if dark else "light"]
    material = ART_THEME["apps"][key] if key in ART_THEME["apps"] else ART_THEME["material"]
    p = palette(material, dark)
    return {**base, "_surface": p, "card0": p["surface"], "card1": p["ground"],
            "bg0": p["surface"], "bg1": p["ground"], "label": p["ink"],
            "label2": p["muted"], "muted": p["muted"], "line": p["edge"],
            "accent": p["accent"], "bar": p["ink"], "tile": p["ground"],
            "badge_bg": p["ground"], "badge_fg": p["ink"]}


def banner(t: dict, compact: bool = False) -> str:
    config = {**ART_THEME, "tagline": TAGLINE, "footer": "MOSTLYGINO.COM · " + BUILD}
    return material_banner(config, t["_surface"]["dark"], t["icon"], compact)


if __name__ == "__main__":
    import cards
    import showcase

    (HERE / "assets/cards").mkdir(exist_ok=True)
    for name in THEMES:
        theme = material_theme(name == "dark")
        (HERE / f"assets/banner-{name}.svg").write_text(banner(theme))
        (HERE / f"assets/banner-{name}-mobile.svg").write_text(banner(theme, True))
        rendered = {**cards.render(theme), **showcase.render(theme, dark=name == "dark")}
        for card, svg in rendered.items():
            (HERE / f"assets/cards/{card}-{name}.svg").write_text(svg)
    from stamp import stamp_readme
    stamp_readme()
    print("assets/ rendered, README links stamped")
