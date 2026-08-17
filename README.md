# European Legends — Office Adventure Game: Analysis

An independent review of the ruleset for *European Legends Office Adventure Game*, a charity team-building game being run for the EIB Group on 17 September 2026 (8 guilds, up to 40 players, ~100-minute trading/crafting/quest economy).

This repo is a working companion to the original ruleset, not a replacement for it — it doesn't reproduce quest content, only the structural/economic mechanics needed for analysis.

## Contents

- **[Written balance & design analysis](analysis/game-balance-analysis.md)** — now on revision 4, through three rounds of independent review (see §0 of the analysis for the full changelog). Also available as a [styled page](https://anselmotalotta.github.io/european-legends-analysis/).
- **`simulation/toy_scheduling_model.py`** — a small Monte Carlo model backing up the room-scheduling risk in §1/§7 of the analysis with actual numbers, not just assertion. Not the full economic simulation.
- **`simulation/rotation_schedule.py`** — finds and verifies the fixed room/opponent rotation recommended in §1 (capacity-correct, no repeated opponents, no same-specialty pairings) by exhaustive search, so the table in the analysis is reproducible rather than hand-typed.
- **`assets/`** — reference figures from the original document (item tiers, conversion chart, guild list).

## Status

- [x] Written analysis (v1)
- [x] Independent review of v1 — found real errors, incorporated (→ v2)
- [x] Independent review of v2 — mistakenly reviewed stale v1 content, false alarm; but 2 genuine gaps found and fixed (→ v3)
- [x] Independent review of v3 — found a real flaw in the proposed room rotation plus several precision issues, all fixed (→ v4)
- [ ] Further independent review of v4
- [ ] Full agent-based simulation (plan specified in §8 of the analysis)
