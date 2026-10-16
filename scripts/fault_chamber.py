#!/usr/bin/env python3
"""Render the FAULT CHAMBER profile hero.

The asset is intentionally generated from deterministic vector geometry instead
of a stock illustration.  Depth communicates replicated node-local state;
mint, amber, and rose communicate verified, uncertain, and faulted state.

Requirements used only while authoring the committed media:
  - Inkscape
  - ffmpeg

Run from the repository root:

    python3 scripts/fault_chamber.py
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "fault-chamber"
FRAMES = 44
FPS = 8

THEMES = {
    "dark": {
        "bg": "#0D141C",
        "bg2": "#111D27",
        "plate": "#17232D",
        "plate2": "#22323D",
        "edge": "#49606D",
        "grid": "#6D8591",
        "text": "#F1F5F3",
        "muted": "#9AAAB1",
        "mint": "#73DFC1",
        "amber": "#F3BB69",
        "rose": "#D97C99",
        "shadow": "#020608",
    },
    "light": {
        "bg": "#F1F5F3",
        "bg2": "#E4ECE9",
        "plate": "#D9E3E0",
        "plate2": "#C6D4D1",
        "edge": "#6D8387",
        "grid": "#7B9295",
        "text": "#142029",
        "muted": "#586A70",
        "mint": "#087C67",
        "amber": "#9C6813",
        "rose": "#A83F60",
        "shadow": "#748784",
    },
}


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def smooth(value: float) -> float:
    value = clamp(value)
    return value * value * (3.0 - 2.0 * value)


def phase(frame: int, start: int, end: int) -> float:
    if end == start:
        return 1.0 if frame >= end else 0.0
    return smooth((frame - start) / (end - start))


def mix(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def text(x: float, y: float, value: str, *, size: int, fill: str,
         weight: int = 500, anchor: str = "start", tracking: float = 0,
         mono: bool = False, opacity: float = 1.0) -> str:
    family = "'SFMono-Regular',Consolas,'Liberation Mono',monospace" if mono else "'Arial Narrow','Helvetica Neue',Arial,sans-serif"
    safe = (value.replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;"))
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" '
        f'font-family="{family}" font-size="{size}" font-weight="{weight}" '
        f'letter-spacing="{tracking}" fill="{fill}" opacity="{opacity:.3f}">{safe}</text>'
    )


def line(x1: float, y1: float, x2: float, y2: float, color: str,
         width: float = 1.0, opacity: float = 1.0, dash: str | None = None) -> str:
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{width}" stroke-opacity="{opacity:.3f}"{dash_attr}/>'
    )


def poly(points: list[tuple[float, float]], fill: str, *, stroke: str = "none",
         width: float = 1.0, opacity: float = 1.0) -> str:
    data = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    return (
        f'<polygon points="{data}" fill="{fill}" fill-opacity="{opacity:.3f}" '
        f'stroke="{stroke}" stroke-width="{width}"/>'
    )


def iso_block(cx: float, cy: float, w: float, d: float, h: float, t: dict,
              *, accent: str, lift: float = 0.0, label: str = "") -> str:
    cy -= lift
    top = [(cx, cy - d / 2), (cx + w / 2, cy), (cx, cy + d / 2), (cx - w / 2, cy)]
    left = [(cx - w / 2, cy), (cx, cy + d / 2), (cx, cy + d / 2 + h), (cx - w / 2, cy + h)]
    right = [(cx + w / 2, cy), (cx, cy + d / 2), (cx, cy + d / 2 + h), (cx + w / 2, cy + h)]
    glow = f'<ellipse cx="{cx:.1f}" cy="{cy + d / 2 + h + 10:.1f}" rx="{w * .62:.1f}" ry="{d * .34:.1f}" fill="{accent}" opacity=".10" filter="url(#blur)"/>'
    body = [
        glow,
        poly(left, t["plate"], stroke=t["edge"], width=1.2),
        poly(right, t["plate2"], stroke=t["edge"], width=1.2),
        poly(top, t["bg2"], stroke=accent, width=1.8),
        poly([(cx - w * .24, cy - 1), (cx, cy + d * .24), (cx + w * .24, cy - 1), (cx, cy - d * .24)], accent, opacity=.16),
        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="5.5" fill="{accent}" filter="url(#glow)"/>',
        text(cx, cy + d / 2 + h + 28, label, size=12, fill=t["text"], weight=700, anchor="middle", tracking=1.3, mono=True),
    ]
    return "".join(body)


def log_stack(cx: float, cy: float, t: dict, *, minority: bool,
              repair: float, conflict: float, scale: float = 1.0) -> str:
    parts: list[str] = []
    cell_w = 22 * scale
    cell_h = 7 * scale
    gap = 4 * scale
    start_x = cx - (5 * cell_w + 4 * gap) / 2
    for row in range(3):
        y = cy + row * 13 * scale
        for col in range(5):
            x = start_x + col * (cell_w + gap)
            fill = t["mint"]
            opacity = .25 + row * .08
            if minority and col >= 3:
                if conflict < .95:
                    fill = t["rose"]
                    opacity = .22 + .65 * (1 - conflict)
                else:
                    fill = t["mint"]
                    opacity = .22 + .55 * repair
            parts.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell_w:.1f}" height="{cell_h:.1f}" '
                f'rx="{1.7 * scale:.1f}" fill="{fill}" opacity="{opacity:.3f}"/>'
            )
    return "".join(parts)


def grid(t: dict, width: int, height: int, mobile: bool) -> str:
    parts: list[str] = []
    horizon = 285 if not mobile else 410
    center = width / 2
    for i in range(-8, 9):
        x = center + i * (62 if not mobile else 50)
        parts.append(line(center, horizon - 40, x, height - 72, t["grid"], .8, .15))
    for j in range(8):
        y = horizon + 18 + j * (31 if not mobile else 28)
        parts.append(line(0, y, width, y, t["grid"], .8, .11))
    return "".join(parts)


def trace_packet(a: tuple[float, float], b: tuple[float, float], progress: float,
                 color: str) -> str:
    x = mix(a[0], b[0], progress)
    y = mix(a[1], b[1], progress)
    return (
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="10" fill="{color}" opacity=".10" filter="url(#blur)"/>'
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="{color}" filter="url(#glow)"/>'
    )


def scene(theme_name: str, frame: int, mobile: bool = False) -> str:
    t = THEMES[theme_name]
    w, h = (760, 760) if mobile else (1200, 520)

    partition = phase(frame, 11, 17) * (1 - phase(frame, 30, 36))
    election = phase(frame, 17, 24)
    repair = phase(frame, 30, 38)
    conflict = phase(frame, 29, 35)
    receipt = phase(frame, 35, 41)
    packet = phase(frame, 3, 11)

    if mobile:
        nodes = {
            "n1": (380, 280),
            "n2": (535, 345),
            "n3": (465, 465),
            "n4": (290, 470),
            "n5": (225, 345),
        }
        block_w, block_d, block_h = 78, 42, 52
        log_offset = 63
        title_x, title_y = 46, 62
    else:
        nodes = {
            "n1": (620, 156),
            "n2": (845, 235),
            "n3": (740, 352),
            "n4": (480, 352),
            "n5": (375, 235),
        }
        block_w, block_d, block_h = 94, 48, 58
        log_offset = 69
        title_x, title_y = 50, 65

    leaders = {"n1": t["amber"], "n2": t["mint"] if election > .5 else t["edge"]}
    links = [("n1", "n2"), ("n2", "n3"), ("n3", "n4"), ("n4", "n5"), ("n5", "n1"), ("n1", "n3")]

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="FAULT CHAMBER: a five-node Raft cluster is partitioned, elects a leader, repairs conflicting history, and emits a verification receipt">',
        "<defs>",
        f'<linearGradient id="background" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{t["bg"]}"/><stop offset="1" stop-color="{t["bg2"]}"/></linearGradient>',
        f'<radialGradient id="halo"><stop stop-color="{t["mint"]}" stop-opacity=".15"/><stop offset="1" stop-color="{t["mint"]}" stop-opacity="0"/></radialGradient>',
        '<filter id="blur" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="10"/></filter>',
        '<filter id="glow" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>',
        f'<clipPath id="frame"><rect width="{w}" height="{h}" rx="18"/></clipPath>',
        "</defs>",
        '<g clip-path="url(#frame)">',
        f'<rect width="{w}" height="{h}" rx="18" fill="url(#background)"/>',
        f'<circle cx="{w * .54:.1f}" cy="{h * .54:.1f}" r="{h * .52:.1f}" fill="url(#halo)"/>',
        grid(t, w, h, mobile),
    ]

    # Header and scenario identity.
    parts.extend([
        text(title_x, title_y, "FAULT CHAMBER", size=19 if mobile else 17,
             fill=t["mint"], weight=700, tracking=3.1, mono=True),
        text(title_x, title_y + (44 if mobile else 42), "A SYSTEM UNDER PRESSURE",
             size=38 if mobile else 43, fill=t["text"], weight=800,
             tracking=-1.4),
        text(title_x, title_y + (74 if mobile else 70),
             "Five nodes. One partition. History repaired in public.",
             size=14 if mobile else 15, fill=t["muted"], weight=500),
    ])

    if not mobile:
        parts.extend([
            text(w - 50, 55, "RAFT + MVCC / SCENARIO 04", size=11,
                 fill=t["muted"], anchor="end", tracking=1.4, mono=True),
            text(w - 50, 77, "VISUAL TRACE / RUN THE LIVE LAB TO EXECUTE", size=10,
                 fill=t["edge"], anchor="end", tracking=.8, mono=True),
        ])

    # Network links; links crossing the fault plane visibly break.
    for left, right in links:
        a, b = nodes[left], nodes[right]
        crosses = ({left, right} & {"n4", "n5"}) and ({left, right} & {"n1", "n2", "n3"})
        if crosses and partition > .05:
            gap = .16 * partition
            ax, ay = mix(a[0], b[0], .5 - gap), mix(a[1], b[1], .5 - gap)
            bx, by = mix(a[0], b[0], .5 + gap), mix(a[1], b[1], .5 + gap)
            parts.append(line(a[0], a[1], ax, ay, t["rose"], 2.1, .62))
            parts.append(line(bx, by, b[0], b[1], t["rose"], 2.1, .62))
        else:
            parts.append(line(a[0], a[1], b[0], b[1], t["mint"], 1.6, .30))

    if frame <= 11:
        parts.append(trace_packet(nodes["n1"], nodes["n2"], packet, t["mint"]))

    # The fault plane is physical and only appears during the actual partition.
    if partition > .01:
        if mobile:
            plane = [(310, 240), (350, 220), (465, 535), (405, 555)]
        else:
            plane = [(500, 135), (545, 112), (690, 430), (625, 457)]
        parts.append(poly(plane, t["rose"], stroke=t["rose"], width=1.2, opacity=.08 + .12 * partition))
        p1, p2 = plane[0], plane[3]
        parts.append(line(p1[0], p1[1], p2[0], p2[1], t["rose"], 2.4, .75 * partition, "5 8"))
        label_x = 324 if mobile else 510
        label_y = 240 if mobile else 158
        parts.append(text(label_x, label_y, "PARTITION", size=10, fill=t["rose"], weight=700, tracking=1.5, mono=True, opacity=partition))

    # Node-local replicated logs appear as exposed layers beneath each node.
    for name, (cx, cy) in nodes.items():
        is_minority = name in {"n4", "n5"}
        parts.append(log_stack(cx, cy + log_offset, t, minority=is_minority,
                               repair=repair, conflict=conflict,
                               scale=.78 if mobile else 1.0))

    # Nodes and leader transition.
    for name, (cx, cy) in nodes.items():
        accent = leaders.get(name, t["edge"])
        lift = (15 if mobile else 18) * election if name == "n2" else 0
        if name == "n1":
            if frame < 11:
                accent = t["mint"]
            elif partition > .05:
                accent = t["amber"]
            else:
                accent = t["edge"]
        parts.append(iso_block(cx, cy, block_w, block_d, block_h, t,
                               accent=accent, lift=lift, label=name.upper()))

    # Labels explain the causal state rather than adding decorative UI chrome.
    if partition > .08:
        n1 = nodes["n1"]
        stale_x = n1[0] if mobile else n1[0] + 72
        stale_y = n1[1] - 46 if mobile else n1[1] - 4
        stale_anchor = "middle" if mobile else "start"
        parts.append(text(stale_x, stale_y, "STALE LEADER / TERM 8", size=9,
                          fill=t["amber"], anchor=stale_anchor, tracking=.8,
                          mono=True, opacity=partition))
    if election > .08:
        n2 = nodes["n2"]
        parts.append(text(n2[0] + (0 if mobile else 5), n2[1] - 57,
                          "LEADER / TERM 9", size=9, fill=t["mint"], anchor="middle",
                          tracking=.8, mono=True, opacity=election))

    # Bottom causal rail.
    if mobile:
        rail_y = 620
        steps = [(56, "COMMIT"), (205, "PARTITION"), (380, "ELECTION"), (545, "REPAIR")]
        rail_end = 704
    else:
        rail_y = 456
        steps = [(48, "COMMIT"), (230, "PARTITION"), (430, "ELECTION"), (630, "REPAIR")]
        rail_end = 790
    parts.append(line(steps[0][0], rail_y, rail_end, rail_y, t["edge"], 1.4, .48))
    current = 0
    if frame >= 11:
        current = 1
    if frame >= 22:
        current = 2
    if frame >= 35:
        current = 3
    for index, (x, label) in enumerate(steps):
        active = index <= current
        color = t["mint"] if active else t["edge"]
        if label == "PARTITION" and partition > .1:
            color = t["rose"]
        parts.append(f'<circle cx="{x}" cy="{rail_y}" r="5" fill="{color}"/>')
        parts.append(text(x, rail_y + 24, label, size=9, fill=color,
                          anchor="middle", tracking=1.1, mono=True))

    # Receipt resolves only after repair. It is compact on desktop and full width on mobile.
    if mobile:
        rx, ry, rw, rh = 48, 670, 664, 68
    else:
        rx, ry, rw, rh = 832, 430, 320, 66
    parts.append(
        f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="8" '
        f'fill="{t["plate"]}" stroke="{t["mint"]}" stroke-opacity="{.2 + .8 * receipt:.3f}" opacity="{.28 + .72 * receipt:.3f}"/>'
    )
    parts.append(text(rx + 18, ry + 24, "RECEIPT", size=10, fill=t["mint"],
                      weight=700, tracking=1.5, mono=True, opacity=.35 + .65 * receipt))
    parts.append(text(rx + 18, ry + 45, "partition → election → repair", size=10,
                      fill=t["text"], mono=True, opacity=.35 + .65 * receipt))
    parts.append(text(rx + rw - 18, ry + 36, "PASS", size=16, fill=t["mint"],
                      weight=800, anchor="end", tracking=1.2, mono=True,
                      opacity=.2 + .8 * receipt))

    parts.extend([
        "</g>",
        f'<rect x=".75" y=".75" width="{w - 1.5}" height="{h - 1.5}" rx="18" fill="none" stroke="{t["edge"]}" stroke-width="1.5"/>',
        "</svg>",
    ])
    return "".join(parts)


def run(command: list[str]) -> None:
    subprocess.run(command, check=True, stdout=subprocess.DEVNULL)


def render_variant(theme: str, mobile: bool, temp_root: Path) -> None:
    suffix = "mobile" if mobile else "desktop"
    frame_dir = temp_root / f"{theme}-{suffix}"
    frame_dir.mkdir(parents=True, exist_ok=True)
    width, height = (760, 760) if mobile else (1200, 520)

    for index in range(FRAMES):
        svg = frame_dir / f"frame-{index:03d}.svg"
        png = frame_dir / f"frame-{index:03d}.png"
        svg.write_text(scene(theme, index, mobile), encoding="utf-8")
        run([
            "inkscape", str(svg), "--export-type=png", f"--export-filename={png}",
            f"--export-width={width}", f"--export-height={height}",
        ])

    stem = f"fault-chamber-{'mobile-' if mobile else ''}{theme}"
    output = OUT / f"{stem}.png"
    run([
        "ffmpeg", "-y", "-framerate", str(FPS),
        "-i", str(frame_dir / "frame-%03d.png"),
        "-plays", "1", "-f", "apng", str(output),
    ])

    final_png = OUT / f"{stem}-still.png"
    shutil.copy2(frame_dir / f"frame-{FRAMES - 1:03d}.png", final_png)


def evidence_stack(theme_name: str) -> str:
    """A quiet exploded cutaway for the portfolio's evidence contract."""
    t = THEMES[theme_name]
    w, h = 1200, 250
    items = [
        ("CLAIM", "named result", t["mint"]),
        ("ATTACK", "controlled fault", t["rose"]),
        ("ORACLE", "deterministic check", t["amber"]),
        ("BOUNDARY", "losing regime", t["rose"]),
        ("RECEIPT", "source-bound result", t["mint"]),
    ]
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Evidence stack: claim, attack, oracle, boundary, and source-bound receipt">',
        "<defs>",
        f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{t["bg"]}"/><stop offset="1" stop-color="{t["bg2"]}"/></linearGradient>',
        '<filter id="shadow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="8"/></filter>',
        "</defs>",
        f'<rect width="{w}" height="{h}" rx="16" fill="url(#bg)"/>',
        text(44, 54, "EVIDENCE STACK", size=15, fill=t["mint"], weight=700, tracking=2.6, mono=True),
        text(44, 88, "A public claim is only as strong as the path back to its source.", size=17, fill=t["text"], weight=600),
        text(44, 116, "Each layer has a different job; none is decorative.", size=12, fill=t["muted"]),
    ]
    start_x = 500
    for index, (name, detail, accent) in enumerate(items):
        cx = start_x + index * 145
        cy = 96 + (index % 2) * 19
        top = [(cx, cy - 27), (cx + 61, cy), (cx, cy + 27), (cx - 61, cy)]
        side_l = [(cx - 61, cy), (cx, cy + 27), (cx, cy + 50), (cx - 61, cy + 23)]
        side_r = [(cx + 61, cy), (cx, cy + 27), (cx, cy + 50), (cx + 61, cy + 23)]
        parts.append(f'<ellipse cx="{cx}" cy="{cy + 55}" rx="67" ry="13" fill="{t["shadow"]}" opacity=".16" filter="url(#shadow)"/>')
        parts.append(poly(side_l, t["plate"], stroke=t["edge"], width=1.0))
        parts.append(poly(side_r, t["plate2"], stroke=t["edge"], width=1.0))
        parts.append(poly(top, t["bg2"], stroke=accent, width=1.5))
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="4.5" fill="{accent}"/>')
        parts.append(text(cx, cy + 78, name, size=10, fill=accent, weight=700,
                          anchor="middle", tracking=1.3, mono=True))
        parts.append(text(cx, cy + 96, detail, size=9, fill=t["muted"],
                          anchor="middle", mono=True))
        if index < len(items) - 1:
            nx = start_x + (index + 1) * 145
            ny = 96 + ((index + 1) % 2) * 19
            parts.append(line(cx + 62, cy + 13, nx - 62, ny - 13, accent, 1.4, .55, "4 5"))
    parts.extend([
        f'<rect x=".75" y=".75" width="{w - 1.5}" height="{h - 1.5}" rx="16" fill="none" stroke="{t["edge"]}" stroke-width="1.5"/>',
        "</svg>",
    ])
    return "".join(parts)


def main() -> None:
    for binary in ("inkscape", "ffmpeg"):
        if not shutil.which(binary):
            raise SystemExit(f"{binary} is required to render FAULT CHAMBER")
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="fault-chamber-") as temp:
        temp_root = Path(temp)
        for theme in THEMES:
            render_variant(theme, False, temp_root)
            render_variant(theme, True, temp_root)
            (OUT / f"evidence-stack-{theme}.svg").write_text(
                evidence_stack(theme), encoding="utf-8"
            )
    print(f"Rendered FAULT CHAMBER assets in {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
