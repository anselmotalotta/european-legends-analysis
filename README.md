# European Legends — Office Adventure Game

## What this is

A charity team-building game ("European Legends Office Adventure
Game") is being run for the EIB Group on 17 September 2026 — 8 teams
("guilds") of 5 players, trading and crafting their way through a
100-minute in-person event. This repository holds an independent
review of that game's rules, a corrected/completed version of the
rules, and a computer simulation used to test how well the game
actually works before it's run for real.

## What's here

- **[The rules you should actually use](analysis/corrected-ruleset-v2.md)** — a corrected, ready-to-print version of the game's rules, with the fixes below already applied. Also available as a [Word document](analysis/corrected-ruleset-v2.docx) if that's easier to edit or print. **Start here if you just want the rules for the event.**
- **[Why those corrections were made](analysis/game-balance-analysis.md)** — the full written analysis behind the corrected rules: what was wrong or risky in the original rules and why, also available as a [styled web page](https://anselmotalotta.github.io/european-legends-analysis/).
- **[The simulator](simulation/README.md)** — a small program that plays hundreds of practice games to test open questions the written analysis couldn't answer alone (e.g. do teams actually need to trade with each other?). Includes step-by-step instructions for running it, no programming experience required.

## What's still open

Two things need input from the event organizer before the rules are
fully final:

- Each guild's special item and unique quest are still placeholders (marked clearly in the corrected rules).
- Whether the game's trading incentives need tuning is being investigated by the simulator, not yet conclusively answered.

---

## Project history

*(For anyone curious how this repo got here — not needed to use anything above.)*

- **`simulation/toy_scheduling_model.py`** and **`simulation/rotation_schedule.py`** — small standalone scripts used to check specific claims in the written analysis (room-scheduling risk, the fixed rotation table) before the full simulator existed.
- **`assets/`** — reference figures from the original rules document (item tiers, conversion chart, guild list).
- The written analysis went through 5 revisions and 4 rounds of independent review (errors found and fixed each round — see §0 of the analysis for the full changelog) before being judged mature enough to move to simulation.
- The simulator went through 3 rounds of independent code review (PR #1 in this repo) before merging — see the "Review history" section at the bottom of [`simulation/README.md`](simulation/README.md).
