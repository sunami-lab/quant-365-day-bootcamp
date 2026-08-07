# Authoring spec — 365-Day Quant Bootcamp day records

You are writing the day-by-day content for a one-year quantitative-finance curriculum. Read this whole
file before writing anything. Your task prompt tells you which weeks you own.

## Who this is for

Chen-Yang Su, a postdoctoral researcher in statistical/human genetics at UW-Madison. Write to him
directly, in second person. He is a peer, not a student who needs encouragement. No cheerleading, no
"you've got this", no exclamation marks.

**What he already has, and you must not re-teach:**

- Probability and mathematical statistics at PhD level. Likelihood, estimation, hypothesis testing,
  asymptotics, the delta method, the bootstrap.
- Linear algebra and regression to the point of fluency. OLS, GLS, ridge, generalized linear models,
  mixed models.
- **Instrumental variables**, deeply. Mendelian randomization is IV estimation; he knows weak-instrument
  bias, exclusion restrictions, two-stage least squares, and the sensitivity analyses.
- **Massive multiple testing**, deeply. Genome-wide significance, Bonferroni, FDR, winner's curse,
  replication, the difference between a discovery threshold and a reporting threshold.
- **Bayesian model comparison.** Colocalization is posterior model probability over shared-causal-variant
  hypotheses.
- High-dimensional covariance structure. Linkage-disequilibrium matrices are estimated covariance
  matrices with the same conditioning problems as a 3,000-asset return covariance.
- Python (numpy/pandas/scikit-learn), R, the shell, HPC job scheduling, git, reproducible pipelines.
- Deep learning, at a from-scratch level — he is finishing a 50-day bootcamp that builds an autograd
  engine, a BPE tokenizer and a decoder-only transformer, and covers LoRA, DPO and RAG.

**What he does not have:**

- Any finance. He does not know what a futures roll is, what a limit order book looks like, what a
  dividend adjustment does to a price series, or why anyone would buy a put.
- Stochastic calculus. He has never seen Itô's lemma.
- Time-series econometrics as a finance practitioner uses it — cointegration, GARCH, HAC, state space.
- Any C++, and only casual SQL.
- The vocabulary, culture, and interview format of the industry.

**Exploit the transfer, hard.** This is the single instruction that most changes the quality of what you
write. Where a quant concept is a thing he already knows under a different name, say so in one clause and
move on at the higher level:

- Backtest overfitting is genome-wide multiple testing. The deflated Sharpe ratio is a significance
  threshold corrected for the number of strategies tried. He does not need convincing that this matters;
  he needs the finance-specific machinery.
- Ledoit-Wolf shrinkage of a return covariance is the same conditioning problem as an LD matrix.
- A factor model is a mixed model with the factors as fixed effects and idiosyncratic return as residual.
- Information coefficient is a Spearman correlation between a predictor and a future outcome.
- Purged, embargoed cross-validation exists for the same reason you cannot put relatives in different
  folds of a genetic prediction study — leakage through dependence structure.
- Survivorship bias in an equity universe is ascertainment bias in a cohort.

Do NOT force the analogy where it does not fit. A forced analogy is worse than none.

**His goal, in his words:** become a buy-side quantitative researcher (statistical arbitrage / ML alpha),
and in parallel run his own capital. Hiring is the first priority. He is aiming to apply during 2027.

## Time budget — this is the hardest constraint to respect

Every study day is sized for **about one hour**. Task minutes must sum to **50–70**. Catch-up and
milestone days sum to **30–60**.

One hour is not much. The single most common failure in writing this curriculum is scheduling three
hours of work and calling it one. Be honest:

- A 50-minute lecture video plus "then implement it" is **two days**, not one.
- A dense textbook chapter is typically 45–60 minutes for 15–20 pages, and that is the whole day.
- A paper is 40–60 minutes to read properly. One paper is a day. Not three papers.
- Writing working code that does something new takes longer than you think. A day whose task is "build
  a backtester" is not a day; it is a week, and you must split it.

When a task genuinely needs more than an hour, **split it across consecutive days and say so explicitly**
in the task text ("continue yesterday's `impact.py`; today only the fitting, the plots are tomorrow").
A year is 365 hours. There is room. Do not compress.

## Output format

Write a single JSON file — an array of day objects — to the path given in your task prompt. No prose
around it, no markdown fences, just the JSON array. Every string double-quoted. Do not include the
fields `date`, `weekday`, `week`, `phase` or `kind`: those are generated from the calendar and merged in.
Include `day` so the merge can find your records.

```json
[
  {
    "day": 29,
    "title": "Log returns and why the average is a lie",
    "why": "One sentence on what this day unlocks. No hype, no restating the title.",
    "objectives": [
      "State, without looking, when the log return and the simple return differ by more than a basis point.",
      "Explain why the arithmetic mean of daily returns overstates what you actually earned, and by how much."
    ],
    "tasks": [
      {"text": "Read X section Y, running the code yourself. Stop at Z and predict the sign before you look.", "minutes": 35},
      {"text": "Second task, imperative and specific.", "minutes": 25}
    ],
    "resources": [
      {"label": "Exact label as given in the master list", "url": "https://exact.url/from/master/list", "kind": "textbook"}
    ],
    "deliverable": "The concrete artifact you should have at the end of the hour. A file, a plot, a number, a paragraph.",
    "checkpoint": "One question you must be able to answer without looking. If you can't, you are not done.",
    "prep_for_tomorrow": [
      "Imperative bullet, genuinely doable in ten minutes tonight.",
      "Second bullet."
    ],
    "drill": ["Only on catch-up and milestone days. See the drill thread below."],
    "project": "Only on days that move the running strategy forward. See the running project below."
  }
]
```

Field rules:

- `title`: a specific claim or object, not a topic label. "Volatility" is bad. "Why realized volatility
  and implied volatility disagree, and who is paying for the gap" is good. Under about 65 characters
  where you can manage it.
- `why`: one sentence. It is the first thing he reads. Never restate the title. Never start with
  "Today you will".
- `objectives`: 2–3 items, each **checkable**. "Understand cointegration" is not checkable. "Given two
  price series, say which of the Engle-Granger and Johansen procedures you would run and why" is.
- `tasks`: 2–4 items at one hour total. Each starts with a verb. Include section numbers, chapter
  numbers, page ranges, video timestamps, file names, function names, ticker symbols, parameter values —
  whatever makes it unambiguous what to actually do. A task a reader has to interpret is a task they skip.
- `resources`: every URL the day needs, and **only URLs from the master list** (see the link rule).
  Most days need one to three. A day with eight links is a day with no plan.
- `deliverable`: something on disk. Days that leave nothing behind did not happen.
- `checkpoint`: one question, answerable out loud in ninety seconds.
- `prep_for_tomorrow`: 2–4 imperative bullets, each doable in ten minutes. These become the evening
  reminder email, so they must be things like: download the PDF, clone the repo, start the data download,
  open the notebook, create the account, skim the abstract. **Never** "read chapter 7" — that is tomorrow's
  work, not tonight's prep. The last day of the year gets `"prep_for_tomorrow": []`.
- `drill`: **only** on catch-up and milestone days (day numbers divisible by 7). See below.
- `project`: **only** on days that move the running strategy forward. See below.

## The link rule

**Only use URLs from the master list at the end of this file.** Copy the `label` and `url` exactly as
given — the site deduplicates resources by URL, so a URL that differs by a trailing slash creates a
phantom second entry.

If you genuinely need a URL that is not on the list, you must verify it with WebFetch first and confirm
it returns the content you expect. Do not guess URL patterns. Do not assume `/chapter-7` exists because
`/chapter-6` does. A dead link in a study guide is worse than no link.

Several entries in the master list are **paid books**. That is fine and expected — the core quant
references are not free. Link to the publisher or author page, never to a pirated PDF, and when a day's
work depends on a paid book, say which chapter and give a free alternative in a second resource where
one exists.

## Writing style

Concrete over abstract. Numbers, tickers, file names, section numbers, function names, effect
directions, dollar amounts.

Banned, because they read as machine-generated filler:

- "delve into", "underscore", "highlight", "shed light on", "gain insight into", "leverage" (as a verb),
  "navigate the", "unlock", "master the art of"
- "plays a crucial/pivotal/key role", "is essential for", "a deep understanding of", "a solid foundation"
- "the landscape of", "the realm of", "the world of", "in today's markets"
- "In this day, we will explore…", or any sentence that restates the day's title
- stacked hedging: "may potentially help you to possibly understand"
- "Furthermore/Moreover/Additionally" chains
- reflexive "Importantly," / "Notably," / "It is worth noting that"
- grouping things in threes out of habit when there are two or four
- the word "journey", in any sense

Worked examples:

- BAD: "Today we delve into the fascinating world of market microstructure, which plays a crucial role
  in modern trading."
- GOOD: "Every backtest you have written so far assumed you traded at the closing price. Today you find
  out who was on the other side of that trade and what they charged you for it."

- BAD: "Complete the exercises to solidify your understanding of cointegration."
- GOOD: "Run Engle-Granger on KO/PEP over 2015–2019, then again on two series you generated as
  independent random walks. The second one will sometimes pass at 5%. Record how often over 200 draws."

- BAD: "Learn about the Sharpe ratio and its limitations."
- GOOD: "Simulate 1,000 strategies with true Sharpe 0, three years of daily returns each, and plot the
  distribution of realized Sharpe. Read the 95th percentile off the plot. That number is the bar any
  backtest has to clear before it means anything, and it is higher than you expect."

Write in the second person, present or imperative. Prefer short sentences. Let one sentence in a
paragraph be very short when it carries the point.

**Be skeptical in his voice.** This curriculum's spine is that most published quantitative-finance
results do not survive contact with costs, with out-of-sample data, or with the number of hypotheses
that were actually tested. Where a day teaches a technique that is widely abused, say so in the same
breath as teaching it. Never sell a strategy.

## The drill thread — interview preparation, spread over the year

Every catch-up and milestone day (every day number divisible by 7, so days 7, 14, 21, …, 364) carries a
`drill` array of **2–4 items** on top of its tasks. Budget 20 minutes; the day's `minutes` do not count
it, so keep catch-up task minutes at the low end when the drill is heavy.

Interview preparation does not work as a block at the end. Probability under time pressure decays if you
touch it once and sticks if you touch it fifty times. The drill thread runs the whole year.

Roughly this progression, and your task prompt tells you which stretch you own:

- **Weeks 1–13:** combinatorics, conditional probability, Bayes, expectation and variance tricks,
  symmetry arguments, the classic urn/coin/dice canon. Mental arithmetic drills — two-digit
  multiplication, percentages, fraction-to-decimal — 5 minutes every drill day, forever.
- **Weeks 14–26:** random walks, gambler's ruin, martingales and optional stopping, order statistics,
  Poisson processes, Markov chains, expected-value games.
- **Weeks 27–39:** statistics and ML interview questions as asked at buy-side firms; explaining bias-variance,
  regularization, and cross-validation out loud in ninety seconds; SQL and Python coding problems;
  starting to rehearse his own genetics research as a five-minute research presentation.
- **Weeks 40–52:** timed mixed sets under a clock; market-making and trading games; estimation/Fermi
  questions; mock interviews; the "why do you want to leave academia" and "what would you do with a
  million dollars" questions, which are asked and which academics answer badly.

Drill items must be **specific and finishable in 20 minutes total**, e.g.:

- GOOD: "Ten two-digit multiplications against a 60-second clock, then the 1/7 through 6/7 decimal
  expansions from memory. Write the time down; you are looking for the trend over months, not today."
- GOOD: "Solve the broken-stick problem: break a unit stick at two uniform random points, what is the
  probability the pieces form a triangle? Do it by drawing the sample space, not by simulation. Then
  check with 100,000 simulated draws."
- BAD: "Practice probability problems." — not a drill, it is a category.

## The running project

There is one continuous system built across the whole year, and it is both the interview portfolio
artifact and the thing that eventually trades his own money. Days that move it forward carry a `project`
string of one or two sentences saying what got added and why. Roughly 60–90 days across the year should
have one; do not attach it to every day.

Its arc:

1. **Weeks 3–4** — a point-in-time daily data store: US equities and ETFs, corporate actions handled,
   in DuckDB/Parquet, with the ingestion re-runnable and the as-of semantics tested.
2. **Weeks 9–14** — the first strategies on top of it: a mean-reversion pair and a trend follower, both
   evaluated against the noise floor established in phase 2.
3. **Weeks 15–19** — portfolio construction: covariance estimation, factor neutralization, sizing.
4. **Weeks 20–23** — the research harness rebuilt properly: event-driven, point-in-time, cost-aware,
   with tests that catch look-ahead by construction.
5. **Weeks 24–29** — the alpha book: five to eight signals, each with IC, decay, turnover and capacity,
   then combined.
6. **Weeks 30–34** — an ML layer, and the honest verdict on whether it beat the linear baseline.
7. **Weeks 41–44** — execution and impact: what the fills really cost, and what the true capacity is.
8. **Weeks 45–47** — production: scheduled, logged, monitored, reconciled, running against a paper
   brokerage account.
9. **Weeks 48–52** — the track record and the write-up, which is what he actually shows an interviewer.

Keep this thread consistent. If week 22 says the harness stores fills in `fills.parquet`, week 45 must
not silently rename it. If you need a decision that an earlier week should have made, make it and state
it plainly in the `project` text.

## Milestones

Eleven milestones plus the capstone, each replacing that week's catch-up day. On a milestone day the
tasks are "assemble and write it up", not new material. Milestone days must still fit 30–60 minutes of
task time — the work was done during the week; the milestone day is where it becomes a document.

| Day | Milestone |
|---:|:--|
| 28 | Market map and a point-in-time data store |
| 63 | Stylized facts and the noise floor |
| 98 | A pairs strategy that survives out of sample |
| 133 | A factor risk model built from scratch |
| 161 | The research platform |
| 203 | The alpha book |
| 238 | Machine learning against the linear baseline |
| 280 | An option pricer and a delta-hedging study |
| 308 | Execution, impact and honest capacity |
| 329 | The system in production |
| 357 | The interview dossier |
| 365 | Capstone |

## Catch-up days

Every seventh day that is not a milestone is `catchup`. They are deliberately not full of new material.
Structure them as: finish anything outstanding from the week, then one consolidation exercise that
forces retrieval from memory (re-derive it, redraw it, write the comparison table, explain it out loud),
then the drill. Say explicitly in `why` that if he is on track the day is his to spend or skip. Do not
pull new material forward into them.

## The phase and week map

Your task prompt names your weeks. This is the whole year, so you can see what comes before and after
you and hand off cleanly. Do not teach something a later week owns; do not assume something an earlier
week did not cover.

### Phase 1 — Markets (weeks 1–4, days 1–28)
Vocabulary and plumbing. He cannot research instruments he cannot name.
- **Week 1** (1–7): the shape of the industry and who pays whom; equities, ETFs, futures, options, bonds
  and FX at the level of what each contract actually obliges you to do.
- **Week 2** (8–14): exchanges and mechanics — order types, the book, matching, auctions, tick and lot
  size, fees and rebates, short selling and borrow, margin and leverage.
- **Week 3** (15–21): market data — bars, adjusted vs unadjusted prices, corporate actions, survivorship,
  point-in-time, and building the data store.
- **Week 4** (22–28): how money is actually made — risk premia, market making, statistical arbitrage,
  relative value, trend, event-driven; fee structures, capacity, and where a one-person operation can
  and cannot compete. **Milestone day 28.**

### Phase 2 — Returns and noise (weeks 5–9, days 29–63)
The statistics of not fooling yourself, which is the part his training makes him unusually good at.
- **Week 5** (29–35): returns — simple vs log, aggregation across time and assets, compounding,
  volatility drag, the arithmetic-geometric gap.
- **Week 6** (36–42): stylized facts — fat tails and tail-index estimation, volatility clustering,
  autocorrelation of returns versus of absolute returns, the leverage effect.
- **Week 7** (43–49): the Sharpe ratio as an estimator — its standard error, its distribution, what
  autocorrelation does to it, annualization, drawdown and the ratios built on it.
- **Week 8** (50–56): multiple testing applied to strategies — the deflated Sharpe ratio, the probability
  of backtest overfitting, White's reality check, data snooping. Lean hard on what he already knows.
- **Week 9** (57–63): resampling — bootstrap, block bootstrap, permutation tests on strategies, and
  simulating the null. **Milestone day 63.**

### Phase 3 — Time series (weeks 10–14, days 64–98)
- **Week 10** (64–70): stationarity, ACF/PACF, AR/MA/ARMA, estimation and order selection.
- **Week 11** (71–77): unit roots, ADF and KPSS, spurious regression, differencing, HAC standard errors.
- **Week 12** (78–84): cointegration — Engle-Granger, Johansen, error correction, Ornstein-Uhlenbeck and
  the half-life of mean reversion.
- **Week 13** (85–91): volatility modelling — EWMA, the GARCH family, realized volatility, HAR, and how
  to evaluate a volatility forecast.
- **Week 14** (92–98): state space and the Kalman filter, dynamic hedge ratios, regime switching.
  **Milestone day 98.**

### Phase 4 — Portfolios and risk (weeks 15–19, days 99–133)
- **Week 15** (99–105): Markowitz, the efficient frontier, and the estimation error that makes it
  unusable raw; equal weighting as a benchmark that is hard to beat.
- **Week 16** (106–112): covariance in high dimensions — sample covariance breakdown, Ledoit-Wolf
  shrinkage, random matrix theory and Marchenko-Pastur, factor covariance.
- **Week 17** (113–119): factor models — CAPM through Fama-French and Carhart, risk factors versus alpha
  factors, structural risk models, exposures and neutralization.
- **Week 18** (120–126): risk measurement — volatility targeting, VaR and expected shortfall and where
  they fail, drawdown, stress testing, correlations that break exactly when you need them.
- **Week 19** (127–133): sizing — Kelly, fractional Kelly, risk of ruin, leverage and margin mechanics.
  **Milestone day 133.**

### Phase 5 — The research harness (weeks 20–23, days 134–161)
The part that separates people who backtest from people who research.
- **Week 20** (134–140): point-in-time data, the full taxonomy of look-ahead, survivorship, restatements,
  timestamps and lag conventions.
- **Week 21** (141–147): backtest architecture — vectorized versus event-driven, the event loop, the fill
  model, and what each one lies about.
- **Week 22** (148–154): transaction costs — spread, impact, slippage, borrow, financing, turnover, and
  the cost curve that turns a Sharpe of 2 into a Sharpe of 0.3.
- **Week 23** (155–161): testing the tester — unit tests that make look-ahead impossible rather than
  unlikely, synthetic data with a known answer, the null-strategy test. **Milestone day 161.**

### Phase 6 — Alpha (weeks 24–29, days 162–203)
The core craft of the job he wants.
- **Week 24** (162–168): what a signal is — cross-sectional versus time-series, ranking, z-scoring,
  winsorizing, neutralization.
- **Week 25** (169–175): evaluating a signal — information coefficient, IC decay, information ratio,
  quantile spreads, turnover, capacity, and the tearsheet.
- **Week 26** (176–182): the classic equity signals — value, momentum, quality, low volatility, size,
  short-term reversal — replicated honestly, including the ones that no longer work.
- **Week 27** (183–189): time-series signals — trend, carry, seasonality, volatility — mostly on futures.
- **Week 28** (190–196): data beyond price — fundamentals from EDGAR, text and news, and where a language
  model is genuinely the right tool versus where it is a leak waiting to happen.
- **Week 29** (197–203): combining signals — alpha correlation, orthogonalization, weighting, and why
  combining at the portfolio level differs from combining at the signal level. **Milestone day 203.**

### Phase 7 — Machine learning (weeks 30–34, days 204–238)
- **Week 30** (204–210): why standard ML breaks here — non-IID observations, signal-to-noise two orders
  of magnitude below anything he has worked with, non-stationarity; purged and embargoed cross-validation;
  walk-forward.
- **Week 31** (211–217): labelling — fixed horizon, the triple barrier, meta-labelling, sample weights,
  sample uniqueness and overlapping outcomes.
- **Week 32** (218–224): models — regularized linear, gradient boosting, random forests; hyperparameter
  search that does not leak; feature importance that survives a permutation test.
- **Week 33** (225–231): neural networks on financial data — sequence models, cross-sectional models,
  and the honest accounting of when the capacity pays; language models on filings and news.
- **Week 34** (232–238): the audit — the ML strategy against the linear baseline, on the same test set,
  with the same costs. **Milestone day 238.**

### Phase 8 — Derivatives (weeks 35–40, days 239–280)
The most formal mathematics of the year and the furthest from his training. Go slowly.
- **Week 35** (239–245): stochastic processes — random walk to Brownian motion, quadratic variation, the
  Itô integral, Itô's lemma.
- **Week 36** (246–252): geometric Brownian motion, replication, the risk-neutral measure, and
  Black-Scholes derived both as a PDE and as an expectation.
- **Week 37** (253–259): the greeks, delta hedging, the gamma-theta trade-off, and discrete-hedging error.
- **Week 38** (260–266): implied volatility, the smile and skew, term structure, the surface, SVI, and
  the no-arbitrage conditions a surface must satisfy.
- **Week 39** (267–273): beyond Black-Scholes — local volatility, stochastic volatility, jumps; Monte
  Carlo pricing with variance reduction; binomial trees.
- **Week 40** (274–280): volatility as an asset class — the variance risk premium, variance swaps, VIX,
  and which option trades have a documented edge. **Milestone day 280.**

### Phase 9 — Microstructure (weeks 41–44, days 281–308)
- **Week 41** (281–287): the limit order book — mechanics, queue priority, depth, spread decomposition,
  adverse selection.
- **Week 42** (288–294): the models — Kyle, Glosten-Milgrom, informed versus uninformed flow, and price
  impact, linear against square-root.
- **Week 43** (295–301): execution — Almgren-Chriss, TWAP/VWAP/implementation shortfall, participation
  rate, and measuring his own slippage against arrival price.
- **Week 44** (302–308): capacity and the latency hierarchy — what high-frequency firms actually do, and
  why he is not competing with them. **Milestone day 308.**

### Phase 10 — Production (weeks 45–47, days 309–329)
- **Week 45** (309–315): the data layer — SQL properly, DuckDB and Parquet, schema design for time
  series, and making Python fast enough (vectorization, polars, numba) with measurements rather than
  folklore.
- **Week 46** (316–322): C++ literacy — enough to read a matching engine, to reason about memory layout
  and cache, to know the latency numbers, and to write something small that works.
- **Week 47** (323–329): running it — scheduling, logging, monitoring, alerting, reconciliation, and a
  paper account at a real broker. **Milestone day 329.**

### Phase 11 — The interview (weeks 48–51, days 330–357)
By now the drill thread has run for eleven months. This phase is consolidation and campaign, not a
standing start.
- **Week 48** (330–336): the probability canon under a clock — conditional probability, expectation
  tricks, symmetry, martingales and optional stopping, random walks, order statistics.
- **Week 49** (337–343): trading games and market making — pricing under uncertainty, updating on order
  flow, EV under time pressure, and mental arithmetic at speed.
- **Week 50** (344–350): the other rounds — statistics and ML questions, coding, the research
  presentation, and market intuition.
- **Week 51** (351–357): the campaign — CV, project write-ups, the firm list, referrals and outreach,
  mock interviews, and how offers are actually negotiated. **Milestone day 357.**

### Phase 12 — Capstone (week 52, days 358–365)
- **Days 358–364**: final integration — the research dossier, the live paper-traded book with a track
  record he did not tamper with, and a written retrospective on what he believed in September 2026 that
  turned out to be wrong.
- **Day 365**: the capstone. `prep_for_tomorrow` is `[]`.

## Verify your own numbers

Where a day asserts a number, check it before you write it. If a task says "the 95th percentile of
realized Sharpe under the null is about 0.9", either compute it or phrase it so he computes it. If a
task cites a chapter number, a paper's year, or a contract specification, it must be right. Wrong numbers
in a study guide are discovered at exactly the moment they do the most damage to trust in everything else.

## Master resource list

It lives in `prompts/resources-master.md`, beside this file. **Read it in full before writing anything.**
Every URL in it was fetched and confirmed live on 6–7 August 2026. Copy `label` and `url` exactly.

It ends with a "Do not use" section listing links that are dead, renamed, or traps — libraries that look
maintained and are not, a Leanpub URL that resolves to a different book, a data vendor that renamed
itself, and a limit-order-book site where every dead path returns HTTP 200. Read that section too. It is
shorter than the list and will save you from the errors most likely to end up in the finished site.
