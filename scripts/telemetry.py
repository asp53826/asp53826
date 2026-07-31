#!/usr/bin/env python3
"""Generates the portfolio telemetry panel on the profile README.

Counts are *measured*, not typed in. The script walks every public repo,
finds its test files, and counts the actual test functions in them. If a repo
gains tests the panel moves on the next run; if this file's numbers ever
disagree with the repos, the repos win.

Runs in GitHub Actions with nothing but the built-in token, and writes two
self-contained SVGs. No third-party service is involved, so there is nothing
that can rate-limit the profile or take it down.

    GITHUB_TOKEN=... python3 scripts/telemetry.py
"""

import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

USER = os.environ.get("PROFILE_USER", "asp53826")
API = "https://api.github.com"
TOKEN = os.environ.get("GITHUB_TOKEN", "")

# Repos that are portfolio work. Anything else the account holds (forks,
# coursework, the profile repo itself) is deliberately excluded rather than
# filtered heuristically, so the panel can't silently start counting noise.
PORTFOLIO = [
    "edgar-mcp", "xbrl-normalize", "lob-market-making", "aad-greeks",
    "raft-mvcc", "wal-recovery", "lsm-tree", "columnar-engine",
    "vllm-lite", "annlite", "dist-train", "rag-eval", "feature-store",
    "grammar-decode", "agent-harness", "codebase-qa", "track-fusion",
    "sdr-receiver", "sar-focus", "vio-nav",
]

TEST_PATTERNS = [
    re.compile(rb"^\s*(?:async\s+)?def\s+test_\w+", re.M),  # pytest / unittest
    re.compile(rb"^\s*TEST\w*\s*\(", re.M),          # gtest
    re.compile(rb"^\s*(?:public\s+)?void\s+test\w+", re.M | re.I),
]

W = 1200
PAD = 40
ROW = 26

DARK = dict(name="dark", bg="#0d1117", panel="#010409", border="#30363d",
            dim="#7d8590", text="#e6edf3", accent="#56d4dd", green="#3fb950",
            amber="#d29922", grid="#c9d1d9", bar="#1f6feb")
LIGHT = dict(name="light", bg="#ffffff", panel="#f6f8fa", border="#d1d9e0",
             dim="#59636e", text="#1f2328", accent="#0550ae", green="#1a7f37",
             amber="#9a6700", grid="#1f2328", bar="#0969da")

LANG_COLOUR = {
    "Python": "#3572A5", "C++": "#f34b7d", "TypeScript": "#3178c6",
    "HTML": "#e34c26", "CSS": "#563d7c", "Makefile": "#427819",
    "Shell": "#89e051", "Dockerfile": "#384d54", "Java": "#b07219",
    "C": "#555555",
}


def api(path):
    req = urllib.request.Request(f"{API}{path}")
    req.add_header("Accept", "application/vnd.github+json")
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        print(f"  ! {path} -> {e.code}", file=sys.stderr)
        return None


def raw(repo, path, branch="main"):
    url = f"https://raw.githubusercontent.com/{USER}/{repo}/{branch}/{path}"
    req = urllib.request.Request(url)
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read()
    except urllib.error.HTTPError:
        return b""


def count_tests(repo, files):
    """Count test functions by reading the test files.

    Counting files would be easy and meaningless -- one file can hold sixty
    tests or one. Counting `def test_` is what a reader of the README would
    check by hand, so it is what gets reported.
    """
    total = 0
    for path in files:
        body = raw(repo, path)
        for pattern in TEST_PATTERNS:
            total += len(pattern.findall(body))
    return total


def collect():
    out = []
    langs = {}
    for name in PORTFOLIO:
        meta = api(f"/repos/{USER}/{name}")
        if meta is None:
            continue
        branch = meta.get("default_branch", "main")
        tree = api(f"/repos/{USER}/{name}/git/trees/{branch}?recursive=1") or {}
        files = [t["path"] for t in tree.get("tree", []) if t.get("type") == "blob"]
        tests = [f for f in files
                 if re.search(r"(^|/)tests?/", f) or "test_" in os.path.basename(f)]
        tests = [f for f in tests if f.endswith((".py", ".cpp", ".cc", ".java"))]

        n = count_tests(name, tests)
        repo_langs = api(f"/repos/{USER}/{name}/languages") or {}
        for k, v in repo_langs.items():
            langs[k] = langs.get(k, 0) + v

        out.append(dict(name=name, tests=n, files=len(files),
                        bytes=sum(repo_langs.values()),
                        topics=meta.get("topics", []),
                        desc=meta.get("description") or ""))
        print(f"  {name:16s} {n:4d} tests   {len(files):3d} files")
    return out, langs


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def build(repos, langs, t, stamp):
    head_h = 44
    stats_h = 58
    chart_h = ROW * len(repos) + 18
    lang_h = 78
    H = head_h + stats_h + chart_h + lang_h + 28

    peak = max((r["tests"] for r in repos), default=1) or 1
    total_tests = sum(r["tests"] for r in repos)
    total_bytes = sum(langs.values())
    bar_x = PAD + 150
    bar_w = W - bar_x - PAD - 70

    body = []

    # -- stats row ---------------------------------------------------------
    y = head_h + 34
    cells = [(f"{len(repos)}", "repositories"), (f"{total_tests:,}", "test functions"),
             (f"{total_bytes/1024:,.0f} KB", "source"),
             (f"{len(langs)}", "languages"),
             (f"{sum(r['files'] for r in repos)}", "files")]
    cx = PAD
    for i, (big, label) in enumerate(cells):
        body.append(
            f'<g class="ln" style="animation-delay:{0.1+i*0.07:.2f}s">'
            f'<text x="{cx}" y="{y}" class="mono lg" fill="{t["accent"]}">{big}</text>'
            f'<text x="{cx}" y="{y+16}" class="mono xs" fill="{t["dim"]}">{label}</text></g>')
        cx += 215

    # -- per-repo bars -----------------------------------------------------
    top = head_h + stats_h + 20
    for i, r in enumerate(repos):
        yy = top + i * ROW
        w = max(2.0, bar_w * r["tests"] / peak)
        delay = 0.5 + i * 0.05
        body.append(
            f'<g class="ln" style="animation-delay:{delay:.2f}s">'
            f'<text x="{PAD}" y="{yy+4}" class="mono sm" fill="{t["text"]}">{esc(r["name"])}</text>'
            f'<rect x="{bar_x}" y="{yy-8}" width="{bar_w}" height="12" rx="3" '
            f'fill="{t["border"]}" opacity="0.35"/>'
            f'<rect x="{bar_x}" y="{yy-8}" width="{w:.1f}" height="12" rx="3" '
            f'fill="{t["bar"]}" class="bar" style="animation-delay:{delay:.2f}s"/>'
            f'<text x="{bar_x+bar_w+10}" y="{yy+4}" class="mono sm" '
            f'fill="{t["green"]}">{r["tests"]}</text></g>')

    # -- language strip ----------------------------------------------------
    ly = top + chart_h + 26
    body.append(f'<text x="{PAD}" y="{ly-12}" class="mono xs" '
                f'fill="{t["dim"]}">language distribution, by bytes of source</text>')
    x = PAD
    strip_w = W - 2 * PAD
    ordered = sorted(langs.items(), key=lambda kv: -kv[1])
    for i, (lang, n) in enumerate(ordered):
        seg = strip_w * n / max(total_bytes, 1)
        body.append(
            f'<rect x="{x:.1f}" y="{ly}" width="{max(seg,1):.1f}" height="14" '
            f'fill="{LANG_COLOUR.get(lang, t["dim"])}" class="seg" '
            f'style="animation-delay:{1.2+i*0.06:.2f}s"/>')
        x += seg

    lx = PAD
    for i, (lang, n) in enumerate(ordered):
        pct = 100.0 * n / max(total_bytes, 1)
        if pct < 0.4:
            continue
        body.append(
            f'<g class="ln" style="animation-delay:{1.4+i*0.05:.2f}s">'
            f'<rect x="{lx}" y="{ly+28}" width="9" height="9" rx="2" '
            f'fill="{LANG_COLOUR.get(lang, t["dim"])}"/>'
            f'<text x="{lx+15}" y="{ly+37}" class="mono xs" fill="{t["dim"]}">'
            f'{esc(lang)} {pct:.1f}%</text></g>')
        lx += 30 + len(f"{lang} {pct:.1f}%") * 7.0

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Portfolio telemetry: {len(repos)} repositories, {total_tests} test functions, {total_bytes/1024:.0f} KB of source across {len(langs)} languages.">
  <defs>
    <pattern id="g-{t['name']}" width="24" height="24" patternUnits="userSpaceOnUse">
      <circle cx="1" cy="1" r="1" fill="{t['grid']}" opacity="0.07"/>
    </pattern>
  </defs>
  <style>
    .mono {{ font-family: ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace; }}
    .lg {{ font-size: 26px; font-weight: 600; }}
    .sm {{ font-size: 13px; }}
    .xs {{ font-size: 11px; }}
    .ln {{ opacity: 0; animation: fade .5s cubic-bezier(.2,.7,.3,1) forwards; }}
    .bar {{ transform: scaleX(0); transform-box: fill-box; transform-origin: left center;
            animation: grow .8s cubic-bezier(.2,.8,.3,1) forwards; }}
    .seg {{ opacity: 0; animation: fade .5s ease forwards; }}
    @keyframes fade {{ from {{ opacity: 0; transform: translateX(-6px); }}
                       to {{ opacity: 1; transform: none; }} }}
    @keyframes grow {{ to {{ transform: scaleX(1); }} }}
    @media (prefers-reduced-motion: reduce) {{
      .ln, .seg {{ opacity: 1; animation: none; }}
      .bar {{ transform: none; animation: none; }}
    }}
  </style>

  <rect width="{W}" height="{H}" rx="12" fill="{t['bg']}"/>
  <rect width="{W}" height="{H}" rx="12" fill="url(#g-{t['name']})"/>
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{t['border']}"/>
  <rect x="1" y="1" width="{W-2}" height="42" rx="12" fill="{t['panel']}"/>
  <rect x="1" y="30" width="{W-2}" height="13" fill="{t['panel']}"/>
  <line x1="0" y1="43" x2="{W}" y2="43" stroke="{t['border']}"/>
  <circle cx="26" cy="22" r="6" fill="#ff5f57"/>
  <circle cx="46" cy="22" r="6" fill="{t['amber']}"/>
  <circle cx="66" cy="22" r="6" fill="{t['green']}"/>
  <text x="{W//2}" y="27" text-anchor="middle" class="mono xs" fill="{t['dim']}">portfolio telemetry — counted from source, refreshed {stamp}</text>

  {''.join(body)}
</svg>
"""


def main():
    print(f"collecting {len(PORTFOLIO)} repos for {USER}")
    repos, langs = collect()
    if not repos:
        print("no repos collected; refusing to overwrite good SVGs with an "
              "empty panel", file=sys.stderr)
        return 1

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    os.makedirs("assets", exist_ok=True)
    for theme in (DARK, LIGHT):
        path = f"assets/telemetry-{theme['name']}.svg"
        with open(path, "w") as f:
            f.write(build(repos, langs, theme, stamp))
        print("wrote", path)

    total = sum(r["tests"] for r in repos)
    with open("assets/summary.json", "w") as f:
        json.dump({"repos": len(repos), "tests": total,
                   "bytes": sum(langs.values()), "generated": stamp}, f, indent=2)
    print(f"total: {len(repos)} repos, {total} tests")
    return 0


if __name__ == "__main__":
    sys.exit(main())
