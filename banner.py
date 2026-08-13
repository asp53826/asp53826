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

PROJECTS = [
    {
        "slug": "counterexample",
        "index": "F-00",
        "title": "COUNTEREXAMPLE",
        "subtitle": "PUBLIC FAILURE REGISTER",
        "proof": "12 FAILURES  /  8 ENGINES  /  SIGNED RELEASE",
        "copy": "Mechanism, attack, oracle, boundary, and downloadable receipt.",
        "accent": "fault",
    },
    {
        "slug": "raft-mvcc",
        "index": "S-01",
        "title": "RAFT + MVCC",
        "subtitle": "CONSENSUS UNDER ATTACK",
        "proof": "598 ASSERTIONS  /  5 NODES  /  LINEARIZABILITY",
        "copy": "Partitions, stale leaders, conflict repair, serializable snapshots.",
        "accent": "pass",
    },
    {
        "slug": "tensorforge-webgpu",
        "index": "M-02",
        "title": "TENSORFORGE",
        "subtitle": "BROWSER TENSOR COMPILER",
        "proof": "TYPED IR  /  FUSION  /  WGSL  /  LIVE ORACLE",
        "copy": "Inspect shape inference, liveness, allocation, and generated kernels.",
        "accent": "signal",
    },
    {
        "slug": "track-fusion",
        "index": "A-03",
        "title": "SIGNALROOM",
        "subtitle": "AUTONOMY MISSION CONTROL",
        "proof": "IMM  /  JPDA  /  OSPA  /  FAILURE SWEEP",
        "copy": "Replay truth, measurements, residuals, uncertainty, and losing regimes.",
        "accent": "trigger",
    },
    {
        "slug": "edgar-mcp",
        "index": "D-04",
        "title": "EDGAR MCP",
        "subtitle": "BOUNDED FINANCIAL DATA",
        "proof": "32 TESTS  /  138× WARM READ  /  10 REQ/S CEILING",
        "copy": "Identity resolution, filing windows, cache validation, global pacing.",
        "accent": "violet",
    },
    {
        "slug": "vllm-lite",
        "index": "M-05",
        "title": "vLLM-LITE",
        "subtitle": "PAGED INFERENCE SCHEDULER",
        "proof": "90 TESTS  /  94% KV USE  /  2.9× THROUGHPUT",
        "copy": "Continuous batching, prefix caching, speculative decoding, honest limits.",
        "accent": "signal",
    },
]

ROUTES = [
    ("systems", "SYSTEMS", "CONSENSUS · STORAGE · QUERY"),
    ("ml-infrastructure", "ML INFRA", "COMPILERS · SERVING · RETRIEVAL"),
    ("defense", "AUTONOMY", "SDR · SAR · FUSION · VIO"),
    ("quant", "QUANT", "EDGAR · MARKETS · ADJOINTS"),
]


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


def instrument_tokens(t):
    """Add the logic-analyzer colors used by the verification instrument."""
    return {
        **t,
        "backplane": "#071319" if t["name"] == "dark" else "#F3F8F8",
        "surface": "#0D2028" if t["name"] == "dark" else "#FFFFFF",
        "surface2": "#102B34" if t["name"] == "dark" else "#E7F1F2",
        "alloy": "#D8E5E8" if t["name"] == "dark" else "#10242B",
        "quiet": "#789098" if t["name"] == "dark" else "#536A72",
        "signal": "#72E4DA" if t["name"] == "dark" else "#087C78",
        "trigger": "#FFB45E" if t["name"] == "dark" else "#9A5700",
        "fault": "#FF6B7E" if t["name"] == "dark" else "#C52F4B",
        "pass": "#7CE7A6" if t["name"] == "dark" else "#167A43",
        "violet": "#B39BFF" if t["name"] == "dark" else "#6546C6",
        "hairline": "#25424B" if t["name"] == "dark" else "#B9CCD0",
    }


def instrument_defs(t, prefix):
    return f"""
  <defs>
    <linearGradient id="{prefix}-panel" x1="0" y1="0" x2="1" y2="1">
      <stop stop-color="{t['backplane']}"/><stop offset=".62" stop-color="{t['surface']}"/><stop offset="1" stop-color="{t['surface2']}"/>
    </linearGradient>
    <pattern id="{prefix}-grid" width="24" height="24" patternUnits="userSpaceOnUse">
      <path d="M24 0H0V24" fill="none" stroke="{t['hairline']}" stroke-opacity=".24"/>
    </pattern>
    <filter id="{prefix}-glow" x="-100%" y="-100%" width="300%" height="300%">
      <feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>"""


def instrument_style():
    return f"""
  <style>
    .display {{ font-family: {SANS}; }}
    .utility {{ font-family: {MONO}; }}
    .packet {{ stroke-dasharray: 4 15; animation: packet 4.8s linear infinite; }}
    .packet.return {{ animation-direction: reverse; animation-duration: 7s; }}
    .sweep {{ animation: sweep 5.5s ease-in-out infinite; }}
    .pulse {{ transform-box: fill-box; transform-origin: center; animation: instrument-pulse 2.6s ease-in-out infinite; }}
    .boot {{ opacity:1; transform:none; animation:boot .55s cubic-bezier(.2,.8,.2,1) backwards; }}
    .b2 {{ animation-delay:.12s; }} .b3 {{ animation-delay:.24s; }} .b4 {{ animation-delay:.36s; }}
    @keyframes packet {{ to {{ stroke-dashoffset:-190; }} }}
    @keyframes sweep {{ 0%,100% {{ transform:translateX(-140px); opacity:0; }} 20%,80% {{ opacity:.12; }} 50% {{ transform:translateX(1240px); opacity:.04; }} }}
    @keyframes instrument-pulse {{ 0%,100% {{ opacity:.5; transform:scale(.82); }} 50% {{ opacity:1; transform:scale(1.18); }} }}
    @keyframes boot {{ from {{ opacity:0; transform:translateY(7px); }} }}
    @media (prefers-reduced-motion: reduce) {{
      .packet,.sweep,.pulse,.boot {{ animation:none; }} .boot {{ opacity:1; transform:none; }} .sweep {{ display:none; }}
    }}
  </style>"""


def instrument_hero(theme, repo_count, test_count, source_kb):
    t = instrument_tokens(theme)
    stages = [
        (612, "CLAIM", t["signal"]),
        (732, "ATTACK", t["fault"]),
        (852, "ORACLE", t["trigger"]),
        (972, "BOUNDARY", t["violet"]),
        (1092, "RECEIPT", t["pass"]),
    ]
    nodes = []
    for i, (x, label, color) in enumerate(stages):
        nodes.append(f"""
      <g class="boot b{min(i + 1, 4)}">
        <rect x="{x-47}" y="190" width="94" height="62" rx="7" fill="{t['surface']}" stroke="{t['hairline']}"/>
        <circle cx="{x}" cy="210" r="5" fill="{color}"/><circle cx="{x}" cy="210" r="11" fill="none" stroke="{color}" class="pulse"/>
        <text x="{x}" y="235" text-anchor="middle" class="utility" font-size="10" letter-spacing="1.2" fill="{t['alloy']}">{label}</text>
      </g>""")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="440" viewBox="0 0 1200 440" role="img" aria-label="Aaryan Patel verification instrument for systems and machine learning infrastructure.">
{instrument_defs(t, 'hero-' + t['name'])}
{instrument_style()}
  <rect width="1200" height="440" rx="18" fill="url(#hero-{t['name']}-panel)"/>
  <rect width="1200" height="440" rx="18" fill="url(#hero-{t['name']}-grid)"/>
  <rect x="1" y="1" width="1198" height="438" rx="17" fill="none" stroke="{t['hairline']}"/>
  <rect width="1200" height="44" rx="18" fill="{t['surface']}" fill-opacity=".86"/>
  <path d="M0 44H1200" stroke="{t['hairline']}"/>
  <circle cx="22" cy="22" r="4" fill="{t['fault']}"/><circle cx="38" cy="22" r="4" fill="{t['trigger']}"/><circle cx="54" cy="22" r="4" fill="{t['pass']}"/>
  <text x="76" y="27" class="utility" font-size="11" letter-spacing="2" fill="{t['quiet']}">EVIDENCE INSTRUMENT // AP-26</text>
  <text x="1168" y="27" text-anchor="end" class="utility" font-size="10" letter-spacing="1.3" fill="{t['pass']}">VERIFIABLE</text>

  <g class="boot">
    <text x="50" y="102" class="utility" font-size="11" letter-spacing="3" fill="{t['signal']}">SYSTEMS + ML INFRASTRUCTURE</text>
    <text x="50" y="174" class="display" font-size="62" font-weight="780" letter-spacing="-3" fill="{t['alloy']}">AARYAN PATEL</text>
    <text x="50" y="210" class="utility" font-size="14" fill="{t['alloy']}">C++ · Python · distributed systems · databases · GPU compilers</text>
    <text x="50" y="238" class="utility" font-size="12" fill="{t['quiet']}">Build the mechanism. Attack the assumption. Publish where it loses.</text>
  </g>

  <path d="M554 221H1144" fill="none" stroke="{t['hairline']}" stroke-width="2"/>
  <path d="M554 221H1144" fill="none" stroke="{t['signal']}" stroke-width="3" class="packet"/>
  {''.join(nodes)}

  <g class="boot b3">
    <rect x="50" y="292" width="1100" height="105" rx="10" fill="{t['surface']}" fill-opacity=".9" stroke="{t['hairline']}"/>
    <path d="M306 307V382M562 307V382M818 307V382" stroke="{t['hairline']}"/>
    <text x="76" y="335" class="utility" font-size="24" font-weight="700" fill="{t['signal']}">{repo_count:02d}</text>
    <text x="76" y="360" class="utility" font-size="10" letter-spacing="1.4" fill="{t['quiet']}">PUBLIC SYSTEMS</text>
    <text x="332" y="335" class="utility" font-size="24" font-weight="700" fill="{t['pass']}">{test_count:,}</text>
    <text x="332" y="360" class="utility" font-size="10" letter-spacing="1.4" fill="{t['quiet']}">TEST FUNCTIONS</text>
    <text x="588" y="335" class="utility" font-size="24" font-weight="700" fill="{t['trigger']}">{source_kb:,} KB</text>
    <text x="588" y="360" class="utility" font-size="10" letter-spacing="1.4" fill="{t['quiet']}">MEASURED SOURCE</text>
    <text x="844" y="335" class="utility" font-size="24" font-weight="700" fill="{t['violet']}">4 ROUTES</text>
    <text x="844" y="360" class="utility" font-size="10" letter-spacing="1.4" fill="{t['quiet']}">ROLE-SPECIFIC ENTRY</text>
  </g>
  <rect x="-140" y="0" width="120" height="440" fill="{t['signal']}" class="sweep"/>
</svg>
"""


def proof_bus(theme):
    t = instrument_tokens(theme)
    stage_data = [
        (100, "01", "CLAIM", "Name the invariant"),
        (325, "02", "ATTACK", "Break the assumption"),
        (550, "03", "ORACLE", "Decide pass or fail"),
        (775, "04", "BOUNDARY", "Publish the losing regime"),
        (1000, "05", "RECEIPT", "Bind source and artifact"),
    ]
    cards = []
    colors = [t["signal"], t["fault"], t["trigger"], t["violet"], t["pass"]]
    for (x, idx, name, sub), color in zip(stage_data, colors):
        cards.append(f"""
    <g class="boot b{min(int(idx), 4)}">
      <rect x="{x-82}" y="82" width="164" height="116" rx="8" fill="{t['surface']}" stroke="{t['hairline']}"/>
      <text x="{x-60}" y="111" class="utility" font-size="10" fill="{color}">{idx}</text>
      <text x="{x-60}" y="145" class="display" font-size="17" font-weight="720" letter-spacing=".4" fill="{t['alloy']}">{name}</text>
      <text x="{x-60}" y="171" class="utility" font-size="9" fill="{t['quiet']}">{sub}</text>
      <circle cx="{x+56}" cy="106" r="5" fill="{color}"/><circle cx="{x+56}" cy="106" r="11" fill="none" stroke="{color}" class="pulse"/>
    </g>""")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="265" viewBox="0 0 1200 265" role="img" aria-label="Verification bus from claim through attack, oracle, boundary, and signed receipt.">
{instrument_defs(t, 'bus-' + t['name'])}
{instrument_style()}
  <rect width="1200" height="265" rx="16" fill="url(#bus-{t['name']}-panel)"/><rect width="1200" height="265" rx="16" fill="url(#bus-{t['name']}-grid)"/>
  <rect x="1" y="1" width="1198" height="263" rx="15" fill="none" stroke="{t['hairline']}"/>
  <text x="18" y="32" class="utility" font-size="10" letter-spacing="2" fill="{t['quiet']}">VERIFICATION BUS // EVERY PUBLIC CLAIM PASSES ALL FIVE GATES</text>
  <path d="M100 140H1100" stroke="{t['hairline']}" stroke-width="4"/>
  <path d="M100 140H1100" stroke="{t['signal']}" stroke-width="3" class="packet"/>
  {''.join(cards)}
  <text x="600" y="238" text-anchor="middle" class="utility" font-size="10" letter-spacing="1.3" fill="{t['quiet']}">SOURCE → TEST → LIMITATION → DIGEST → REPRODUCIBLE COMMAND</text>
</svg>
"""


def project_card(theme, project):
    t = instrument_tokens(theme)
    accent = t[project["accent"]]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="570" height="224" viewBox="0 0 570 224" role="img" aria-label="{project['title']}: {project['copy']}">
{instrument_defs(t, 'card-' + project['slug'] + '-' + t['name'])}
{instrument_style()}
  <rect width="570" height="224" rx="12" fill="url(#card-{project['slug']}-{t['name']}-panel)"/>
  <rect width="570" height="224" rx="12" fill="url(#card-{project['slug']}-{t['name']}-grid)"/>
  <rect x="1" y="1" width="568" height="222" rx="11" fill="none" stroke="{t['hairline']}"/>
  <rect x="0" y="0" width="6" height="224" rx="3" fill="{accent}"/>
  <text x="28" y="34" class="utility" font-size="10" letter-spacing="1.6" fill="{accent}">{project['index']} // {project['subtitle']}</text>
  <text x="28" y="84" class="display" font-size="30" font-weight="780" letter-spacing="-1" fill="{t['alloy']}">{project['title']}</text>
  <text x="28" y="113" class="utility" font-size="11" fill="{t['quiet']}">{project['copy']}</text>
  <rect x="28" y="139" width="514" height="42" rx="6" fill="{t['surface']}" stroke="{t['hairline']}"/>
  <circle cx="47" cy="160" r="5" fill="{accent}"/><circle cx="47" cy="160" r="11" fill="none" stroke="{accent}" class="pulse"/>
  <text x="67" y="165" class="utility" font-size="10" letter-spacing=".5" fill="{t['alloy']}">{project['proof']}</text>
  <text x="28" y="207" class="utility" font-size="9" letter-spacing="1.3" fill="{t['quiet']}">OPEN LIVE PROOF  →</text>
  <path d="M412 205H540" stroke="{accent}" stroke-width="2" class="packet"/>
</svg>
"""


def route_button(theme, slug, title, subtitle):
    t = instrument_tokens(theme)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="280" height="82" viewBox="0 0 280 82" role="img" aria-label="Open {title} recruiter route.">
{instrument_defs(t, 'route-' + slug + '-' + t['name'])}
  <style>.display{{font-family:{SANS}}}.utility{{font-family:{MONO}}}.signal{{stroke-dasharray:4 10;animation:route 4s linear infinite}}@keyframes route{{to{{stroke-dashoffset:-112}}}}@media(prefers-reduced-motion:reduce){{.signal{{animation:none}}}}</style>
  <rect width="280" height="82" rx="9" fill="url(#route-{slug}-{t['name']}-panel)"/><rect x="1" y="1" width="278" height="80" rx="8" fill="none" stroke="{t['hairline']}"/>
  <circle cx="23" cy="24" r="5" fill="{t['signal']}"/><text x="39" y="29" class="display" font-size="15" font-weight="720" fill="{t['alloy']}">{title}</text>
  <text x="23" y="54" class="utility" font-size="8.5" letter-spacing=".4" fill="{t['quiet']}">{subtitle}</text>
  <path d="M204 63H257" stroke="{t['signal']}" stroke-width="2" class="signal"/><path d="M250 57L258 63L250 69" fill="none" stroke="{t['signal']}" stroke-width="2"/>
</svg>
"""


def linkedin_banner():
    t = instrument_tokens(DARK)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1584" height="396" viewBox="0 0 1584 396" role="img" aria-label="Aaryan Patel, systems and machine learning infrastructure engineer.">
{instrument_defs(t, 'linkedin-banner')}
  <style>.display{{font-family:{SANS}}}.utility{{font-family:{MONO}}}</style>
  <rect width="1584" height="396" fill="url(#linkedin-banner-panel)"/><rect width="1584" height="396" fill="url(#linkedin-banner-grid)"/>
  <path d="M0 330H1584" stroke="{t['hairline']}"/><path d="M0 340H1584" stroke="{t['hairline']}" stroke-opacity=".5"/>
  <g opacity=".78">
    <circle cx="176" cy="198" r="118" fill="none" stroke="{t['hairline']}"/><circle cx="176" cy="198" r="82" fill="none" stroke="{t['signal']}" stroke-dasharray="5 13"/>
    <path d="M30 198H322M176 52V344" stroke="{t['hairline']}"/><circle cx="176" cy="198" r="26" fill="{t['surface']}" stroke="{t['signal']}"/>
    <text x="176" y="195" text-anchor="middle" class="utility" font-size="10" fill="{t['signal']}">VERIFY</text><text x="176" y="211" text-anchor="middle" class="utility" font-size="8" fill="{t['quiet']}">THEN CLAIM</text>
  </g>
  <text x="385" y="88" class="utility" font-size="13" letter-spacing="3" fill="{t['signal']}">SYSTEMS + ML INFRASTRUCTURE</text>
  <text x="385" y="157" class="display" font-size="56" font-weight="780" letter-spacing="-2" fill="{t['alloy']}">AARYAN PATEL</text>
  <text x="385" y="198" class="utility" font-size="15" fill="{t['alloy']}">C++ · Python · distributed systems · databases · GPU compilers</text>
  <text x="385" y="229" class="utility" font-size="12" fill="{t['quiet']}">Industrial data engineering @ MP Equipment  ·  UGA ’26</text>
  <path d="M385 274H1460" stroke="{t['hairline']}" stroke-width="3"/>
  <path d="M385 274H1460" stroke="{t['signal']}" stroke-width="2" stroke-dasharray="4 15"/>
  <g class="utility" font-size="10" letter-spacing="1" fill="{t['alloy']}">
    <text x="385" y="304">CLAIM</text><text x="596" y="304">ATTACK</text><text x="807" y="304">ORACLE</text><text x="1018" y="304">BOUNDARY</text><text x="1250" y="304">RECEIPT</text>
  </g>
  <g fill="{t['signal']}"><circle cx="405" cy="274" r="6"/><circle cx="616" cy="274" r="6" fill="{t['fault']}"/><circle cx="827" cy="274" r="6" fill="{t['trigger']}"/><circle cx="1038" cy="274" r="6" fill="{t['violet']}"/><circle cx="1270" cy="274" r="6" fill="{t['pass']}"/></g>
  <text x="1460" y="356" text-anchor="end" class="utility" font-size="10" letter-spacing="1.5" fill="{t['pass']}">asp53826.github.io</text>
</svg>
"""


def linkedin_card(slug, index, title, subtitle, proof, copy, accent_key):
    t = instrument_tokens(DARK)
    accent = t[accent_key]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="627" viewBox="0 0 1200 627" role="img" aria-label="{title}: {copy}">
{instrument_defs(t, 'li-' + slug)}
  <style>.display{{font-family:{SANS}}}.utility{{font-family:{MONO}}}</style>
  <rect width="1200" height="627" fill="url(#li-{slug}-panel)"/><rect width="1200" height="627" fill="url(#li-{slug}-grid)"/>
  <rect x="1" y="1" width="1198" height="625" fill="none" stroke="{t['hairline']}"/>
  <rect x="0" y="0" width="13" height="627" fill="{accent}"/>
  <text x="70" y="78" class="utility" font-size="18" letter-spacing="3" fill="{accent}">{index} // {subtitle}</text>
  <text x="70" y="195" class="display" font-size="74" font-weight="790" letter-spacing="-3" fill="{t['alloy']}">{title}</text>
  <text x="70" y="248" class="utility" font-size="19" fill="{t['quiet']}">{copy}</text>
  <path d="M70 342H1100" stroke="{t['hairline']}" stroke-width="5"/><path d="M70 342H1100" stroke="{accent}" stroke-width="3" stroke-dasharray="7 22"/>
  <g class="utility" font-size="15" letter-spacing="1" fill="{t['alloy']}">
    <text x="70" y="384">CLAIM</text><text x="280" y="384">ATTACK</text><text x="490" y="384">ORACLE</text><text x="700" y="384">BOUNDARY</text><text x="930" y="384">RECEIPT</text>
  </g>
  <g><circle cx="93" cy="342" r="9" fill="{t['signal']}"/><circle cx="303" cy="342" r="9" fill="{t['fault']}"/><circle cx="513" cy="342" r="9" fill="{t['trigger']}"/><circle cx="723" cy="342" r="9" fill="{t['violet']}"/><circle cx="953" cy="342" r="9" fill="{t['pass']}"/></g>
  <rect x="70" y="446" width="1060" height="94" rx="10" fill="{t['surface']}" stroke="{t['hairline']}"/>
  <circle cx="111" cy="493" r="10" fill="{accent}"/><circle cx="111" cy="493" r="22" fill="none" stroke="{accent}" opacity=".58"/>
  <text x="150" y="502" class="utility" font-size="18" letter-spacing="1" fill="{t['alloy']}">{proof}</text>
  <text x="70" y="590" class="utility" font-size="13" letter-spacing="2" fill="{t['quiet']}">LIVE PROOF  /  SOURCE  /  TESTS  /  LIMITS</text>
  <text x="1130" y="590" text-anchor="end" class="utility" font-size="13" letter-spacing="1.5" fill="{accent}">OPEN →</text>
</svg>
"""


def main():
    repo_count, test_count, source_kb = summary()
    Path("assets").mkdir(exist_ok=True)
    Path("assets/projects").mkdir(exist_ok=True)
    Path("assets/routes").mkdir(exist_ok=True)
    Path("assets/linkedin").mkdir(exist_ok=True)
    for theme in (DARK, LIGHT):
        Path(f"banner-{theme['name']}.svg").write_text(
            instrument_hero(theme, repo_count, test_count, source_kb).replace("\n  \n", "\n\n")
        )
        Path(f"assets/proof-bus-{theme['name']}.svg").write_text(
            proof_bus(theme).replace("\n  \n", "\n\n")
        )
        Path(f"assets/system-map-{theme['name']}.svg").write_text(system_map(theme))
        for project in PROJECTS:
            Path(f"assets/projects/{project['slug']}-{theme['name']}.svg").write_text(
                project_card(theme, project)
            )
        for slug, title, subtitle in ROUTES:
            Path(f"assets/routes/{slug}-{theme['name']}.svg").write_text(
                route_button(theme, slug, title, subtitle)
            )
        print(f"wrote banner-{theme['name']}.svg")
        print(f"wrote assets/proof-bus-{theme['name']}.svg")
        print(f"wrote assets/system-map-{theme['name']}.svg")

    Path("assets/linkedin/banner.svg").write_text(linkedin_banner())
    linked_in_cards = [
        ("counterexample", "F-00", "COUNTEREXAMPLE", "PUBLIC FAILURE REGISTER", "12 FAILURES  /  8 ENGINES  /  SIGNED RELEASE", "Operate constrained failures and verify downloadable receipts.", "fault"),
        ("faultline", "S-01", "FAULTLINE", "DISTRIBUTED FAILURE LAB", "C++17 + WASM  /  5 NODES  /  LINEARIZABILITY", "Partition a live cluster, heal it, and inspect the safety decision.", "pass"),
        ("tensorforge", "M-02", "TENSORFORGE", "WEBGPU TENSOR COMPILER", "TYPED IR  /  FUSION  /  WGSL  /  LIVE ORACLE", "Compile tensor graphs and inspect every transformation in the browser.", "signal"),
        ("engineering-os", "R-03", "ENGINEERING OS", "RECRUITER COMMAND CENTER", "4 ROUTES  /  PROOF TOURS  /  EVIDENCE MANIFEST", "Choose a role and reach the strongest reproducible evidence quickly.", "violet"),
        ("vllm-lite", "M-04", "vLLM-LITE", "PAGED INFERENCE SCHEDULER", "90 TESTS  /  94% KV USE  /  2.9× THROUGHPUT", "Continuous batching, prefix caching, speculation, and honest limits.", "trigger"),
    ]
    for args in linked_in_cards:
        Path(f"assets/linkedin/{args[0]}.svg").write_text(linkedin_card(*args))
    print("wrote LinkedIn banner and five Featured cards")


if __name__ == "__main__":
    main()
