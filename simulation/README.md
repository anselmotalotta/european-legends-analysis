# European Legends Simulator

## What this is

A small computer program that plays hundreds of practice rounds of the
*European Legends Office Adventure Game* (the charity team-building
game — see the [full rules](../analysis/corrected-ruleset-v2.md)) and
reports back what tends to happen: how often teams finish the game
fairly, how much they trade with each other, how much debt weaker
teams end up in, and so on.

## What it does

It builds a simplified computer model of the game's economy — teams
producing raw materials, crafting them into more valuable items,
visiting activity rooms, borrowing coins when short, and trading with
each other — and runs that model over and over with small random
variations (different starting hands, different luck, different
skill levels), the same way you might playtest a board game hundreds
of times to see how balanced it is, except a computer can do it in
seconds instead of months.

## Exactly what gets simulated

Each "practice game" the computer plays follows the same shape as the
real event, simplified down to the parts that affect who wins and by
how much:

1. **Setup.** Each of the 8 guilds gets its starting materials and 10
   coins, following the [rules](../analysis/corrected-ruleset-v2.md).
2. **Four rounds, each with an activity room and a trading break.**
   In each round, every guild visits one of the four themed rooms
   (following the fixed room schedule from the rules), pays its entry
   fee, and "does" the room's two quests. The simulator doesn't
   actually generate music quizzes or puzzles — instead, each guild is
   given a random skill level for that room (representing how good
   that mix of 5 real people happens to be at that kind of challenge)
   and scored using the room's real scoring table from the rules. This
   is deliberately a simplification: the point of this tool is to test
   the *economy* (trading, crafting, debt), not to predict trivia
   scores.
3. **Between rounds, guilds produce, craft, and trade.** Each guild
   makes more of its own raw material, converts materials into more
   valuable goods where it makes sense to, and — depending on how
   "smart" that guild is playing (see below) — tries to trade or buy
   what it's missing from other guilds.
4. **Guilds that come up short take a loan** from the Game Master,
   exactly as the real rules describe, and owe it back double at the
   end.
5. **At the end, everything is added up**: leftover coins, plus
   whatever items a guild is still holding (sold at the rules' stated
   prices), minus any loan debt. Highest total wins that practice
   game.

The simulator plays this out 500 times per comparison (with small
random differences each time, like real luck would produce) and
reports back the *averages and patterns* across all 500 — one single
practice game doesn't tell you much, but 500 of them tell you how the
game tends to go.

**Two kinds of guild behavior are tested side by side**, because how
well people play matters:
- **"Greedy" guilds** play thoughtfully — they hold onto items they'll
  need for upcoming rooms instead of selling them too early, and they
  actively look for good trades.
- **"Casual" guilds** play more carelessly — they convert items into
  more valuable ones as soon as they can without thinking ahead, and
  rarely bother trading.

Every run tests three mixes of these — all guilds playing "greedy,"
all playing "casual," and a 50/50 mix — since a real event will have a
mix of experienced and first-time players.

## What it's for

The [written rules analysis](../analysis/game-balance-analysis.md)
raised several open questions that can't be answered just by reading
the rules — for example: *do teams actually need to trade with each
other to do well, or can a team just play alone and still win?* This
simulator exists to answer questions like that with real numbers
instead of guesswork, and to let us try out rule changes (a different
room schedule, a different loan penalty, etc.) and see which version
is actually better before deciding to use it at the real event.

## How to use it

You don't need any programming experience to run this — just follow
the steps below exactly, one at a time.

### Step 1 — Install Python (skip if you already have it)

This tool is written in a programming language called **Python**.
Macs and Linux computers usually already have it. Windows computers
usually don't.

**Check whether you already have it:**

1. Open a terminal:
   - **Mac:** press `Cmd + Space`, type `Terminal`, press Enter.
   - **Windows:** press the Windows key, type `cmd`, press Enter.
   - **Linux:** open your Terminal app.
2. Type this and press Enter:
   ```
   python3 --version
   ```
   (On Windows, if that says it isn't recognized, try `python --version` instead.)
3. If you see something like `Python 3.11.4`, you already have it — skip to Step 2.

**If you got an error** ("command not found" or similar), install Python:

1. Go to https://www.python.org/downloads/ in your web browser.
2. Click the big yellow "Download Python" button.
3. Open the file you downloaded and follow the installer.
   - **On Windows**, make sure to tick the box that says **"Add Python to PATH"** before clicking Install — this step is easy to miss and things won't work without it.
4. Once it's finished, close and reopen your terminal, then repeat the check above to confirm it worked.

### Step 2 — Download this project

1. Go to the project's page: https://github.com/anselmotalotta/european-legends-analysis
2. Click the green **"Code"** button, then click **"Download ZIP"**.
3. Find the downloaded ZIP file (usually in your Downloads folder) and unzip it:
   - **Mac:** double-click it.
   - **Windows:** right-click it and choose "Extract All".
4. You'll now have a folder named something like `european-legends-analysis-main`.

### Step 3 — Open a terminal inside the project folder

- **Mac:** open the folder in Finder, right-click anywhere inside the empty space, and choose **"New Terminal at Folder"**.
- **Windows:** open the folder in File Explorer, click once in the address bar at the top (where the folder path is written), type `cmd`, and press Enter.

A terminal window should open, already "inside" that folder.

### Step 4 — Move into the simulator folder

Type this and press Enter:

```
cd simulation
```

### Step 5 — Run it

Type this and press Enter:

```
python3 -m sim.experiment
```

(On Windows, if that doesn't work, try `python -m sim.experiment` instead.)

It will take a few seconds to run — it's quietly playing through 500
practice games behind the scenes. When it's done, you'll see a report
like this, printed three times (once for each mix of "smart" and
"casual" play styles being tested):

```
===================================================
 Policy mix: all-greedy
===================================================

  --- fixed_rotation ---
  Ran 500 practice games.
  Average final score across all guilds: 66.8 coins (lowest game: 9, highest: 119).
  All 8 guilds visited all 4 rooms in 100% of games.
  On average, each guild made 2.7 exchanges with other guilds - swaps or coin purchases - (7% of guilds made none at all).
  On average, each guild took out 0.2 loan(s), ending the game owing 1.2 coins in debt.

  --- free_choice ---
  Ran 500 practice games.
  ...
```

This exact output is what you should see if you run it yourself — the
simulator is fully reproducible, so your numbers should match these
precisely, not just roughly.

### Step 6 — Understanding what you're looking at

The output is organized in three layers. Here's how to read it, using
the example above:

**1. "Policy mix"** — which of the three guild-behavior mixes (see
above) is being tested. You'll see this three times: `all-greedy`,
`all-casual`, and `mixed`. Compare across these three blocks to see
how much *player skill/behavior* changes the outcome, independent of
the rules themselves.

**2. Inside each policy mix, two rule versions side by side** —
`fixed_rotation` (the recommended room-scheduling rule from the
written rules analysis) and `free_choice` (what happens if guilds are
just left to pick their own rooms, with no schedule). Both are run
under *identical* random luck (same starting hands, same skill draws)
so any difference between them is caused by the rule change itself,
not by one side getting luckier. Comparing these two tells you whether
a specific rule change actually helps.

**3. Five numbers per rule version**, in plain terms:

| Line | What it tells you |
|---|---|
| "Ran 500 practice games" | How many times this exact setup was played out |
| "Average final score" | Roughly how many coins the typical guild ends with — higher is better, and the range (lowest/highest) shows how much luck alone can swing a result |
| "visited all 4 rooms in X% of games" | How often *every* guild manages to complete the whole game without getting shut out of a room — this is the number that shows whether the room-scheduling rule is actually fair |
| "made N exchanges with other guilds" | How much trading actually happens — this is the number that speaks to the open question "do guilds need to trade to do well?" |
| "took out N loan(s)... owing N coins in debt" | How often guilds run short on coins and end up starting the game behind |

**Putting it together for the example above:** under thoughtful
("greedy") play, the recommended fixed room schedule gets every guild
through the whole game (100%) and keeps debt low (1.2 coins), while
leaving the schedule open (`free_choice`) drops full completion to
38% and pushes average debt up sharply — a concrete, numeric reason to
use the fixed schedule rather than open scheduling at the real event.

### Something not working?

- **`command not found: python3`** — Python isn't installed correctly. Go back to Step 1.
- **`No module named sim`** — you're not inside the `simulation` folder. Go back to Step 4 and make sure `cd simulation` worked (your terminal prompt should now show `simulation` at the end).
- **Anything else** — copy the exact error message and ask whoever set this up for you for help.

---

## For developers

*(Everything below this line assumes you're comfortable reading code.
If you just want to run the simulator, everything you need is above.)*

### Design principles

1. **Every ambiguous rule (analysis §4) is a config flag with a documented default**, not a silent hard-code — see [`sim/config.py`](sim/config.py). Nothing here should be read as "the real rules definitely work this way"; several flags are explicit modeling choices pending clarification from the organizer.
2. **Multiple agent policies from day one** — see [`sim/policies.py`](sim/policies.py). `GreedyPolicy` reasons about shadow value and upcoming room needs (analysis §2.2); `CasualPolicy` treats items as flat liquidation values and crafts up greedily (the naive model the analysis's first draft used and corrected). Every decision point — craft choice, room-access valuation, trade/purchase initiation and acceptance, reward-card selection — is a genuinely different concrete rule between the two policies, not a shared implementation with a label swapped.
3. **Comparative, not predictive** — [`sim/experiment.py`](sim/experiment.py) runs paired batches under the same policy mix, using common random numbers across both arms (same seed range, so both configs face the same skill draws/starting hands/shuffles), and reports the difference. Treat outputs as "design A differs from design B under these policies," not as a forecast of the real event's numbers.

### Scope of this first version

Deliberately small: the core economy, room access, crafting, trading,
loans, reward cards, and scoring are modeled cleanly. **Not modeled**:
guild-special Tier-3 items and unique per-guild quests (analysis
§2.6) — still "in elaboration" in the source document, so there's
nothing concrete to simulate yet.

### Known simplifications (stated, not hidden)

- **Quest performance is abstracted**, not content-simulated. Each guild draws a `quest_skill` in `[0, 1]` per room-quest and scores are read off each quest's own table (`sim/quests.py`) using that skill. Actually simulating "identify 10 musical excerpts" would be noise dressed up as precision for an economy simulator.
- **One trade/purchase attempt per guild per trading break** — not exhaustive matchmaking.
- **Free-choice scheduling requires 2 guilds per room to count as a valid visit** (matching "only two guilds can compete in each room in the same round" in the source), stricter than the standalone [`../toy_scheduling_model.py`](../toy_scheduling_model.py), which didn't model that constraint — this is why the full engine's free-choice completion rate is somewhat lower than that model's 38.2%.

### Layout

- `sim/items.py` — Tier-1/2/3 items, the conversion recipe graph, room prerequisites, sell prices.
- `sim/config.py` — frozen rules interpretation; every §4 ambiguity is a flagged default here.
- `sim/rotation.py` — the verified fixed room/opponent rotation and starting-hand coordination from analysis §1/§2.1.
- `sim/guild.py` — per-guild state (coins, inventory, loans, rooms visited, trades).
- `sim/quests.py` — quest scoring (abstracted skill model, see above).
- `sim/policies.py` — `GreedyPolicy` and `CasualPolicy` agent behaviors.
- `sim/engine.py` — the round-by-round game loop.
- `sim/metrics.py` — aggregate statistics across many games.
- `sim/experiment.py` — comparative batch runner (`--json` flag prints raw data instead of the plain-English summary).
- `sim/tuning_sweep.py` — the loan-interest / coin-purchase / reward-pick-order comparison behind the "Tuning sweep" section below.
- `tests/` — pytest suite (37 tests) covering recipes, rotation integrity, loan math, end-to-end engine behavior, and review fixes.

Run the test suite with:
```
python3 -m pytest tests/ -v
```

### Not yet done (left for a future iteration)

- Shadow-value-by-round and marginal per-room expected value (analysis §8 items 6-7) — need price inference / counterfactual re-runs, not just bookkeeping.
- Guild-special items and unique quests (§2.6), once finalized in the source.
- A more thorough trade-matching mechanism (still one attempt per guild per break, across two instruments — barter and coin purchase).
- Explaining the specialty win-rate spread noted below (§8 item 8) rather than just reporting it.
- Two of §8's design variants — Tier-3 prices and mandatory trading windows — aren't swept yet (loan interest, coin-purchase availability, and reward-pick-order now are, see below).
- A separate `Guild.purchase_count` distinct from `trade_count`: right now barter swaps and coin purchases both increment the same counter, so "trades" in the metrics is really barter+purchases combined. Worked around by hand-instrumenting for the tuning sweep below, but should be a real metric.

### Findings from this version so far (illustrative, not final)

500-game batches, paired seeds — these are the exact numbers `python3 -m sim.experiment` prints (see the example output above):

- **The fixed room rotation reaches 100% room completion by construction**, vs. 38% for free-choice scheduling under the same policies — reproducing the standalone toy model's ~38.2% finding inside the full economic engine.
- **Corrected finding, superseding an earlier version of this line:** rational ("greedy") guilds exchange *more* often than casual ones (2.7/guild vs. 1.4/guild), not less — but instrumenting the split (barter vs. coin purchase) that the metric doesn't separate yet reveals why, and it matters: **under all-greedy play, essentially 100% of those exchanges are coin purchases and ~0% are barter swaps** (0 barters observed in a 200-game sample). Under all-casual play, it's a roughly even mix of both. In other words, "smart" guilds mostly buy their way to what they need with coins rather than negotiate a swap with another guild — solo chaining (§2.5) plus a coin side-payment is usually enough on its own, so the genuinely networking-relevant behavior (a two-sided barter that requires actually talking to another guild) is more common under *casual* play, even though total transaction count is higher under greedy play. This is a meaningfully different answer to "does the economy need trading?" than either "yes" or "no" — it needs *some* form of exchange, but rational play satisfies that with money, not negotiation, which matters if the goal is the event's stated networking purpose specifically.
- **Casual and mixed policy mixes produce meaningfully more loan debt than all-greedy play** (mean debt/guild: 10.3 casual vs. 1.2 greedy, fixed rotation).
- **Specialty win-rate is not stable across policy mixes** in this version — which specialty leads changes depending on the policy mix, more consistent with noise or a mix-dependent interaction than a fixed structural bias, but not yet explained (§8 item 8).

### Tuning sweep: what the numbers actually support

The findings above raised two live questions: is the loan interest rate too harsh, and would restricting coin purchases push guilds toward more genuine barter? Rather than guess, both were tested directly with `sim/tuning_sweep.py` — 400-game batches, common random numbers across every variant compared, so differences reflect the rule change, not luck.

**Loan interest (mixed player skill):**

| Multiplier | Mean debt/guild | Score std. dev. |
|---|---|---|
| 1.0× (no penalty) | 3.6 | 20.0 |
| **1.5×** | **5.6** | **22.2** |
| 2.0× (original) | 7.1 | 24.4 |

Higher interest doesn't just mean more debt — it measurably widens the overall score spread, i.e. makes the game less fair. **Conclusion: lowered to 1.5× in the corrected ruleset.** 1.0× (no penalty at all) wasn't adopted despite testing best, because none of this simulator's agent policies model a guild *deliberately* exploiting a penalty-free loan — that risk isn't ruled out by this data, so 1.5× is the more conservative choice: a real but reduced penalty.

**Coin purchases between guilds, allowed vs. disabled:**

| | Exchanges/guild | (of which barter) |
|---|---|---|
| All-greedy, purchases allowed | 2.7 | 0.0 |
| All-greedy, purchases disabled | 0.0 | 0.0 |
| All-casual, purchases allowed | 1.4 | ~0.7 |
| All-casual, purchases disabled | 0.8 | 0.8 |

This is the finding that overturned the obvious-sounding fix: disabling purchases doesn't convert skilled guilds' coin-based exchanges into barter — it just removes the exchange, full stop, because a rational guild's barter offer rarely clears on its own (same shadow-value-vs-liquidation-value gap as §2.2). **Conclusion: no change** — removing purchases would make skilled guilds interact with each other *less*, the opposite of the goal.

**Reward-pick order (winner-first vs. loser-first vs. random):** score standard deviation was 24.4 / 24.0 / 24.2 — no meaningful difference, and specialty spread was, if anything, slightly worse under loser-first. **Conclusion: no change** — this rule isn't a real lever on the fairness question, despite looking like a plausible one on paper.

Reproduce all three with `python3 -m sim.tuning_sweep`.

### Review history

This simulator went through three rounds of independent code review before merging (see PR #1 in this repo's history for the full transcript). Round 1 found four real issues — an unpaired comparison that let sampling noise masquerade as a design effect, a biased deterministic tie-break, a missing coin-purchase mechanism that materially changed the headline trading finding, and a boolean config flag too narrow to express a three-way design variant — all fixed and covered by regression tests in `tests/test_review_r1_fixes.py`. Rounds 2 and 3 confirmed the fixes and approved.
