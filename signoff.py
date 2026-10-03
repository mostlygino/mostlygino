"""Render Gino's reusable maker's card. Run: ZERON=../zeron python3 signoff.py.

Surface: the site's iOS contact card, made into a glass maker's plaque.
Uses the site's blue, type hierarchy, easing and actual traced autograph.
The portrait is an export of Gino's approved borderless cobalt artwork.
One signature-writing pass settles; reduced motion is complete at first paint.
No scripts, remote images, fonts or interactive controls inside the SVG.
"""

import base64
import html
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
# the portrait and traced autograph live in the private site repo, not here
ZERON = Path(os.environ.get("ZERON", HERE.parent / "zeron"))
SOURCE = ZERON / "docs/brand/signoff/docs/signoff"
OUT = HERE / "assets/signoff"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,'SF Mono',Menlo,Consolas,monospace"


def text(x, y, value, size, fill, *, weight=400, mono=False, spacing=0):
    return (f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" '
            f'font-family="{MONO if mono else SANS}" font-weight="{weight}" '
            f'letter-spacing="{spacing}">{html.escape(value)}</text>')


def render(dark=False, mobile=False, compact=False, animated=True):
    w = 720 if mobile else 1440
    h = (300 if mobile else 240) if compact else (640 if mobile else 420)
    ink, muted, accent = ("#ffffff", "#b8bcc7", "#4da2ff") if dark else ("#111217", "#515866", "#0062cc")
    surface, ground = ("#25262b", "#111217") if dark else ("#ffffff", "#eceef5")
    edge = "#555963" if dark else "#b9c0ce"
    line = "#3b414e" if dark else "#c8cfdd"
    portrait = base64.b64encode((SOURCE / "portrait.jpg").read_bytes()).decode()
    autograph = json.loads((SOURCE / "autograph.json").read_text(encoding="utf-8"))
    animate = animated and not compact
    if compact:
        px, py, ps = (32, 34, 108) if mobile else (36, 36, 168)
        tx, headline_y = (164, 67) if mobile else (244, 77)
        sx, sy, sw = (474, 176, 188) if mobile else (1110, 54, 242)
    else:
        px, py, ps = (44, 48, 150) if mobile else (60, 62, 250)
        tx, headline_y = (44, 288) if mobile else (364, 153)
        sx, sy, sw = (406, 372, 252) if mobile else (1094, 113, 256)
    border = f'M 64 1 H {w-64} Q {w-1} 1 {w-1} 64 V {h-64} Q {w-1} {h-1} {w-64} {h-1} H 64 Q 1 {h-1} 1 {h-64} V 64 Q 1 1 64 1 Z'
    css = ""
    if animate:
        css = '''@media (prefers-reduced-motion: no-preference) {
          .pen {stroke-dasharray:1;stroke-dashoffset:1;animation:write 2.8s .35s cubic-bezier(.32,.72,0,1) both}
          .complete {animation:complete 3.3s step-end both}
          .glint {animation:glint 1.5s 3.1s cubic-bezier(.32,.72,0,1) both}
        }
        @keyframes write {to {stroke-dashoffset:0}}
        @keyframes complete {0% {opacity:0} 100% {opacity:1}}
        @keyframes glint {0% {transform:translateX(-480px);opacity:0} 20% {opacity:.5} 85% {opacity:.2} 100% {transform:translateX(1500px);opacity:0}}
        '''
    paths = ''.join(f'<path d="{d}"/>' for d in autograph['ink'])
    mask = ' mask="url(#pen-mask)"' if animate else ''
    signature = (f'<svg x="{sx}" y="{sy}" width="{sw}" height="{sw*104/244:.2f}" viewBox="41 10 244 104">'
                 f'<g{mask}>'
                 f'<g fill="{accent}" transform="translate(0,142) scale(.1,-.1)">{paths}</g></g></svg>')
    pieces = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
      <title id="title">Built with love by Gino</title>
      <desc id="desc">Security engineer and maker. Cobalt enamel portrait and Gino's handwritten signature. mostlygino.com.</desc>
      <defs>
        <linearGradient id="surface" x2=".85" y2="1"><stop stop-color="{surface}"/><stop offset="1" stop-color="{ground}"/></linearGradient>
        <linearGradient id="rim" x2=".2" y2="1"><stop stop-color="white" stop-opacity="{'.32' if dark else '.98'}"/><stop offset=".45" stop-color="{edge}"/><stop offset="1" stop-color="{edge}" stop-opacity=".5"/></linearGradient>
        <linearGradient id="sheen" x2="1" y2=".3"><stop stop-color="white" stop-opacity="{'.035' if dark else '.6'}"/><stop offset="1" stop-color="white" stop-opacity="0"/></linearGradient>
        <linearGradient id="gloss"><stop stop-color="white" stop-opacity="0"/><stop offset=".5" stop-color="white" stop-opacity=".28"/><stop offset="1" stop-color="white" stop-opacity="0"/></linearGradient>
        <linearGradient id="heart" x2=".3" y2="1"><stop stop-color="#8bcaff"/><stop offset=".48" stop-color="#1681ff"/><stop offset="1" stop-color="#004aab"/></linearGradient>
        <radialGradient id="bloom"><stop stop-color="{accent}" stop-opacity="{'.12' if dark else '.07'}"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient>
        <pattern id="dots" width="12" height="12" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".6" fill="{muted}" opacity=".16"/></pattern>
        <clipPath id="card"><path d="{border}"/></clipPath>
        <clipPath id="portrait"><rect x="{px}" y="{py}" width="{ps}" height="{ps}" rx="{ps*.25}"/></clipPath>
        <filter id="lift" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="9" stdDeviation="9" flood-color="#001a48" flood-opacity="{'.5' if dark else '.19'}"/></filter>
        <mask id="pen-mask" maskUnits="userSpaceOnUse" x="0" y="0" width="300" height="142"><path class="pen" d="{autograph['pen']}" pathLength="1" fill="none" stroke="white" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/><rect class="complete" width="300" height="142" fill="white"/></mask>
      </defs>
      <style>{css}</style>
      <path d="{border}" fill="url(#surface)" stroke="url(#rim)" stroke-width="2"/>
      <g clip-path="url(#card)">
        <ellipse cx="{w*.14}" cy="{h*.1}" rx="500" ry="360" fill="url(#bloom)"/>
        <path d="M0 0 H{w*.77} L{w*.50} {h} H0Z" fill="url(#sheen)"/>
        <rect x="{w-350}" width="350" height="{h}" fill="url(#dots)"/>
      </g>
      <rect x="{px}" y="{py}" width="{ps}" height="{ps}" rx="{ps*.25}" fill="#0754be" filter="url(#lift)"/>
      <image x="{px}" y="{py}" width="{ps}" height="{ps}" href="data:image/jpeg;base64,{portrait}" clip-path="url(#portrait)"/>
      <rect x="{px+.5}" y="{py+.5}" width="{ps-1}" height="{ps-1}" rx="{ps*.25}" fill="none" stroke="white" stroke-opacity=".3"/>
    ''']
    if compact:
        pieces += [text(tx, headline_y, 'Built with love by', 24 if mobile else 27, muted),
                   text(tx, headline_y+49, 'Gino', 40 if mobile else 48, ink, weight=650, spacing=-1.4),
                   text(tx, headline_y+84, 'Security engineer · maker', 20 if mobile else 22, muted)]
        if mobile:
            pieces += [f'<path d="M32 180H688" stroke="{line}"/>', text(32, 242, 'mostlygino.com', 23, accent, weight=600)]
        else:
            pieces += [text(tx, 194, 'mostlygino.com', 22, accent, weight=600),
                       f'<path d="M1062 48V192" stroke="{line}"/>', text(1141, 189, 'SIGNED, GINO', 13, muted, mono=True, spacing=2)]
    else:
        eyex, eyey = (224, 96) if mobile else (364, 77)
        pieces += [f'<g transform="translate({eyex},{eyey-22}) scale(.9)"><path d="M16 28C10 23 1 17 1 10C1 1 12-2 16 6C20-2 31 1 31 10C31 17 22 23 16 28Z" fill="url(#heart)" stroke="{accent}" stroke-width=".7"/><path d="M5 10C5 5 10 3 13 7" fill="none" stroke="white" stroke-opacity=".65" stroke-width="1.7" stroke-linecap="round"/></g>',
                   text(eyex+44, eyey, 'THE HUMAN BEHIND THE CODE', 13 if mobile else 14, muted, mono=True, spacing=1.8),
                   text(tx, headline_y, 'Built with love', 66 if mobile else 67, ink, weight=650, spacing=-2.8),
                   text(tx, headline_y+61, 'by Gino', 40 if mobile else 42, ink, weight=500, spacing=-1.2),
                   text(tx, headline_y+108, 'Security engineer · maker', 25, muted)]
        if mobile:
            pieces += [text(224, 142, 'Pretty interfaces.', 21, ink, weight=500), text(224, 173, 'Ugly threat models.', 21, muted),
                       text(462, 508, 'SIGNED, GINO', 14, muted, mono=True, spacing=2),
                       f'<path d="M44 546H676" stroke="{line}"/>', text(44, 595, 'mostlygino.com', 24, accent, weight=600),
                       text(388, 594, 'SECURITY · PRIVACY · CRAFT', 13, muted, mono=True, spacing=.5)]
        else:
            pieces += [f'<path d="M1048 80V292" stroke="{line}"/>', text(1143, 270, 'SIGNED, GINO', 14, muted, mono=True, spacing=2),
                       f'<path d="M60 344H1380" stroke="{line}"/>', text(60, 386, 'PRETTY INTERFACES. UGLY THREAT MODELS.', 14, muted, mono=True, spacing=1.6),
                       text(725, 386, 'SECURITY · PRIVACY · CRAFT', 13, muted, mono=True, spacing=.8),
                       text(1145, 387, 'mostlygino.com', 23, accent, weight=600)]
    pieces.append(signature)
    if animate:
        pieces.append(f'<g clip-path="url(#card)"><path class="glint" d="M0 0H80L-80 {h}H-160Z" fill="url(#gloss)" opacity="0"/></g>')
    pieces.append('</svg>')
    return '\n'.join(line.rstrip() for piece in pieces for line in piece.splitlines()) + '\n'


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for theme in ('light', 'dark'):
        for mobile in (False, True):
            suffix = f'{theme}{"-mobile" if mobile else ""}'
            for static in (False, True):
                name = f'built-with-love-{suffix}{"-static" if static else ""}.svg'
                (OUT / name).write_text(render(theme == 'dark', mobile, animated=not static), encoding="utf-8")
            (OUT / f'built-with-love-compact-{suffix}.svg').write_text(render(theme == 'dark', mobile, compact=True, animated=False), encoding="utf-8")
    print('Rendered 12 sign-off SVGs.')


if __name__ == '__main__':
    main()
