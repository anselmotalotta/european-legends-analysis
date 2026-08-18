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
lowered from double to 1.5×, keeping a real penalty while choosing the
gentler of the tested rates for a charity event — that's a plain
values choice, though, not a fairness fix the numbers proved
necessary, since a closer check found neither the debt totals nor the
score-spread widening at higher rates are independent evidence of
anything (no guild's behavior actually changes with the rate). The
trading question — does this game need guilds to exchange items to do
well — is still genuinely open: an earlier answer to it was retracted
after a deeper audit found the simulator itself wasn't yet capable of
answering it either way. It also found and fixed a second real rule
problem: under identical play, individual guilds were winning between
3% and 24% of the time depending only on which guild they were — a
7-times gap traced to the starting-hand table (§10) giving half the
guilds a materially worse hand than the other half for reasons that
had nothing to do with the Round-1 rule it was designed around. Fixed
by picking the other, equally valid option for the affected guilds;
verified to bring the gap down to noise level. See the simulation's
README for the full picture.

---

## The story

We were sent **[the original ruleset](analysis/original-ruleset-v1.docx)** — a charity game document for an EIB Group event, written by a colleague putting together a fun, trading-and-crafting adventure for 40 people, and asked to review it and validate it before it got used for real. What follows is what that turned into.

### Reading it properly, more than once

The first pass was a straightforward design review: read the rules closely, check the numbers against each other, and flag anything that looked unbalanced, contradictory, or risky for a live event with 40 people and a fixed 100-minute clock. That pass found real problems — a room-scheduling system with zero spare capacity that could leave guilds locked out of a room for the rest of the game, a starting-hand rule with a genuine math error in how it was analyzed, a loan penalty that was described incorrectly, a quest-scoring rule that contradicted itself, and a schedule with no slack anywhere in it for the ordinary friction of running a live event.

Rather than stop at one pass, that analysis was put in front of independent review, repeatedly — four rounds of it. That process wasn't smooth, and we're leaving the bumps in rather than editing them out: one review round turned out to be checking a stale, already-superseded version of the document (caught, diagnosed to a GitHub Pages caching delay, and fixed by making sure every future review pointed at the exact current commit). Another round caught a rotation schedule that solved room capacity perfectly but — undetected until someone checked — paired every guild against the *same* opponent for the entire game, which would have quietly undermined the event's own networking goal. Each round found something real, and each finding got fixed and re-verified rather than argued away. By the fifth revision, an independent reviewer's own assessment was that the analysis had gone from "good instincts, several material errors" to "genuinely strong" — worth building on rather than second-guessing further.

### From written argument to tested evidence

A written analysis can only go so far. Some of the most important questions — does this game actually require guilds to trade with each other, or can a well-run guild just play alone and win? how much does a loan penalty actually hurt the guilds that need one? — can't be settled by reading the rules more carefully. They need the game actually played, many times, under different conditions. So we built one: a small computer program that plays out the guild economy — production, crafting, room visits, trading, loans, scoring — hundreds of times per comparison, fast enough to test an idea in seconds instead of running a real rehearsal.

That simulator went through the same discipline as the written analysis: three rounds of independent code review before it was trusted, catching a real bug each time — including one subtle enough that the existing tests didn't catch it (the model gave silently different results between separate runs of the identical program, traced to how Python orders items internally, not to anything about the game). Every fix is backed by a regression test, and the whole thing is written so someone with no programming background can run it themselves in a few minutes and read what it found in plain English, not a wall of numbers.

### What the simulation actually found

Once the tool existed, we used it to settle the open questions with real numbers instead of guesswork — and it didn't just confirm what we expected, it corrected us more than once, including one case where the correction was aimed at our own interpretation of the simulator's own output, not at the game.

- **The recommended fixed room schedule isn't marginally better than leaving room choice open — it's the difference between every guild finishing the game and roughly one in three not.** Under the same play quality, the fixed schedule gets 100% of guilds through all four rooms; open scheduling gets only 38%, with meaningfully more debt for everyone caught out by it.
- **Loan interest was lowered — and our first two explanations for why were both wrong, caught by two separate rounds of the same review process.** Testing different interest rates on the loan penalty showed debt scaling up with the rate, and score spread widening too. The first correction: strip the debt back out of the final score, and the outcomes are identical no matter the interest rate — nothing about how a guild plays actually changes based on the rate, so the wider spread is just arithmetic, not a fairness effect. We initially still treated the rising debt totals themselves as real evidence for the change. A later, deeper review round caught that this was the same mistake one level removed: the *number* of loans guilds take is identical at every interest rate too, since nothing in the model reads that number when deciding whether to borrow — so "more debt at higher interest" is just a fixed total times a bigger constant, not guilds struggling more. The real reason we lowered it to one and a half times the shortfall is, in the end, simpler than either of our first two explanations: it's a gentler penalty, chosen on its own merits for a charity event — a values choice, not something the simulation proved was necessary.
- **Whether the game needs trading — we had an answer, and then we didn't.** An earlier version of this project reported a specific, satisfying-sounding finding: guilds that play well do trade more, but almost all of it is one guild paying another in coins rather than a genuine swap, and removing that option doesn't produce more real bartering, it just makes guilds interact less. That finding survived one full round of independent review. A second, deeper audit — this one auditing the simulator's code against the actual rules, not just checking the analysis's logic — found it was standing on ground that wasn't solid: the simulated guilds can't negotiate a price (every trade clears at one fixed number) and never look for the specific kind of trade the rules actually create the most opportunity for (swapping raw materials to craft, not just paying for room access). A model that can't do either of those things isn't equipped to answer whether trading is necessary, in either direction. So we're retracting that finding here, not softening it — it's back to a genuinely open question, and we're leaving the record of having been wrong about it rather than quietly rewriting it away.
- **A theorized "snowball" effect — the room winner always getting first pick of the reward, potentially letting one guild's early lead compound — tested as a non-issue.** Comparing winner-picks-first against loser-picks-first and random order showed no meaningful difference in fairness. So that rule was left exactly as originally written; not every plausible-sounding concern turns out to matter once you check.
- **The real surprise came from a question we weren't even trying to answer — and this is the one with a genuinely happy ending.** While chasing down the trading and loan-interest corrections above, we found something nobody had been looking for: playing the exact same rules with every guild equally skilled, individual guilds win anywhere from 3% to 24% of the time, purely depending on which of the 8 guilds they are — a 7-times difference that has nothing to do with production specialty. We spent real effort trying to explain it (RNG quirks in how the simulator processes rooms, which opponents a guild happens to face, how smart the agents are about picking rewards) and ruled every one of those out one by one — one fix we tried to make the agents play more realistically actually made the gap *worse*, not better. We published that as an open, unsolved question. Within a day, an independent reviewer solved it: the starting-hand table (§10) gives each guild a fixed set of opening materials, and while every guild's hand was checked to satisfy the *one* requirement we'd designed it around (being able to afford its first room), nobody had checked a second, quieter requirement — whether a guild's own raw material was actually useful to craft with *the specific three items in its own hand*. For exactly half the guilds, it wasn't; they used their production once and then sat on dead stock for the rest of the game, while the other half kept converting all evening. We verified the finding independently — reproduced the exact numbers, and worked out the underlying mechanic ourselves from the recipe chart before checking it against the explanation we'd been given — and then verified the fix actually works: reassigning those guilds' starting hands to their other, equally valid option (one that still pays the first room's fee, but also leaves their production useful) brought the gap down from 7-times to something indistinguishable from ordinary luck. Adopted in the ruleset. This is the clearest example in the whole project of the simulator doing exactly what it was built for: finding a real, quantifiable, fixable balance problem that no amount of reading the rules would have surfaced.

### Where that leaves things

The [corrected ruleset](analysis/corrected-ruleset-v2.md) is not a rewrite — it's the same document, in the same shape, with each specific fix explained inline and a short table up front listing exactly what changed and why, so nothing was altered silently. Every change in it is backed by either a clear logical argument (the scheduling fix, the scoring contradiction, the loan-mechanics clarification) or by actual tested evidence (the fixed room schedule, the starting-hand fairness fix). It's available as a plain document to read and as a Word file in the same format the original arrived in, ready to hand to helpers or print, with the two things that still need the organizer's own input — each guild's special item and unique quest — clearly marked rather than guessed at, alongside the one thing that still needs further work: the trading question above.

The one thing we're not claiming: that this is now a finished, closed investigation. Quite the opposite — the deepest review round of this whole project happened *after* we thought the simulation work was essentially done, and it overturned more than it confirmed, though this time round it also handed us a genuine fix rather than just an open question. Two findings have now survived every single round of scrutiny and come out the other side as adopted rules: the fixed room schedule gets every guild through the whole game where open scheduling doesn't, and the corrected starting-hand table closes a real 7-times fairness gap. Everything else — the loan interest justification, and the trading conclusion — is flagged honestly as either a values choice or a genuinely open question in [`simulation/README.md`](simulation/README.md), not papered over. That felt like the right note to end on: confident about what's been checked and fixed, plain about what hasn't.

### The mechanics, for the curious

- **`simulation/toy_scheduling_model.py`** and **`simulation/rotation_schedule.py`** — small standalone scripts used to check specific claims in the written analysis (room-scheduling risk, the fixed rotation table) before the full simulator existed.
- **`assets/`** — reference figures from the original rules document (item tiers, conversion chart, guild list).
- The written analysis went through 7 revisions across 6 rounds of independent review (errors found and fixed each round — see §0 of the analysis for the full changelog) — four rounds reviewing the document directly, and two more indirectly, when code-level review of the simulator surfaced conclusions in the analysis that no longer held up (once for the retractions, once for the starting-hand fix).
- The simulator went through 3 rounds of independent code review on its first version before merging. The loan-interest/coin-purchase tuning pass that followed went through a second review cycle: a dedicated fidelity audit of the simulator's code against the actual rules (producing the retractions above), followed by a further round that traced the fairness gap to its root cause and proposed the fix, verified independently in this project before being adopted — see the "Review history" section at the bottom of [`simulation/README.md`](simulation/README.md).
