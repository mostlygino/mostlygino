"""The README cards above the fold: nav pills, intro, stats and one card per
project in the reel. Rendered by make.py, light and dark, like cards.py.

SVG has no text wrapping, so wrap() breaks lines on an estimated glyph width
(system sans runs about half its size per character). Every project card gets
the height of the tallest one, so the two-up grid lines up.
"""

from __future__ import annotations

from cards import bar, frame, kicker
from make import MONO, SANS
from projects import app_icon

SANS_W, MONO_W = 0.48, 0.61  # average advance per character, as a share of font size


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;")


def wrap(text: str, width: float, size: float) -> list[str]:
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if line and len(trial) * size * SANS_W > width:
            lines.append(line)
            line = word
        else:
            line = trial
    return lines + [line] if line else lines


def chips(t: dict, x: float, y: float, items: list[str], accent: str | None = None, size: int = 15) -> tuple[str, float]:
    """A row of pill chips; returns the markup and the x where the row ends."""
    out, h = [], round(size * 2.25)
    for item in items:
        w = len(item) * size * MONO_W + 28
        stroke = accent or t["line"]
        fill = accent or t["label"]
        out.append(
            f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="{h}" rx="{h / 2}" fill="{t["tile"] if accent else "none"}" '
            f'stroke="{stroke}" stroke-opacity="{0.55 if accent else 1}"/>'
            f'<text x="{x + w / 2:.0f}" y="{y + h * 0.66:.0f}" text-anchor="middle" font-family="{MONO}" font-size="{size}" '
            f'fill="{fill}" fill-opacity="{1 if accent else 0.78}">{esc(item)}</text>'
        )
        x += w + 10
    return "".join(out), x


# nav ------------------------------------------------------------------------

NAV = [("showreel", "Showreel", "↓"), ("more", "More", "↓"), ("contact", "Contact", "↓"), ("site", "mostlygino.com", "↗")]


def pill(t: dict, label: str, arrow: str) -> str:
    body = f"""  <text x="36" y="45" font-family="{SANS}" font-size="23" font-weight="600" fill="{t["label"]}">{label}</text>
  <text x="264" y="46" text-anchor="end" font-family="{SANS}" font-size="24" fill="{t["accent"]}">{arrow}</text>"""
    return frame(t, 300, 72, f"{label} {arrow}", body)


# intro ----------------------------------------------------------------------

ROLES = ["security & compliance", "ISO 27001 · NIS2", "social engineering", "trust & safety tooling"]
STACK = ["Python", "TypeScript", "Swift", "C · eBPF", "Shell", "Next.js", "Docker", "Claude Code"]
PITCH = ["The person between your data", "and a very bad day."]
LEDE = ("I break into things, legally, mostly. Then I build the tools the defenders actually use, "
        "and write the policy that keeps them honest.")
CREDO = "Everything in the reel is in daily use: self-hosted, keys on the server, and the AI never gets the final say."


def intro(t: dict) -> str:
    y = 150
    head = "".join(
        f'<text x="64" y="{y + i * 64}" font-size="58" font-weight="700" letter-spacing="-2" '
        f'fill="{t["accent"] if i else t["label"]}">{line}</text>' for i, line in enumerate(PITCH)
    )
    y += 64 + 58
    lede = wrap(LEDE, 1120, 25)
    body_lines = "".join(
        f'<text x="64" y="{y + i * 36}" font-size="25" font-weight="600" fill="{t["label"]}">{esc(line)}</text>'
        for i, line in enumerate(lede)
    )
    y += len(lede) * 36 + 8
    credo = wrap(CREDO, 1120, 23)
    body_lines += "".join(
        f'<text x="64" y="{y + i * 34}" font-size="23" fill="{t["muted"]}">{esc(line)}</text>'
        for i, line in enumerate(credo)
    )
    y += len(credo) * 34 + 32
    roles, _ = chips(t, 64, y, ROLES, t["accent"], size=17)
    stack, _ = chips(t, 64, y + 52, STACK, size=17)
    h = y + 52 + 38 + 56
    body = f"""  {kicker(t, 64, 82, "SECURITY · COMPLIANCE · BUILD")}
  <g font-family="{SANS}">{head}{body_lines}</g>
  {roles}
  {stack}"""
    return frame(t, 1280, h, f"{' '.join(PITCH)} {LEDE} {CREDO}", body)


# stats ----------------------------------------------------------------------

STATS = [
    ("7", "projects", "in the reel"),
    (None, "coverage cells", "an AI must fill"),
    (None, "report cards", "per indicator"),
    ("3", "operating systems,", "one toolbox"),
    ("0", "accessibility errors", "on mostlygino.com"),
    ("0", "external LLM APIs", "in the T&S tools"),
]


def stats(t: dict) -> str:
    tiles, step = [], 1280 / len(STATS)
    for i, (value, a, b) in enumerate(STATS):
        cx = step * i + step / 2
        big = (f'<text x="{cx:.0f}" y="104" text-anchor="middle" font-family="{SANS}" font-size="64" font-weight="700" '
               f'letter-spacing="-2" fill="{t["label"]}">{value}</text>' if value else bar(t, cx - 34, 58, 68, 48))
        tiles.append(
            big
            + f'<text x="{cx:.0f}" y="152" text-anchor="middle" font-family="{SANS}" font-size="19" fill="{t["muted"]}">{esc(a)}</text>'
            + f'<text x="{cx:.0f}" y="178" text-anchor="middle" font-family="{SANS}" font-size="19" fill="{t["muted"]}">{esc(b)}</text>'
        )
        if i:
            tiles.append(f'<path d="M{step * i:.0f} 44V190" stroke="{t["line"]}"/>')
    label = "; ".join(f"{v or 'redacted'} {a} {b}" for v, a, b in STATS)
    return frame(t, 1280, 232, label, "  " + "".join(tiles))


# projects -------------------------------------------------------------------

# key, name, mark, category, where it runs, line, latest, stack, accent (dark, light), live
PROJECTS = [
    ("zeron", "mostlygino.com", "mg", "Website", "Web",
     "My site. Apple on the surface, Unix underneath.",
     "A terminal that opens like an app, a CTF with signed certificates, and /declassify for the lines I can't print.",
     ["Next.js 16", "TypeScript", "Tailwind", "Vercel"], ("#4da2ff", "#0062cc"), True),
    ("enma", "enma", "閻", "Offensive security", "Docker",
     "An autonomous penetration tester that can't lie about what it tested.",
     "Rebuilt as the judge of the underworld: a ledger, a mirror and a verdict it withholds until every cell is proven.",
     ["Python", "Docker", "Claude Code", "MCP"], ("#e34234", "#c4321f"), False),
    ("gravedigger", "Gravedigger", "G", "Threat intel", "Web, self-hosted",
     "Paste an indicator, get the whole story. Self-hosted abuse triage.",
     "Dozens of checks per scan, run in parallel, and a briefing that only speaks about what was actually checked.",
     ["Node.js", "Python", "DuckDB", "Playwright"], ("#f97316", "#c2410c"), False),
    ("hettie", "Hettie", "H", "Knowledge", "Web, self-hosted",
     "Cited answers from your own wiki. TLP-aware and self-hosted.",
     "Search went from 252 ms to 70 ms at the median, on an index 40% smaller.",
     ["Python", "FastAPI", "RAG", "MCP"], ("#e0b070", "#9a6a1c"), False),
    ("relay", "Relay", "R", "Service desk", "Web, self-hosted",
     "A keyboard-first ticket console you'd actually want to work in.",
     "16 ⌘ shortcuts, a demo mode, and AI drafts a human still has to send.",
     ["Python", "vanilla JS", "per-user vaults"], ("#38bdf8", "#0284c7"), False),
    ("tsukumo", "Tsukumo", "付", "Toolbox", "macOS, Linux, Windows",
     "A script toolbox for networks, abuse handling and daily chores, behind one TUI.",
     "v1.0: one installer, three profiles, the same result on bash and PowerShell.",
     ["Python", "Bash", "PowerShell"], ("#00e08a", "#008f5a"), False),
    ("kuro", "Kuro", "黒", "Desktop", "macOS",
     "A minimal, void-like macOS desktop with drawn badges and motion everywhere.",
     "Drawn Wi-Fi, battery and coffee badges with live cards, and a bar that renews its own Claude login.",
     ["Swift", "SketchyBar", "AeroSpace"], ("#bf5af2", "#8e3bbd"), False),
]
CARD_W, TEXT_W = 640, 560


def project_body(t: dict, p: tuple, accent: str) -> tuple[str, float, list[str]]:
    key, name, mark, category, where, line, latest, stack, _, live = p
    status = "LIVE" if live else "PRIVATE"
    sw = len(status) * 15 * MONO_W + 26
    glyph = (
        f'<rect x="40" y="40" width="68" height="68" rx="18" fill="{accent}" fill-opacity="0.14" stroke="{accent}" stroke-opacity="0.5"/>',
        f'<text x="74" y="{86 if len(mark) == 1 else 84}" text-anchor="middle" font-family="{SANS}" '
        f'font-size="{34 if len(mark) == 1 else 28}" font-weight="700" fill="{accent}">{mark}</text>',
    )
    parts = [
        "".join(glyph) if key == "zeron" else app_icon(key, 36, 36, 76),
        f'<text x="128" y="72" font-family="{SANS}" font-size="31" font-weight="700" letter-spacing="-0.6" fill="{t["label"]}">{esc(name)}</text>',
        f'<text x="129" y="100" font-family="{MONO}" font-size="16" letter-spacing="1" fill="{t["muted"]}">{esc(category.upper())} · {esc(where.upper())}</text>',
        f'<rect x="{600 - sw:.0f}" y="44" width="{sw:.0f}" height="30" rx="15" fill="none" stroke="{accent if live else t["line"]}"/>',
        f'<text x="{600 - sw / 2:.0f}" y="64" text-anchor="middle" font-family="{MONO}" font-size="15" letter-spacing="1" '
        f'fill="{accent if live else t["muted"]}">{status}</text>',
    ]
    y = 160
    for text in wrap(line, TEXT_W, 22):
        parts.append(f'<text x="40" y="{y}" font-family="{SANS}" font-size="22" font-weight="600" fill="{t["label"]}">{esc(text)}</text>')
        y += 30
    y += 14
    parts.append(f'<path d="M40 {y}H600" stroke="{t["line"]}"/>')
    y += 34
    parts.append(f'<text x="40" y="{y}" font-family="{MONO}" font-size="16" letter-spacing="2.2" fill="{accent}">LATEST</text>')
    y += 32
    for text in wrap(latest, TEXT_W, 20):
        parts.append(f'<text x="40" y="{y}" font-family="{SANS}" font-size="20" fill="{t["muted"]}">{esc(text)}</text>')
        y += 28
    return "".join(parts), y + 12, stack


def project(t: dict, p: tuple, dark: bool, height: float) -> str:
    accent = p[8][0] if dark else p[8][1]
    body, _, stack = project_body(t, p, accent)
    row, _ = chips(t, 40, height - 76, stack, size=16)
    return frame(t, CARD_W, height, f"{p[1]}: {p[5]} Latest: {p[6]} Stack: {', '.join(stack)}.", f"  {body}{row}")


def classified(t: dict, height: float) -> str:
    red = t["red"]
    parts = [
        f'<rect x="40" y="40" width="68" height="68" rx="18" fill="{red}" fill-opacity="0.12" stroke="{red}" stroke-opacity="0.5"/>',
        bar(t, 58, 64, 32, 20),
        bar(t, 128, 48, 190, 28),
        bar(t, 129, 88, 250, 14),
        f'<g transform="translate(540 64) rotate(-8)"><rect x="-68" y="-18" width="136" height="36" rx="6" fill="none" '
        f'stroke="{red}" stroke-width="2.6"/><text x="0" y="6" text-anchor="middle" font-family="{MONO}" font-size="15" '
        f'font-weight="800" letter-spacing="3" fill="{red}">CLASSIFIED</text></g>',
        bar(t, 40, 144, 540, 20), bar(t, 40, 174, 360, 20),
        f'<path d="M40 222H600" stroke="{t["line"]}"/>',
        f'<text x="40" y="256" font-family="{MONO}" font-size="16" letter-spacing="2.2" fill="{red}">LATEST</text>',
        bar(t, 40, 274, 520, 18), bar(t, 40, 302, 430, 18),
        f'<text x="40" y="{height - 48}" font-family="{SANS}" font-size="20" fill="{t["muted"]}">Some work can\'t be named in public. Ask for the file.</text>',
    ]
    return frame(t, CARD_W, height, "A classified project: some work can't be named in public. Ask for the file.", "  " + "".join(parts))


def render(t: dict, dark: bool) -> dict[str, str]:
    height = max(project_body(t, p, p[8][0])[1] for p in PROJECTS) + 74 + 12
    out = {f"nav-{key}": pill(t, label, arrow) for key, label, arrow in NAV}
    out.update({"intro": intro(t), "stats": stats(t), "project-classified": classified(t, height)})
    out.update({f"project-{p[0]}": project(t, p, dark, height) for p in PROJECTS})
    return out
