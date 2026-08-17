# Simulator

An agent-based simulation of the guild economy described in
[`../analysis/game-balance-analysis.md`](../analysis/game-balance-analysis.md)
§8. Built per that section's guardrails:

1. **Every ambiguous rule (analysis §4) is a config flag with a documented default**, not a silent hard-code — see [`sim/config.py`](sim/config.py). Nothing here should be read as "the real rules definitely work this way"; several flags are explicit modeling choices pending clarification from the organizer.
2. **Multiple agent policies from day one** — see [`sim/policies.py`](sim/policies.py). `GreedyPolicy` reasons about shadow value and upcoming room needs (analysis §2.2); `CasualPolicy` treats items as flat liquidation values and crafts up greedily (the naive model the analysis's first draft used and corrected). Every decision point the analysis's §8 review round required — craft choice, room-access valuation, trade initiation/acceptance, and reward-card selection — is a genuinely different concrete rule between the two policies, not a shared implementation with a label swapped.
3. **Comparative, not predictive** — [`sim/experiment.py`](sim/experiment.py) runs paired batches (e.g. fixed rotation vs. free-choice scheduling) under the same policy mix, **using common random numbers across both arms** (same seed range, so both configs face the same skill draws/starting hands/shuffles), and reports the difference. Treat outputs as "design A differs from design B under these policies," not as a forecast of the real event's numbers.

## Review history

**r1** (commit `1d80903`) verified the economy against the original design document directly and found the core mechanics faithful, but flagged two real bugs and one significant, undisclosed scope gap — all fixed in the current commit:

- **F1 (fixed):** `compare()` ran its two arms on disjoint seed ranges despite claiming to be "paired" — every reported difference was design effect *plus* unmeasured sampling noise. Confirmed concretely: an unpaired run of the specialty win-rate metric showed a fully inverted ranking that vanished once seeds were shared. Now both arms of `compare()` use the same `seed_start` (common random numbers).
- **F2 (fixed):** room-score ties were resolved as `score_a >= score_b`, which silently made "guild A" (whichever guild is listed first in `FIXED_ROTATION`'s tuples) win every tie — not the random tie-break the source document specifies. Pulled into a pure `resolve_room_winner()` function and fixed to break ties randomly; `resolve_pick_order()` separately handles the §2.7/§8 reward-pick-order question, which is a different thing from who actually won.
- **F3 (fixed, and this changes the headline finding):** the original version had no way for a guild to buy a needed item with coins — only item-for-item trades were modeled, despite the source document saying guilds may exchange items "for coins or other items." This mattered a lot: a guild's shadow value for a needed item (up to 15) could exceed a seller's liquidation valuation of it (at most 14), and a coin side-payment is exactly what bridges that gap. **`seek_purchase`/`accept_purchase` are now implemented on both policies, and the previously-reported "greedy play produces ~0 trades" finding no longer holds** — see below.
- **F4 (fixed):** `winner_picks_reward_first` was a boolean, but §8's design-variant list has three cases (winner-first / loser-first / random), and "random" is also the source document's own rule for tie-breaking which *item* gets chosen. Replaced with `reward_pick_order: str`.
- Two smaller findings (reward-pool exclusion applying regardless of payment method; unconditional Tier-1→Tier-2 crafting quietly consuming would-be trade inventory) were judged harmless but are now called out in code comments rather than left silent.

See `tests/test_review_r1_fixes.py` for regression tests locking in each fix.

## Scope of this first version

Deliberately small, per the review's guardrail: the core economy, room
access, crafting, trading, loans, reward cards, and scoring are modeled
cleanly. **Not modeled**: guild-special Tier-3 items and unique
per-guild quests (analysis §2.6) — these are still "in elaboration" in
the source document, so there's nothing concrete to simulate yet.

## Known simplifications (stated, not hidden)

- **Quest performance is abstracted**, not content-simulated. Each guild draws a `quest_skill` in `[0, 1]` per room-quest and scores are read off each quest's own table (`sim/quests.py`) using that skill. This is a real simplification — actually simulating "identify 10 musical excerpts" would be noise dressed up as precision for an economy simulator. If quest-specific skill correlation matters later (e.g. "guilds good at music are also good at art"), that's a natural extension.
- **One trade attempt per guild per trading break.** A guild's policy proposes at most one trade and searches partners in random order until one accepts. This is not exhaustive matchmaking; a more thorough market-clearing mechanism is a plausible future refinement if trade volume turns out to matter a lot.
- **Free-choice scheduling requires 2 guilds per room to count as a valid visit** (matching "only two guilds can compete in each room in the same round" in the source), stricter than the standalone [`../toy_scheduling_model.py`](../toy_scheduling_model.py), which didn't model that constraint. This is why the full engine's free-choice completion rate (§ below) is somewhat lower than the toy model's 38.2% — not a bug, a more faithful constraint.

## Early findings from this version (illustrative, not final)

Running `python3 -m sim.experiment` (or see `tests/test_engine.py` / `tests/test_review_r1_fixes.py` for the pinned assertions), 400-game batches, paired seeds:

- **The §1 fixed rotation reaches 100% room completion by construction**, vs. ~37% for free-choice scheduling under the same policies — reproducing the standalone toy model's ~38.2% finding inside the full economic engine, not just the isolated scheduling model.
- **Trading is no longer near-zero under rational play, now that coin purchases are modeled (F3 above).** All-greedy: mean 2.7 trades/guild, 5% of guilds finish with zero trades (previously ~2.7 vs. 0, and 5% vs. 100% before the fix). The self-sufficient "solo chaining" mechanism from §2.5 is still real and still visible — greedy guilds trade far less than casual ones — but it does **not** eliminate trading once a coin side-payment is available to bridge the shadow-value/liquidation-value gap. **Revised takeaway: the room-circuit's type-converting reward mechanic reduces reliance on trading, but doesn't make it unnecessary once guilds can pay coin premiums for exactly what they need.** This is a materially different conclusion from the pre-fix version of this document, which should be treated as superseded.
- **Casual and mixed policy mixes still produce meaningfully more loan debt than all-greedy play** (mean debt/guild: ~13 casual vs. ~1.3 greedy) — behavior quality matters a lot for who ends up in debt, independent of the trading question.
- **Specialty win-rate is not stable across policy mixes** in this version — Charcoal-specialty guilds (Prague/Vienna) lead under all-greedy and all-casual play, but Flax/Saltpetre lead under a 50/50 mix, with Charcoal trailing. This looks more like noise or a mix-dependent interaction than a fixed structural bias, but it's not yet explained (§8 item 8) — worth investigating further before drawing any conclusion about guild-specialty fairness, and worth more trials than the ones run so far given how much the ranking moved between mixes.

These are first-version results from one specific implementation of "rational" and "casual," not conclusions about the real event — see the caveats above. They have already changed once (see review history) and may change again as the model is extended.

## Running it

```bash
cd simulation
python3 -m pytest tests/ -v      # 32 tests, ~0.3s
python3 -m sim.experiment         # comparative batches, prints JSON summaries
```

No dependencies beyond the Python 3 standard library and `pytest` for tests.

## Layout

- `sim/items.py` — Tier-1/2/3 items, the conversion recipe graph, room prerequisites, sell prices.
- `sim/config.py` — frozen rules interpretation; every §4 ambiguity is a flagged default here.
- `sim/rotation.py` — the verified fixed room/opponent rotation and starting-hand coordination from analysis §1/§2.1.
- `sim/guild.py` — per-guild state (coins, inventory, loans, rooms visited, trades).
- `sim/quests.py` — quest scoring (abstracted skill model, see above).
- `sim/policies.py` — `GreedyPolicy` and `CasualPolicy` agent behaviors.
- `sim/engine.py` — the round-by-round game loop.
- `sim/metrics.py` — aggregate statistics across many games.
- `sim/experiment.py` — comparative batch runner.
- `tests/` — pytest suite covering recipes, rotation integrity, loan math, end-to-end engine behavior, and review r1's fixes (`test_review_r1_fixes.py`).

## Not yet done (left for a future iteration)

- Shadow-value-by-round and marginal per-room expected value (analysis §8 items 6-7) — need price inference / counterfactual re-runs, not just bookkeeping.
- Guild-special items and unique quests (§2.6), once finalized in the source.
- A more thorough trade-matching mechanism (still one attempt per guild per break, now across two instruments - barter and coin purchase - rather than one).
- Explaining the specialty win-rate instability noted above (§8 item 8) rather than just reporting it.
- The full §8 design-variant sweep (loan interest, Tier-3 prices, reward-pick-order, mandatory trading windows) - `sim/experiment.py` and `sim/config.py`'s `reward_pick_order` support this now, but only the rotation comparison is wired up as a worked example.
