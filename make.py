"""Render the README banner and cards, light and dark, from the mostlygino.com tokens.

    python3 make.py

Colours mirror zeron/src/styles/globals.css. GitHub renders SVG through <img>,
so no web fonts and no links inside: system stack only. The glyph field is the
site's own backdrop in miniature, seeded so a re-render gives the same bytes.
"""

import base64
import os
import random
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).parent
# the site's repo, next to this one: the tagline and the build come from it,
# so they match mostlygino.com instead of whatever was typed here last
ZERON = Path(os.environ.get("ZERON", HERE.parent / "zeron"))


def icon(name: str) -> str:
    """The portrait in the site's light: assets/icon.png on light, icon-dark.png on dark."""
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
        "icon": icon("icon.png"),
    },
    "dark": {
        "bg0": "#0b0f1f", "bg1": "#000000", "dots": "#121865", "label": "#ffffff",
        "label2": "rgba(235,235,245,0.66)", "glyph": "#5a6a9c", "accent": "#4da2ff",
        "badge_bg": "rgba(118,118,128,0.24)", "badge_fg": "rgba(235,235,245,0.66)",
        "shadow": "0.7",
        "card0": "#10131d", "card1": "#05060a", "line": "rgba(255,255,255,0.10)", "bar": "#000000",
        "tile": "rgba(77,162,255,0.14)", "red": "#ff453a", "muted": "rgba(235,235,245,0.52)",
        "icon": icon("icon-dark.png"),
    },
}

CORPUS = (
    "whoami sudo make coffee curl -I /coffee 418 reboot ls -la ~/opinions "
    "cat /.well-known/security.txt ssh -J hop1,hop2 nmap -sV subfinder -d "
    "sqlmap -u https:// jwt alg:none /etc/motd 10.10.1.1 tcpopen 22 OpenSSH9.6 "
    "Status:301 Size:178 wordlist.txt bloodhound --collect ffuf -w FUZZ "
    "Bearer eyJ /api/v1/users rm -rf ~/saas history | grep oops "
)
CHARS = "-=:.*+#"


def glyph_lines(seed: int = 418) -> list[tuple[int, int, str]]:
    """Rows of corpus fragments broken up by noise, like the live field."""
    rng = random.Random(seed)
    rows = []
    for y in range(28, H, 17):
        x = rng.randint(860, 900)
        line = "".join(
            rng.choice(CHARS) if rng.random() < 0.35 else CORPUS[(y * 7 + i) % len(CORPUS)]
            for i in range(60)
        )
        rows.append((x, y, line.replace("&", "&amp;").replace("<", "&lt;")))
    return rows


def banner(t: dict) -> str:
    glyphs = "".join(
        f'<text x="{x}" y="{y}">{s}</text>' for x, y, s in glyph_lines()
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Gino. {TAGLINE.replace(' · ', ', ')}.">
  <defs>
    <radialGradient id="bg" cx="30%" cy="30%" r="90%">
      <stop offset="0" stop-color="{t["bg0"]}"/><stop offset="1" stop-color="{t["bg1"]}"/>
    </radialGradient>
    <pattern id="dots" width="12" height="12" patternUnits="userSpaceOnUse">
      <circle cx="1" cy="1" r="1" fill="{t["dots"]}"/>
    </pattern>
    <radialGradient id="fade" cx="86%" cy="50%" r="38%">
      <stop offset="0" stop-color="#fff" stop-opacity="1"/>
      <stop offset="0.7" stop-color="#fff" stop-opacity="0.45"/>
      <stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </radialGradient>
    <mask id="field"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>
    <linearGradient id="beam" x1="0" y1="0" x2="1" y2="0" gradientUnits="objectBoundingBox">
      <stop offset="0" stop-color="{t["glyph"]}"/>
      <stop offset="0.45" stop-color="{t["glyph"]}"/>
      <stop offset="0.5" stop-color="{t["accent"]}"/>
      <stop offset="0.55" stop-color="{t["glyph"]}"/>
      <stop offset="1" stop-color="{t["glyph"]}"/>
      <animateTransform attributeName="gradientTransform" type="translate" values="-0.6 0;0.6 0;-0.6 0" dur="14s" repeatCount="indefinite"/>
    </linearGradient>
    <filter id="lift" x="-30%" y="-30%" width="160%" height="170%">
      <feDropShadow dx="0" dy="14" stdDeviation="16" flood-color="#000" flood-opacity="{t["shadow"]}"/>
    </filter>
  </defs>

  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <rect width="{W}" height="{H}" fill="url(#dots)" opacity="0.55"/>

  <!-- the site's glyph field, faded out towards the edges -->
  <g mask="url(#field)" font-family="{MONO}" font-size="12" fill="url(#beam)" opacity="0.75">{glyphs}</g>

  <!-- the listing header: icon, name, tagline, build -->
  <image href="data:image/png;base64,{t["icon"]}" x="96" y="112" width="152" height="152" filter="url(#lift)"/>
  <g font-family="{SANS}">
    <text x="288" y="196" font-size="92" font-weight="600" letter-spacing="-3.2" fill="{t["label"]}">Gino</text>
    <text x="292" y="236" font-size="24" fill="{t["label2"]}">{TAGLINE}</text>
    <rect x="292" y="258" width="50" height="24" rx="6" fill="{t["badge_bg"]}"/>
    <text x="317" y="275" text-anchor="middle" font-family="{MONO}" font-size="12" letter-spacing="1" fill="{t["badge_fg"]}">BETA</text>
    <text x="354" y="275" font-family="{MONO}" font-size="14" fill="{t["label2"]}">{BUILD}</text>
  </g>
</svg>
"""


if __name__ == "__main__":
    import cards
    import showcase

    (HERE / "assets/cards").mkdir(exist_ok=True)
    for name, theme in THEMES.items():
        (HERE / f"assets/banner-{name}.svg").write_text(banner(theme))
        rendered = {**cards.render(theme), **showcase.render(theme, dark=name == "dark")}
        for card, svg in rendered.items():
            (HERE / f"assets/cards/{card}-{name}.svg").write_text(svg)
    print("assets/ rendered")
