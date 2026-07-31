#!/usr/bin/env python3
"""Generate the profile's source-backed 21-tool execution matrix.

The labels in this panel are technologies used in the public repositories,
their build manifests, CI workflows, or benchmark/verification paths. They are
not certifications and they are deliberately rendered as first-party SVGs.

    python3 scripts/toolchain.py
"""

from html import escape
from pathlib import Path


W = 1200
H = 486
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"
SANS = "Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"

DARK = {
    "name": "dark", "bg": "#050814", "panel": "#0a1020",
    "panel2": "#0d1628", "line": "#20314d", "text": "#f4f8ff",
    "muted": "#8da2bf", "cyan": "#4de7ff", "blue": "#4f8cff",
    "violet": "#9b7bff", "amber": "#ffcb66", "green": "#68f5ae",
}
LIGHT = {
    "name": "light", "bg": "#f7fbff", "panel": "#ffffff",
    "panel2": "#eef5ff", "line": "#c4d5ea", "text": "#0b1730",
    "muted": "#526a88", "cyan": "#007d9d", "blue": "#145fe0",
    "violet": "#7048d7", "amber": "#9b6400", "green": "#087a4c",
}

ROWS = [
    ("BUILD SURFACE", "compile · automate · package", "cyan", [
        ("C++17", "SYSTEMS"),
        ("Python", "CONTROL"),
        ("SQL", "QUERY"),
        ("Bash", "AUTOMATE"),
        ("Git", "VERSION"),
        ("GNU Make", "BUILD"),
        ("Docker", "PACKAGE"),
    ]),
    ("PROOF + DELIVERY", "attack · verify · publish", "violet", [
        ("GitHub Actions", "CI"),
        ("pytest", "TEST"),
        ("ASan + UBSan", "MEMORY"),
        ("DRAT-trim", "PROOF"),
        ("CaDiCaL", "ORACLE"),
        ("HTTPX", "CLIENT"),
        ("GitHub Pages", "LIVE"),
    ]),
    ("RUNTIME + DATA", "compute · retrieve · serve", "green", [
        ("NumPy", "ARRAY"),
        ("SciPy", "NUMERIC"),
        ("PyTorch", "TENSOR"),
        ("FAISS", "BASELINE"),
        ("FastAPI", "SERVE"),
        ("SQLite", "DURABLE"),
        ("MCP", "PROTOCOL"),
    ]),
]


def tile(theme, x, y, width, index, name, role, colour):
    delay = index * 0.035
    return f"""
    <g class="tile" style="animation-delay:{delay:.3f}s">
      <rect x="{x:.1f}" y="{y}" width="{width:.1f}" height="72" rx="10"
            fill="{theme['panel']}" stroke="{theme['line']}"/>
      <path d="M{x+1:.1f} {y+28}H{x+width-1:.1f}" stroke="{theme['line']}"/>
      <path d="M{x+12:.1f} {y}H{x+43:.1f}" stroke="{colour}" stroke-width="2.5"/>
      <text x="{x+12:.1f}" y="{y+19}" class="mono code" fill="{theme['muted']}">{index:02d}</text>
      <circle cx="{x+width-14:.1f}" cy="{y+14}" r="3" fill="{colour}" class="pip"/>
      <text x="{x+12:.1f}" y="{y+49}" class="sans tool" fill="{theme['text']}">{escape(name)}</text>
      <text x="{x+12:.1f}" y="{y+64}" class="mono role" fill="{colour}">{escape(role)}</text>
    </g>"""


def build(theme):
    left = 208
    right = 42
    gap = 9
    width = (W - left - right - gap * 6) / 7
    ys = [132, 238, 344]
    colours = [theme["cyan"], theme["blue"], theme["violet"],
               theme["amber"], theme["green"], theme["blue"], theme["cyan"]]
    tiles = []
    labels = []
    index = 1
    for row_index, ((title, subtitle, colour_key, items), y) in enumerate(zip(ROWS, ys)):
        colour = theme[colour_key]
        labels.append(f"""
    <g class="row-label" style="animation-delay:{row_index * .10:.2f}s">
      <text x="42" y="{y+27}" class="mono row-title" fill="{colour}">{escape(title)}</text>
      <text x="42" y="{y+48}" class="mono row-sub" fill="{theme['muted']}">{escape(subtitle)}</text>
      <path d="M42 {y+66}H181" stroke="{theme['line']}"/>
      <circle cx="187" cy="{y+66}" r="3" fill="{colour}" class="pip"/>
    </g>""")
        for col, (name, role) in enumerate(items):
            x = left + col * (width + gap)
            tiles.append(tile(theme, x, y, width, index, name, role,
                              colours[(col + row_index) % len(colours)]))
            index += 1

    aria = ("Execution matrix of 21 source-backed technologies: C++17, Python, "
            "SQL, Bash, Git, GNU Make, Docker, GitHub Actions, pytest, sanitizers, "
            "DRAT-trim, CaDiCaL, HTTPX, GitHub Pages, NumPy, SciPy, PyTorch, FAISS, "
            "FastAPI, SQLite, and MCP.")
    label_markup = "".join(labels).strip()
    tile_markup = "".join(tiles).strip()
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(aria)}">
  <defs>
    <linearGradient id="bg-{theme['name']}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{theme['bg']}"/>
      <stop offset=".52" stop-color="{theme['panel']}"/>
      <stop offset="1" stop-color="{theme['panel2']}"/>
    </linearGradient>
    <linearGradient id="signal-{theme['name']}" x1="0" x2="1">
      <stop stop-color="{theme['cyan']}" stop-opacity="0"/>
      <stop offset=".48" stop-color="{theme['cyan']}" stop-opacity=".72"/>
      <stop offset="1" stop-color="{theme['green']}" stop-opacity="0"/>
    </linearGradient>
    <pattern id="grid-{theme['name']}" width="22" height="22" patternUnits="userSpaceOnUse">
      <path d="M22 0H0V22" fill="none" stroke="{theme['muted']}" stroke-opacity=".055"/>
    </pattern>
  </defs>
  <style>
    .mono {{ font-family: {MONO}; }}
    .sans {{ font-family: {SANS}; }}
    .code {{ font-size:9px; letter-spacing:1.2px; }}
    .tool {{ font-size:13px; font-weight:720; }}
    .role {{ font-size:8.5px; font-weight:650; letter-spacing:1.1px; }}
    .row-title {{ font-size:11px; font-weight:700; letter-spacing:1.2px; }}
    .row-sub {{ font-size:9.5px; letter-spacing:.35px; }}
    .tile,.row-label {{ animation:enter .65s cubic-bezier(.18,.78,.28,1) backwards; }}
    .pip {{ animation:pulse 2.6s ease-in-out infinite; transform-box:fill-box; transform-origin:center; }}
    .signal {{ animation:signal 6s linear infinite; }}
    @keyframes enter {{ from {{ transform:translateY(8px); }} }}
    @keyframes pulse {{ 0%,100% {{ opacity:.35; transform:scale(.8); }} 50% {{ opacity:1; transform:scale(1.2); }} }}
    @keyframes signal {{ to {{ stroke-dashoffset:-180; }} }}
    @media (prefers-reduced-motion: reduce) {{
      .tile,.row-label,.pip,.signal {{ animation:none; }}
    }}
  </style>
  <rect width="{W}" height="{H}" rx="16" fill="url(#bg-{theme['name']})"/>
  <rect width="{W}" height="{H}" rx="16" fill="url(#grid-{theme['name']})"/>
  <rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="15.25" fill="none" stroke="{theme['line']}" stroke-width="1.5"/>

  <text x="42" y="46" class="sans" font-size="22" font-weight="760" letter-spacing=".7" fill="{theme['text']}">EXECUTION MATRIX // 21</text>
  <text x="42" y="70" class="mono" font-size="11" letter-spacing="1.15" fill="{theme['muted']}">TOOLS THAT BUILD, BREAK, MEASURE, AND SHIP THE PUBLIC SYSTEMS</text>
  <circle cx="1014" cy="45" r="4" fill="{theme['green']}" class="pip"/>
  <text x="1028" y="49" class="mono" font-size="10.5" letter-spacing="1.1" fill="{theme['green']}">SOURCE BACKED</text>
  <path d="M42 96H1158" stroke="{theme['line']}"/>
  <path class="signal" d="M42 96H1158" stroke="url(#signal-{theme['name']})" stroke-width="2" stroke-dasharray="28 152"/>

  {label_markup}
  {tile_markup}

  <line x1="42" y1="444" x2="1158" y2="444" stroke="{theme['line']}"/>
  <text x="42" y="467" class="mono" font-size="9.5" letter-spacing="1" fill="{theme['muted']}">PUBLIC SOURCE · BUILD MANIFESTS · CI WORKFLOWS · EXTERNAL ORACLES</text>
  <text x="1158" y="467" text-anchor="end" class="mono" font-size="9.5" fill="{theme['muted']}">NO DECORATIVE CERTIFICATIONS</text>
</svg>
"""


def main():
    Path("assets").mkdir(exist_ok=True)
    for theme in (DARK, LIGHT):
        path = Path(f"assets/toolchain-{theme['name']}.svg")
        path.write_text(build(theme))
        print(f"wrote {path} ({path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
