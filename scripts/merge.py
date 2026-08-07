#!/usr/bin/env python3
"""Merge authored per-phase JSON into data/schedule.yml.

The curriculum was written one phase at a time. Each author produced a JSON array
of day records carrying content fields only -- title, why, objectives, tasks,
resources, deliverable, checkpoint, prep_for_tomorrow, and optionally drill and
project. The calendar fields (date, weekday, week, phase, kind, milestone) come
from scripts/skeleton.py, so the two can never disagree.

    python3 scripts/merge.py /path/to/authored/           # writes data/schedule.yml
    python3 scripts/merge.py /path/to/authored/ --check    # report only, write nothing

Re-runnable: it rebuilds schedule.yml from the JSON every time, so fixing one
phase and merging again is safe.
"""

import argparse
import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import skeleton  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "schedule.yml"

CONTENT_FIELDS = [
    "title", "why", "objectives", "tasks", "resources",
    "deliverable", "checkpoint", "prep_for_tomorrow", "drill", "project",
]
# Fields the calendar owns. An author who sets one is overruled, loudly.
CALENDAR_FIELDS = ["date", "weekday", "week", "phase", "kind", "milestone"]

META = {
    "title": "365-Day Quant Bootcamp",
    "start_date": "2026-08-07",
    "end_date": "2027-08-06",
    "timezone": "America/Chicago",
    "day_url_template": (
        "https://github.com/sunami-lab/quant-365-day-bootcamp/blob/main/days/{slug}.qmd"
    ),
    "prep_for_day_1": [
        "Create the Python 3.12 environment and install the core stack. The Setup page has the "
        "exact commands: it is one uv venv and one uv pip install, about ten minutes.",
        "Open a free Alpaca account. It takes five minutes, it is the broker the running strategy "
        "eventually trades against, and approval is not instant.",
        "Create the private quant-365-work repository with the directory layout on the Setup page, "
        "and put a .gitignore in it before anything else. Data never gets committed.",
        "Email the Wisconsin School of Business about a WRDS account. If UW-Madison's subscription "
        "covers you, that single form is worth more than every paid data API combined.",
    ],
}


def load_authored(src):
    records, seen_calendar = {}, []
    files = sorted(Path(src).glob("*.json"))
    if not files:
        sys.exit(f"no JSON files in {src}")
    for path in files:
        try:
            block = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            sys.exit(f"{path.name}: invalid JSON -- {exc}")
        if not isinstance(block, list):
            sys.exit(f"{path.name}: expected a JSON array, got {type(block).__name__}")
        for rec in block:
            day = rec.get("day")
            if day is None:
                sys.exit(f"{path.name}: a record has no 'day'")
            if day in records:
                sys.exit(f"day {day} appears in both {records[day]['_src']} and {path.name}")
            for field in CALENDAR_FIELDS:
                if field in rec and field != "milestone":
                    seen_calendar.append(f"{path.name} day {day} set {field}")
                    rec.pop(field)
            rec["_src"] = path.name
            records[day] = rec
    if seen_calendar:
        print(f"note: dropped {len(seen_calendar)} author-set calendar field(s); "
              f"the calendar owns those. First: {seen_calendar[0]}")
    return records


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src", help="directory of authored per-phase JSON files")
    ap.add_argument("--check", action="store_true", help="report coverage and write nothing")
    args = ap.parse_args()

    authored = load_authored(args.src)
    calendar = skeleton.build()

    missing = [d["day"] for d in calendar if d["day"] not in authored]
    extra = sorted(set(authored) - {d["day"] for d in calendar})
    if extra:
        sys.exit(f"authored days outside 1..{len(calendar)}: {extra}")

    days = []
    for cal in calendar:
        rec = authored.get(cal["day"])
        if rec is None:
            continue
        day = dict(cal)  # calendar first, so its keys lead in the YAML
        for field in CONTENT_FIELDS:
            if field in rec and rec[field] not in (None, ""):
                day[field] = rec[field]
        # An empty prep list on the final day is meaningful, not missing.
        if cal["day"] == len(calendar):
            day["prep_for_tomorrow"] = []
        days.append(day)

    by_phase = {}
    for d in days:
        by_phase[d["phase"]] = by_phase.get(d["phase"], 0) + 1
    print(f"{len(days)} of {len(calendar)} days authored")
    for name, first, last in skeleton.PHASES:
        want = sum(1 for c in calendar if first <= c["week"] <= last)
        print(f"  {name:<24} {by_phase.get(name, 0):>3} / {want}")
    if missing:
        runs, start = [], missing[0]
        for a, b in zip(missing, missing[1:] + [None]):
            if b != (a or 0) + 1:
                runs.append(f"{start}" if start == a else f"{start}-{a}")
                start = b
        print(f"missing: {', '.join(runs)}")

    if args.check:
        return 0
    if missing:
        print("refusing to write an incomplete schedule; fix the gaps or pass --check")
        return 1

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(
        "# 365-Day Quant Bootcamp -- single source of truth.\n"
        "# Calendar fields come from scripts/skeleton.py; content is merged by scripts/merge.py.\n"
        "# Edit here, then run: python3 scripts/build.py\n\n"
        + yaml.safe_dump({"meta": META, "days": days}, sort_keys=False, width=100,
                         allow_unicode=True, default_flow_style=False),
        encoding="utf-8",
    )
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
