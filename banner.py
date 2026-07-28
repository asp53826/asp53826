#!/usr/bin/env python3
"""Generates the terminal banner at the top of the README.

Two themes, same layout, so the light and dark versions can't drift apart.
Run it and commit the output:

    python3 banner.py
"""

W, H = 1200, 368
PAD = 40
LINE = 30
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

DARK = {
    "name": "dark",
    "bg": "#0d1117",
    "panel": "#010409",
    "border": "#30363d",
    "grid": "#c9d1d9",
    "dim": "#7d8590",
    "text": "#e6edf3",
    "accent": "#56d4dd",
    "green": "#3fb950",
    "amber": "#d29922",
}

LIGHT = {
    "name": "light",
    "bg": "#ffffff",
    "panel": "#f6f8fa",
    "border": "#d1d9e0",
    "grid": "#1f2328",
    "dim": "#59636e",
    "text": "#1f2328",
    "accent": "#0550ae",
    "green": "#1a7f37",
    "amber": "#9a6700",
}

SYSTEMS = [
    "vllm-lite", "annlite", "dist-train", "feature-store", "rag-eval",
    "agent-harness", "codebase-qa", "grammar-decode", "track-fusion",
    "sdr-receiver", "sar-focus",
]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def prompt_line(y, cmd, t, delay):
    """A `$ cmd` line, typed in."""
    return f"""  <g class="ln" style="animation-delay:{delay}s">
    <text x="{PAD}" y="{y}" class="mono sz" fill="{t['green']}">$</text>
    <text x="{PAD + 22}" y="{y}" class="mono sz" fill="{t['text']}">{esc(cmd)}</text>
  </g>"""


CHIP_ROW = 28


def chips(y, t, delay):
    """The repo names, wrapping onto as many rows as they need.

    Wrapping rather than shrinking: the tenth repo overflowed a single row by
    3px, and the fix that scales is to let the block grow downward instead of
    quietly reducing the type every time one is added.

    Returns the markup and the row count, so the caller can shift what follows.
    """
    out, x, row = [], PAD, 0
    for i, name in enumerate(SYSTEMS):
        w = len(name) * 8.4 + 20
        if x + w > W - PAD:
            row, x = row + 1, PAD
        yy = y + row * CHIP_ROW
        out.append(
            f'    <g class="ln" style="animation-delay:{delay + i * 0.06:.2f}s">'
            f'<rect x="{x:.0f}" y="{yy - 15}" width="{w:.0f}" height="24" rx="5" '
            f'fill="none" stroke="{t["border"]}"/>'
            f'<text x="{x + 10:.0f}" y="{yy + 2}" class="mono sm" fill="{t["dim"]}">{name}</text></g>'
        )
        x += w + 8
    return "\n".join(out), row + 1


def build(t):
    y = 92
    body = [
        prompt_line(y, "whoami", t, 0.15),
        f'  <g class="ln" style="animation-delay:0.45s">'
        f'<text x="{PAD}" y="{y + LINE}" class="mono sz" fill="{t["text"]}">'
        f'Aaryan Patel <tspan fill="{t["dim"]}">— computer science @ UGA</tspan></text></g>',
        f'  <g class="ln" style="animation-delay:0.6s">'
        f'<text x="{PAD}" y="{y + LINE * 2}" class="mono sm" fill="{t["dim"]}">'
        f'I build the infrastructure under machine learning, from scratch, and then measure it.</text></g>',
        prompt_line(y + LINE * 3 + 14, "ls ~/systems", t, 0.9),
    ]
    chip_svg, chip_rows = chips(y + LINE * 4 + 20, t, 1.1)
    extra = (chip_rows - 1) * CHIP_ROW
    body += [
        chip_svg,
        prompt_line(y + LINE * 5 + 34 + extra, "pytest -q --all", t, 1.7),
    ]

    final_y = y + LINE * 6 + 34 + extra
    head, tail = "602 passed", " across 11 repositories"
    # Monospace advance is 0.6em, so the caret can be placed after the text
    # instead of guessed at. A hardcoded x here sat on top of the last word.
    caret_x = PAD + len(head + tail) * 18 * 0.6 + 6
    body.append(
        f'  <g class="ln" style="animation-delay:2.0s">'
        f'<text x="{PAD}" y="{final_y}" class="mono sz" fill="{t["green"]}">{head}'
        f'<tspan fill="{t["dim"]}">{tail}</tspan></text>'
        f'<rect x="{caret_x:.0f}" y="{final_y - 15}" width="10" height="20" fill="{t["accent"]}" class="caret"/></g>'
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Aaryan Patel — computer science at UGA. Builds machine learning infrastructure from scratch.">
  <defs>
    <pattern id="grid-{t['name']}" width="24" height="24" patternUnits="userSpaceOnUse">
      <circle cx="1" cy="1" r="1" fill="{t['grid']}" opacity="0.07"/>
    </pattern>
  </defs>
  <style>
    .mono {{ font-family: {MONO}; }}
    .sz {{ font-size: 18px; }}
    .sm {{ font-size: 14px; }}
    .ln {{ opacity: 0; animation: in 0.45s cubic-bezier(0.2, 0.7, 0.3, 1) forwards; }}
    .caret {{ animation: blink 1.1s steps(1) infinite; }}
    @keyframes in {{ from {{ opacity: 0; transform: translateX(-6px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{
      .ln {{ opacity: 1; animation: none; }}
      .caret {{ animation: none; }}
    }}
  </style>

  <rect width="{W}" height="{H}" rx="12" fill="{t['bg']}"/>
  <rect width="{W}" height="{H}" rx="12" fill="url(#grid-{t['name']})"/>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12" fill="none" stroke="{t['border']}"/>

  <rect x="1" y="1" width="{W - 2}" height="42" rx="12" fill="{t['panel']}"/>
  <rect x="1" y="30" width="{W - 2}" height="13" fill="{t['panel']}"/>
  <line x1="0" y1="43" x2="{W}" y2="43" stroke="{t['border']}"/>
  <circle cx="26" cy="22" r="6" fill="#ff5f57"/>
  <circle cx="46" cy="22" r="6" fill="{t['amber']}"/>
  <circle cx="66" cy="22" r="6" fill="{t['green']}"/>
  <text x="{W // 2}" y="27" text-anchor="middle" class="mono sm" fill="{t['dim']}">asp53826 — ~/systems — zsh</text>

{chr(10).join(body)}
</svg>
"""


for theme in (DARK, LIGHT):
    path = f"banner-{theme['name']}.svg"
    with open(path, "w") as f:
        f.write(build(theme))
    print("wrote", path)
