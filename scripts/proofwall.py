#!/usr/bin/env python3
"""Generate the 'measured against a baseline' panel.

Only results expressible as a ratio against a *named* baseline appear here.
That rule is the whole point: throughput, utilisation and drift are not
comparable quantities, so plotting them on one axis would be decoration
pretending to be evidence. A ratio against a stated baseline is comparable,
and the baseline is printed on every row so the claim can be checked.

Results without a baseline ratio (crash campaigns, conformance rates, coverage)
are deliberately absent rather than rescaled to fit. They live in the tables.

    python3 scripts/proofwall.py
"""

import math
from pathlib import Path

W = 1200
PAD = 44
ROW = 52
TOP = 132
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"
SANS = "Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"

DARK = {
    "name": "dark", "bg": "#050814", "panel": "#0a1020", "panel2": "#0d1628",
    "line": "#20314d", "text": "#f4f8ff", "muted": "#8da2bf",
    "cyan": "#4de7ff", "blue": "#4f8cff", "violet": "#9b7bff",
    "amber": "#ffcb66", "green": "#68f5ae",
}
LIGHT = {
    "name": "light", "bg": "#f7fbff", "panel": "#ffffff", "panel2": "#eef5ff",
    "line": "#c4d5ea", "text": "#0b1730", "muted": "#526a88",
    "cyan": "#007d9d", "blue": "#145fe0", "violet": "#7048d7",
    "amber": "#9b6400", "green": "#087a4c",
}

# (repo, ratio, headline, baseline it was measured against, colour token)
ROWS = [
    ("edgar-mcp", 138.0, "138x", "warm cached 10-K read vs cold fetch", "cyan"),
    ("aad-greeks", 49.0, "49.0x", "all Greeks vs central differences, 50 inputs", "blue"),
    ("vio-nav", 51.9, "51.9x", "translation drift vs inertial dead reckoning", "violet"),
    ("vllm-lite", 4.48, "4.48x", "KV-cache utilisation vs static batching (94% / 21%)", "green"),
    ("lob-market-making", 4.38, "4.38x", "Sharpe, inventory-skewed vs naive (5.7 / 1.3)", "amber"),
    ("dist-train", 4.00, "4.00x", "bytes per worker vs all-gather, 8 workers", "violet"),
    ("query-planner", 2.15, "2.15x", "bushy DP vs left-deep DP, same 25 queries", "blue"),
    ("columnar-engine", 1.94, "1.94x", "batched filter vs scalar, same result set", "cyan"),
    ("cdcl-sat", 1.94, "1.94x", "VSIDS decay vs frozen scores, same 25 instances", "amber"),
    ("annlite", 1.83, "1.83x", "query throughput vs FAISS at 0.999 recall", "green"),
]

# dst-harness is deliberately absent. Its result is 12 of 12 planted defects
# caught with a clean control over 2,000 seeds, which is a conformance rate and
# not a ratio over a baseline - the same reason the crash campaigns stay in the
# tables. cdcl-sat's comparison against CaDiCaL is absent for a different
# reason: the ratio inverts with instance size (0.5x at 150 variables, 2.7x
# against at 300), so any single number would be a choice of instance size
# rather than a result. The ablation above has no such freedom.

TICKS = [1, 2, 5, 10, 25, 50, 100, 200]
LO, HI = 1.0, 200.0


def x_of(v, x0, span):
    """Log scale. The range runs 1.8x to 138x; linear would compress every
    result below 10x into the first tenth of the axis."""
    return x0 + span * (math.log10(v) - math.log10(LO)) / (math.log10(HI) - math.log10(LO))


def build(t):
    h = TOP + ROW * len(ROWS) + 58
    label_w = 210
    x0 = PAD + label_w + 18
    span = W - x0 - PAD - 96

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" '
        f'width="{W}" height="{h}" role="img" '
        f'aria-label="Measured speedups against named baselines across '
        f'{len(ROWS)} systems">',
        "<defs>",
        f'<linearGradient id="sheen-{t["name"]}" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{t["cyan"]}" stop-opacity="0"/>'
        f'<stop offset=".5" stop-color="{t["cyan"]}" stop-opacity=".55"/>'
        f'<stop offset="1" stop-color="{t["cyan"]}" stop-opacity="0"/></linearGradient>',
        f'<linearGradient id="vign-{t["name"]}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{t["panel2"]}"/>'
        f'<stop offset="1" stop-color="{t["panel"]}"/></linearGradient>',
    ]
    for key in ("cyan", "blue", "violet", "amber", "green"):
        out.append(
            f'<linearGradient id="bar-{key}-{t["name"]}" x1="0" y1="0" x2="1" y2="0">'
            f'<stop offset="0" stop-color="{t[key]}" stop-opacity=".30"/>'
            f'<stop offset="1" stop-color="{t[key]}" stop-opacity="1"/></linearGradient>'
        )
    out.append(f'<filter id="glow-{t["name"]}" x="-40%" y="-70%" width="180%" height="240%">'
               f'<feGaussianBlur stdDeviation="4.5" result="b"/>'
               f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    out.append("</defs>")

    # Every animated element rests at its *final* state and animates backwards
    # out of a hidden one. The obvious way round — opacity:0 plus an animation
    # to 1 — leaves the panel blank for anyone whose renderer does not run CSS
    # animation, which includes reduced-motion users and most static
    # rasterisers. Content first, motion as decoration.
    css = f"""
    .bar {{ transform-origin: {x0}px 0;
            animation: grow 1.15s cubic-bezier(.16,.84,.34,1) backwards; }}
    .fade {{ animation: fade .7s ease-out backwards; }}
    .sweep {{ animation: sweep 5.5s ease-in-out infinite; }}
    .tick-line {{ stroke-dasharray: 3 6; }}
    .pip {{ animation: pip 2.6s ease-in-out infinite; }}
    @keyframes grow {{ from {{ transform: scaleX(0); }} }}
    @keyframes fade {{ from {{ opacity: 0; }} }}
    @keyframes sweep {{
      0%   {{ transform: translateX(-140px); opacity: 0; }}
      12%  {{ opacity: .85; }}
      88%  {{ opacity: .85; }}
      100% {{ transform: translateX({W}px); opacity: 0; }}
    }}
    @keyframes pip {{ 0%,100% {{ opacity:.35; }} 50% {{ opacity:1; }} }}
    @media (prefers-reduced-motion: reduce) {{
      .bar, .fade, .pip {{ animation: none !important; }}
      .sweep {{ display: none; }}
    }}
    """
    out.append(f"<style>{css}</style>")

    out.append(f'<rect width="{W}" height="{h}" rx="16" fill="url(#vign-{t["name"]})"/>')
    out.append(f'<rect x=".5" y=".5" width="{W-1}" height="{h-1}" rx="16" fill="none" '
               f'stroke="{t["line"]}"/>')

    # header
    out.append(f'<text x="{PAD}" y="52" font-family="{SANS}" font-size="23" font-weight="700" '
               f'fill="{t["text"]}" letter-spacing=".5">MEASURED AGAINST A BASELINE</text>')
    out.append(f'<text x="{PAD}" y="76" font-family="{MONO}" font-size="12.5" '
               f'fill="{t["muted"]}">every bar is a ratio over the baseline named on its right '
               f'— log axis, because the range spans two decades</text>')
    out.append(f'<circle class="pip" cx="{W-PAD-96}" cy="46" r="4" fill="{t["green"]}"/>')
    out.append(f'<text x="{W-PAD-82}" y="50" font-family="{MONO}" font-size="12" '
               f'fill="{t["muted"]}">REPRODUCIBLE</text>')

    # axis
    axis_y = TOP - 26
    for v in TICKS:
        x = x_of(v, x0, span)
        out.append(f'<line class="tick-line" x1="{x:.1f}" y1="{axis_y}" x2="{x:.1f}" '
                   f'y2="{TOP + ROW*len(ROWS) - 16}" stroke="{t["line"]}" stroke-width="1"/>')
        out.append(f'<text x="{x:.1f}" y="{axis_y-7}" font-family="{MONO}" font-size="11" '
                   f'fill="{t["muted"]}" text-anchor="middle">{v}x</text>')

    for i, (repo, ratio, headline, baseline, key) in enumerate(ROWS):
        y = TOP + i * ROW
        delay = 0.10 * i
        bw = x_of(ratio, x0, span) - x0

        out.append(f'<text class="fade" style="animation-delay:{delay:.2f}s" x="{PAD}" '
                   f'y="{y+5}" font-family="{MONO}" font-size="13.5" font-weight="600" '
                   f'fill="{t["text"]}">{repo}</text>')

        out.append(f'<rect x="{x0}" y="{y-11}" width="{span}" height="17" rx="4" '
                   f'fill="{t["panel"]}" opacity=".55"/>')
        out.append(
            f'<rect class="bar" style="animation-delay:{delay:.2f}s" x="{x0}" y="{y-11}" '
            f'width="{bw:.1f}" height="17" rx="4" fill="url(#bar-{key}-{t["name"]})" '
            f'filter="url(#glow-{t["name"]})"/>'
        )
        out.append(f'<text class="fade" style="animation-delay:{delay+.28:.2f}s" '
                   f'x="{x0+bw+10:.1f}" y="{y+3}" font-family="{MONO}" font-size="13" '
                   f'font-weight="700" fill="{t[key]}">{headline}</text>')
        out.append(f'<text class="fade" style="animation-delay:{delay+.34:.2f}s" x="{x0}" '
                   f'y="{y+22}" font-family="{MONO}" font-size="11" '
                   f'fill="{t["muted"]}">{baseline}</text>')

    out.append(f'<rect class="sweep" x="-140" y="{TOP-34}" width="140" '
               f'height="{ROW*len(ROWS)+18}" fill="url(#sheen-{t["name"]})"/>')

    foot = ("ratios only — utilisation, conformance and crash-campaign results have no "
            "baseline ratio and are reported in the tables instead")
    out.append(f'<text x="{PAD}" y="{h-22}" font-family="{MONO}" font-size="11" '
               f'fill="{t["muted"]}">{foot}</text>')
    out.append("</svg>")
    return "\n".join(out)


def main():
    Path("assets").mkdir(exist_ok=True)
    for theme in (DARK, LIGHT):
        p = Path(f"assets/proof-{theme['name']}.svg")
        p.write_text(build(theme))
        print(f"  wrote {p} ({p.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
