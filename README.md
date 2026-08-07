# 365-Day Quant Bootcamp

A day-by-day year taking a statistician with no finance background to hireable as a **buy-side
quantitative researcher**, with a trading system built along the way. 7 August 2026 – 6 August 2027,
about one hour a day.

Six study days then a lighter seventh, fifty-two times over, then a capstone. Eleven of those seventh
days are milestones instead. Every day page carries its own objectives, timed tasks with checkboxes that
persist in your browser, every link it needs, a deliverable, a checkpoint question, and the two-to-four
things worth doing the night before. Every seventh day also carries an interview drill, so that
preparation is spread over fifty sittings rather than crammed into July 2027.

## Layout

```
data/schedule.yml       Single source of truth. All 365 days.
scripts/skeleton.py     Owns the calendar: day numbers, dates, weeks, phases, which days are milestones.
scripts/build.py        schedule.yml -> days/*.qmd, timeline.qmd, resources.qmd, drills.qmd,
                        project.qmd, _includes/site-js.html. Validates before it writes.
scripts/progress.js     Checkbox persistence and the "today is day N" banner. Inlined by build.py.
scripts/send_reminder.py  The evening email.
prompts/                How the curriculum was written: the authoring spec handed to the subagents.
_quarto.yml             Site config (cosmo / darkly, navbar, search).
styles.css              Day cards, task list, timeline, phase grid, drill and milestone blocks.
index.qmd               Landing page.
setup.qmd               Day 0: environment, accounts, repositories, disk budget.
milestones.qmd          The twelve deliverables and what makes each one good.
hiring.qmd              The target roles, the interview process, the timeline, and the honest gaps.
assessment.qmd          Self-check questions per phase, plus the day-365 list.
timeline.qmd            Generated — all 365 days, grouped by phase and week.
resources.qmd           Generated — every link, grouped by kind.
drills.qmd              Generated — the interview thread in order.
project.qmd             Generated — the running strategy, in order.
days/day-001.qmd …      Generated — one page per day.
```

Generated files are committed so the site builds with Quarto alone, no Python step needed to render.

## Reading it

The site is at <https://sunami-lab.github.io/quant-365-day-bootcamp/>, rebuilt from `main` on every
push (see **Publishing** below). To read it locally instead:

```bash
quarto preview          # live reload at localhost:4200 — this is the good one
quarto render           # writes _site/, open _site/index.html
```

Quarto is the only dependency for rendering; PyYAML is the only one for regenerating.

`.github/workflows/render.yml` also renders on every push and attaches `_site/` to the run as a
downloadable artifact, so you can get the built site from the Actions tab on a machine without Quarto.
That workflow additionally re-runs `scripts/build.py` and **fails if the committed pages have drifted
from `data/schedule.yml`**, which is the mistake this layout invites.

## Changing the schedule

Edit `data/schedule.yml`, then regenerate:

```bash
python3 scripts/build.py
```

Never edit `days/*.qmd`, `timeline.qmd`, `resources.qmd`, `drills.qmd`, `project.qmd` or
`_includes/site-js.html` directly — the next build overwrites them.

`build.py` validates before it writes anything, and refuses to run on: a gap or duplicate in the day
numbers, a duplicate date, a weekday that disagrees with its date, a missing required field, a resource
without a usable URL, task minutes outside 45–80 for a study day or 25–75 for a catch-up day, or a
non-empty `prep_for_tomorrow` on the last day.

A day record looks like this:

```yaml
- day: 47
  date: '2026-09-22'
  weekday: Tuesday
  week: 7
  phase: Returns and noise
  kind: study            # study | catchup | milestone | capstone
  title: The Sharpe ratio has a standard error
  why: One sentence on what this day unlocks.
  objectives: [...]      # 2-3 checkable claims
  tasks:
    - text: What to actually do, with section numbers and file names.
      minutes: 35
  resources:
    - label: Lo (2002) - The Statistics of Sharpe Ratios
      url: https://example.org/paper.pdf
      kind: paper        # textbook | paper | course | video | repo | tool | data | problems | reference
  deliverable: The artifact you should have by the end of the hour.
  checkpoint: The question you must be able to answer without notes.
  prep_for_tomorrow: [...]   # 2-4 ten-minute items; this is what the evening email sends
  drill: [...]               # catch-up and milestone days only; the interview thread
  project: One sentence on what this day added to the running strategy.  # optional
```

`prep_for_tomorrow` on day N describes how to prepare for day N+1. Day 365's is empty. The items for the
night before day 1 live in `meta.prep_for_day_1`.

`scripts/skeleton.py` owns the calendar. If you want to shift the start date, change `START` there,
re-emit, and merge the new dates into `schedule.yml` — do not renumber by hand.

## The daily email

`.github/workflows/daily-reminder.yml` runs `scripts/send_reminder.py` at 22:00 UTC: 5 pm in Madison
from March to November, 4 pm in winter. The script reads `data/schedule.yml`, works out tomorrow's date,
and emails the `prep_for_tomorrow` items from the *preceding* day's record together with a preview of
tomorrow. On a date the schedule does not cover — before day 1, during a pause, after 6 August 2027 — it
sends nothing.

The 50-day LLM bootcamp pinned its send to exactly 5 pm local by starting the cron early and sleeping
off the difference. It could afford to: Actions minutes are free on public repositories. This one was
private when it was written, where they are metered and sleeping three hours a day would have spent the
entire monthly allowance doing nothing, so it sends whenever the runner starts instead. It is public
now and the sleep would be free again, but drifting an hour with the seasons is not worth a job that
idles for three hours. GitHub's scheduler also runs late under load, which moves the email later in the
evening but never skips it.

Editing the schedule and pushing is enough to change what the emails say — there is nothing to keep in
sync by hand.

### Setup

Three repository secrets, under Settings → Secrets and variables → Actions:

| Secret | Value |
|:--|:--|
| `GMAIL_ADDRESS` | the Gmail account that sends |
| `GMAIL_APP_PASSWORD` | a Google **app password**, not your account password — requires 2-Step Verification, generated at <https://myaccount.google.com/apppasswords> |
| `RECIPIENT_EMAIL` | optional; defaults to `GMAIL_ADDRESS` |

The same three you set on `chenyangsu/llm-50-day-bootcamp`. Secret values are not readable through the
API, so they have to be set again here:

```bash
gh secret set GMAIL_ADDRESS       --repo sunami-lab/quant-365-day-bootcamp
gh secret set GMAIL_APP_PASSWORD  --repo sunami-lab/quant-365-day-bootcamp
```

### Testing without sending

```bash
python3 scripts/send_reminder.py --dry-run                    # tonight's email
python3 scripts/send_reminder.py --dry-run --today 2027-03-14 # any date
```

The workflow also has a manual trigger (Actions → Daily reminder email → Run workflow) with `dry_run`
and `today` inputs, so you can exercise the real send path on demand.

### The 60-day problem

GitHub disables scheduled workflows in a repository after 60 days without a push. This course runs for
365 days and most of those days you will be committing to your *work* repo, not this one, so the
reminder would switch itself off somewhere around October. `.github/workflows/keepalive.yml` pushes one
commit a month to hold the clock open. Delete it if you would rather re-enable by hand when GitHub
emails you.

## Publishing

Live at <https://sunami-lab.github.io/quant-365-day-bootcamp/>.

`sunami-lab` is on GitHub's **free** organisation plan, which will not serve Pages from a private
repository. This repository is public, so it does. `.github/workflows/publish.yml` renders on every push
to `main` and pushes `_site/` to the `gh-pages` branch, which Pages serves from the branch root. Three
things have to stay true for that to keep working:

| Setting | Value |
|:--|:--|
| Repository visibility | public |
| Repository variable `PUBLISH_PAGES` | `true` (Settings → Secrets and variables → Actions → Variables) |
| Settings → Pages source | branch `gh-pages`, folder `/` |
| `site-url` in `_quarto.yml` | `https://sunami-lab.github.io/quant-365-day-bootcamp/`, so open-graph tags and absolute links resolve |

To take the site down, set `PUBLISH_PAGES` to anything other than `true`. That stops the deploy but
leaves the already-published `gh-pages` branch being served, so delete that branch too if you need the
site actually gone.

`quarto preview` locally is still the better way to read it while you are editing.

## Related repositories

| Repo | What |
|:--|:--|
| [`sunami-lab/quant-365-work`](https://github.com/sunami-lab/quant-365-work) | Notebooks, the strategy code, and the twelve milestone reports. Create this; it is where the work goes. |
| [`chenyangsu/llm-50-day-bootcamp`](https://github.com/chenyangsu/llm-50-day-bootcamp) | The 50-day LLM bootcamp this is modelled on. Same generator design, public. |
