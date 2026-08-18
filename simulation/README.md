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
   actually generate music quizzes or puzzles — instead, each quest
   gets its own fresh random skill draw (representing how good that
   mix of 5 real people happens to be at that specific challenge) and
   is scored using the room's real scoring table from the rules. This
   is deliberately a simplification: the point of this tool is to test
   the *economy* (trading, crafting, debt), not to predict trivia
   scores — and it's a known-incomplete one (see "Known simplifications"
   below): it doesn't model a team being consistently strong or weak
   across the whole evening, only quest to quest.
3. **Between rounds, guilds produce, craft, and trade.** Each guild
   makes more of its own raw material, converts materials into more
   valuable goods where it makes sense to, and — depending on how
   "smart" that guild is playing (see below) — tries to trade or buy
   what it's missing from other guilds.
4. **Guilds that come up short take a loan** from the Game Master,
   exactly as the real rules describe, and owe it back at one and a
   half times the amount borrowed, per the corrected rules.
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
  Average final score across all guilds: 75.4 coins (lowest game: 34, highest: 117).
  All 8 guilds visited all 4 rooms in 100% of games.
  On average, each guild made 3.5 exchanges with other guilds - swaps or coin purchases - (0% of guilds made none at all).
  On average, each guild took out 0.0 loan(s), ending the game owing 0.0 coins in debt.

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
through the whole game (100%) with no guild ever forced into a loan,
while leaving the schedule open (`free_choice`) drops full completion
to 38% and pushes average debt up to 7.7 coins — a concrete, numeric
reason to use the fixed schedule rather than open scheduling at the
real event. (This is the one finding in this whole project that
hasn't needed any correction across every review round — see Findings
below for the ones that did.)

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

A second independent review ("fidelity audit," see Review history below) found that three of these simplifications specifically undermine the conclusions this tool is used to draw — those are marked **⚠ affects headline findings** and explained in more detail in Findings below, not just listed.

- **⚠ No price negotiation.** Every coin purchase is offered and accepted at exactly `room_coin_fallback_fee` (15) — the same number is the Game Master's fallback fee, the buyer's offer, and (when the seller also needs the item) the seller's minimum. Every trade this model completes is an indifference transfer, not a negotiated deal. Real players haggle; this model doesn't.
- **⚠ Agents never take a "bad deal."** Both `GreedyPolicy` and `CasualPolicy` value a needed item identically (`room_access_value` returns the same flat number for both), and `accept_trade`/`accept_purchase` only ever accept when the numbers favor them. Real colleagues at a charity event give things away, trade for goodwill, and misprice constantly — neither policy models that, so "rational" and "casual" bracket two arithmetic settings, not the range of real human trading behavior.
- **⚠ Guilds never trade for crafting materials, only for room access.** Each guild produces 6 units of its own Tier-1 material and never trades for the complementary type needed to craft it into anything — `seek_trade`/`seek_purchase` only ever pursue Tier-2 room prerequisites. Measured: guilds end the game holding most of their own produced units, unused (5 of 9 available, after the starting-hand fix below — worse before it). The rules construct real gains from trade here (two guilds pooling complementary raw materials); the agents can't see them, so "does this game need trading" is being answered by a model that's blind to what may be the single largest trade opportunity the rules create. One interesting side effect of the starting-hand fix: genuine barter (not just coin purchase) has started clearing occasionally in testing, something that never happened before it — see Findings below.
- **Quest performance is abstracted**, not content-simulated. A fresh `quest_skill` in `[0, 1]` is drawn independently for every quest a guild attempts (`sim/quests.py`) — not shared across a room's 2 quests (an earlier version did this and inflated per-room score spread by ~36%, since fixed) and **not persistent across a guild's 4 rooms either**. A real team of 5 colleagues plausibly carries some consistent strength across the evening; this model has none. Measured: forcing one skill per guild for the whole game instead produces ~70% higher score spread (30.75 vs. 17.86, 300-game sample) than the current fully-independent model — so every spread-based fairness number in this document should be read as a **floor**, not an estimate.
- **The largest equalizing part of a real guild's score isn't modeled.** Each guild's unique quest (15–20 coins) and guild-special Tier-3 item (+6 over a plain Tier-3) are still "in elaboration" in the source (§2.6) and out of scope here — but together they could be up to ~43% of a typical modeled score (61 coins), and both are roughly equal-for-everyone rather than skill-dependent, meaning they'd *compress* relative spread, not widen it. Every fairness/spread figure in this document is therefore also an upper bound for this reason, independent of the skill-persistence point above.
- **Trading is confined to the four break windows, one attempt per guild per window** — the source says items can be exchanged "anywhere and at any time during the game" (§9); this model only allows it during the three trading breaks and the final window, once per guild each. Not exhaustive matchmaking, and not the "anytime" the rules describe.
- **No time, movement, or Guildhall-queueing model.** Every action executes instantly. A completion rate like "100% of games" says nothing about whether 8 guilds can physically transact at one Guildhall inside a real 10-minute break — see analysis §5.
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
- `tests/` — pytest suite (50 tests) covering recipes, rotation integrity, loan math, end-to-end engine behavior, and review fixes.

Run the test suite with:
```
python3 -m pytest tests/ -v
```

### Not yet done (left for a future iteration)

**Highest priority, from the fidelity audit (see Review history):**
- **Give agents real price negotiation** instead of a single hardcoded constant, and **give them a reason to trade for crafting complements**, not just room access — both required before "does this game need trading" can be answered by this model.

*(The per-guild fairness gap that used to top this list is resolved — see Findings below.)*

**Also open:**
- A persistent per-guild skill component (a guild-level mean plus per-quest noise), so score spread reflects a "some teams are just stronger" effect the current fully-independent-per-quest model has none of.
- Modeling guild-special items and unique quests (§2.6), once finalized in the source — see the upper-bound caveat above.
- Shadow-value-by-round and marginal per-room expected value (analysis §8 items 6-7) — need price inference / counterfactual re-runs, not just bookkeeping.
- A more thorough trade-matching mechanism (still one attempt per guild per break, across two instruments — barter and coin purchase) and modeling the "anywhere/anytime" trading the rules actually describe, not just break windows.
- Giving `CasualPolicy` a genuine willingness to accept locally unfavorable trades (real charity-event behavior), so the two policies bracket actual human variation rather than two arithmetic settings of the same valuation function.
- A time/movement/Guildhall-queueing model, if the operational risk in analysis §5 is worth quantifying rather than just flagging.
- Two of §8's design variants — Tier-3 prices and mandatory trading windows — aren't swept yet.

### Findings from this version so far (illustrative, not final)

**What's solid:** the fixed room rotation reaches 100% room completion by construction, vs. 38% for free-choice scheduling under the same policies — reproducing the standalone toy model's ~38.2% finding inside the full economic engine. This claim doesn't depend on price, policy, or skill modeling, and it's the strongest result this project has produced.

**What's retracted or reopened, after a fidelity audit found the model's own simplifications were controlling the answers (see Review history):**

- ~~Does this economy need trading?~~ **Not currently supportable, in either direction.** Two of this model's simplifications each independently undermine that question on their own: no price negotiation (R1 below), and agents that never seek out the crafting-material trades the rules actually construct (R7 below). Any prior version of this document that answered this question — including a "twist" answer about coin purchases vs. barter — was answering a question this model isn't yet equipped to answer. It needs the fixes listed in Not yet done first.
- ~~Loan interest measurably widens fairness beyond the debt itself~~ **Also not supportable — corrected twice.** First correction: the score-spread widening across interest rates turned out to be pure arithmetic (a bigger constant subtracted from an unchanged distribution), not a behavioral effect — confirmed by a `stdev_excluding_debt` metric that's identical at every rate. Second correction, found by review r5: even "debt scales with the multiplier" isn't independent evidence — the number and size of loans taken is *identical* across multipliers (pinned by a regression test), so debt is that same fixed total times different constants. **The honest justification for 1.5× is a plain values choice** — a gentler penalty for a charity event — not a simulation finding of any kind.
- **A large, real, per-guild fairness gap was found — and its root cause was too, and fixed.** An earlier version of this document reported "specialty win-rate is not stable... more consistent with noise." That was wrong on two counts. First, averaging by specialty hides the real effect: under identical (all-greedy) play, individual guild win rates ranged from 3.3% (Gdansk) to 23.5% (Lisbon) — a **7.2× spread** — with two guilds sharing a specialty (e.g. Prague 20.3% vs. Vienna 14.2%, both Charcoal) differing substantially, because specialty and rotation position are independent variables in this design. Second, a separate methodology bug made an earlier "mixed policy" reading of this even worse: `mixed_policy()` used a *fixed* `random.Random(seed=0)` shuffle, so the same 4 guilds were "greedy" (which scores far higher than "casual") in literally every game of a batch — producing a spurious 37.7× spread that was really just measuring which guilds got the better policy, not rotation fairness. Found and fixed in this project, not by external review: `run_batch`/`compare` now accept a per-trial callable (`mixed_policy_per_trial`) so the assignment varies game to game, the way real team strength would.

  **What was ruled out for the 7.2× gap first** (all measured, not assumed): specialty (it's per-guild); the engine's shared sequential RNG stream and processing order (reversing which room is processed first within a round doesn't change the ranking); simple opponent-identity clustering (doesn't hold cleanly across all 8 guilds); and reward-card/trade-target urgency (fixing `choose_reward_card`/`seek_trade` to prioritize a guild's actual next room instead of an arbitrary order — a genuine, kept improvement in policy realism — made the gap *larger*, 7.2× vs. an earlier 3.4× reading, not smaller).

  **Root cause found by an independent review, verified independently in this project, and fixed.** `COORDINATED_MISSING_MATERIAL` (`sim/rotation.py`) assigns each guild's starting hand to guarantee it can pay its Round-1 room fee — but that constraint has two valid solutions per guild, and the version in place through this point had picked, for exactly 4 of the 8 guilds (Bursa, Stockholm, Gdansk, Venice), the option that leaves the guild's own Tier-1 specialty able to pair with only 1 of its 3 remaining hand types under the recipe cycle (`sim/items.py`), instead of 2. Those 4 guilds spend their one usable partner card early and then hold every further unit of their own production (6 units/game) as dead 1-coin stock; the other 4 keep converting all game. Verified directly: mean leftover Tier-1 inventory was a clean 5.0-vs-7.0 split tracking exactly this grouping (`mean_score` tracked the same way: 74.9-78.3 for the 2-partner group, 64.9-69.5 for the 1-partner group). **The fix**: reassign the missing-material choice for those 4 guilds to their other, equally Round-1-valid option, which gives every guild 2 usable partners. Verified after the fix: leftover inventory becomes uniform (5.0 for all 8 guilds), and per-guild win-rate spread drops to **~1.8-2.1× at 400-2000 games** — consistent with ordinary sampling noise for an 8-way outcome, not a structural effect. See `sim/rotation.py`'s updated table and `tests/test_review_pr3_r3_starting_hand_fix.py`.

  **The honest caveat, raised by the same review:** real players can trade away dead stock in a way this model's agents can't (the R7 limitation above), so the real-event gap was likely always somewhat smaller than 7.2×. But the underlying asymmetry — 4 guilds structurally needing to trade to use their own production, 4 not — was real regardless of that caveat, and worth fixing on its own terms rather than counting on trading to mask it. Interestingly, fixing it also produced the first genuine, unprompted barter this project has observed (see the Known simplifications note above) — with complementary rather than lopsided surpluses, barter has something to actually clear on now and then, where before it never did.

### Tuning sweep: what the numbers actually support

`sim/tuning_sweep.py` runs four comparisons — 400-game batches, common random numbers across every variant compared (and, since the fidelity audit, a genuinely per-trial-random policy mix, not a fixed one — see Findings above), so differences reflect the rule change, not luck or a confound.

**Loan interest (mixed player skill, per-trial random mix):**

| Multiplier | Mean debt/guild | Score std. dev. | Score std. dev., debt excluded |
|---|---|---|---|
| 1.0× (no penalty) | 2.3 | 17.3 | 15.3 |
| **1.5×** | **3.6** | **18.9** | **15.3** |
| 2.0× (original) | 4.6 | 20.2 | 15.3 |

The debt-excluded column is identical at every multiplier — no guild plays any differently depending on the interest rate, because nothing in this model's decision-making reads that number. Per an independent review (r5): even "mean debt scales with the multiplier" isn't independent evidence of anything — the number and size of loans taken is identical across multipliers (confirmed: total loan *count* is pinned by a regression test), so debt is just that same fixed total times a bigger constant. **The honest justification for 1.5× is a plain values choice** — a gentler penalty for a charity/team-building event, no more, no less. 1.0× wasn't adopted because none of this simulator's agent policies model a guild *deliberately* exploiting a penalty-free loan, so that risk isn't ruled out by this data.

**Coin purchases between guilds, allowed vs. disabled** (barter and purchase counts tracked separately):

| | Barters/guild | Purchases/guild |
|---|---|---|
| All-greedy, purchases allowed | 0.2 | 3.3 |
| All-greedy, purchases disabled | 0.5 | 0.0 |
| All-casual, purchases allowed | 0.8 | 0.6 |
| All-casual, purchases disabled | 0.7 | 0.0 |

Disabling purchases no longer means "0 barters either way," as it did before the starting-hand fix — a small amount of genuine barter now clears on its own (0.2 → 0.5 barters/guild under skilled play, disabled vs. allowed), because the fix gives guilds complementary rather than lopsided surpluses. It's still a small effect, and **this result should not be read as settling the trading question** — see Findings above: with no price negotiation and no crafting-complement trading motive, this comparison is still showing what one hardcoded price threshold does, not what a flexible economy would do.

**Reward-pick order (winner-first vs. loser-first vs. random, mixed play, per-trial random):** score standard deviation 18.9 / 19.5 / 18.9, per-guild win-rate ratio 2.06× / 1.74× / 2.74× — no consistent pattern (random's 2.74× looks higher, but is within the noise range confirmed by Sweep D below at similar sample sizes). **Conclusion: no change** — this rule isn't a real lever on the fairness question.

**Per-guild fairness under identical (all-greedy) play** — the cleanest read on the rotation/starting-hand design itself, with no policy or skill-mix confound. **These numbers are after the starting-hand fix described in Findings above** — for comparison, before the fix this ranged from 3.3% (Gdansk) to 23.5% (Lisbon), a 7.2× spread:

| Guild | Win rate | Specialty |
|---|---|---|
| Bursa | 18.0% | Wax |
| Venice | 16.0% | Saltpetre |
| Gdansk | 14.0% | Saltpetre |
| Ghent | 13.5% | Flax |
| Lisbon | 11.3% | Wax |
| Prague | 9.8% | Charcoal |
| Stockholm | 8.7% | Flax |
| Vienna | 8.7% | Charcoal |

2.1× spread at 400 games, narrowing to 1.8× at 2000 games (checked separately) — consistent with ordinary sampling noise for an 8-way outcome around an expected 12.5% each, not a remaining structural effect.

Reproduce all four with `python3 -m sim.tuning_sweep`.

### Review history

This simulator went through three rounds of independent code review before merging its first version (see PR #1 in this repo's history for the full transcript) — an unpaired comparison letting sampling noise masquerade as a design effect, a biased deterministic tie-break, a missing coin-purchase mechanism, and a boolean config flag too narrow for a three-way variant, all found and fixed.

The loan-interest/coin-purchase tuning pass (PR #3) went through a second round covering three different kinds of review. A first pass (r1-r6) caught two real bugs in the writeup — the score-spread "distortion" claim was arithmetic, not behavioral, and a trade counter conflated barter with purchases, producing a factually wrong sentence — both fixed and covered by `tests/test_review_pr3_fixes.py`. A second pass, a dedicated fidelity audit (r2, r4-r6), checked the simulator mechanic-by-mechanic against the ruleset and found the specific simplifications (R1-R8) now documented throughout this file. Two of the audit's own numbers were themselves corrected mid-review after the reviewer traced their own claims back to the code rather than a docstring — recorded in Known simplifications above, not edited out. `tests/test_review_pr3_r2_fidelity_audit.py` covers what's fixed (R2, R8 reporting) and pins what's confirmed-but-not-fixed (R1, R7) as documented limitations.

A third pass (r7), reviewing the fix for R2 and the R8 investigation described above, went further than confirming them: it independently traced R8's root cause to the starting-hand table and proposed the fix now adopted (see Findings above). That claim was verified in this project before being adopted, not taken on trust — reproduced the exact same numbers (leftover inventory, mean score, win rate) independently, confirmed the mechanistic explanation programmatically against the recipe graph and hand table, checked the proposed fix didn't break the existing Round-1-craftability guarantee, and measured the actual before/after effect on the win-rate spread (7.2× → ~1.8-2.1×) rather than accepting the fix on the strength of the argument alone. `tests/test_review_pr3_r3_starting_hand_fix.py` covers all four properties (2-partner hand, Round-1 craftability, the fixed win-rate spread, and uniform leftover inventory).
