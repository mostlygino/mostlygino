"""Material-themed banners and self-contained animated README showreels.

Run python3 projects.py after editing readme-theme.json or the local icons.
Both schemes share the app's real artwork and keep reduced motion static.
"""
import base64
import json
from pathlib import Path

from readme_art import banner, palette, surface

HERE = Path(__file__).parent
W, H = 1280, 400
THEME = json.loads((HERE / "readme-theme.json").read_text())


def app_icon(name: str, x: int, y: int, size: int) -> str:
    data = base64.b64encode((HERE / f"assets/icons/{name}.png").read_bytes()).decode()
    return (f'<image href="data:image/png;base64,{data}" x="{x}" y="{y}" '
            f'width="{size}" height="{size}"/>')


APP_BANNERS = {
    "enma": ("Enma", "Evidence before verdict", "An autonomous penetration tester that cannot lie about what it tested.", "LEDGER · MIRROR · VERDICT"),
    "gravedigger": ("Gravedigger", "An evidence dossier", "Everything buried about a target. Surfaced.", "IP · DOMAIN · URL · HASH · CIDR · ASN"),
    "hettie": ("Hettie", "Your knowledge, cited", "Cited answers from your own wiki.", "HYBRID RETRIEVAL · CITATION CHECK · TLP GATE"),
    "relay": ("Relay", "Every queue, one keyboard", "The ticket client you would actually want to work in.", "TICKETS · KEYBOARD · HUMAN REVIEW"),
    "tsukumo": ("Tsukumo", "Every tool gets a soul", "One toolbox for the work you do every day.", "MACOS · LINUX · WINDOWS"),
    "kuro": ("Kuro", "A quiet desktop", "A desktop that is mostly not there.", "SKETCHYBAR · AEROSPACE · SWIFT"),
    "shiru": ("Shīru", "Sealed by hand", "Native OpenPGP for the Mac.", "GNUPG · YUBIKEY · TOUCH ID · POST-QUANTUM"),
    "onmitsu": ("Onmitsu", "Personal exposure intelligence", "Know your footprint. Take back your privacy.", "STACK DIRECTION · NEXT.JS · POSTGRESQL · PYTHON · TOR"),
}
REEL = ["zeron", "enma", "gravedigger", "hettie", "relay", "tsukumo", "kuro", "shiru", "onmitsu", "classified"]
HOLD, FADE = 3.4, 0.8


def reel(dark: bool = True, compact: bool = False) -> str:
    """Every project banner in one SVG, sliding through them forever like a carousel.

    CSS keyframes, because GitHub shows SVG through <img>: no script, but
    animation runs. Banners go in as data URIs, since an <img>-loaded SVG may
    not fetch anything. Reduced motion shows the first slide and stops.
    """
    mode = ("dark" if dark else "light") + ("-mobile" if compact else "")
    w, h = (640, 480) if compact else (W, H)
    n, step = len(REEL), HOLD + FADE
    total = n * step
    fade_pct, hold_pct = FADE / total * 100, step / total * 100
    slides, dots = [], []
    for i, name in enumerate(REEL):
        data = base64.b64encode((HERE / f"assets/{name}-{mode}.svg").read_bytes()).decode()
        delay = f"{i * step - FADE:.2f}s"
        slides.append(
            f'<image class="s" style="animation-delay:{delay}" href="data:image/svg+xml;base64,{data}" '
            f'width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice"/>'
        )
        x = w / 2 - (n - 1) * 11 + i * 22
        dots.append(f'<rect class="d" style="animation-delay:{delay}" x="{x - 4}" y="{h - 22}" width="8" height="4" rx="2"/>')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Showreel: {", ".join(REEL)}">
  <style>
    .s {{ transform: translateX({w}px); animation: slide {total:.2f}s infinite; }}
    .d {{ fill: #ffffff; opacity: 0.25; animation: dot {total:.2f}s linear infinite; }}
    @keyframes slide {{
      0% {{ transform: translateX({w}px); animation-timing-function: cubic-bezier(0.32, 0.72, 0, 1); }}
      {fade_pct:.3f}% {{ transform: translateX(0); }}
      {hold_pct:.3f}% {{ transform: translateX(0); animation-timing-function: cubic-bezier(0.32, 0.72, 0, 1); }}
      {hold_pct + fade_pct:.3f}% {{ transform: translateX(-{w}px); }}
      100% {{ transform: translateX(-{w}px); }}
    }}
    @keyframes dot {{
      0% {{ opacity: 0.25; }} {fade_pct:.3f}% {{ opacity: 0.9; }}
      {hold_pct:.3f}% {{ opacity: 0.9; }} {hold_pct + fade_pct:.3f}% {{ opacity: 0.25; }} 100% {{ opacity: 0.25; }}
    }}
    @media (prefers-reduced-motion: reduce) {{
      .s, .d {{ animation: none; }}
      .s {{ transform: translateX({w}px); }} .s:first-of-type {{ transform: none; }}
    }}
  </style>
  <rect width="{w}" height="{h}" fill="{'#121314' if dark else '#ede5d8'}"/>
  {"".join(slides)}
  <rect x="{w / 2 - n * 11 - 6}" y="{h - 30}" width="{n * 22 + 12}" height="20" rx="10" fill="#000000" fill-opacity="0.45"/>
  {"".join(dots)}
</svg>
"""


if __name__ == "__main__":
    for mode in ("light", "dark"):
        dark = mode == "dark"
        for key, (name, eyebrow, tagline, footer) in APP_BANNERS.items():
            config = dict(name=name, eyebrow=eyebrow, tagline=tagline, footer=footer, material=THEME["apps"][key])
            icon = base64.b64encode((HERE / f"assets/icons/{key}.png").read_bytes()).decode()
            (HERE / f"assets/{key}-{mode}.svg").write_text(banner(config, dark, icon))
            (HERE / f"assets/{key}-{mode}-mobile.svg").write_text(banner(config, dark, icon, True))
        # the site's app icon, like every other app here; the portrait stays the profile's
        icon = base64.b64encode((HERE / "assets/icons/zeron.png").read_bytes()).decode()
        site = {**THEME, "name": "mostlygino.com", "tagline": "Pretty interfaces. Ugly threat models."}
        (HERE / f"assets/zeron-{mode}.svg").write_text(banner(site, dark, icon))
        (HERE / f"assets/zeron-{mode}-mobile.svg").write_text(banner(site, dark, icon, True))
        p = palette(THEME["material"], dark)
        redacted = f'<g fill="{p["ink"]}"><rect x="64" y="90" width="650" height="50" rx="4"/><rect x="64" y="166" width="430" height="24" rx="3"/></g><text x="64" y="265" font-family="monospace" font-size="27" fill="{p["muted"]}">Some work cannot be named in public.</text><text x="64" y="315" font-family="monospace" font-size="23" fill="{p["accent"]}">Ask for the file.</text><g transform="translate(960 200) rotate(-10)"><rect x="-145" y="-38" width="290" height="76" rx="8" fill="none" stroke="{p["accent"]}" stroke-width="3"/><text text-anchor="middle" y="12" font-family="monospace" font-size="32" fill="{p["accent"]}">CLASSIFIED</text></g>'
        (HERE / f"assets/classified-{mode}.svg").write_text(surface(W,H,p,"Classified project. Ask for the file.",redacted))
        mobile_redacted = f'<g fill="{p["ink"]}"><rect x="32" y="70" width="390" height="40" rx="4"/><rect x="32" y="135" width="280" height="22" rx="3"/></g><text x="32" y="235" font-family="monospace" font-size="26" fill="{p["muted"]}">Some work stays private.</text><text x="32" y="285" font-family="monospace" font-size="25" fill="{p["accent"]}">Ask for the file.</text>'
        (HERE / f"assets/classified-{mode}-mobile.svg").write_text(surface(640,480,p,"Classified project. Ask for the file.",mobile_redacted))
        (HERE / f"assets/showreel-{mode}.svg").write_text(reel(dark))
        (HERE / f"assets/showreel-{mode}-mobile.svg").write_text(reel(dark, True))
    # Preserve existing asset URLs for external links; README uses both schemes.
    for name in [*REEL, "showreel"]:
        (HERE / f"assets/{name}.svg").write_bytes((HERE / f"assets/{name}-dark.svg").read_bytes())
    print("Light/dark material banners and showreels rendered.")
    from stamp import stamp_readme
    stamp_readme()
