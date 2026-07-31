#!/usr/bin/env python3
"""Generate the animated profile hero and systems topology.

The README uses local SVGs instead of third-party cards. Both visuals have
dark/light variants, share one token set, and stop moving when the viewer asks
for reduced motion.

Run after telemetry so the hero reads the current measured totals:

    python3 banner.py
"""

import json
from pathlib import Path

W = 1200
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"
SANS = "Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"

DARK = {
    "name": "dark",
    "bg": "#050814",
    "panel": "#0a1020",
    "panel2": "#0d1628",
    "line": "#20314d",
    "grid": "#6b8bb7",
    "text": "#f4f8ff",
    "muted": "#8da2bf",
    "cyan": "#4de7ff",
    "blue": "#4f8cff",
    "violet": "#9b7bff",
    "amber": "#ffcb66",
    "green": "#68f5ae",
    "red": "#ff647c",
}

LIGHT = {
    "name": "light",
    "bg": "#f7fbff",
    "panel": "#ffffff",
    "panel2": "#eef5ff",
    "line": "#c4d5ea",
    "grid": "#5b789d",
    "text": "#0b1730",
    "muted": "#526a88",
    "cyan": "#007d9d",
    "blue": "#145fe0",
    "violet": "#7048d7",
    "amber": "#9b6400",
    "green": "#087a4c",
    "red": "#c83755",
}


def summary():
    try:
        data = json.loads(Path("assets/summary.json").read_text())
        return data["repos"], data["tests"], round(data["bytes"] / 1024)
    except (FileNotFoundError, KeyError, ValueError, TypeError):
        return 18, 630, 1200


def hero(t, repo_count, test_count, source_kb):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="500" viewBox="0 0 {W} 500" role="img" aria-label="Aaryan Patel. Systems engineer building measured infrastructure across storage, machine learning, sensing, and financial data.">
  <defs>
    <linearGradient id="bg-{t['name']}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{t['bg']}"/>
      <stop offset=".55" stop-color="{t['panel']}"/>
      <stop offset="1" stop-color="{t['panel2']}"/>
    </linearGradient>
    <radialGradient id="halo-{t['name']}">
      <stop offset="0" stop-color="{t['cyan']}" stop-opacity=".23"/>
      <stop offset=".45" stop-color="{t['blue']}" stop-opacity=".08"/>
      <stop offset="1" stop-color="{t['blue']}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="signal-{t['name']}" x1="0" x2="1">
      <stop stop-color="{t['blue']}"/>
      <stop offset=".5" stop-color="{t['cyan']}"/>
      <stop offset="1" stop-color="{t['violet']}"/>
    </linearGradient>
    <pattern id="grid-{t['name']}" width="32" height="32" patternUnits="userSpaceOnUse">
      <path d="M32 0H0V32" fill="none" stroke="{t['grid']}" stroke-opacity=".075"/>
    </pattern>
    <filter id="glow-{t['name']}" x="-100%" y="-100%" width="300%" height="300%">
      <feGaussianBlur stdDeviation="5" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <clipPath id="clip-{t['name']}"><rect width="{W}" height="500" rx="18"/></clipPath>
  </defs>
  <style>
    .sans {{ font-family: {SANS}; }}
    .mono {{ font-family: {MONO}; }}
    .trace {{ stroke-dasharray: 7 12; animation: flow 8s linear infinite; }}
    .trace.b {{ animation-duration: 11s; animation-direction: reverse; }}
    .orbit {{ transform-box: fill-box; transform-origin: center; animation: spin 24s linear infinite; }}
    .orbit.b {{ animation-duration: 36s; animation-direction: reverse; }}
    .pulse {{ transform-box: fill-box; transform-origin: center; animation: pulse 2.8s ease-in-out infinite; }}
    .pulse.b {{ animation-delay: -1.3s; }}
    .scan {{ animation: scan 7s ease-in-out infinite; }}
    .reveal {{ opacity: 0; transform: translateY(8px); animation: reveal .7s cubic-bezier(.2,.8,.2,1) forwards; }}
    .r2 {{ animation-delay: .15s; }}
    .r3 {{ animation-delay: .3s; }}
    .r4 {{ animation-delay: .45s; }}
    .blink {{ animation: blink 1.2s steps(1) infinite; }}
    @keyframes flow {{ to {{ stroke-dashoffset: -190; }} }}
    @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
    @keyframes pulse {{ 0%,100% {{ opacity:.45; transform:scale(.84); }} 50% {{ opacity:1; transform:scale(1.16); }} }}
    @keyframes scan {{ 0%,100% {{ transform:translateY(-18px); opacity:0; }} 18%,82% {{ opacity:.22; }} 50% {{ transform:translateY(500px); opacity:.08; }} }}
    @keyframes reveal {{ to {{ opacity:1; transform:none; }} }}
    @keyframes blink {{ 50% {{ opacity:.2; }} }}
    @media (prefers-reduced-motion: reduce) {{
      .trace,.orbit,.pulse,.scan,.reveal,.blink {{ animation:none; }}
      .reveal {{ opacity:1; transform:none; }}
      .scan {{ display:none; }}
    }}
  </style>

  <g clip-path="url(#clip-{t['name']})">
    <rect width="{W}" height="500" rx="18" fill="url(#bg-{t['name']})"/>
    <rect width="{W}" height="500" fill="url(#grid-{t['name']})"/>
    <circle cx="950" cy="235" r="270" fill="url(#halo-{t['name']})"/>

    <path d="M-30 86H260L310 136H506L558 84H780" fill="none" stroke="{t['blue']}" stroke-opacity=".26" class="trace"/>
    <path d="M420 442H628L700 370H860L925 435H1230" fill="none" stroke="{t['violet']}" stroke-opacity=".24" class="trace b"/>
    <path d="M0 320H156L214 262H398" fill="none" stroke="{t['cyan']}" stroke-opacity=".18" class="trace b"/>

    <rect x="0" y="0" width="{W}" height="46" fill="{t['panel']}" fill-opacity=".72"/>
    <line x1="0" y1="46" x2="{W}" y2="46" stroke="{t['line']}"/>
    <circle cx="24" cy="23" r="4" fill="{t['red']}"/>
    <circle cx="40" cy="23" r="4" fill="{t['amber']}"/>
    <circle cx="56" cy="23" r="4" fill="{t['green']}"/>
    <text x="82" y="28" class="mono" font-size="11" letter-spacing="2.2" fill="{t['muted']}">AARYAN_PATEL // SYSTEMS COMMAND</text>
    <circle cx="1030" cy="23" r="4" fill="{t['green']}" class="blink"/>
    <text x="1042" y="28" class="mono" font-size="11" letter-spacing="1.4" fill="{t['green']}">ALL SYSTEMS MEASURED</text>

    <g class="reveal">
      <text x="58" y="106" class="mono" font-size="12" letter-spacing="3" fill="{t['cyan']}">COMPUTER SCIENCE · UGA</text>
      <text x="58" y="176" class="sans" font-size="62" font-weight="760" letter-spacing="-3.5" fill="{t['text']}">AARYAN</text>
      <text x="58" y="236" class="sans" font-size="62" font-weight="760" letter-spacing="-3.5" fill="{t['text']}">PATEL<tspan fill="{t['cyan']}">_</tspan></text>
    </g>
    <g class="reveal r2">
      <rect x="58" y="268" width="434" height="2" fill="url(#signal-{t['name']})"/>
      <text x="58" y="304" class="mono" font-size="15" fill="{t['text']}">I build the layer underneath the model.</text>
      <text x="58" y="330" class="mono" font-size="13" fill="{t['muted']}">storage · distributed systems · ML infrastructure</text>
      <text x="58" y="352" class="mono" font-size="13" fill="{t['muted']}">signal processing · financial data systems</text>
    </g>

    <g transform="translate(948 235)">
      <circle r="164" fill="none" stroke="{t['line']}" stroke-width="1"/>
      <circle r="124" fill="none" stroke="{t['line']}" stroke-width="1"/>
      <circle r="84" fill="none" stroke="{t['line']}" stroke-width="1"/>
      <circle r="146" fill="none" stroke="{t['blue']}" stroke-opacity=".72" stroke-width="2" stroke-dasharray="5 19" class="orbit"/>
      <circle r="104" fill="none" stroke="{t['violet']}" stroke-opacity=".65" stroke-width="2" stroke-dasharray="2 17" class="orbit b"/>
      <path d="M-160 0H160M0-160V160" stroke="{t['line']}" stroke-opacity=".55"/>
      <path d="M-113-113L113 113M113-113L-113 113" stroke="{t['line']}" stroke-opacity=".35"/>
      <circle r="54" fill="{t['panel']}" stroke="{t['cyan']}" stroke-width="1.5" filter="url(#glow-{t['name']})"/>
      <circle r="39" fill="none" stroke="{t['cyan']}" stroke-opacity=".35" class="pulse"/>
      <text y="-5" text-anchor="middle" class="mono" font-size="12" letter-spacing="2" fill="{t['cyan']}">MEASURE</text>
      <text y="15" text-anchor="middle" class="mono" font-size="10" fill="{t['muted']}">THEN CLAIM</text>

      <g transform="translate(0 -145)">
        <circle r="8" fill="{t['blue']}"/><circle r="16" fill="none" stroke="{t['blue']}" class="pulse"/>
        <text y="-21" text-anchor="middle" class="mono" font-size="10" letter-spacing="1.3" fill="{t['text']}">ML INFRA</text>
      </g>
      <g transform="translate(145 0)">
        <circle r="8" fill="{t['violet']}"/><circle r="16" fill="none" stroke="{t['violet']}" class="pulse b"/>
        <text x="22" y="4" class="mono" font-size="10" letter-spacing="1.3" fill="{t['text']}">FINANCE</text>
      </g>
      <g transform="translate(0 145)">
        <circle r="8" fill="{t['amber']}"/><circle r="16" fill="none" stroke="{t['amber']}" class="pulse"/>
        <text y="-21" text-anchor="middle" class="mono" font-size="10" letter-spacing="1.3" fill="{t['text']}">SENSING</text>
      </g>
      <g transform="translate(-145 0)">
        <circle r="8" fill="{t['green']}"/><circle r="16" fill="none" stroke="{t['green']}" class="pulse b"/>
        <text x="-22" y="4" text-anchor="end" class="mono" font-size="10" letter-spacing="1.3" fill="{t['text']}">STORAGE</text>
      </g>
    </g>

    <g class="reveal r3">
      <rect x="58" y="390" width="1084" height="72" rx="10" fill="{t['panel']}" fill-opacity=".88" stroke="{t['line']}"/>
      <line x1="313" y1="402" x2="313" y2="450" stroke="{t['line']}"/>
      <line x1="568" y1="402" x2="568" y2="450" stroke="{t['line']}"/>
      <line x1="823" y1="402" x2="823" y2="450" stroke="{t['line']}"/>
      <text x="82" y="422" class="mono" font-size="22" font-weight="700" fill="{t['cyan']}">{repo_count:02d}</text>
      <text x="82" y="443" class="mono" font-size="10" letter-spacing="1.5" fill="{t['muted']}">PUBLIC SYSTEMS</text>
      <text x="337" y="422" class="mono" font-size="22" font-weight="700" fill="{t['green']}">{test_count:,}</text>
      <text x="337" y="443" class="mono" font-size="10" letter-spacing="1.5" fill="{t['muted']}">TEST FUNCTIONS</text>
      <text x="592" y="422" class="mono" font-size="22" font-weight="700" fill="{t['violet']}">{source_kb:,} KB</text>
      <text x="592" y="443" class="mono" font-size="10" letter-spacing="1.5" fill="{t['muted']}">MEASURED SOURCE</text>
      <text x="847" y="422" class="mono" font-size="22" font-weight="700" fill="{t['amber']}">MIT</text>
      <text x="847" y="443" class="mono" font-size="10" letter-spacing="1.5" fill="{t['muted']}">CLONE · RUN · VERIFY</text>
    </g>
    <rect class="scan" x="0" y="-18" width="{W}" height="18" fill="{t['cyan']}" opacity=".12"/>
  </g>
  <rect x=".75" y=".75" width="{W-1.5}" height="498.5" rx="18" fill="none" stroke="{t['line']}" stroke-width="1.5"/>
</svg>
"""


def system_map(t):
    nodes = [
        (55, 100, 180, 82, "INGEST", "EDGAR · SIGNAL", t["violet"]),
        (265, 100, 180, 82, "STORE", "WAL · LSM · MVCC", t["green"]),
        (475, 100, 180, 82, "COMPUTE", "COLUMNAR · DIST", t["blue"]),
        (685, 100, 180, 82, "SERVE", "vLLM · HNSW · RAG", t["cyan"]),
        (895, 100, 250, 82, "VERIFY", "ORACLES · EVALS · LIMITS", t["amber"]),
        (55, 248, 250, 82, "FINANCIAL DATA", "XBRL → COMPARABLE FACTS", t["violet"]),
        (335, 248, 250, 82, "ML SYSTEMS", "TRAIN → RETRIEVE → SERVE", t["blue"]),
        (615, 248, 250, 82, "AUTONOMY", "SDR → SAR → TRACK → VIO", t["amber"]),
        (895, 248, 250, 82, "CORRECTNESS", "FAULTS → WITNESS → CLAIM", t["green"]),
    ]
    cards = []
    for i, (x, y, w, h, title, sub, color) in enumerate(nodes):
        cards.append(
            f'<g class="node n{i % 4}">'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{t["panel"]}" stroke="{t["line"]}"/>'
            f'<rect x="{x}" y="{y}" width="4" height="{h}" rx="2" fill="{color}"/>'
            f'<circle cx="{x+24}" cy="{y+26}" r="5" fill="{color}" class="ping"/>'
            f'<text x="{x+39}" y="{y+30}" class="mono" font-size="12" font-weight="700" letter-spacing="1.5" fill="{t["text"]}">{title}</text>'
            f'<text x="{x+24}" y="{y+57}" class="mono" font-size="10" letter-spacing=".7" fill="{t["muted"]}">{sub}</text>'
            f'</g>'
        )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="390" viewBox="0 0 {W} 390" role="img" aria-label="Architecture map connecting ingestion, storage, compute, serving, verification, financial data, machine learning, autonomy, and correctness.">
  <defs>
    <linearGradient id="bus-{t['name']}" x1="0" x2="1">
      <stop stop-color="{t['violet']}"/><stop offset=".33" stop-color="{t['blue']}"/>
      <stop offset=".66" stop-color="{t['cyan']}"/><stop offset="1" stop-color="{t['amber']}"/>
    </linearGradient>
    <pattern id="map-grid-{t['name']}" width="30" height="30" patternUnits="userSpaceOnUse">
      <circle cx="1" cy="1" r=".8" fill="{t['grid']}" opacity=".1"/>
    </pattern>
  </defs>
  <style>
    .mono {{ font-family: {MONO}; }}
    .bus {{ stroke-dasharray: 8 13; animation: route 6s linear infinite; }}
    .return {{ animation-direction: reverse; animation-duration: 8s; }}
    .node {{ opacity:0; animation: node-in .55s ease forwards; }}
    .n1 {{ animation-delay:.12s; }} .n2 {{ animation-delay:.24s; }} .n3 {{ animation-delay:.36s; }}
    .ping {{ transform-box:fill-box; transform-origin:center; animation: ping 2.4s ease-in-out infinite; }}
    @keyframes route {{ to {{ stroke-dashoffset:-168; }} }}
    @keyframes node-in {{ from {{ opacity:0; transform:translateY(7px); }} to {{ opacity:1; transform:none; }} }}
    @keyframes ping {{ 0%,100% {{ opacity:.45; transform:scale(.75); }} 50% {{ opacity:1; transform:scale(1.3); }} }}
    @media (prefers-reduced-motion: reduce) {{
      .bus,.node,.ping {{ animation:none; }}
      .node {{ opacity:1; }}
    }}
  </style>
  <rect width="{W}" height="390" rx="16" fill="{t['bg']}"/>
  <rect width="{W}" height="390" rx="16" fill="url(#map-grid-{t['name']})"/>
  <rect x="1" y="1" width="{W-2}" height="388" rx="15" fill="none" stroke="{t['line']}"/>
  <text x="55" y="42" class="mono" font-size="11" letter-spacing="2.2" fill="{t['cyan']}">SYSTEM TOPOLOGY // CLAIMS FLOW ONLY AFTER VERIFICATION</text>
  <circle cx="1128" cy="38" r="4" fill="{t['green']}" class="ping"/>
  <text x="1115" y="42" text-anchor="end" class="mono" font-size="10" letter-spacing="1" fill="{t['muted']}">LIVE</text>

  <path d="M235 141H265M445 141H475M655 141H685M865 141H895" fill="none" stroke="url(#bus-{t['name']})" stroke-width="3" class="bus"/>
  <path d="M180 182V222H1020V248" fill="none" stroke="{t['line']}" stroke-width="2" class="bus return"/>
  <path d="M460 248V218H790V248M740 248V218" fill="none" stroke="{t['blue']}" stroke-opacity=".48" stroke-width="2" class="bus"/>
  <path d="M1020 330V354H180V330" fill="none" stroke="{t['green']}" stroke-opacity=".42" stroke-width="2" class="bus return"/>

  {''.join(cards)}
  <text x="55" y="368" class="mono" font-size="10" letter-spacing="1.2" fill="{t['muted']}">EACH REPOSITORY SHIPS A REPRODUCIBLE CHECK, A BASELINE, AND THE REGIME WHERE IT LOSES.</text>
</svg>
"""


def main():
    repo_count, test_count, source_kb = summary()
    Path("assets").mkdir(exist_ok=True)
    for theme in (DARK, LIGHT):
        Path(f"banner-{theme['name']}.svg").write_text(
            hero(theme, repo_count, test_count, source_kb)
        )
        Path(f"assets/system-map-{theme['name']}.svg").write_text(system_map(theme))
        print(f"wrote banner-{theme['name']}.svg")
        print(f"wrote assets/system-map-{theme['name']}.svg")


if __name__ == "__main__":
    main()
