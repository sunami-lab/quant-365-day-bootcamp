# How this curriculum was written

Kept in the repository rather than beside it, because this one is private anyway and the method is the
part most worth reusing.

| File | What it is |
|:--|:--|
| [`authoring-spec.md`](authoring-spec.md) | The spec handed to fourteen parallel subagents, one per phase or half-phase. Defines the reader, the one-hour budget, the JSON schema for a day record, the banned-phrase list, the drill thread, the running project, and the whole 52-week map so each author could see what came before and after them. |
| [`resources-master.md`](resources-master.md) | Every URL the year is allowed to use, verified live on 6–7 August 2026, plus a "Do not use" section of links that are dead, renamed, or actively misleading. |

```
skeleton.py ──► the calendar (365 days, 12 phases, which days are milestones)
                          │
authoring-spec.md ────────┼──► 14 subagents ──► authored/*.json ──► merge.py ──► schedule.yml
resources-master.md ──────┘                                                          │
                                                                    build.py ────────┤
                                                                                     ├──► the site
                                                                    send_reminder.py ┘    and the email
```

## The four constraints that did the work

**The calendar is code, not prose.** `scripts/skeleton.py` owns every day's number, date, weekday, week,
phase and kind. Authors were given their day numbers and forbidden from setting calendar fields;
`merge.py` drops them if they try. Across 365 days written by fourteen different agents, no date can
disagree with its weekday and no phase boundary can drift, because none of them was ever typed.

**A hard link rule.** Only URLs from the pre-verified master list. Six research agents built that list,
each fetching every URL it proposed rather than recalling it. That mattered more than expected: one
agent probed two plausible-looking identifiers and got a paper about financial education in Ghana and a
neutrino-cosmology preprint, which is exactly the failure the rule exists to prevent. Afterwards
`scripts/check_links.py` swept all 248 URLs — 232 answered 200, 15 were hosts that serve a wrong status
to scripts, and one had a broken certificate chain and was cut.

**The "do not use" list is worth as much as the list itself.** Quantitative finance has an unusual
density of resources that look current and are not: four Quantopian libraries abandoned in 2020 without
ever being marked archived, `backtrader` dormant since 2023 behind 22,000 stars, `mlfinlab` quietly
relicensed, IEX Cloud dead since 2024 but still the default in most tutorials, `polygon.io` renamed,
`crsp.org` redirecting to Morningstar after the 2026 acquisition, and a limit-order-book vendor whose
single-page app returns HTTP 200 for every dead path. A curriculum written from memory would have
recommended most of these.

**Checkable objectives, and a minute budget that had to be respected.** "Understand cointegration" was
ruled out; "given two price series, say which of Engle-Granger and Johansen you would run and why" was
the required shape. The one-hour ceiling was stated as the hardest constraint in the spec, with worked
examples of the failure — a 50-minute lecture plus "then implement it" is two days, not one.

## What the spec spends most of its words on

Not finance. The reader has PhD-level statistics, instrumental variables, massive multiple testing,
Bayesian model comparison and high-dimensional covariance, and none of it under those names. So the
spec's longest section is a list of the places where a quant concept is something he already knows:
backtest overfitting is genome-wide multiple testing, an information coefficient is a Spearman
correlation, Ledoit-Wolf shrinkage is the LD-matrix conditioning problem, purged cross-validation exists
for the reason you cannot split relatives across folds, survivorship bias is ascertainment bias.

The instruction was to name the mapping in one clause and then go straight to the finance-specific
machinery — and never to force it where it does not fit, because a forced analogy is worse than none.

## What was deliberately not automated

The twelve milestones, the self-check questions, the phase structure and the running project's arc were
written by hand before any agent ran, because they are the spine that keeps fourteen independently
written phases pointing at the same thing. The agents filled in days against that spine; they did not
choose it.
