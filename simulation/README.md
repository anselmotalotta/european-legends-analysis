# Simulator

An agent-based simulation of the guild economy described in
[`../analysis/game-balance-analysis.md`](../analysis/game-balance-analysis.md)
§8. Built per that section's guardrails:

1. **Every ambiguous rule (analysis §4) is a config flag with a documented default**, not a silent hard-code — see [`sim/config.py`](sim/config.py). Nothing here should be read as "the real rules definitely work this way"; several flags are explicit modeling choices pending clarification from the organizer.
2. **Multiple agent policies from day one** — see [`sim/policies.py`](sim/policies.py). `GreedyPolicy` reasons about shadow value and upcoming room needs (analysis §2.2); `CasualPolicy` treats items as flat liquidation values and crafts up greedily (the naive model the analysis's first draft used and corrected). Every decision point the analysis's §8 review round required — craft choice, room-access valuation, trade initiation/acceptance, and reward-card selection — is a genuinely different concrete rule between the two policies, not a shared implementation with a label swapped.
3. **Comparative, not predictive** — [`sim/experiment.py`](sim/experiment.py) runs paired batches (e.g. fixed rotation vs. free-choice scheduling) under the same policy mix and reports the difference. Treat outputs as "design A differs from design B under these policies," not as a forecast of the real event's numbers.

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

Running `python3 -m sim.experiment` (or see `tests/test_engine.py` for the pinned assertions):

- **The §1 fixed rotation reaches 100% room completion by construction**, vs. ~37% for free-choice scheduling under the same policies — reproducing the standalone toy model's ~38.2% finding inside the full economic engine, not just the isolated scheduling model.
- **Under fully rational (`greedy`) play on both sides, spontaneous trading essentially never happens** — in 100-game batches, 0 completed trades. Tracing why: the reward-card mechanic (§2.3/§2.5) lets greedy guilds self-provision so precisely that they rarely hold genuine surplus, and when a rational guild does propose a trade, the partner almost always values what's being asked for (something both guilds structurally need at the same time) more than what's being offered. This is a real, direct empirical input to the analysis's central open question in §2.5 — under this model, rational solo chaining dominates over trading, at least when all guilds play identically well.
- **Mixed and casual policy mixes do produce trades** (casual guilds create real surplus/mismatches a rational neighbor can profit from), and produce meaningfully more loan debt than all-greedy play. This suggests trading volume in the real event may depend more on skill/behavior heterogeneity among the 40 actual players than on the base economic structure — worth keeping in mind when the organizer reads "does this game need trading" results from later, more thorough runs.

These are first-version results from one specific implementation of "rational" and "casual," not conclusions about the real event — see the caveats above.

## Running it

```bash
cd simulation
python3 -m pytest tests/ -v      # 25 tests, ~0.2s
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
- `tests/` — pytest suite covering recipes, rotation integrity, loan math, and end-to-end engine behavior.

## Not yet done (left for a future iteration)

- Shadow-value-by-round and marginal per-room expected value (analysis §8 items 6-7) — need price inference / counterfactual re-runs, not just bookkeeping.
- Guild-special items and unique quests (§2.6), once finalized in the source.
- A more thorough trade-matching mechanism, if the "greedy play produces ~0 trades" finding above turns out to be worth investigating further rather than accepting as a real result.
- The full §8 design-variant sweep (loan interest, Tier-3 prices, winner/loser-picks-first, mandatory trading windows) - `sim/experiment.py` has the scaffolding (`compare()`) but only the rotation comparison is wired up as an example.
