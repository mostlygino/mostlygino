"""Banners for Enma and Relay, and the showreel that slides through every banner.

    python3 projects.py

Same frame as the Hettie and Gravedigger banners (1280x360, dark ground,
faint grid, one accent glow), so the showreel reads as one set. The other
slides (zeron, classified, tsukumo, kuro, ...) are hand-drawn SVGs in assets/.
"""

import base64
from pathlib import Path

HERE = Path(__file__).parent
W, H = 1280, 360
SANS = "-apple-system,BlinkMacSystemFont,'SF Pro Display','Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,'SF Mono',Menlo,Consolas,monospace"

def app_icon(name: str, x: int, y: int, size: int) -> str:
    """Embed the local artwork: SVGs loaded as GitHub images cannot fetch files."""
    data = base64.b64encode((HERE / f"assets/icons/{name}.png").read_bytes()).decode()
    return (f'<image href="data:image/png;base64,{data}" x="{x}" y="{y}" '
            f'width="{size}" height="{size}"/>')


INK = ("#0a0b0e", "#05070a", "#07090d")
SUMI = ("#120e0b", "#0a0806", "#0d0a08")  # Enma's warm black


def frame(title: str, desc: str, accent: str, glow_x: float, body: str,
          ground: tuple[str, str, str] = INK, glow: float = 0.20) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
  <title id="title">{title}</title>
  <desc id="desc">{desc}</desc>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{ground[0]}"/><stop offset="0.55" stop-color="{ground[1]}"/><stop offset="1" stop-color="{ground[2]}"/>
    </linearGradient>
    <radialGradient id="glow" cx="{glow_x}" cy="0.45" r="0.5">
      <stop offset="0" stop-color="{accent}" stop-opacity="{glow:.2f}"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/>
    </radialGradient>
    <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">
      <path d="M32 0H0V32" fill="none" stroke="#ffffff" stroke-opacity="0.035"/>
    </pattern>
  </defs>
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <rect width="{W}" height="{H}" fill="url(#grid)"/>
  <rect width="{W}" height="{H}" fill="url(#glow)"/>
{body}
</svg>
"""


GOLD, VERMILION, PAPER = "#d4a24c", "#e34234", "#f2ead8"
MINCHO = "'Hiragino Mincho ProN','Yu Mincho','Noto Serif JP',serif"


def enma() -> str:
    # 21 coverage cells, the count REQUIRED_BY_MODE carries; three still unproven.
    open_cells = {6, 13, 17}
    cells = []
    for i in range(21):
        x, y = 760 + (i % 7) * 62, 88 + (i // 7) * 62
        tick = i not in open_cells
        fill = GOLD if tick else VERMILION
        cells.append(
            f'<rect x="{x}" y="{y}" width="50" height="50" rx="10" fill="{fill}" fill-opacity="{0.14 if tick else 0.1}" '
            f'stroke="{fill}" stroke-opacity="{0.55 if tick else 0.9}"/>'
            + (f'<path d="M{x+15} {y+26} l7 7 l13 -15" fill="none" stroke="{fill}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
               if tick else f'<rect x="{x+18}" y="{y+23}" width="14" height="4" rx="2" fill="{fill}"/>')
        )
    body = f"""  {app_icon("enma", 70, 100, 160)}
  <g font-family="{SANS}">
    <text x="262" y="176" font-size="84" font-weight="700" letter-spacing="-2" fill="{PAPER}">enma <tspan font-size="40" font-weight="500" fill="{VERMILION}" font-family="{MINCHO}">閻魔</tspan></text>
    <text x="266" y="216" font-size="20" fill="{PAPER}" fill-opacity="0.72">An autonomous penetration tester</text>
    <text x="266" y="244" font-size="20" fill="{PAPER}" fill-opacity="0.72">that cannot lie about what it tested.</text>
  </g>
  {"".join(cells)}
  <g font-family="{MONO}" font-size="13">
    <text x="760" y="300" fill="{VERMILION}">verdict: withheld, 3 cells unproven</text>
    <text x="760" y="322" fill="{PAPER}" fill-opacity="0.45">ledger · mirror · verdict · terminal cockpit</text>
  </g>"""
    desc = ("enma, 閻魔, the judge: an autonomous penetration tester that keeps a ledger "
            "and withholds a verdict until every cell is proven.")
    return frame("enma", desc, VERMILION, 0.8, body, ground=SUMI, glow=0.16)


def relay() -> str:
    rows = [
        ("Phishing site on customer VPS", "Abuse", True),
        ("Portscan complaint, repeat sender", "Abuse", False),
        ("Password reset for portal", "Support", False),
        ("Spamhaus listing, /24", "Security", False),
    ]
    items = []
    for i, (subject, queue, active) in enumerate(rows):
        y = 70 + i * 54
        items.append(
            f'<rect x="740" y="{y}" width="460" height="44" rx="10" fill="{"#38bdf8" if active else "#ffffff"}" '
            f'fill-opacity="{0.14 if active else 0.04}" stroke="{"#38bdf8" if active else "#ffffff"}" stroke-opacity="{0.7 if active else 0.08}"/>'
            f'<text x="760" y="{y+27}" font-size="15" fill="#e6f6ff" fill-opacity="{1 if active else 0.62}">{subject}</text>'
            f'<text x="1184" y="{y+27}" text-anchor="end" font-family="{MONO}" font-size="12" fill="#38bdf8" fill-opacity="0.8">{queue}</text>'
        )
    keys = "".join(
        f'<rect x="{740 + i * 64}" y="296" width="52" height="30" rx="7" fill="#ffffff" fill-opacity="0.05" stroke="#ffffff" stroke-opacity="0.18"/>'
        f'<text x="{766 + i * 64}" y="316" text-anchor="middle" font-family="{MONO}" font-size="13" fill="#e6f6ff">{k}</text>'
        for i, k in enumerate(["j", "k", "r", "a", "e", "⌘K"])
    )
    body = f"""  {app_icon("relay", 70, 100, 160)}
  <g font-family="{SANS}">
    <text x="250" y="186" font-size="84" font-weight="700" letter-spacing="-2" fill="#e6f6ff">Relay</text>
    <text x="254" y="226" font-size="20" fill="#e6f6ff" fill-opacity="0.72">The ticket client you would</text>
    <text x="254" y="254" font-size="20" fill="#e6f6ff" fill-opacity="0.72">actually want to work in.</text>
  </g>
  <g font-family="{SANS}">{"".join(items)}</g>
  {keys}"""
    return frame("Relay", "Relay: a keyboard-first ticket console.", "#38bdf8", 0.75, body)


REEL = ["zeron", "enma", "gravedigger", "hettie", "relay", "tsukumo", "kuro", "classified"]
HOLD, FADE = 3.4, 0.8  # seconds a slide rests, seconds a slide takes to move


def reel() -> str:
    """Every project banner in one SVG, sliding through them forever like a carousel.

    CSS keyframes, because GitHub shows SVG through <img>: no script, but
    animation runs. Banners go in as data URIs, since an <img>-loaded SVG may
    not fetch anything. Reduced motion shows the first slide and stops.
    """
    n, step = len(REEL), HOLD + FADE
    total = n * step
    fade_pct, hold_pct = FADE / total * 100, step / total * 100
    slides, dots = [], []
    for i, name in enumerate(REEL):
        data = base64.b64encode((HERE / f"assets/{name}.svg").read_bytes()).decode()
        delay = f"{i * step - FADE:.2f}s"
        slides.append(
            f'<image class="s" style="animation-delay:{delay}" href="data:image/svg+xml;base64,{data}" '
            f'width="{W}" height="{H}" preserveAspectRatio="xMidYMid slice"/>'
        )
        x = W / 2 - (n - 1) * 11 + i * 22
        dots.append(f'<rect class="d" style="animation-delay:{delay}" x="{x - 4}" y="{H - 22}" width="8" height="4" rx="2"/>')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Showreel: {", ".join(REEL)}">
  <style>
    .s {{ transform: translateX({W}px); animation: slide {total:.2f}s infinite; }}
    .d {{ fill: #ffffff; opacity: 0.25; animation: dot {total:.2f}s linear infinite; }}
    @keyframes slide {{
      0% {{ transform: translateX({W}px); animation-timing-function: cubic-bezier(0.32, 0.72, 0, 1); }}
      {fade_pct:.3f}% {{ transform: translateX(0); }}
      {hold_pct:.3f}% {{ transform: translateX(0); animation-timing-function: cubic-bezier(0.32, 0.72, 0, 1); }}
      {hold_pct + fade_pct:.3f}% {{ transform: translateX(-{W}px); }}
      100% {{ transform: translateX(-{W}px); }}
    }}
    @keyframes dot {{
      0% {{ opacity: 0.25; }} {fade_pct:.3f}% {{ opacity: 0.9; }}
      {hold_pct:.3f}% {{ opacity: 0.9; }} {hold_pct + fade_pct:.3f}% {{ opacity: 0.25; }} 100% {{ opacity: 0.25; }}
    }}
    @media (prefers-reduced-motion: reduce) {{
      .s, .d {{ animation: none; }}
      .s {{ transform: translateX({W}px); }} .s:first-of-type {{ transform: none; }}
    }}
  </style>
  <rect width="{W}" height="{H}" fill="#05070a"/>
  {"".join(slides)}
  <rect x="{W / 2 - n * 11 - 6}" y="{H - 30}" width="{n * 22 + 12}" height="20" rx="10" fill="#000000" fill-opacity="0.45"/>
  {"".join(dots)}
</svg>
"""


if __name__ == "__main__":
    (HERE / "assets/enma.svg").write_text(enma())
    (HERE / "assets/relay.svg").write_text(relay())
    out = reel()
    assert out.count('class="s"') == out.count('class="d"') == len(REEL)
    (HERE / "assets/showreel.svg").write_text(out)
    print("assets/enma.svg assets/relay.svg assets/showreel.svg rendered")
