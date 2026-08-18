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
  Average final score across all guilds: 66.8 coins (lowest game: 12, highest: 121).
  All 8 guilds visited all 4 rooms in 100% of games.
  On average, each guild made 2.5 trades with other guilds (7% of guilds made no trades at all).
  On average, each guild took out 0.2 loan(s), ending the game owing 1.3 coins in debt.

  --- free_choice ---
  Ran 500 practice games.
  ...
```

Each block compares two versions of the rules side by side — in the
example above, **"fixed_rotation"** is the recommended room-scheduling
rule from the written analysis, and **"free_choice"** is what happens
if teams are just left to pick rooms on their own. Reading down the
two blocks tells you which version actually works better, and by how
much.

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
- `tests/` — pytest suite (32 tests) covering recipes, rotation integrity, loan math, end-to-end engine behavior, and review fixes.

Run the test suite with:
```
python3 -m pytest tests/ -v
```

### Not yet done (left for a future iteration)

- Shadow-value-by-round and marginal per-room expected value (analysis §8 items 6-7) — need price inference / counterfactual re-runs, not just bookkeeping.
- Guild-special items and unique quests (§2.6), once finalized in the source.
- A more thorough trade-matching mechanism (still one attempt per guild per break, across two instruments — barter and coin purchase).
- Explaining the specialty win-rate spread noted below (§8 item 8) rather than just reporting it.
- The full §8 design-variant sweep (loan interest, Tier-3 prices, reward-pick-order, mandatory trading windows) - `sim/experiment.py` and `sim/config.py`'s `reward_pick_order` support this now, but only the rotation comparison is wired up as a worked example.
- A separate `Guild.purchase_count` distinct from `trade_count`: right now barter swaps and coin purchases both increment the same counter, so "trades" in the metrics is really barter+purchases combined.

### Findings from this version so far (illustrative, not final)

400-game batches, paired seeds:

- **The fixed room rotation reaches 100% room completion by construction**, vs. ~37% for free-choice scheduling under the same policies — reproducing the standalone toy model's ~38.2% finding inside the full economic engine.
- **Trading happens under rational play, but far less than under casual play.** All-greedy: mean 2.7 trades/guild, 5% of guilds finish with zero trades. The self-sufficient "solo chaining" mechanism from analysis §2.5 is real and reduces reliance on trading, but doesn't eliminate it once a coin side-payment can bridge the gap between a needed item's value and a seller's liquidation value for it.
- **Casual and mixed policy mixes produce meaningfully more loan debt than all-greedy play** (mean debt/guild: ~13 casual vs. ~1.3 greedy).
- **Specialty win-rate is not stable across policy mixes** in this version — which specialty leads changes depending on the policy mix, more consistent with noise or a mix-dependent interaction than a fixed structural bias, but not yet explained (§8 item 8).

### Review history

This simulator went through three rounds of independent code review before merging (see PR #1 in this repo's history for the full transcript). Round 1 found four real issues — an unpaired comparison that let sampling noise masquerade as a design effect, a biased deterministic tie-break, a missing coin-purchase mechanism that materially changed the headline trading finding, and a boolean config flag too narrow to express a three-way design variant — all fixed and covered by regression tests in `tests/test_review_r1_fixes.py`. Rounds 2 and 3 confirmed the fixes and approved.
