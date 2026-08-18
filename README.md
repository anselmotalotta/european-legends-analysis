# European Legends — Office Adventure Game

A charity team-building adventure game for the EIB Group, played by 8
guilds of 5 players over a 100-minute event on 17 September 2026.
Guilds produce and trade raw materials, craft them into more valuable
goods, and compete in four themed activity rooms — music, art,
history, riddles — to raise money for charity and finish with the
most coins.

## The rules

**[Read the rules](analysis/corrected-ruleset-v2.md)** — everything
needed to run the event: setup, the 100-minute schedule, the guilds,
the trading/crafting economy, the four activity rooms and their
quests, and scoring. Also available as a
[Word document](analysis/corrected-ruleset-v2.docx) if that's easier
to edit or print.

Two things are still placeholders, marked clearly in the rules, and
need the organizer's input before the event: each guild's special item
and unique quest.

## Background

The rules above are a corrected version of an earlier draft. An
independent design review found and fixed several real issues in that
draft — an unbalanced room schedule, a scoring contradiction, and
others. **[Read the full analysis](analysis/game-balance-analysis.md)**
(also as a [styled page](https://anselmotalotta.github.io/european-legends-analysis/))
for the reasoning behind each fix.

To answer questions the written analysis couldn't settle on its own, a
**[computer simulation](simulation/README.md)** plays through hundreds
of practice games and reports back what tends to happen — includes
step-by-step instructions to run it yourself, no programming
experience required. It's already changed one rule: loan interest was
lowered from double to 1.5× after testing showed the original rate
measurably widened the gap between stronger and weaker guilds. It also
answered the trading question, with a twist — guilds do need to
exchange items to do well, but skilled play satisfies that mostly
through coin purchases rather than genuine back-and-forth barter, and
testing found that simply restricting purchases doesn't fix that, it
just reduces how much guilds interact at all. See the simulation's
README for the full picture.

---

## Project history

*(For anyone curious how this repo got here — not needed to use anything above.)*

- **`simulation/toy_scheduling_model.py`** and **`simulation/rotation_schedule.py`** — small standalone scripts used to check specific claims in the written analysis (room-scheduling risk, the fixed rotation table) before the full simulator existed.
- **`assets/`** — reference figures from the original rules document (item tiers, conversion chart, guild list).
- The written analysis went through 5 revisions and 4 rounds of independent review (errors found and fixed each round — see §0 of the analysis for the full changelog) before being judged mature enough to move to simulation.
- The simulator went through 3 rounds of independent code review (PR #1 in this repo) before merging — see the "Review history" section at the bottom of [`simulation/README.md`](simulation/README.md).
