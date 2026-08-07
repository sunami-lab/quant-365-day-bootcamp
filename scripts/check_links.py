#!/usr/bin/env python3
"""Check every URL in data/schedule.yml, concurrently.

A dead link in a study guide is discovered at the moment it does the most damage
to trust in everything else, so this runs over the whole schedule rather than
spot-checking.

    python3 scripts/check_links.py                # check all, print failures
    python3 scripts/check_links.py --all          # print every result
    python3 scripts/check_links.py --workers 16

Some hosts return 403 to anything that is not a browser -- matplotlib.org,
cppreference.com and the *.ml4trading.io docs all do -- so 403 and 405 are
reported separately from genuine failures rather than counted as dead.
"""

import argparse
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SCHEDULE = ROOT / "data" / "schedule.yml"

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/126.0.0.0 Safari/537.36")
# Status codes that mean "I can see you are a script", not "this page is gone".
BOT_WALLED = {403, 405, 406, 429, 503}

# Hosts that go further and serve a wrong status to scripts. Kaggle answers 404
# to urllib for competition pages that return 200 with the right content in a
# browser (verified against a control slug, which 404s in both). SEC requires a
# User-Agent naming a contact address. FRED refuses the connection outright from
# some networks. Treat a failure from these as "check by hand", never as dead.
BOT_WALLED_HOSTS = {
    "www.kaggle.com", "kaggle.com",
    "www.sec.gov", "data.sec.gov",
    "fred.stlouisfed.org",
    "academic.oup.com", "link.springer.com", "www.cambridge.org",
    "matplotlib.org", "en.cppreference.com",
    "alphalens.ml4trading.io", "pyfolio.ml4trading.io", "zipline.ml4trading.io",
    "www.interactivebrokers.com", "www.bloomberg.com",
}


def check(item, timeout):
    url, days = item
    req = urllib.request.Request(url, headers={"User-Agent": UA}, method="HEAD")
    ctx = ssl.create_default_context()
    for method in ("HEAD", "GET"):
        req.method = method
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
                return url, resp.status, days, ""
        except urllib.error.HTTPError as exc:
            if method == "HEAD" and exc.code in (400, 403, 405, 406, 501):
                continue  # some servers only answer GET
            return url, exc.code, days, exc.reason or ""
        except Exception as exc:  # timeouts, DNS, TLS
            if method == "HEAD":
                continue
            return url, None, days, f"{type(exc).__name__}: {exc}"
    return url, None, days, "no response"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true", help="print every result, not just problems")
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--timeout", type=float, default=25.0)
    args = ap.parse_args()

    data = yaml.safe_load(SCHEDULE.read_text(encoding="utf-8"))
    urls = {}
    for day in data["days"]:
        for res in day.get("resources", []):
            urls.setdefault(res["url"], []).append(day["day"])

    print(f"checking {len(urls)} distinct URLs across {len(data['days'])} days\n")
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(lambda i: check(i, args.timeout), sorted(urls.items())))

    ok, walled, dead = [], [], []
    for url, status, days, note in results:
        row = (url, status, days, note)
        host = urllib.parse.urlparse(url).netloc
        if status and 200 <= status < 400:
            ok.append(row)
        elif status in BOT_WALLED or host in BOT_WALLED_HOSTS:
            walled.append(row)
        else:
            dead.append(row)

    if args.all:
        for url, status, days, _ in ok:
            print(f"  {status}  {url}  (day {days[0]}{'+' if len(days) > 1 else ''})")
        print()

    if walled:
        print(f"{len(walled)} refused an automated request -- open these in a browser to confirm:")
        for url, status, days, note in walled:
            print(f"  {status}  {url}  (days {days[:4]}) {note}")
        print()

    if dead:
        print(f"{len(dead)} FAILED:")
        for url, status, days, note in dead:
            print(f"  {status or 'ERR'}  {url}  (days {days[:4]}) {note}")
        print()

    counts = Counter(s for _, s, _, _ in results)
    print(f"{len(ok)} ok, {len(walled)} bot-walled, {len(dead)} failed")
    print("status codes: " + ", ".join(f"{k}: {v}" for k, v in sorted(
        counts.items(), key=lambda kv: (kv[0] is None, kv[0]))))
    return 1 if dead else 0


if __name__ == "__main__":
    sys.exit(main())
