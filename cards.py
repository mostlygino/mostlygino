"""The README cards below the showreel, light and dark. Rendered by make.py.

Same rules as the banner: system fonts only, no links inside (GitHub shows SVG
through <img>, so the README wraps each card in its own link), and every bar
is a bar in the source too: nothing redacted is hidden in these files.
"""

from make import BUILD, ICON, MONO, SANS


def frame(t: dict, w: int, h: int, label: str, body: str) -> str:
    label = label.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{label}">
  <defs>
    <linearGradient id="card" x1="0" y1="0" x2="0.6" y2="1">
      <stop offset="0" stop-color="{t["card0"]}"/><stop offset="1" stop-color="{t["card1"]}"/>
    </linearGradient>
    <pattern id="dots" width="12" height="12" patternUnits="userSpaceOnUse">
      <circle cx="1" cy="1" r="1" fill="{t["dots"]}"/>
    </pattern>
    <filter id="lift" x="-20%" y="-20%" width="140%" height="150%">
      <feDropShadow dx="0" dy="14" stdDeviation="18" flood-color="#000" flood-opacity="{t["shadow"]}"/>
    </filter>
  </defs>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="22" fill="url(#card)" stroke="{t["line"]}" stroke-width="1.5"/>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="22" fill="url(#dots)" opacity="0.18"/>
{body}
</svg>
"""


def bar(t: dict, x: float, y: float, w: float, h: float = 16) -> str:
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{t["bar"]}" stroke="{t["line"]}"/>'


def kicker(t: dict, x: float, y: float, text: str) -> str:
    return (f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="17" letter-spacing="2.4" '
            f'fill="{t["muted"]}">{text}</text>')


def footnote(t: dict) -> str:
    body = f"""  <g fill="none" stroke="{t["accent"]}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
    <rect x="44" y="58" width="30" height="23" rx="6"/><path d="M51 58v-7a8 8 0 0 1 16 0v7"/>
  </g>
  <g font-family="{SANS}">
    <text x="96" y="60" font-size="26" font-weight="600" fill="{t["label"]}">Source is private.</text>
    <text x="96" y="92" font-size="20" fill="{t["muted"]}">Walkthroughs on request.</text>
  </g>
  <path d="M640 28v76" stroke="{t["line"]}" stroke-width="1.5"/>
  {bar(t, 682, 54, 60, 24)}
  <g font-family="{SANS}">
    <text x="764" y="60" font-size="26" font-weight="600" fill="{t["label"]}">And more, under bars.</text>
    <text x="764" y="92" font-size="20" fill="{t["muted"]}">For the redacted details, get in touch.</text>
  </g>
  <text x="1232" y="80" text-anchor="end" font-family="{SANS}" font-size="34" fill="{t["accent"]}">→</text>"""
    return frame(t, 1280, 132, "Source is private, walkthroughs on request. And more, under bars: for the redacted details, get in touch.", body)


RULES = [
    ("The AI never has the last word", 150),
    ("Fail closed", 170),
    ("Missing is not clean", 160),
    ("Keys stay on the server", 126),
    ("Self-hosted by default", 140),
    ("Keyboard first", None),
]


def principles(t: dict) -> str:
    rows = []
    for i, (rule, width) in enumerate(RULES):
        y = 124 + i * 50
        tick = (f'<circle cx="53" cy="{y - 8}" r="12" fill="{t["tile"]}" stroke="{t["accent"]}" stroke-width="1.8"/>'
                f'<path d="M47 {y - 8} l4.5 4.5 l7.5 -8.5" fill="none" stroke="{t["accent"]}" stroke-width="2.2" '
                f'stroke-linecap="round" stroke-linejoin="round"/>')
        text = f'<text x="78" y="{y}" font-family="{SANS}" font-size="22" font-weight="600" fill="{t["label"]}">{rule}</text>'
        where = (bar(t, 600 - width, y - 20, width, 20) if width else
                 f'<text x="600" y="{y}" text-anchor="end" font-family="{MONO}" font-size="17" fill="{t["muted"]}">⌘K almost everywhere</text>')
        rows.append(f"  {tick}{text}{where}")
    body = f"""  {kicker(t, 40, 56, "HOW I BUILD")}
  <text x="600" y="56" text-anchor="end" font-family="{MONO}" font-size="17" letter-spacing="2.4" fill="{t["muted"]}">WHERE IT SHOWS</text>
  <path d="M40 76H600" stroke="{t["line"]}"/>
{chr(10).join(rows)}
  <text x="40" y="416" font-family="{SANS}" font-size="19" fill="{t["muted"]}">Six rules, in every project. The where: on request.</text>"""
    label = "How I build: " + "; ".join(r for r, _ in RULES) + ". Where each rule shows is redacted."
    return frame(t, 640, 448, label, body)


STORIES = [("ENMA", 196, 150), ("GRAVEDIGGER", 172, 164), ("HETTIE", 188, 132), (None, 164, 156)]


def stories(t: dict) -> str:
    rows = []
    for i, (name, broke, fixed) in enumerate(STORIES):
        y = 178 + i * 58
        who = (f'<text x="40" y="{y}" font-family="{MONO}" font-size="19" letter-spacing="0.6" fill="{t["label"]}">{name}</text>'
               if name else bar(t, 40, y - 17, 110, 20))
        rows.append(f"  {who}{bar(t, 206, y - 17, broke, 20)}{bar(t, 430, y - 17, fixed, 20)}")
    body = f"""  {kicker(t, 40, 56, "STORIES WORTH ASKING ABOUT")}
  <g transform="translate(530 60) rotate(-9)">
    <rect x="-74" y="-19" width="148" height="38" rx="6" fill="none" stroke="{t["red"]}" stroke-width="2.6"/>
    <text x="0" y="6" text-anchor="middle" font-family="{MONO}" font-size="16" font-weight="800" letter-spacing="3.5" fill="{t["red"]}">CLASSIFIED</text>
  </g>
  <path d="M40 96H600" stroke="{t["line"]}"/>
  <g font-family="{MONO}" font-size="14" letter-spacing="1.4" fill="{t["muted"]}">
    <text x="40" y="130">PROJECT</text><text x="206" y="130">WHAT BROKE</text><text x="430" y="130">WHAT FIXED IT</text>
  </g>
{chr(10).join(rows)}
  <text x="40" y="416" font-family="{SANS}" font-size="19" fill="{t["muted"]}">The war stories are real. Ask for the file.</text>"""
    return frame(t, 640, 448, "Stories worth asking about: what broke and what fixed it in enma, Gravedigger, Hettie and one more. Classified; ask.", body)


def site(t: dict) -> str:
    """One banner for the whole site: a pitch on the left, the site's own listing header on the right."""
    body = f"""  {kicker(t, 64, 88, "THE REST LIVES ON")}
  <g font-family="{SANS}">
    <text x="62" y="178" font-size="76" font-weight="700" letter-spacing="-2.6" fill="{t["label"]}">mostly<tspan fill="{t["accent"]}">gino</tspan>.com</text>
    <text x="64" y="230" font-size="27" font-weight="500" fill="{t["label2"]}">Apple on the surface. Unix underneath.</text>
    <text x="64" y="270" font-size="22" fill="{t["muted"]}">Who I am, what I use, and a few things to find.</text>
  </g>
  <rect x="64" y="318" width="290" height="62" rx="31" fill="{t["accent"]}"/>
  <text x="209" y="357" text-anchor="middle" font-family="{SANS}" font-size="23" font-weight="600" fill="{t["bg1"]}">Visit the site ↗</text>

  <g filter="url(#lift)">
    <rect x="712" y="56" width="508" height="348" rx="18" fill="{t["card0"]}" stroke="{t["line"]}" stroke-width="1.5"/>
  </g>
  <path d="M712 104H1220" stroke="{t["line"]}"/>
  <circle cx="740" cy="80" r="6" fill="#ff5f57"/><circle cx="760" cy="80" r="6" fill="#febc2e"/><circle cx="780" cy="80" r="6" fill="#28c840"/>
  <rect x="866" y="66" width="200" height="28" rx="9" fill="{t["badge_bg"]}"/>
  <text x="966" y="85" text-anchor="middle" font-family="{MONO}" font-size="14" fill="{t["badge_fg"]}">mostlygino.com</text>
  <image href="data:image/png;base64,{ICON}" x="752" y="140" width="104" height="104"/>
  <g font-family="{SANS}">
    <text x="880" y="186" font-size="46" font-weight="600" letter-spacing="-1.4" fill="{t["label"]}">Gino</text>
    <text x="882" y="214" font-size="18" fill="{t["label2"]}">Security &amp; compliance</text>
  </g>
  <rect x="882" y="228" width="44" height="22" rx="6" fill="{t["badge_bg"]}"/>
  <text x="904" y="243" text-anchor="middle" font-family="{MONO}" font-size="11" letter-spacing="1" fill="{t["badge_fg"]}">BETA</text>
  <text x="936" y="244" font-family="{MONO}" font-size="13" fill="{t["label2"]}">{BUILD}</text>
  <rect x="752" y="292" width="428" height="48" rx="13" fill="none" stroke="{t["line"]}" stroke-width="1.5"/>
  <text x="774" y="322" font-family="{SANS}" font-size="17" fill="{t["muted"]}">Search, or type a command</text>
  <rect x="1122" y="303" width="44" height="26" rx="7" fill="{t["badge_bg"]}"/>
  <text x="1144" y="321" text-anchor="middle" font-family="{SANS}" font-size="14" fill="{t["badge_fg"]}">⌘K</text>
  <text x="752" y="376" font-family="{MONO}" font-size="13" letter-spacing="1.6" fill="{t["muted"]}">ABOUT  ·  TOOLS  ·  HARDWARE  ·  NOTES</text>"""
    return frame(t, 1280, 452, "mostlygino.com: Apple on the surface, Unix underneath. Who I am, what I use, and a few things to find. Visit the site.", body)


def contact(t: dict) -> str:
    body = f"""  {kicker(t, 64, 82, "CONTACT")}
  <g font-family="{SANS}">
    <text x="62" y="154" font-size="64" font-weight="700" letter-spacing="-2" fill="{t["label"]}">Get in <tspan fill="{t["accent"]}">touch.</tspan></text>
    <text x="64" y="204" font-size="25" fill="{t["muted"]}">A walkthrough of a project, or the details</text>
    <text x="64" y="238" font-size="25" fill="{t["muted"]}">behind a redacted line. Just ask.</text>
  </g>
  <rect x="704" y="60" width="512" height="200" rx="18" fill="{t["tile"]}" stroke="{t["line"]}"/>
  <g fill="none" stroke="{t["accent"]}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
    <rect x="744" y="96" width="46" height="34" rx="6"/><path d="M747 100l20 15 20-15"/>
  </g>
  <text x="744" y="186" font-family="{MONO}" font-size="31" fill="{t["label"]}">hello@mostlygino.com</text>
  <text x="744" y="222" font-family="{MONO}" font-size="18" fill="{t["muted"]}">Encrypted mail welcome. Keys below.</text>"""
    return frame(t, 1280, 320, "Get in touch: hello@mostlygino.com. A walkthrough of a project, or the details behind a redacted line. Just ask.", body)


# (card name, local part, kicker, what it is for, fingerprint). The .asc files live in keys/.
KEYS = [
    ("hello", "hello", "PGP · GENERAL", "Walkthroughs, questions, the story behind a bar.",
     "339A0B04A8B0EDD4A7F9434E6A3AD9395C3A3E4F"),
    ("security", "security", "PGP · SECURITY REPORTS", "Found a hole in my stuff? Encrypt the report to this.",
     "AE4A744AE08C3B75D563B9B71E1064795299BF97"),
]
KEY_CREATED = "2026-09-27"


def key(t: dict, local: str, kick: str, blurb: str, fpr: str) -> str:
    """One key, two-up: the address, what it is for, and the fingerprint with its long key ID marked."""
    from showcase import chips

    step, size = 112, 32
    groups = [fpr[i:i + 4] for i in range(0, 40, 4)]
    rows = []
    for i, g in enumerate(groups):
        x, y = 40 + (i % 5) * step, 288 if i < 5 else 334
        fill = t["accent"] if i >= 6 else t["label"]
        rows.append(f'<text x="{x}" y="{y}" fill="{fill}">{g}</text>')
    id_x0, id_x1 = 40 + step, 40 + 4 * step + size * 0.61 * 4
    tags, _ = chips(t, 40, 386, ["ed25519", "cv25519", KEY_CREATED])
    body = f"""  {kicker(t, 40, 56, kick)}
  <rect x="544" y="28" width="56" height="56" rx="14" fill="{t["tile"]}" stroke="{t["line"]}"/>
  <g fill="none" stroke="{t["accent"]}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="563" cy="56" r="8"/><path d="M571 56H590M584 56v7M590 56v5"/>
  </g>
  <text x="40" y="130" font-family="{MONO}" font-size="30" fill="{t["label"]}">{local}<tspan fill="{t["muted"]}">@mostlygino.com</tspan></text>
  <text x="40" y="166" font-family="{SANS}" font-size="20" fill="{t["muted"]}">{blurb}</text>
  <path d="M40 198H600" stroke="{t["line"]}"/>
  <text x="40" y="240" font-family="{MONO}" font-size="14" letter-spacing="1.4" fill="{t["muted"]}">FINGERPRINT</text>
  <g font-family="{MONO}" font-size="{size}">{"".join(rows)}</g>
  <path d="M{id_x0:.0f} 350H{id_x1:.0f}" stroke="{t["accent"]}" stroke-opacity="0.55" stroke-width="1.5"/>
  <text x="{id_x1:.0f}" y="372" text-anchor="end" font-family="{MONO}" font-size="12" letter-spacing="1.4" fill="{t["muted"]}">LONG KEY ID</text>
  {tags}
  <text x="600" y="410" text-anchor="end" font-family="{SANS}" font-size="20" font-weight="600" fill="{t["accent"]}">.asc ↓</text>"""
    label = f"PGP key for {local}@mostlygino.com, ed25519. Fingerprint {' '.join(groups)}. Download the .asc."
    return frame(t, 640, 448, label, body)


def render(t: dict) -> dict[str, str]:
    out = {"footnote": footnote(t), "principles": principles(t), "stories": stories(t), "contact": contact(t)}
    out["site"] = site(t)
    for name, local, kick, blurb, fpr in KEYS:
        out[f"key-{name}"] = key(t, local, kick, blurb, fpr)
    return out
