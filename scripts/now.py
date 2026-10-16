#!/usr/bin/env python3
"""Generates the "now shipping" strip under the profile banner.

It shows the most recent *human* commit across the public portfolio: the
newest-pushed public repo (not a fork, not this profile repo) and its latest
commit that was not made by a bot, a merge, or a dependency update. So the
strip only ever moves when real work lands.

Like the other generators it uses only the built-in Actions token and writes
self-contained SVGs. If the API is unavailable the existing SVGs are left
untouched, so a bad run can never blank the profile.

    GITHUB_TOKEN=... python3 scripts/now.py
    python3 scripts/now.py --repo NAME --message "..." --date 2026-10-16   # manual / offline
"""

import argparse
import json
import os
import sys
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from banner import DARK, LIGHT, MONO, SANS, instrument_tokens  # noqa: E402

USER = os.environ.get("PROFILE_USER", "asp53826")
API = "https://api.github.com"
TOKEN = os.environ.get("GITHUB_TOKEN", "")
SKIP_REPOS = {USER, "my-garden"}
SKIP_PREFIXES = ("merge ", "chore(deps", "bump ", "refresh profile")


def get(path):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": f"{USER}-profile"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    with urllib.request.urlopen(urllib.request.Request(API + path, headers=headers), timeout=20) as r:
        return json.load(r)


def is_human(c):
    login = (c.get("author") or {}).get("login", "")
    msg = c["commit"]["message"].strip().lower()
    return not login.endswith("[bot]") and "[skip ci]" not in msg and not msg.startswith(SKIP_PREFIXES)


def latest_human_commit():
    repos = get(f"/users/{USER}/repos?sort=pushed&per_page=30&type=owner")
    for repo in repos:
        if repo["fork"] or repo["archived"] or repo["private"] or repo["name"] in SKIP_REPOS:
            continue
        for c in get(f"/repos/{USER}/{repo['name']}/commits?per_page=15"):
            if is_human(c):
                when = c["commit"]["author"]["date"][:10]
                return repo["name"], c["commit"]["message"].splitlines()[0], when
    return None


def ago(day):
    days = (datetime.now(timezone.utc).date() - date.fromisoformat(day)).days
    return "today" if days <= 0 else "yesterday" if days == 1 else f"{days} days ago"


def strip(theme, repo, message, day):
    t = instrument_tokens(theme)
    if len(message) > 64:
        message = message[:61].rstrip() + "…"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="56" viewBox="0 0 1200 56" role="img" aria-label="Now shipping: {escape(repo)}, {escape(message)}, {ago(day)}.">
  <style>
    .display {{ font-family: {SANS}; }} .utility {{ font-family: {MONO}; }}
    .live {{ transform-box: fill-box; transform-origin: center; animation: live 2.2s ease-in-out infinite; }}
    .caret {{ animation: caret 1.1s steps(1) infinite; }}
    @keyframes live {{ 0%,100% {{ opacity:.45; transform:scale(.8); }} 50% {{ opacity:1; transform:scale(1.25); }} }}
    @keyframes caret {{ 50% {{ opacity:0; }} }}
    @media (prefers-reduced-motion: reduce) {{ .live,.caret {{ animation:none; }} }}
  </style>
  <rect x="1" y="1" width="1198" height="54" rx="10" fill="{t['surface']}" stroke="{t['hairline']}"/>
  <circle cx="28" cy="28" r="5" fill="{t['pass']}"/><circle cx="28" cy="28" r="10" fill="none" stroke="{t['pass']}" class="live"/>
  <text x="48" y="33" class="utility" font-size="11" letter-spacing="2" fill="{t['pass']}">NOW SHIPPING</text>
  <path d="M168 16V40" stroke="{t['hairline']}"/>
  <text x="186" y="33" class="utility" font-size="13" font-weight="700" fill="{t['signal']}">{escape(repo)}</text>
  <text x="{196 + 8 * len(repo)}" y="33" class="utility" font-size="13" fill="{t['alloy']}">› {escape(message)}<tspan class="caret" fill="{t['signal']}"> ▍</tspan></text>
  <text x="1176" y="33" text-anchor="end" class="utility" font-size="11" letter-spacing="1" fill="{t['quiet']}">{ago(day).upper()}</text>
</svg>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo"), ap.add_argument("--message"), ap.add_argument("--date")
    a = ap.parse_args()
    if a.repo and a.message and a.date:
        found = (a.repo, a.message, a.date)
    else:
        try:
            found = latest_human_commit()
        except Exception as e:  # network / rate limit: keep yesterday's strip
            print(f"now.py: API unavailable ({e}); keeping existing strip")
            return
    if not found:
        print("now.py: no human commit found; keeping existing strip")
        return
    Path("assets").mkdir(exist_ok=True)
    for theme in (DARK, LIGHT):
        Path(f"assets/now-{theme['name']}.svg").write_text(strip(theme, *found))
    print(f"wrote assets/now-*.svg: {found[0]} › {found[1]} ({found[2]})")


if __name__ == "__main__":
    main()
