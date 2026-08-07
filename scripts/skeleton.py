#!/usr/bin/env python3
"""Emit the fixed scaffolding of the 365 days: number, date, weekday, week, phase, kind.

Content (title, why, objectives, tasks, resources, deliverable, checkpoint, prep,
drill) is authored separately and merged into data/schedule.yml. This script owns
only the parts that are arithmetic, so the calendar can never drift from the phases.

    python3 scripts/skeleton.py            # print a summary table
    python3 scripts/skeleton.py --json     # emit the skeleton as JSON
"""

import argparse
import json
from datetime import date, timedelta

START = date(2026, 8, 7)
TOTAL_DAYS = 365

# (phase name, first week, last week). Weeks are 1-indexed and 7 days long, except
# week 52, which carries the capstone as an eighth day.
PHASES = [
    ("Markets", 1, 4),
    ("Returns and noise", 5, 9),
    ("Time series", 10, 14),
    ("Portfolios and risk", 15, 19),
    ("The research harness", 20, 23),
    ("Alpha", 24, 29),
    ("Machine learning", 30, 34),
    ("Derivatives", 35, 40),
    ("Microstructure", 41, 44),
    ("Production", 45, 47),
    ("The interview", 48, 51),
    ("Capstone", 52, 52),
]

# Milestone days replace that week's catch-up day. Day 365 is the capstone.
MILESTONES = {
    28: "Market map and a point-in-time data store",
    63: "Stylized facts and the noise floor",
    98: "A pairs strategy that survives out of sample",
    133: "A factor risk model built from scratch",
    161: "The research platform",
    203: "The alpha book",
    238: "Machine learning against the linear baseline",
    280: "An option pricer and a delta-hedging study",
    308: "Execution, impact and honest capacity",
    329: "The system in production",
    357: "The interview dossier",
    365: "Capstone",
}


def week_of(day):
    """Week 52 absorbs day 365, so it is eight days long."""
    return min(52, (day - 1) // 7 + 1)


def phase_of(week):
    for name, first, last in PHASES:
        if first <= week <= last:
            return name
    raise ValueError(f"week {week} is outside the phase table")


def kind_of(day):
    if day == TOTAL_DAYS:
        return "capstone"
    if day in MILESTONES:
        return "milestone"
    if day % 7 == 0:
        return "catchup"
    return "study"


def build():
    out = []
    for day in range(1, TOTAL_DAYS + 1):
        d = START + timedelta(days=day - 1)
        week = week_of(day)
        rec = {
            "day": day,
            "date": d.strftime("%Y-%m-%d"),
            "weekday": d.strftime("%A"),
            "week": week,
            "phase": phase_of(week),
            "kind": kind_of(day),
        }
        if day in MILESTONES:
            rec["milestone"] = MILESTONES[day]
        out.append(rec)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true", help="emit JSON instead of the summary")
    args = ap.parse_args()

    days = build()
    if args.json:
        print(json.dumps(days, indent=2))
        return

    print(f"{TOTAL_DAYS} days, {days[0]['date']} ({days[0]['weekday']}) "
          f"to {days[-1]['date']} ({days[-1]['weekday']})")
    print()
    print(f"{'phase':<24} {'weeks':<10} {'days':<12} {'dates':<26} milestones")
    for name, first, last in PHASES:
        block = [d for d in days if first <= d["week"] <= last]
        ms = ", ".join(str(d["day"]) for d in block if d["day"] in MILESTONES)
        weeks = f"{first}-{last}"
        span = f"{block[0]['day']}-{block[-1]['day']}"
        dates = f"{block[0]['date']} to {block[-1]['date']}"
        print(f"{name:<24} {weeks:<10} {span:<12} {dates:<26} {ms}")
    print()
    counts = {}
    for d in days:
        counts[d["kind"]] = counts.get(d["kind"], 0) + 1
    print("  ".join(f"{k}: {v}" for k, v in sorted(counts.items())))
    catchup_weekdays = {d["weekday"] for d in days if d["kind"] in ("catchup", "milestone")}
    print(f"catch-up and milestone days all fall on: {', '.join(sorted(catchup_weekdays))}")


if __name__ == "__main__":
    main()
