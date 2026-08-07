#!/usr/bin/env python3
"""Generate the Quarto pages for the 365-day quant bootcamp from data/schedule.yml.

data/schedule.yml is the single source of truth. Everything under days/, plus
timeline.qmd, resources.qmd, drills.qmd, project.qmd and _includes/site-js.html,
is generated from it and must not be hand-edited -- edit the YAML and re-run
this script instead.

    python3 scripts/build.py
"""

import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SCHEDULE = ROOT / "data" / "schedule.yml"
DAYS_DIR = ROOT / "days"

KIND_LABEL = {
    "study": "Study day",
    "catchup": "Catch-up day",
    "milestone": "Milestone",
    "capstone": "Capstone",
}

KIND_ORDER = [
    "textbook", "paper", "course", "video", "repo", "tool", "data", "problems", "reference",
]
KIND_HEADING = {
    "textbook": "Books and long-form references",
    "paper": "Papers",
    "course": "Courses",
    "video": "Lectures and video",
    "repo": "Code repositories",
    "tool": "Libraries, platforms and docs",
    "data": "Data sources",
    "problems": "Problem sets and drills",
    "reference": "Reference and reading",
}


def yq(value):
    """Quote a string for a YAML frontmatter scalar. JSON strings are valid YAML."""
    return json.dumps(value, ensure_ascii=False)


def long_date(iso):
    d = datetime.strptime(iso, "%Y-%m-%d")
    return f"{d.strftime('%A')}, {d.day} {d.strftime('%B %Y')}"


def short_date(iso):
    d = datetime.strptime(iso, "%Y-%m-%d")
    return f"{d.strftime('%a')} {d.day} {d.strftime('%b')}"


def month_year(iso):
    d = datetime.strptime(iso, "%Y-%m-%d")
    return d.strftime("%B %Y")


def slug(day):
    return f"day-{day['day']:03d}"


def anchor(text):
    return "".join(c if c.isalnum() else "-" for c in text.lower()).strip("-")


def total_minutes(day):
    return sum(t.get("minutes", 0) for t in day.get("tasks", []))


def day_page(day, prev_day, next_day):
    kind = day.get("kind", "study")
    lines = []
    lines.append("---")
    lines.append("title: " + yq("Day {} — {}".format(day["day"], day["title"])))
    subtitle = (
        f"{long_date(day['date'])} · Week {day['week']} of 52 · "
        f"{day['phase']} · {KIND_LABEL.get(kind, 'Study day')} · {total_minutes(day)} min"
    )
    lines.append("subtitle: " + yq(subtitle))
    lines.append("---")
    lines.append("")

    nav = []
    nav.append(f"[← Day {prev_day['day']}]({slug(prev_day)}.qmd)" if prev_day else "[← Setup](../setup.qmd)")
    nav.append("[All 365 days](../timeline.qmd)")
    nav.append(f"[Day {next_day['day']} →]({slug(next_day)}.qmd)" if next_day else "[Milestones →](../milestones.qmd)")
    lines.append(f'::: {{.day-nav .kind-{kind}}}')
    lines.append(" · ".join(nav))
    lines.append(":::")
    lines.append("")

    if day.get("milestone"):
        label = "Capstone" if kind == "capstone" else f"Milestone — {day['milestone']}"
        lines.append('::: {.milestone-banner}')
        lines.append(f"**{label}.** [What makes it good](../milestones.qmd#m{day['day']})")
        lines.append(":::")
        lines.append("")

    if day.get("why"):
        lines.append('::: {.why}')
        lines.append(day["why"])
        lines.append(":::")
        lines.append("")

    if day.get("objectives"):
        lines.append("## What you should be able to do tonight")
        lines.append("")
        for obj in day["objectives"]:
            lines.append(f"- {obj}")
        lines.append("")

    tasks = day.get("tasks", [])
    if tasks:
        lines.append(f"## Tasks <span class='task-total'>{total_minutes(day)} min</span>")
        lines.append("")
        lines.append('::: {.task-list}')
        for task in tasks:
            lines.append('::: {.task}')
            minutes = task.get("minutes")
            badge = f"[{minutes} min]{{.task-min}} " if minutes else ""
            lines.append(f'<input type="checkbox" class="task-check"> {badge}{task["text"]}')
            lines.append(":::")
        lines.append(":::")
        lines.append("")

    if day.get("drill"):
        lines.append("## Drill <span class='task-total'>interview thread</span>")
        lines.append("")
        lines.append(
            "Spaced repetition, not cramming. Every drill in the year is collected on the "
            "[drills page](../drills.qmd)."
        )
        lines.append("")
        lines.append('::: {.task-list .drill}')
        for item in day["drill"]:
            lines.append('::: {.task}')
            lines.append(f'<input type="checkbox" class="task-check"> {item}')
            lines.append(":::")
        lines.append(":::")
        lines.append("")

    if day.get("project"):
        lines.append("## The running strategy")
        lines.append("")
        lines.append('::: {.project}')
        lines.append(day["project"])
        lines.append(":::")
        lines.append("")

    if day.get("resources"):
        lines.append("## Resources")
        lines.append("")
        for res in day["resources"]:
            tag = f" [{res['kind']}]{{.res-kind}}" if res.get("kind") else ""
            lines.append(f"- [{res['label']}]({res['url']}){tag}")
        lines.append("")

    if day.get("deliverable"):
        lines.append("## Deliverable")
        lines.append("")
        lines.append('::: {.deliverable}')
        lines.append(day["deliverable"])
        lines.append(":::")
        lines.append("")

    if day.get("checkpoint"):
        lines.append("## Checkpoint")
        lines.append("")
        lines.append('::: {.checkpoint}')
        lines.append(day["checkpoint"])
        lines.append(":::")
        lines.append("")

    prep = day.get("prep_for_tomorrow") or []
    if prep:
        nxt = f"Day {next_day['day']}, {long_date(next_day['date'])}" if next_day else "tomorrow"
        lines.append("## Prepare for tomorrow")
        lines.append("")
        lines.append(f"Ten minutes tonight so {nxt} starts clean. This is what the evening email sends you.")
        lines.append("")
        lines.append('::: {.task-list .prep}')
        for item in prep:
            lines.append('::: {.task}')
            lines.append(f'<input type="checkbox" class="task-check"> {item}')
            lines.append(":::")
        lines.append(":::")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def phase_blocks(days):
    """Days grouped into (phase, [days]) in schedule order, preserving phase order."""
    blocks = []
    for day in days:
        if not blocks or blocks[-1][0] != day["phase"]:
            blocks.append((day["phase"], []))
        blocks[-1][1].append(day)
    return blocks


def timeline_page(days, meta):
    lines = []
    lines.append("---")
    lines.append('title: "The 365 days"')
    lines.append("subtitle: " + yq(f"{long_date(meta['start_date'])} → {long_date(meta['end_date'])}"))
    lines.append("toc-depth: 2")
    lines.append("---")
    lines.append("")

    weekdays = {
        datetime.strptime(d["date"], "%Y-%m-%d").strftime("%A")
        for d in days
        if d.get("kind") in ("catchup", "milestone")
    }
    subject = f"Every seventh day is a {weekdays.pop()} and" if len(weekdays) == 1 else "Every seventh day"
    lines.append(
        "Six study days, then a lighter seventh, fifty-two times over, then the capstone. "
        f"{subject} is deliberately unallocated. Eleven of those seventh days are milestones instead, "
        "where the week's work turns into something you could show someone."
    )
    lines.append("")

    for before, after in zip(days, days[1:]):
        gap = datetime.strptime(after["date"], "%Y-%m-%d") - datetime.strptime(before["date"], "%Y-%m-%d")
        if gap.days > 1:
            lines.append(
                f"Paused after day {before['day']} ({short_date(before['date'])}) and resumed at "
                f"day {after['day']} on {long_date(after['date'])}."
            )
            lines.append("")

    blocks = phase_blocks(days)
    lines.append("| Phase | Weeks | Days | When |")
    lines.append("|:--|:--|:--|:--|")
    for phase, block in blocks:
        weeks = f"{block[0]['week']}–{block[-1]['week']}"
        span = f"{block[0]['day']}–{block[-1]['day']}"
        when = f"{month_year(block[0]['date'])} – {month_year(block[-1]['date'])}"
        lines.append(f"| [{phase}](#{anchor(phase)}) | {weeks} | {span} | {when} |")
    lines.append("")

    lines.append('::: {.timeline}')
    lines.append("")
    for phase, block in blocks:
        lines.append(f"## {phase}")
        lines.append("")
        by_week = {}
        for day in block:
            by_week.setdefault(day["week"], []).append(day)
        for week in sorted(by_week):
            wdays = by_week[week]
            span = f"{short_date(wdays[0]['date'])} – {short_date(wdays[-1]['date'])}"
            lines.append(f"### Week {week} <span class='week-span'>{span}</span>")
            lines.append("")
            lines.append("| Day | Date | Focus | |")
            lines.append("|---:|:---|:---|:---|")
            for day in wdays:
                kind = day.get("kind", "study")
                marker = {
                    "catchup": "catch-up", "milestone": "milestone", "capstone": "capstone",
                }.get(kind, "")
                marker_cell = f"[{marker}]{{.pill .pill-{kind}}}" if marker else ""
                lines.append(
                    f"| [{day['day']}](days/{slug(day)}.qmd) | {short_date(day['date'])} "
                    f"| [{day['title']}](days/{slug(day)}.qmd) | {marker_cell} |"
                )
            lines.append("")
    lines.append(":::")
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def resources_page(days):
    seen = {}
    for day in days:
        for res in day.get("resources", []):
            entry = seen.setdefault(
                res["url"],
                {"label": res["label"], "kind": res.get("kind", "reference"), "days": []},
            )
            entry["days"].append(day["day"])

    by_kind = {}
    for url, entry in seen.items():
        by_kind.setdefault(entry["kind"], []).append((url, entry))

    lines = []
    lines.append("---")
    lines.append('title: "Every resource"')
    lines.append('subtitle: "Every link the year uses, grouped by what it is."')
    lines.append("---")
    lines.append("")
    lines.append(
        f"{len(seen)} distinct resources across the 365 days. The day numbers after each entry tell you "
        "where it is used, so an entry used on twelve days is one you will live in."
    )
    lines.append("")

    ordered = [k for k in KIND_ORDER if k in by_kind] + [k for k in sorted(by_kind) if k not in KIND_ORDER]
    for kind in ordered:
        lines.append(f"## {KIND_HEADING.get(kind, kind.title())}")
        lines.append("")
        for url, entry in sorted(by_kind[kind], key=lambda kv: min(kv[1]["days"])):
            nums = sorted(set(entry["days"]))
            shown = nums if len(nums) <= 12 else nums[:12]
            refs = ", ".join(f"[{n}](days/day-{n:03d}.qmd)" for n in shown)
            if len(nums) > len(shown):
                refs += f" and {len(nums) - len(shown)} more"
            lines.append(f"- [{entry['label']}]({url}) — day{'s' if len(nums) > 1 else ''} {refs}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def drills_page(days):
    lines = []
    lines.append("---")
    lines.append('title: "Every drill"')
    lines.append('subtitle: "The interview thread, in the order it appears. One sitting a week for a year."')
    lines.append("toc-depth: 2")
    lines.append("---")
    lines.append("")
    lines.append(
        "Interview preparation is not a phase you do at the end. Probability under pressure decays "
        "if you touch it once; it sticks if you touch it fifty times. Every seventh day carries a drill, "
        "and they accumulate here."
    )
    lines.append("")
    with_drill = [d for d in days if d.get("drill")]
    lines.append(f"{len(with_drill)} drill sittings across the year.")
    lines.append("")
    for phase, block in phase_blocks(days):
        block = [d for d in block if d.get("drill")]
        if not block:
            continue
        lines.append(f"## {phase}")
        lines.append("")
        for day in block:
            lines.append(
                f"**[Day {day['day']}](days/{slug(day)}.qmd)** · {short_date(day['date'])}"
            )
            lines.append("")
            for item in day["drill"]:
                lines.append(f"- {item}")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def project_page(days):
    lines = []
    lines.append("---")
    lines.append('title: "The running strategy"')
    lines.append('subtitle: "One trading system, built over the whole year. Every day that moves it forward, in order."')
    lines.append("toc-depth: 2")
    lines.append("---")
    lines.append("")
    lines.append(
        "The days that teach and the days that build are the same days. From the first week you are "
        "assembling one system — data, signals, portfolio construction, costs, execution, monitoring — "
        "and by the capstone it is running on a schedule against a paper account with a track record you "
        "did not tamper with. This page is that thread pulled out of the calendar."
    )
    lines.append("")
    with_project = [d for d in days if d.get("project")]
    lines.append(f"{len(with_project)} days move the system forward.")
    lines.append("")
    for phase, block in phase_blocks(days):
        block = [d for d in block if d.get("project")]
        if not block:
            continue
        lines.append(f"## {phase}")
        lines.append("")
        for day in block:
            lines.append(
                f"**[Day {day['day']}](days/{slug(day)}.qmd)** · {short_date(day['date'])} · "
                f"{day['title']}"
            )
            lines.append("")
            lines.append(f": {day['project']}")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def site_js_include(days, meta):
    """Inline the schedule data and progress script into one HTML include.

    Inlining sidesteps relative-path breakage between /index.html and /days/day-001.html
    once the site is served from a project subpath.
    """
    payload = [
        {
            "day": d["day"],
            "date": d["date"],
            "title": d["title"],
            "kind": d.get("kind", "study"),
            "week": d["week"],
            "phase": d["phase"],
        }
        for d in days
    ]
    progress = (ROOT / "scripts" / "progress.js").read_text(encoding="utf-8")
    return (
        "<!-- Generated by scripts/build.py -- do not edit. -->\n"
        "<script>\n"
        "const BOOTCAMP_START = " + json.dumps(meta["start_date"]) + ";\n"
        "const BOOTCAMP_DAYS = " + json.dumps(payload, ensure_ascii=False) + ";\n"
        + progress
        + "\n</script>\n"
    )


REQUIRED = ["day", "date", "weekday", "week", "phase", "kind", "title", "why",
            "objectives", "tasks", "deliverable", "checkpoint"]


def validate(days, meta):
    """Fail loudly on the mistakes that a 365-day hand-merged YAML actually makes."""
    problems = []
    numbers = [d["day"] for d in days]
    if numbers != list(range(1, len(days) + 1)):
        missing = sorted(set(range(1, max(numbers) + 1)) - set(numbers))
        dupes = [n for n, c in Counter(numbers).items() if c > 1]
        problems.append(f"day numbers are not 1..N (missing {missing[:20]}, duplicated {dupes[:20]})")
    dates = [d["date"] for d in days]
    if len(set(dates)) != len(dates):
        dupes = [n for n, c in Counter(dates).items() if c > 1]
        problems.append(f"duplicate dates: {dupes[:20]}")

    for d in days:
        where = f"day {d.get('day', '?')}"
        for field in REQUIRED:
            if not d.get(field):
                problems.append(f"{where}: missing {field}")
        if datetime.strptime(d["date"], "%Y-%m-%d").strftime("%A") != d["weekday"]:
            problems.append(f"{where}: weekday {d['weekday']} does not match {d['date']}")
        mins = total_minutes(d)
        floor, ceil = (25, 75) if d["kind"] in ("catchup", "milestone") else (45, 80)
        if not floor <= mins <= ceil:
            problems.append(f"{where} ({d['kind']}): {mins} min outside {floor}-{ceil}")
        for res in d.get("resources", []):
            if not res.get("url", "").startswith("http"):
                problems.append(f"{where}: resource {res.get('label')!r} has no usable url")
    if days and days[-1].get("prep_for_tomorrow"):
        problems.append("the last day should have an empty prep_for_tomorrow")
    return problems


def main():
    data = yaml.safe_load(SCHEDULE.read_text(encoding="utf-8"))
    days = sorted(data["days"], key=lambda d: d["day"])
    meta = data["meta"]

    problems = validate(days, meta)
    if problems:
        print(f"{len(problems)} problem(s) in data/schedule.yml:", file=sys.stderr)
        for p in problems[:60]:
            print(f"  - {p}", file=sys.stderr)
        if len(problems) > 60:
            print(f"  ... and {len(problems) - 60} more", file=sys.stderr)
        return 1

    DAYS_DIR.mkdir(exist_ok=True)
    for stale in DAYS_DIR.glob("day-*.qmd"):
        stale.unlink()
    for i, day in enumerate(days):
        prev_day = days[i - 1] if i > 0 else None
        next_day = days[i + 1] if i + 1 < len(days) else None
        (DAYS_DIR / f"{slug(day)}.qmd").write_text(day_page(day, prev_day, next_day), encoding="utf-8")

    (ROOT / "timeline.qmd").write_text(timeline_page(days, meta), encoding="utf-8")
    (ROOT / "resources.qmd").write_text(resources_page(days), encoding="utf-8")
    (ROOT / "drills.qmd").write_text(drills_page(days), encoding="utf-8")
    (ROOT / "project.qmd").write_text(project_page(days), encoding="utf-8")
    includes = ROOT / "_includes"
    includes.mkdir(exist_ok=True)
    (includes / "site-js.html").write_text(site_js_include(days, meta), encoding="utf-8")

    total = sum(total_minutes(d) for d in days)
    urls = {r["url"] for d in days for r in d.get("resources", [])}
    drills = sum(1 for d in days if d.get("drill"))
    project = sum(1 for d in days if d.get("project"))
    print(f"wrote {len(days)} day pages, timeline, resources ({len(urls)} links), drills, project, site-js")
    print(f"total scheduled time: {total / 60:.0f} h across {len(days)} days "
          f"({total / len(days):.0f} min/day average)")
    print(f"{drills} drill sittings, {project} days advance the running strategy")
    return 0


if __name__ == "__main__":
    sys.exit(main())
