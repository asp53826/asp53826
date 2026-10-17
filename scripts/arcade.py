#!/usr/bin/env python3
"""Generates the profile's play layer: the animated pieces that make the
README feel like a lab you walk through instead of a page you scroll.

    assets/fun/terminal-*.svg        tmux session: whoami -> make test -> faultline, plus a live monitor pane
    assets/fun/divider-{a,b,c}-*.svg section dividers: heartbeat, logic analyzer, packet bus with a retry
    assets/fun/highscores-*.svg      arcade attract screen built from the measured numbers
    assets/fun/secret-level-*.svg    Konami-code easter egg: partition the cluster, heal it, unlock an achievement
    assets/fun/patrol-*.svg          footer: a robot walks the log and turns every bug into a test

Same rules as the other generators: stdlib only, no external fonts or images,
deterministic output. Every animation is CSS, so prefers-reduced-motion stops
all of it, and the un-animated style of every element is its *final* frame,
so a reduced-motion reader still sees the finished picture. Every number on
screen is one already published in the README.

    python3 scripts/arcade.py
"""

import math
import sys
from pathlib import Path
from xml.sax.saxutils import escape

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from banner import DARK, LIGHT, MONO, SANS, instrument_defs, instrument_tokens  # noqa: E402

OUT = Path("assets/fun")
BOLD = ' font-weight="700"'

# ---------------------------------------------------------------- pixel type

FONT = {
    " ": [".....", ".....", ".....", ".....", ".....", ".....", "....."],
    "A": [".XXX.", "X...X", "X...X", "XXXXX", "X...X", "X...X", "X...X"],
    "B": ["XXXX.", "X...X", "X...X", "XXXX.", "X...X", "X...X", "XXXX."],
    "C": [".XXX.", "X...X", "X....", "X....", "X....", "X...X", ".XXX."],
    "D": ["XXXX.", "X...X", "X...X", "X...X", "X...X", "X...X", "XXXX."],
    "E": ["XXXXX", "X....", "X....", "XXXX.", "X....", "X....", "XXXXX"],
    "F": ["XXXXX", "X....", "X....", "XXXX.", "X....", "X....", "X...."],
    "G": [".XXX.", "X...X", "X....", "X.XXX", "X...X", "X...X", ".XXXX"],
    "H": ["X...X", "X...X", "X...X", "XXXXX", "X...X", "X...X", "X...X"],
    "I": [".XXX.", "..X..", "..X..", "..X..", "..X..", "..X..", ".XXX."],
    "J": ["..XXX", "...X.", "...X.", "...X.", "...X.", "X..X.", ".XX.."],
    "K": ["X...X", "X..X.", "X.X..", "XX...", "X.X..", "X..X.", "X...X"],
    "L": ["X....", "X....", "X....", "X....", "X....", "X....", "XXXXX"],
    "M": ["X...X", "XX.XX", "X.X.X", "X.X.X", "X...X", "X...X", "X...X"],
    "N": ["X...X", "X...X", "XX..X", "X.X.X", "X..XX", "X...X", "X...X"],
    "O": [".XXX.", "X...X", "X...X", "X...X", "X...X", "X...X", ".XXX."],
    "P": ["XXXX.", "X...X", "X...X", "XXXX.", "X....", "X....", "X...."],
    "Q": [".XXX.", "X...X", "X...X", "X...X", "X.X.X", "X..X.", ".XX.X"],
    "R": ["XXXX.", "X...X", "X...X", "XXXX.", "X.X..", "X..X.", "X...X"],
    "S": [".XXXX", "X....", "X....", ".XXX.", "....X", "....X", "XXXX."],
    "T": ["XXXXX", "..X..", "..X..", "..X..", "..X..", "..X..", "..X.."],
    "U": ["X...X", "X...X", "X...X", "X...X", "X...X", "X...X", ".XXX."],
    "V": ["X...X", "X...X", "X...X", "X...X", "X...X", ".X.X.", "..X.."],
    "W": ["X...X", "X...X", "X...X", "X.X.X", "X.X.X", "X.X.X", ".X.X."],
    "X": ["X...X", "X...X", ".X.X.", "..X..", ".X.X.", "X...X", "X...X"],
    "Y": ["X...X", "X...X", ".X.X.", "..X..", "..X..", "..X..", "..X.."],
    "Z": ["XXXXX", "....X", "...X.", "..X..", ".X...", "X....", "XXXXX"],
    "0": [".XXX.", "X...X", "X..XX", "X.X.X", "XX..X", "X...X", ".XXX."],
    "1": ["..X..", ".XX..", "..X..", "..X..", "..X..", "..X..", ".XXX."],
    "2": [".XXX.", "X...X", "....X", "...X.", "..X..", ".X...", "XXXXX"],
    "3": ["XXXXX", "...X.", "..X..", "...X.", "....X", "X...X", ".XXX."],
    "4": ["...X.", "..XX.", ".X.X.", "X..X.", "XXXXX", "...X.", "...X."],
    "5": ["XXXXX", "X....", "XXXX.", "....X", "....X", "X...X", ".XXX."],
    "6": ["..XX.", ".X...", "X....", "XXXX.", "X...X", "X...X", ".XXX."],
    "7": ["XXXXX", "....X", "...X.", "..X..", ".X...", ".X...", ".X..."],
    "8": [".XXX.", "X...X", "X...X", ".XXX.", "X...X", "X...X", ".XXX."],
    "9": [".XXX.", "X...X", "X...X", ".XXXX", "....X", "...X.", ".XX.."],
    ".": [".....", ".....", ".....", ".....", ".....", ".XX..", ".XX.."],
    "-": [".....", ".....", ".....", ".XXX.", ".....", ".....", "....."],
    "%": ["XX...", "XX..X", "...X.", "..X..", ".X...", "X..XX", "...XX"],
    "×": [".....", ".....", "X...X", ".X.X.", "..X..", ".X.X.", "X...X"],
    ":": [".....", ".XX..", ".XX..", ".....", ".XX..", ".XX..", "....."],
    "▶": ["X....", "XX...", "XXX..", "XXXX.", "XXX..", "XX...", "X...."],
    "+": [".....", "..X..", "..X..", "XXXXX", "..X..", "..X..", "....."],
    "!": ["..X..", "..X..", "..X..", "..X..", "..X..", ".....", "..X.."],
    "/": [".....", "....X", "...X.", "..X..", ".X...", "X....", "....."],
}

# Original sprites, drawn for this profile.
BUG_A = [".X.....X.", "..X...X..", "...XXX...", "X.XXXXX.X", ".XXX.XXX.", "XXXX.XXXX", ".XXX.XXX.", "X.XXXXX.X", "...X.X..."]
BUG_B = [".X.....X.", "..X...X..", "...XXX...", "..XXXXX..", "XXXX.XXXX", ".XXX.XXX.", "XXXX.XXXX", "..XXXXX..", ".X.....X."]
SHIP = ["....X....", "...XXX...", "...X.X...", "..XXXXX..", ".XX.X.XX.", "XXXXXXXXX", "X.X...X.X"]
BURST = ["X...X...X", ".X..X..X.", "..X...X..", ".........", "XX..X..XX", ".........", "..X...X..", ".X..X..X.", "X...X...X"]
CROWN = ["X..X..X", "XX.X.XX", "XXXXXXX", ".XXXXX."]
TROPHY = ["XXXXXXXXX", "X.XXXXX.X", "X.XXXXX.X", ".XXXXXXX.", "..XXXXX..", "...XXX...", "....X....", "...XXX...", "..XXXXX.."]
CHECK = ["......X", ".....XX", "X...XX.", "XX.XX..", ".XXX...", "..X...."]
BOT_BODY = ["...XX...", "...XX...", ".XXXXXX.", ".X.XX.X.", ".XXXXXX.", "..XXXX..", "XXXXXXXX", "X.XXXX.X", "..XXXX.."]
BOT_LEGS_A = ["..X..X..", "..X..X.."]
BOT_LEGS_B = ["..X..X..", ".X....X."]


def n(v):
    v = round(v, 2)
    return f"{v:g}"


def rows_path(rows, x, y, s):
    """Pixel art -> one path. Horizontal runs merge into single rectangles."""
    d = []
    for r, row in enumerate(rows):
        c = 0
        while c < len(row):
            if row[c] == ".":
                c += 1
                continue
            start = c
            while c < len(row) and row[c] != ".":
                c += 1
            w = (c - start) * s
            d.append(f"M{n(x + start * s)} {n(y + r * s)}h{n(w)}v{n(s)}h{n(-w)}z")
    return "".join(d)


def glyph(ch):
    return FONT[ch] if ch in FONT else FONT[ch.upper()]


def pixel_path(text, x, y, s, track=1):
    d, cx = [], x
    for ch in text:
        g = glyph(ch)
        d.append(rows_path(g, cx, y, s))
        cx += (len(g[0]) + track) * s
    return "".join(d)


def pixel_width(text, s, track=1):
    return sum(len(glyph(ch)[0]) + track for ch in text) * s - track * s


# ---------------------------------------------------------------- animation

class Sheet:
    """Collects one @keyframes rule per animated element.

    Frames are given in seconds against the element's loop length, so a whole
    scene can be choreographed on one clock and stay in sync.
    """

    def __init__(self, prefix):
        self.prefix, self.rules, self.i = prefix, [], 0

    def anim(self, T, frames, timing="linear", extra=""):
        name = f"{self.prefix}{self.i}"
        self.i += 1
        body = "".join(f"{max(0.0, min(100.0, s / T * 100)):.3f}%{{{css}}}" for s, css in frames)
        self.rules.append(f"@keyframes {name}{{{body}}}")
        return f"animation:{name} {n(T)}s {timing} infinite{extra}"

    def window(self, T, on, off=None, fade_in=0.0, fade_out=0.25):
        """Opacity 0 -> 1 at `on`, back to 0 at `off` (default: end of loop)."""
        off = T - 0.45 if off is None else off
        frames = [(0, "opacity:0")]
        if on > 0:
            frames.append((max(0.0, on - 0.001), "opacity:0"))
        frames += [(on + fade_in, "opacity:1"), (off, "opacity:1"), (min(T, off + fade_out), "opacity:0"), (T, "opacity:0")]
        return self.anim(T, frames)

    def css(self):
        return "".join(self.rules)


REDUCE = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"


def tok(theme):
    t = instrument_tokens(theme)
    dark = t["name"] == "dark"
    t["term"] = "#06141A" if dark else "#FFFFFF"
    t["scan"] = "#FFFFFF" if dark else "#0B2A33"
    t["scan_o"] = ".035" if dark else ".03"
    return t


def svg_open(W, H, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
            f'role="img" aria-label="{escape(label)}">')


def base_style(extra=""):
    return (f".display{{font-family:{SANS}}}.utility{{font-family:{MONO}}}"
            ".fb{transform-box:fill-box}" + extra)


# ---------------------------------------------------------------- terminal

def terminal(theme):
    t = tok(theme)
    sh = Sheet("tm")
    W, H = 1200, 398
    fs, cw, lh = 16, 9.6, 26
    X0, Y0 = 28, 70
    T = 18.0
    HOLD = T - 0.9

    rows = [
        ("cmd", "~", "whoami"),
        ("out", 0.0, [("aaryan patel", "alloy", True), ("  —  builds systems, then tries to break them", "quiet", False)]),
        ("cmd", "~", "cd raft-mvcc && make test"),
        ("out", 0.7, [("  ▸ seeded faults · serializable MVCC · linearizability checker", "quiet", False)]),
        ("out", 0.6, [("  ✓ 598 assertions passed", "pass", True), ("  ·  five-node failover in 11 ticks", "quiet", False)]),
        ("cmd", "~/raft-mvcc", "./faultline --isolate leader"),
        ("out", 0.6, [("  ⚠ two leaders, two terms", "fault", True), ("  —  the old one is stranded in a minority", "quiet", False)]),
        ("out", 0.9, [("  ↺ heal → conflicting history repaired → invariant re-checked", "signal", False)]),
        ("out", 0.5, [("  ✓ one leader", "pass", True), ("  ·  receipt emitted", "quiet", False)]),
        ("cmd", "~/raft-mvcc", "cat ~/now.txt"),
        ("out", 0.0, [("UGA CS · Dec 2026 · MP Equipment · open to systems + ML infra roles", "alloy", False)]),
        ("end", "~/raft-mvcc"),
    ]

    for row in rows:  # every session line has to fit the left pane
        text = (f"aaryan@lab:{row[1]}$ " + row[2]) if row[0] == "cmd" else "".join(x[0] for x in row[2]) if row[0] == "out" else ""
        assert X0 + len(text) * cw < 704, text

    def prompt(cwd, y):
        p = f"aaryan@lab:{cwd}$ "
        spans = (f'<tspan fill="{t["pass"]}" font-weight="700">aaryan@lab</tspan><tspan fill="{t["quiet"]}">:</tspan>'
                 f'<tspan fill="{t["signal"]}">{escape(cwd)}</tspan><tspan fill="{t["quiet"]}">$ </tspan>')
        return len(p), (f'<text x="{X0}" y="{y}" class="utility" font-size="{fs}" textLength="{n(len(p) * cw)}" '
                        f'lengthAdjust="spacing" xml:space="preserve">{spans}</text>')

    body, clock = [], 0.5
    for i, row in enumerate(rows):
        y = Y0 + i * lh
        if row[0] == "cmd":
            _, cwd, cmd = row
            appear, ts = clock, clock + 0.5
            te = ts + len(cmd) * 0.055
            clock = te + 0.3
            plen, ptext = prompt(cwd, y)
            cx, L = X0 + plen * cw, len(cmd) * cw
            cover = sh.anim(T, [(0, "transform:scaleX(1)"),
                                (ts, f"transform:scaleX(1);animation-timing-function:steps({len(cmd)},end)"),
                                (te, "transform:scaleX(0)"), (T, "transform:scaleX(0)")])
            cursor = sh.anim(T, [(0, "opacity:1;transform:translateX(0)"),
                                 (ts, f"opacity:1;transform:translateX(0);animation-timing-function:steps({len(cmd)},end)"),
                                 (te, f"opacity:1;transform:translateX({n(L)}px)"),
                                 (te + 0.001, f"opacity:0;transform:translateX({n(L)}px)"),
                                 (T, f"opacity:0;transform:translateX({n(L)}px)")])
            body.append(
                f'<g style="{sh.window(T, appear, HOLD)}">{ptext}'
                f'<text x="{n(cx)}" y="{y}" class="utility" font-size="{fs}" fill="{t["alloy"]}" textLength="{n(L)}" '
                f'lengthAdjust="spacing" xml:space="preserve">{escape(cmd)}</text>'
                f'<rect x="{n(cx - 1)}" y="{y - 16}" width="{n(L + 3)}" height="22" fill="{t["term"]}" class="cv fb" style="{cover}"/>'
                f'<rect x="{n(cx)}" y="{y - 15}" width="{n(cw)}" height="19" fill="{t["signal"]}" opacity=".85" class="tc" style="{cursor}"/></g>'
            )
        elif row[0] == "out":
            _, pause, spans = row
            clock += pause
            appear = clock
            clock += 0.14
            chars = sum(len(s[0]) for s in spans)
            ts_ = "".join(f'<tspan fill="{t[c]}"{BOLD if b else ""}>{escape(s)}</tspan>' for s, c, b in spans)
            body.append(
                f'<g style="{sh.window(T, appear, HOLD)}"><text x="{X0}" y="{y}" class="utility" font-size="{fs}" '
                f'textLength="{n(chars * cw)}" lengthAdjust="spacing" xml:space="preserve">{ts_}</text></g>'
            )
        else:
            _, cwd = row
            appear = clock + 0.2
            plen, ptext = prompt(cwd, y)
            body.append(
                f'<g style="{sh.window(T, appear, HOLD)}">{ptext}'
                f'<rect x="{n(X0 + plen * cw)}" y="{y - 15}" width="{n(cw)}" height="19" fill="{t["signal"]}" class="blink"/></g>'
            )

    # Right pane: a lab monitor that never stops moving.
    RX, BX, BW = 738, 796, 300
    procs = [("101", "raft-mvcc", "partitioning", "fault"), ("102", "vllm-lite", "batching", "trigger"),
             ("103", "track-fusion", "tracking", "signal"), ("104", "tensorforge", "fusing kernels", "violet"),
             ("105", "counterexample", "publishing losses", "pass")]

    def bar(y, color, frames, rest):
        a = sh.anim(7.0 if color == "signal" else 9.0, frames, "ease-in-out")
        cells = "".join(f"M{BX + 2 + k * 12} {y - 8}v8" for k in range(1, BW // 12))
        return (f'<rect x="{BX}" y="{y - 10}" width="{BW}" height="12" rx="2" fill="none" stroke="{t["hairline"]}"/>'
                f'<rect x="{BX + 2}" y="{y - 8}" width="{BW - 4}" height="8" rx="1" fill="{t[color]}" opacity=".85" '
                f'class="fb" style="transform-origin:0 50%;transform:scaleX({rest});{a}"/>'
                f'<path d="{cells}" stroke="{t["term"]}" stroke-width="2"/>')

    def scale_frames(vals, T_):
        step = T_ / (len(vals) - 1)
        return [(k * step, f"transform:scaleX({v})") for k, v in enumerate(vals)]

    P = 300
    pts = []
    for k in range(0, 2 * P + 1, 5):
        u = 2 * math.pi * k / P
        v = 0.5 * math.sin(u) + 0.3 * math.sin(3 * u + 1.1) + 0.2 * math.sin(7 * u + 2.3)
        pts.append(f"{n(BX + k)},{n(143 - v * 8)}")
    spark = sh.anim(5.0, [(0, "transform:translateX(0)"), (5.0, f"transform:translateX(-{P}px)")])

    mon = [
        f'<text x="{RX}" y="{Y0}" class="utility" font-size="12"><tspan fill="{t["signal"]}" font-weight="700">lab-monitor</tspan>'
        f'<tspan fill="{t["quiet"]}">  ·  5 procs  ·  nothing here is idle</tspan></text>',
        f'<text x="{RX}" y="98" class="utility" font-size="11" fill="{t["quiet"]}">CPU</text>',
        bar(98, "signal", scale_frames([.38, .71, .52, .88, .45, .66, .38], 7.0), ".62"),
        f'<text x="{RX}" y="122" class="utility" font-size="11" fill="{t["quiet"]}">MEM</text>',
        bar(122, "violet", scale_frames([.55, .6, .72, .58, .81, .64, .55], 9.0), ".64"),
        f'<text x="{RX}" y="147" class="utility" font-size="11" fill="{t["quiet"]}">OPS</text>',
        f'<g clip-path="url(#tm-{t["name"]}-spark)"><polyline points="{" ".join(pts)}" fill="none" stroke="{t["pass"]}" '
        f'stroke-width="1.6" stroke-linejoin="round" style="{spark}"/></g>',
        f'<text x="{RX}" y="182" class="utility" font-size="10" letter-spacing="1" fill="{t["quiet"]}" xml:space="preserve">PID    PROCESS          STATE</text>',
        f'<text x="{RX}" y="{H - 44}" class="utility" font-size="11" fill="{t["quiet"]}">uptime: since the first failing test</text>',
    ]
    for k, (pid, name, state, color) in enumerate(procs):
        y = 206 + k * 24
        mon.append(
            f'<text x="{RX}" y="{y}" class="utility" font-size="13" fill="{t["quiet"]}">{pid}</text>'
            f'<text x="{RX + 50}" y="{y}" class="utility" font-size="13" fill="{t["alloy"]}">{name}</text>'
            f'<circle cx="{RX + 203}" cy="{y - 4.5}" r="4.5" fill="{t[color]}" class="dot fb" style="animation-delay:{n(-k * .37)}s"/>'
            f'<text x="{RX + 216}" y="{y}" class="utility" font-size="13" fill="{t[color]}">{state}</text>'
        )

    style = base_style(
        ".cv{transform-origin:100% 50%;transform:scaleX(0)}.tc{opacity:0}"
        ".blink{animation:tmblink 1.05s steps(1) infinite}@keyframes tmblink{50%{opacity:0}}"
        ".dot{transform-origin:center;animation:tmdot 1.6s ease-in-out infinite}"
        "@keyframes tmdot{0%,100%{opacity:.35;transform:scale(.7)}50%{opacity:1;transform:scale(1.15)}}"
        + sh.css() + REDUCE
    )
    nm = t["name"]
    return f"""{svg_open(W, H, "Animated terminal: whoami, make test in raft-mvcc passes 598 assertions, a FAULTLINE leader isolation produces two leaders and heals, then current status. A monitor pane shows five lab processes.")}
  <defs>
    <clipPath id="tm-{nm}-win"><rect width="{W}" height="{H}" rx="12"/></clipPath>
    <clipPath id="tm-{nm}-spark"><rect x="{BX}" y="130" width="{BW}" height="22"/></clipPath>
  </defs>
  <style>{style}</style>
  <g clip-path="url(#tm-{nm}-win)">
    <rect width="{W}" height="{H}" fill="{t['term']}"/>
    <rect width="{W}" height="34" fill="{t['surface2']}"/>
    <path d="M0 34.5H{W}" stroke="{t['hairline']}"/>
    <circle cx="22" cy="17" r="5.5" fill="{t['fault']}"/><circle cx="42" cy="17" r="5.5" fill="{t['trigger']}"/><circle cx="62" cy="17" r="5.5" fill="{t['pass']}"/>
    <text x="{W // 2}" y="21" text-anchor="middle" class="utility" font-size="11" letter-spacing=".5" fill="{t['quiet']}">aaryan@lab — tmux — 2 panes</text>
    <path d="M714.5 34V{H - 26}" stroke="{t['hairline']}"/>
    {''.join(body)}
    {''.join(mon)}
    <rect y="{H - 26}" width="{W}" height="26" fill="{t['surface2']}"/>
    <rect y="{H - 26}" width="58" height="26" fill="{t['pass']}"/>
    <text x="29" y="{H - 9}" text-anchor="middle" class="utility" font-size="11" font-weight="700" fill="{t['term']}">[lab]</text>
    <text x="70" y="{H - 9}" class="utility" font-size="11" fill="{t['alloy']}" xml:space="preserve">0:shell*  1:monitor</text>
    <text x="{W - 14}" y="{H - 9}" text-anchor="end" class="utility" font-size="11" fill="{t['quiet']}">build ▸ break ▸ measure ▸ publish</text>
  </g>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="11.5" fill="none" stroke="{t['hairline']}"/>
</svg>
"""


# ---------------------------------------------------------------- dividers

def edge_fade(nm):
    return (f'<linearGradient id="{nm}-fade" x1="0" x2="1"><stop stop-color="#fff" stop-opacity="0"/>'
            f'<stop offset=".12" stop-color="#fff"/><stop offset=".88" stop-color="#fff"/>'
            f'<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            f'<mask id="{nm}-mask"><rect width="1200" height="48" fill="url(#{nm}-fade)"/></mask>'
            f'<filter id="{nm}-glow" x="-20%" y="-200%" width="140%" height="500%"><feGaussianBlur stdDeviation="2.5"/></filter>')


def divider_heartbeat(theme):
    t, nm = tok(theme), f"dva-{theme['name']}"
    sh = Sheet("dva")
    W, H, mid = 1200, 48, 24
    pts, beats = [(0, mid)], list(range(100, 1200, 200))
    for bx in beats:
        pts += [(bx - 16, mid), (bx - 9, mid - 4), (bx - 4, mid), (bx - 1, mid - 16), (bx + 3, mid + 12),
                (bx + 7, mid), (bx + 16, mid - 4), (bx + 26, mid)]
    pts.append((W, mid))
    seglen = [math.dist(pts[k], pts[k + 1]) for k in range(len(pts) - 1)]
    L, seg, D, T = sum(seglen), 150, 3.6, 4.4
    poly = " ".join(f"{n(x)},{n(y)}" for x, y in pts)
    run = sh.anim(T, [(0, f"stroke-dashoffset:{seg}"), (D, f"stroke-dashoffset:{n(-L)}"), (T, f"stroke-dashoffset:{n(-L)}")])
    # arc length to the fourth beat, so the fault flash fires as the pulse arrives
    target = beats[3]
    acc = 0.0
    for k in range(len(pts) - 1):
        if pts[k][0] >= target - 1:
            break
        acc += seglen[k]
    hit = acc / (L + seg) * D + 0.1
    flash = sh.window(T, hit, hit + 0.18, 0.0, 0.5)
    bx = target
    spike = f"{bx - 6},{mid} {bx - 2},{mid - 21} {bx + 2},{mid + 17} {bx + 5},{mid - 9} {bx + 9},{mid}"
    return f"""{svg_open(W, H, "Divider: a heartbeat trace with a pulse travelling across it")}
  <defs>{edge_fade(nm)}</defs>
  <style>{base_style(".fl{opacity:0}" + sh.css() + REDUCE)}</style>
  <g mask="url(#{nm}-mask)">
    <polyline points="{poly}" fill="none" stroke="{t['hairline']}" stroke-width="1.5" stroke-linejoin="round"/>
    <polyline points="{poly}" fill="none" stroke="{t['signal']}" stroke-width="4" stroke-linejoin="round" stroke-dasharray="{seg} {n(L + seg)}" filter="url(#{nm}-glow)" opacity=".7" style="stroke-dashoffset:{seg};{run}"/>
    <polyline points="{poly}" fill="none" stroke="{t['signal']}" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round" stroke-dasharray="{seg} {n(L + seg)}" style="stroke-dashoffset:{seg};{run}"/>
    <polyline points="{spike}" fill="none" stroke="{t['fault']}" stroke-width="2" stroke-linejoin="round" class="fl" style="{flash}"/>
  </g>
</svg>
"""


def divider_logic(theme):
    t, nm = tok(theme), f"dvb-{theme['name']}"
    sh = Sheet("dvb")
    W, H, P = 1200, 48, 600
    bits = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0]

    def square(levels, step, y, amp):
        d, x, prev = [f"M0 {n(y - amp if levels[0] else y + amp)}"], 0, levels[0]
        for k in range(len(levels) * 3):
            lv = levels[k % len(levels)]
            if lv != prev:
                d.append(f"H{n(x)}V{n(y - amp if lv else y + amp)}")
                prev = lv
            x += step
        d.append(f"H{n(x)}")
        return "".join(d)

    clock = square([1, 0] * (P // 24), 12, 10, 3.5)
    data = square(bits, 24, 24, 4)
    glitch_lv = [0] * 50
    for k in (13, 14, 37):
        glitch_lv[k] = 1
    glitch = square(glitch_lv, 12, 38, 3.5)
    scroll = sh.anim(6.0, [(0, "transform:translateX(0)"), (6.0, f"transform:translateX(-{P}px)")])
    return f"""{svg_open(W, H, "Divider: a scrolling logic-analyzer capture with clock, data, and fault lanes")}
  <defs>{edge_fade(nm)}</defs>
  <style>{base_style(sh.css() + REDUCE)}</style>
  <g mask="url(#{nm}-mask)">
    <g style="{scroll}">
      <path d="{clock}" fill="none" stroke="{t['quiet']}" stroke-width="1.3" opacity=".8"/>
      <path d="{data}" fill="none" stroke="{t['signal']}" stroke-width="1.8"/>
      <path d="{glitch}" fill="none" stroke="{t['trigger']}" stroke-width="1.5"/>
    </g>
    <path d="M600 2V46" stroke="{t['violet']}" stroke-dasharray="2 3" opacity=".9"/>
    <rect x="593" y="0" width="14" height="10" rx="2" fill="{t['violet']}"/>
    <text x="600" y="8" text-anchor="middle" class="utility" font-size="7.5" font-weight="700" fill="{t['term']}">T</text>
  </g>
</svg>
"""


def divider_bus(theme):
    t, nm = tok(theme), f"dvc-{theme['name']}"
    sh = Sheet("dvc")
    W, H, y, T = 1200, 48, 24, 6.8
    nodes = [100, 350, 600, 850, 1100]

    def packet(color, x0, x1, t0, t1, drop=False):
        frames = [(0, f"opacity:0;transform:translate({x0 - 100}px,0)")]
        if t0 > 0:
            frames.append((t0 - 0.001, f"opacity:0;transform:translate({x0 - 100}px,0)"))
        frames.append((t0, f"opacity:1;transform:translate({x0 - 100}px,0)"))
        frames.append((t1, f"opacity:1;transform:translate({x1 - 100}px,0)"))
        if drop:
            frames += [(t1 + 0.12, f"opacity:1;transform:translate({x1 - 100}px,0) rotate(0deg)"),
                       (t1 + 0.7, f"opacity:0;transform:translate({x1 - 92}px,16px) rotate(70deg)")]
        else:
            frames.append((t1 + 0.12, f"opacity:0;transform:translate({x1 - 100}px,0)"))
        frames.append((T, "opacity:0"))
        a = sh.anim(T, frames)
        return f'<g class="pk" style="{a}"><rect x="92" y="{y - 4}" width="16" height="8" rx="2.5" fill="{t[color]}"/></g>'

    drop_at = 2.5
    x_mark = sh.window(T, drop_at, drop_at + 0.9, 0.0, 0.3)
    packets = (packet("signal", 100, 1100, 0.2, 3.2) + packet("fault", 100, 600, 1.0, drop_at, drop=True)
               + packet("pass", 100, 1100, 3.0, 6.0))  # built before the stylesheet is serialized
    return f"""{svg_open(W, H, "Divider: packets cross a five-node bus; one is dropped and its retry gets through")}
  <defs>{edge_fade(nm)}</defs>
  <style>{base_style(".pk,.xm{opacity:0}.pk{transform-box:fill-box;transform-origin:center}" + ".nd{transform-origin:center;animation:dvcnd 2.4s ease-in-out infinite}@keyframes dvcnd{0%,100%{opacity:.55}50%{opacity:1}}" + sh.css() + REDUCE)}</style>
  <g mask="url(#{nm}-mask)">
    <path d="M30 {y}H1170" stroke="{t['hairline']}" stroke-width="2"/>
    {packets}
    {''.join(f'<circle cx="{x}" cy="{y}" r="6" fill="{t["term"]}" stroke="{t["signal"]}" stroke-width="1.5" class="nd fb" style="animation-delay:{n(-k * .4)}s"/>' for k, x in enumerate(nodes))}
    <text x="600" y="{y - 11}" text-anchor="middle" class="utility xm" font-size="9" font-weight="700" fill="{t['fault']}" style="{x_mark}">× DROP → RETRY</text>
  </g>
</svg>
"""


# ---------------------------------------------------------------- high scores

def highscores(theme):
    t = tok(theme)
    nm = f"hs-{t['name']}"
    sh = Sheet("hs")
    W, H, T = 1200, 344, 9.0

    title_colors = [t["trigger"], t["fault"], t["violet"], t["signal"], t["pass"]]
    seg = 4.0 / len(title_colors)
    tframes = []
    for k, c in enumerate(title_colors):
        tframes += [(k * seg, f"fill:{c}"), ((k + 1) * seg - 0.001, f"fill:{c}")]
    title_anim = sh.anim(4.0, tframes)

    scores = [("1ST", "598", "ASSERTIONS", "RAFT-MVCC", "trigger"), ("2ND", "138×", "WARM READ", "EDGAR-MCP", "signal"),
              ("3RD", "2.9×", "THROUGHPUT", "VLLM-LITE", "pass"), ("4TH", "47%", "LESS ERROR", "TRACK-FUSION", "violet"),
              ("5TH", "68", "TESTS", "VIDUR", "alloy")]
    s = 3
    rows = []
    for k, (rank, score, unit, system, color) in enumerate(scores):
        y = 132 + k * 34
        score_right = 48 + pixel_width("1ST", s) + 26 + pixel_width("138×", s)
        d = (pixel_path(rank, 48, y, s) + pixel_path(score, score_right - pixel_width(score, s), y, s)
             + pixel_path(unit, 236, y, s) + pixel_path(system, 446, y, s))
        a0 = 0.35 + k * 0.22
        enter = sh.anim(T, [(0, "opacity:0;transform:translateX(-30px)"), (a0 - 0.001, "opacity:0;transform:translateX(-30px)"),
                            (a0, "opacity:1;transform:translateX(-30px);animation-timing-function:steps(3,end)"),
                            (a0 + 0.3, "opacity:1;transform:translateX(0)"), (T - 0.4, "opacity:1;transform:translateX(0)"),
                            (T - 0.15, "opacity:0;transform:translateX(0)"), (T, "opacity:0")])
        rows.append(f'<g style="{enter}"><path d="{d}" fill="{t[color]}"/></g>')
    arrow = pixel_path("▶", 26, 132, s)

    # playfield
    PX0, PY0, PX1, PY1 = 700, 30, 1170, 300
    stars = []
    seed = 7
    for k in range(26):
        seed = (seed * 1103515245 + 12345) % 2 ** 31
        sx = PX0 + 14 + seed % (PX1 - PX0 - 28)
        seed = (seed * 1103515245 + 12345) % 2 ** 31
        sy = PY0 + 12 + seed % (PY1 - PY0 - 60)
        stars.append(f'<rect x="{sx}" y="{sy}" width="2" height="2" fill="{t["quiet"]}" class="tw" style="animation-delay:{n(-(k * 0.53) % 3)}s"/>')

    bs = 4
    bugs_x = [790, 916, 1042]
    labels = ["SPLIT BRAIN", "STALE READ", "LOST WRITE"]
    by = 86
    ship_base, ship_y = 740, 248
    parts = []
    for k, bx in enumerate(bugs_x):
        move0 = 0.2 + k * 2.0
        fire = move0 + 0.8
        boom = fire + 0.18
        cx = bx + 18
        alive = sh.anim(T, [(0, "opacity:1"), (boom - 0.001, "opacity:1"), (boom, "opacity:0"), (8.3, "opacity:0"),
                            (8.32, "opacity:1"), (8.45, "opacity:0"), (8.58, "opacity:1"), (8.71, "opacity:0"), (8.84, "opacity:1"), (T, "opacity:1")])
        laser = sh.anim(T, [(0, "opacity:0;transform:scaleY(0)"), (fire - 0.001, "opacity:0;transform:scaleY(0)"),
                            (fire, "opacity:1;transform:scaleY(.1)"), (fire + 0.12, "opacity:1;transform:scaleY(1)"),
                            (fire + 0.3, "opacity:0;transform:scaleY(1)"), (T, "opacity:0")])
        burst = sh.anim(T, [(0, "opacity:0;transform:scale(.6)"), (boom - 0.001, "opacity:0;transform:scale(.6)"),
                            (boom, "opacity:1;transform:scale(.6)"), (boom + 0.35, "opacity:0;transform:scale(1.35)"), (T, "opacity:0")])
        plus = sh.anim(T, [(0, "opacity:0;transform:translateY(0)"), (boom - 0.001, "opacity:0;transform:translateY(0)"),
                           (boom + 0.05, "opacity:1;transform:translateY(0)"), (boom + 1.1, "opacity:0;transform:translateY(-12px)"), (T, "opacity:0")])
        parts.append(
            f'<g style="{alive}"><g class="bob"><path d="{rows_path(BUG_A, bx, by, bs)}" fill="{t["fault"]}" class="fa"/>'
            f'<path d="{rows_path(BUG_B, bx, by, bs)}" fill="{t["fault"]}" class="fbb"/></g>'
            f'<text x="{cx}" y="{by + 52}" text-anchor="middle" class="utility" font-size="9" letter-spacing="1" fill="{t["quiet"]}">{labels[k]}</text></g>'
            f'<rect x="{cx - 2}" y="{by + 40}" width="4" height="{ship_y - by - 40}" fill="{t["signal"]}" class="lz fb" filter="url(#{nm}-glow)" style="{laser}"/>'
            f'<path d="{rows_path(BURST, bx, by, bs)}" fill="{t["trigger"]}" class="bz fb" style="{burst}"/>'
            f'<text x="{cx}" y="{by - 8}" text-anchor="middle" class="utility pl" font-size="12" font-weight="700" fill="{t["pass"]}" style="{plus}">+1 TEST</text>'
        )
    # ship choreography: glide under each bug, fire, move on, come home
    sf = [(0, "transform:translateX(0)")]
    for k, bx in enumerate(bugs_x):
        m0 = 0.2 + k * 2.0
        sf += [(m0, f"transform:translateX({sf[-1][1].split('(')[1][:-1]})"), (m0 + 0.75, f"transform:translateX({bx - ship_base}px)")]
    sf += [(7.0, f"transform:translateX({bugs_x[-1] - ship_base}px)"), (8.0, "transform:translateX(0px)"), (T, "transform:translateX(0px)")]
    ship_anim = sh.anim(T, sf, "linear")
    flame = sh.anim(0.24, [(0, "opacity:1"), (0.119, "opacity:1"), (0.12, "opacity:.3"), (0.24, "opacity:.3")])

    # TESTS counter in the corner: 0 -> 3
    cnt = []
    for k in range(4):
        on = 0 if k == 0 else 0.2 + (k - 1) * 2.0 + 0.98
        off = (0.2 + k * 2.0 + 0.98) if k < 3 else T
        style = sh.anim(T, [(0, f"opacity:{1 if k == 0 else 0}"), (max(0.0, on - 0.001), f"opacity:{1 if k == 0 else 0}"),
                            (on, "opacity:1"), (off - 0.001, "opacity:1"), (off, "opacity:0" if k < 3 else "opacity:1"), (T, f"opacity:{0 if k < 3 else 1}")])
        default = "1" if k == 0 else "0"  # motion off: the wave has not started
        cnt.append(f'<path d="{pixel_path(str(k), 1148, 44, 2)}" fill="{t["pass"]}" style="opacity:{default};{style}"/>')
    clear_x = (PX0 + PX1) / 2 - pixel_width("WAVE CLEAR", 3) / 2
    clear = sh.anim(T, [(0, "opacity:0"), (6.0, "opacity:0"), (6.01, "opacity:1"), (6.4, "opacity:1"), (6.41, "opacity:0"),
                        (6.6, "opacity:0"), (6.61, "opacity:1"), (7.0, "opacity:1"), (7.01, "opacity:0"), (7.2, "opacity:0"),
                        (7.21, "opacity:1"), (7.9, "opacity:1"), (7.91, "opacity:0"), (T, "opacity:0")])

    style = base_style(
        f".tw{{animation:hstw 3s steps(2) infinite}}@keyframes hstw{{50%{{opacity:.15}}}}"
        f".fa{{animation:hsfa .5s steps(1) infinite}}.fbb{{opacity:0;animation:hsfb .5s steps(1) infinite}}"
        f"@keyframes hsfa{{50%{{opacity:0}}}}@keyframes hsfb{{50%{{opacity:1}}}}"
        f".bob{{animation:hsbob 1s steps(2) infinite}}@keyframes hsbob{{50%{{transform:translateY(3px)}}}}"
        f".lz{{opacity:0;transform-origin:50% 100%}}.bz{{opacity:0;transform-origin:center}}.pl,.wc{{opacity:0}}"
        f".blinkp{{animation:hsbl 1.2s steps(1) infinite}}@keyframes hsbl{{50%{{opacity:0}}}}"
        f".roll{{animation:hsroll 7s linear infinite}}@keyframes hsroll{{from{{transform:translateY(-60px)}}to{{transform:translateY({H}px)}}}}"
        + sh.css() + REDUCE + "@media (prefers-reduced-motion: reduce){.roll{display:none}}"
    )
    return f"""{svg_open(W, H, "Arcade high-score screen: 598 assertions, 138x warm read, 2.9x throughput, 47% less error, 68 tests. A ship turns split-brain, stale-read and lost-write bugs into tests.")}
  {instrument_defs(t, nm)}
  <defs><pattern id="{nm}-scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="{t['scan']}" opacity="{t['scan_o']}"/></pattern>
  <linearGradient id="{nm}-roll" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{t['signal']}" stop-opacity="0"/><stop offset=".5" stop-color="{t['signal']}" stop-opacity=".06"/><stop offset="1" stop-color="{t['signal']}" stop-opacity="0"/></linearGradient></defs>
  <style>{style}</style>
  <rect width="{W}" height="{H}" rx="16" fill="url(#{nm}-panel)"/><rect width="{W}" height="{H}" rx="16" fill="url(#{nm}-grid)"/>
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="15" fill="none" stroke="{t['hairline']}"/>
  <path d="{pixel_path("HIGH SCORES", 48, 30, 5)}" style="fill:{t['trigger']};{title_anim}"/>
  <text x="48" y="94" class="utility" font-size="10" letter-spacing="2" fill="{t['quiet']}">NO HIGH SCORE WITHOUT A RECEIPT · EVERY ENTRY IS MEASURED IN ITS REPO</text>
  <text x="48" y="118" class="utility" font-size="9" letter-spacing="2" fill="{t['quiet']}" opacity=".8">RANK</text>
  <text x="{48 + pixel_width('1ST', 3) + 26 + pixel_width('138×', 3)}" y="118" text-anchor="end" class="utility" font-size="9" letter-spacing="2" fill="{t['quiet']}" opacity=".8">SCORE</text>
  <text x="236" y="118" class="utility" font-size="9" letter-spacing="2" fill="{t['quiet']}" opacity=".8">UNIT</text>
  <text x="446" y="118" class="utility" font-size="9" letter-spacing="2" fill="{t['quiet']}" opacity=".8">SYSTEM</text>
  <path d="{arrow}" fill="{t['trigger']}" class="blinkp"/>
  {''.join(rows)}
  <path d="{pixel_path("▶ PRESS START", 48, 310, 3)}" fill="{t['signal']}" class="blinkp"/>
  <text x="{48 + pixel_width('▶ PRESS START', 3) + 20}" y="328" class="utility" font-size="10" letter-spacing="1.5" fill="{t['quiet']}">TWO PLAYABLE GAMES BELOW ↓</text>
  <rect x="{PX0}" y="{PY0}" width="{PX1 - PX0}" height="{PY1 - PY0}" rx="6" fill="{t['backplane']}" fill-opacity=".55" stroke="{t['hairline']}" stroke-dasharray="4 4"/>
  {''.join(stars)}
  <path d="{pixel_path("TESTS", 1080, 44, 2)}" fill="{t['quiet']}"/>
  {''.join(cnt)}
  {''.join(parts)}
  <g style="{ship_anim}"><path d="{rows_path(SHIP, ship_base, ship_y, 4)}" fill="{t['signal']}"/>
    <rect x="{ship_base + 14}" y="{ship_y + 28}" width="8" height="5" fill="{t['trigger']}" style="{flame}"/></g>
  <path d="{pixel_path("WAVE CLEAR", clear_x, 168, 3)}" fill="{t['pass']}" class="wc" style="{clear}"/>
  <path d="{pixel_path("CREDIT MIT", PX1 - pixel_width('CREDIT MIT', 2), 316, 2)}" fill="{t['quiet']}"/>
  <rect width="{W}" height="{H}" rx="16" fill="url(#{nm}-scan)" pointer-events="none"/>
  <rect y="0" width="{W}" height="60" fill="url(#{nm}-roll)" class="roll"/>
</svg>
"""


# ---------------------------------------------------------------- secret level

def secret_level(theme):
    t = tok(theme)
    nm = f"sl-{t['name']}"
    sh = Sheet("sl")
    W, H, T = 1200, 344, 13.0
    CX, CY, R = 330, 206, 104
    pos = {}
    for k in range(5):
        a = math.radians(180 + 72 * k)
        pos[k + 1] = (CX + R * math.cos(a), CY + R * math.sin(a))
    edges = [(a, b) for a in range(1, 6) for b in range(a + 1, 6)]

    def line(a, b):
        (x1, y1), (x2, y2) = pos[a], pos[b]
        return f"M{n(x1)} {n(y1)}L{n(x2)} {n(y2)}"

    P_CUT, P_ELECT, P_TWO, P_HEAL, P_DOWN, P_REPAIR, P_OK, P_TOAST = 1.6, 3.2, 4.0, 6.0, 6.8, 7.6, 8.4, 9.0
    END = T - 0.45

    base = "".join(line(a, b) for a, b in edges)
    n1 = "".join(line(1, b) for b in range(2, 6))
    n4_rest = "".join(line(4, b) for b in (2, 3, 5))
    n4_n1 = line(1, 4)

    hb_n1 = sh.window(T, 0, P_CUT, 0, 0.1)
    cut = sh.window(T, P_CUT, P_HEAL, 0, 0.6)
    hb_n4 = sh.window(T, P_ELECT, END, 0.3)
    hb_n4n1 = sh.window(T, P_REPAIR, END, 0.3)

    crack_pts = [(262, 74), (270, 104), (254, 140), (272, 182), (256, 228), (274, 270), (260, 312), (266, 336)]
    crack = "M" + "L".join(f"{x} {y}" for x, y in crack_pts)
    clen = sum(math.dist(crack_pts[k], crack_pts[k + 1]) for k in range(len(crack_pts) - 1))
    crack_anim = sh.anim(T, [(0, f"opacity:0;stroke-dashoffset:{n(clen)}"), (P_CUT - 0.001, f"opacity:0;stroke-dashoffset:{n(clen)}"),
                             (P_CUT, f"opacity:1;stroke-dashoffset:{n(clen)}"), (P_CUT + 0.3, "opacity:1;stroke-dashoffset:0"),
                             (P_HEAL, "opacity:1;stroke-dashoffset:0"), (P_HEAL + 0.6, "opacity:0;stroke-dashoffset:0"), (T, "opacity:0")])
    flash = sh.window(T, P_CUT, P_CUT + 0.08, 0, 0.35)

    nodes = []
    for k in range(1, 6):
        x, y = pos[k]
        nodes.append(f'<circle cx="{n(x)}" cy="{n(y)}" r="22" fill="{t["surface"]}" stroke="{t["signal"]}" stroke-width="2"/>'
                     f'<text x="{n(x)}" y="{n(y + 4.5)}" text-anchor="middle" class="utility" font-size="13" font-weight="700" fill="{t["alloy"]}">N{k}</text>')
    x1, y1 = pos[1]
    x4, y4 = pos[4]
    n1_bad = sh.window(T, P_CUT, P_DOWN + 0.2, 0, 0.3)
    n1_ok = sh.window(T, P_REPAIR, P_REPAIR + 0.25, 0, 0.6)
    elect = sh.anim(T, [(0, "opacity:0;transform:scale(1)"), (P_ELECT - 0.6, "opacity:0;transform:scale(1)"),
                        (P_ELECT - 0.59, "opacity:.9;transform:scale(1)"), (P_ELECT, "opacity:0;transform:scale(1.9)"), (T, "opacity:0")])

    cw_, ch_ = len(CROWN[0]) * 3, len(CROWN) * 3
    crown1 = sh.anim(T, [(0, "opacity:1;transform:translateY(0) rotate(0deg)"), (P_TWO, "opacity:1;transform:translateY(0) rotate(0deg)"),
                         (P_TWO + 0.2, "opacity:1;transform:translateY(0) rotate(-12deg)"), (P_TWO + 0.4, "opacity:1;transform:translateY(0) rotate(10deg)"),
                         (P_TWO + 0.6, "opacity:1;transform:translateY(0) rotate(0deg)"), (P_DOWN, "opacity:1;transform:translateY(0) rotate(0deg)"),
                         (P_DOWN + 0.8, "opacity:0;transform:translateY(46px) rotate(80deg)"), (T, "opacity:0")])
    crown4 = sh.anim(T, [(0, "opacity:0;transform:translateY(-14px)"), (P_ELECT - 0.001, "opacity:0;transform:translateY(-14px)"),
                         (P_ELECT + 0.35, "opacity:1;transform:translateY(0)"), (END, "opacity:1;transform:translateY(0)"),
                         (END + 0.25, "opacity:0;transform:translateY(0)"), (T, "opacity:0")])

    def crown(x, y, color, term, style, cls):
        return (f'<g class="{cls} fb" style="transform-origin:center;{style}">'
                f'<path d="{rows_path(CROWN, x - cw_ / 2, y - 22 - ch_ - 8, 3)}" fill="{t[color]}"/>'
                f'<text x="{n(x + cw_ / 2 + 4)}" y="{n(y - 32)}" class="utility" font-size="10" font-weight="700" fill="{t[color]}">{term}</text></g>')

    two_w = pixel_width("TWO LEADERS!", 3)
    two = sh.anim(T, [(0, "opacity:0")] + [(P_TWO + k * 0.4 + d, f"opacity:{o}") for k in range(4) for d, o in ((0, 1), (0.25, 1), (0.251, 0), (0.399, 0))] + [(T, "opacity:0")])

    console = [
        (P_CUT, [("> ", "quiet"), ("isolate N1", "alloy")]),
        (P_CUT + 0.6, [("  N1 keeps leading — term 1, alone", "quiet")]),
        (P_ELECT, [("  N2–N5 elect N4 — term 2", "signal")]),
        (P_TWO, [("  ⚠ two leaders, two terms", "fault")]),
        (P_HEAL, [("> ", "quiet"), ("heal", "alloy")]),
        (P_DOWN, [("  N1 sees term 2 → steps down", "quiet")]),
        (P_REPAIR, [("  conflicting entries rolled back", "signal")]),
        (P_OK, [("  ✓ one leader · history repaired", "pass")]),
    ]
    con = []
    for k, (on, spans) in enumerate(console):
        y = 100 + k * 24
        ts_ = "".join(f'<tspan fill="{t[c]}"{BOLD if c in ("alloy", "fault", "pass") else ""}>{escape(s)}</tspan>' for s, c in spans)
        con.append(f'<text x="640" y="{y}" class="utility" font-size="13" xml:space="preserve" style="{sh.window(T, on, END)}">{ts_}</text>')

    toast = sh.anim(T, [(0, "opacity:0;transform:translateY(24px)"), (P_TOAST - 0.001, "opacity:0;transform:translateY(24px)"),
                        (P_TOAST, "opacity:1;transform:translateY(24px);animation-timing-function:steps(4,end)"),
                        (P_TOAST + 0.4, "opacity:1;transform:translateY(0)"), (END, "opacity:1;transform:translateY(0)"),
                        (END + 0.25, "opacity:0;transform:translateY(0)"), (T, "opacity:0")])
    shine = sh.anim(T, [(0, "transform:translateX(-80px)"), (P_TOAST + 0.5, "transform:translateX(-80px)"),
                        (P_TOAST + 1.4, "transform:translateX(560px)"), (T, "transform:translateX(560px)")])

    style = base_style(
        ".hb{stroke-dasharray:5 11;animation:slhb 1.2s linear infinite}@keyframes slhb{to{stroke-dashoffset:-32}}"
        ".hide{opacity:0}.cr1{opacity:0}"
        + sh.css() + REDUCE
    )
    return f"""{svg_open(W, H, "Secret level: isolating N1 leaves two leaders in two terms; healing makes N1 step down and repairs history; achievement unlocked.")}
  {instrument_defs(t, nm)}
  <defs><clipPath id="{nm}-toast"><rect x="640" y="276" width="530" height="54" rx="8"/></clipPath></defs>
  <style>{style}</style>
  <rect width="{W}" height="{H}" rx="16" fill="url(#{nm}-panel)"/><rect width="{W}" height="{H}" rx="16" fill="url(#{nm}-grid)"/>
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="15" fill="none" stroke="{t['hairline']}"/>
  <text x="24" y="32" class="utility" font-size="10" letter-spacing="2" fill="{t['trigger']}">SECRET LEVEL 0x1F // YOU FOUND THE CODE. NOW BREAK SOMETHING.</text>
  <rect width="{W}" height="{H}" rx="16" fill="{t['fault']}" fill-opacity=".14" class="hide" style="{flash}"/>
  <path d="{base}" stroke="{t['hairline']}" stroke-width="1.5"/>
  <path d="{n1}" stroke="{t['signal']}" stroke-width="2" class="hb hide" style="{hb_n1}"/>
  <path d="{n1}" stroke="{t['fault']}" stroke-width="2" stroke-dasharray="3 5" class="hide" style="{cut}"/>
  <path d="{n4_rest}" stroke="{t['signal']}" stroke-width="2" class="hb" style="{hb_n4}"/>
  <path d="{n4_n1}" stroke="{t['signal']}" stroke-width="2" class="hb" style="{hb_n4n1}"/>
  <path d="{crack}" fill="none" stroke="{t['trigger']}" stroke-width="7" opacity=".35" filter="url(#{nm}-glow)" stroke-dasharray="{n(clen)}" class="hide" style="{crack_anim}"/>
  <path d="{crack}" fill="none" stroke="{t['trigger']}" stroke-width="2.5" stroke-linejoin="bevel" stroke-dasharray="{n(clen)}" class="hide" style="{crack_anim}"/>
  {''.join(nodes)}
  <circle cx="{n(x1)}" cy="{n(y1)}" r="22" fill="none" stroke="{t['fault']}" stroke-width="3" class="hide" style="{n1_bad}"/>
  <circle cx="{n(x1)}" cy="{n(y1)}" r="22" fill="none" stroke="{t['pass']}" stroke-width="3" class="hide" style="{n1_ok}"/>
  <circle cx="{n(x4)}" cy="{n(y4)}" r="22" fill="none" stroke="{t['pass']}" stroke-width="2" class="hide fb" style="transform-origin:center;{elect}"/>
  {crown(x1, y1, "fault", "T1", crown1, "cr1")}
  {crown(x4, y4, "trigger", "T2", crown4, "cr4")}
  <path d="{pixel_path("TWO LEADERS!", CX - two_w / 2, 44, 3)}" fill="{t['fault']}" class="hide" style="{two}"/>
  {''.join(con)}
  <g style="{toast}">
    <rect x="640" y="276" width="530" height="54" rx="8" fill="{t['surface']}" stroke="{t['trigger']}" stroke-width="1.5"/>
    <path d="{rows_path(TROPHY, 656, 285, 4)}" fill="{t['trigger']}"/>
    <path d="{pixel_path("ACHIEVEMENT UNLOCKED", 708, 288, 2)}" fill="{t['trigger']}"/>
    <text x="708" y="320" class="utility" font-size="12" fill="{t['alloy']}">Partitioned a README <tspan fill="{t['quiet']}">·  +50 chaos  ·  0 data lost</tspan></text>
    <g clip-path="url(#{nm}-toast)"><rect x="640" y="276" width="40" height="54" fill="{t['scan']}" opacity=".12" transform="skewX(-20)" style="{shine}"/></g>
  </g>
</svg>
"""


# ---------------------------------------------------------------- footer patrol

def patrol(theme):
    t = tok(theme)
    sh = Sheet("pt")
    W, H, T = 1200, 182, 14.0
    G = 150  # ground line
    title = "THANKS FOR PLAYING"
    tw = pixel_width(title, 4)
    bugs = [300, 520, 740, 960]
    labels = ["SPLIT BRAIN", "STALE READ", "LOST WRITE", "OFF-BY-ONE"]
    rest_x = 1088  # where the robot stands when motion is off
    speed, pause = 150.0, 0.7

    # robot itinerary
    timeline, x, clock = [(0.0, -60.0)], -60.0, 0.0
    zaps = []
    for bx in bugs:
        stop = bx - 70
        clock += (stop - x) / speed
        timeline.append((clock, stop))
        zaps.append(clock)
        clock += pause
        timeline.append((clock, stop))
        x = stop
    clock += (1260 - x) / speed
    timeline.append((clock, 1260))
    walk_end = clock
    frames = [(s, f"transform:translateX({n(px - rest_x)}px)") for s, px in timeline] + [(T, f"transform:translateX({n(1260 - rest_x)}px)")]
    robot_anim = sh.anim(T, frames)

    respawn = walk_end + 0.6
    parts = []
    for k, (bx, zt) in enumerate(zip(bugs, zaps)):
        hit = zt + 0.45
        bug_alive = sh.anim(T, [(0, "opacity:1"), (hit, "opacity:1"), (hit + 0.001, "opacity:0"), (respawn, "opacity:0"), (respawn + 0.5, "opacity:1"), (T, "opacity:1")])
        fixed = sh.anim(T, [(0, "opacity:0"), (hit, "opacity:0"), (hit + 0.001, "opacity:1"), (respawn, "opacity:1"), (respawn + 0.5, "opacity:0"), (T, "opacity:0")])
        zap = sh.anim(T, [(0, "opacity:0"), (zt + 0.1, "opacity:0"), (zt + 0.101, "opacity:1"), (zt + 0.2, "opacity:1"), (zt + 0.201, "opacity:.2"),
                          (zt + 0.27, "opacity:.2"), (zt + 0.271, "opacity:1"), (hit, "opacity:1"), (hit + 0.001, "opacity:0"), (T, "opacity:0")])
        boom = sh.anim(T, [(0, "opacity:0;transform:scale(.5)"), (hit, "opacity:0;transform:scale(.5)"), (hit + 0.001, "opacity:1;transform:scale(.5)"),
                           (hit + 0.35, "opacity:0;transform:scale(1.3)"), (T, "opacity:0")])
        by = G - 27
        x0 = bx - 70 + 32  # robot's right edge when stopped
        zig = f"M{x0} 128L{x0 + 9} 122L{x0 + 16} 132L{x0 + 25} 124L{x0 + 32} 133L{bx - 2} 128"
        lx = bx + 13.5
        parts.append(
            f'<g style="opacity:0;{bug_alive}"><g class="bob"><path d="{rows_path(BUG_A, bx, by, 3)}" fill="{t["fault"]}" class="fa"/>'
            f'<path d="{rows_path(BUG_B, bx, by, 3)}" fill="{t["fault"]}" class="fbb"/></g>'
            f'<text x="{n(lx)}" y="{G + 22}" text-anchor="middle" class="utility" font-size="9.5" letter-spacing="1" fill="{t["fault"]}">{labels[k]}</text></g>'
            f'<g style="{fixed}"><path d="{rows_path(CHECK, bx + 3, G - 20, 3)}" fill="{t["pass"]}"/>'
            f'<text x="{n(lx)}" y="{G + 22}" text-anchor="middle" class="utility" font-size="9.5" letter-spacing="1" fill="{t["pass"]}" text-decoration="line-through">{labels[k]}</text>'
            f'<text x="{n(lx)}" y="{G - 28}" text-anchor="middle" class="utility" font-size="9" font-weight="700" fill="{t["pass"]}">→ TEST</text></g>'
            f'<path d="{zig}" fill="none" stroke="{t["signal"]}" stroke-width="2.5" stroke-linejoin="bevel" class="zp" style="{zap}"/>'
            f'<path d="{rows_path(BURST, bx, by, 3)}" fill="{t["trigger"]}" class="bz fb" style="{boom}"/>'
        )

    ticks = "".join(f"M{x} {G}v4" for x in range(40, W - 30, 40))
    commits = "".join(f'<circle cx="{x}" cy="{G}" r="2.5" fill="{t["hairline"]}"/>' for x in range(60, W - 40, 120))
    rb_y = G - 44
    eye_d = rows_path(["..X..X.."], rest_x, rb_y + 3 * 4, 4)
    antenna = rows_path(["...XX..."], rest_x, rb_y - 4, 4)
    style = base_style(
        ".fa{animation:ptfa .5s steps(1) infinite}.fbb{opacity:0;animation:ptfb .5s steps(1) infinite}"
        "@keyframes ptfa{50%{opacity:0}}@keyframes ptfb{50%{opacity:1}}"
        ".bob{animation:ptbob 1s steps(2) infinite}@keyframes ptbob{50%{transform:translateY(2px)}}"
        ".la{animation:ptla .32s steps(1) infinite}.lb{opacity:0;animation:ptlb .32s steps(1) infinite}"
        "@keyframes ptla{50%{opacity:0}}@keyframes ptlb{50%{opacity:1}}"
        ".ant{animation:ptant 1.4s steps(1) infinite}@keyframes ptant{50%{opacity:.25}}"
        ".zp,.bz{opacity:0}.bz{transform-origin:center}"
        + sh.css() + REDUCE
    )
    return f"""{svg_open(W, H, "Thanks for playing. A small robot walks the commit log and zaps split-brain, stale-read, lost-write and off-by-one bugs, turning each into a test.")}
  <style>{style}</style>
  <path d="{pixel_path(title, (W - tw) / 2, 14, 4)}" fill="{t['signal']}"/>
  <text x="{W // 2}" y="72" text-anchor="middle" class="utility" font-size="12" fill="{t['quiet']}">now go break something — then publish exactly where it broke.</text>
  <path d="M20 {G}H{W - 20}" stroke="{t['hairline']}" stroke-width="2"/>
  <path d="{ticks}" stroke="{t['hairline']}"/>
  {commits}
  <text x="{W - 24}" y="{G - 8}" text-anchor="end" class="utility" font-size="10" letter-spacing="2" fill="{t['quiet']}">EOF</text>
  {''.join(parts)}
  <g style="{robot_anim}">
    <path d="{antenna}" fill="{t['trigger']}" class="ant"/>
    <path d="{rows_path(BOT_BODY, rest_x, rb_y, 4)}" fill="{t['alloy']}"/>
    <path d="{eye_d}" fill="{t['signal']}"/>
    <path d="{rows_path(BOT_LEGS_A, rest_x, rb_y + 36, 4)}" fill="{t['alloy']}" class="la"/>
    <path d="{rows_path(BOT_LEGS_B, rest_x, rb_y + 36, 4)}" fill="{t['alloy']}" class="lb"/>
  </g>
</svg>
"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    makers = {"terminal": terminal, "divider-a": divider_heartbeat, "divider-b": divider_logic, "divider-c": divider_bus,
              "highscores": highscores, "secret-level": secret_level, "patrol": patrol}
    for name, make in makers.items():
        for theme in (DARK, LIGHT):
            path = OUT / f"{name}-{theme['name']}.svg"
            path.write_text(make(theme))
            print(f"wrote {path}")


if __name__ == "__main__":
    main()
