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

## The story

We were sent **[the original ruleset](analysis/original-ruleset-v1.docx)** — a charity game document for an EIB Group event, written by a colleague putting together a fun, trading-and-crafting adventure for 40 people, and asked to review it and validate it before it got used for real. What follows is what that turned into.

### Reading it properly, more than once

The first pass was a straightforward design review: read the rules closely, check the numbers against each other, and flag anything that looked unbalanced, contradictory, or risky for a live event with 40 people and a fixed 100-minute clock. That pass found real problems — a room-scheduling system with zero spare capacity that could leave guilds locked out of a room for the rest of the game, a starting-hand rule with a genuine math error in how it was analyzed, a loan penalty that was described incorrectly, a quest-scoring rule that contradicted itself, and a schedule with no slack anywhere in it for the ordinary friction of running a live event.

Rather than stop at one pass, that analysis was put in front of independent review, repeatedly — four rounds of it. That process wasn't smooth, and we're leaving the bumps in rather than editing them out: one review round turned out to be checking a stale, already-superseded version of the document (caught, diagnosed to a GitHub Pages caching delay, and fixed by making sure every future review pointed at the exact current commit). Another round caught a rotation schedule that solved room capacity perfectly but — undetected until someone checked — paired every guild against the *same* opponent for the entire game, which would have quietly undermined the event's own networking goal. Each round found something real, and each finding got fixed and re-verified rather than argued away. By the fifth revision, an independent reviewer's own assessment was that the analysis had gone from "good instincts, several material errors" to "genuinely strong" — worth building on rather than second-guessing further.

### From written argument to tested evidence

A written analysis can only go so far. Some of the most important questions — does this game actually require guilds to trade with each other, or can a well-run guild just play alone and win? how much does a loan penalty actually hurt the guilds that need one? — can't be settled by reading the rules more carefully. They need the game actually played, many times, under different conditions. So we built one: a small computer program that plays out the guild economy — production, crafting, room visits, trading, loans, scoring — hundreds of times per comparison, fast enough to test an idea in seconds instead of running a real rehearsal.

That simulator went through the same discipline as the written analysis: three rounds of independent code review before it was trusted, catching a real bug each time — including one subtle enough that the existing tests didn't catch it (the model gave silently different results between separate runs of the identical program, traced to how Python orders items internally, not to anything about the game). Every fix is backed by a regression test, and the whole thing is written so someone with no programming background can run it themselves in a few minutes and read what it found in plain English, not a wall of numbers.

### What the simulation actually found

Once the tool existed, we used it to settle the open questions with real numbers instead of guesswork — and it didn't just confirm what we expected, it corrected us twice.

- **The recommended fixed room schedule isn't marginally better than leaving room choice open — it's the difference between every guild finishing the game and roughly one in three not.** Under the same play quality, the fixed schedule gets 100% of guilds through all four rooms; open scheduling gets only 38%, with meaningfully more debt for everyone caught out by it.
- **Loans were quietly one of the least fair parts of the game.** Testing the loan penalty at different interest rates showed that the original "double" rate didn't just create more debt for guilds that needed a loan — it measurably widened the gap between guilds having a good game and guilds having a bad one. We lowered it to one and a half times the shortfall: still a real penalty, but a meaningfully fairer one, and this is now the adopted rule.
- **Whether the game needs trading turned out to have a more interesting answer than "yes" or "no."** Guilds that play well *do* end up trading — more often, in fact, than guilds that play carelessly. But almost all of that "trading" turned out to be one guild simply paying another guild coins for what it needed, not a genuine back-and-forth swap. Our first instinct was that removing the option to pay coins would push guilds toward real bartering instead — a reasonable-sounding fix. We tested it. It was wrong: take away coin purchases and skilled guilds don't start bartering more, they just stop trading with each other almost entirely. We're reporting that correction here rather than quietly dropping the idea, because it's a good example of why this project insisted on testing ideas instead of just implementing whatever sounded right.
- **A theorized "snowball" effect — the room winner always getting first pick of the reward, potentially letting one guild's early lead compound — tested as a non-issue.** Comparing winner-picks-first against loser-picks-first and random order showed no meaningful difference in fairness. So that rule was left exactly as originally written; not every plausible-sounding concern turns out to matter once you check.

### Where that leaves things

The [corrected ruleset](analysis/corrected-ruleset-v2.md) is not a rewrite — it's the same document, in the same shape, with each specific fix explained inline and a short table up front listing exactly what changed and why, so nothing was altered silently. Every change in it is backed by either a clear logical argument (the scheduling fix, the scoring contradiction, the loan-mechanics clarification) or by actual tested evidence (the loan interest rate, the trading behavior). It's available as a plain document to read and as a Word file in the same format the original arrived in, ready to hand to helpers or print, with the two things that still need the organizer's own input — each guild's special item and unique quest — clearly marked rather than guessed at.

The one thing we're not claiming: that this is now a finished, closed investigation. The simulator still runs on an abstracted, not-fully-real model of quest difficulty, and a couple of interesting open threads — why one guild's specialty seems to win more often than the others, and whether there's a better lever than coin purchases for encouraging real cross-guild interaction — are flagged honestly as unresolved in [`simulation/README.md`](simulation/README.md), not papered over. That felt like the right note to end on: confident about what's been checked, plain about what hasn't.

### The mechanics, for the curious

- **`simulation/toy_scheduling_model.py`** and **`simulation/rotation_schedule.py`** — small standalone scripts used to check specific claims in the written analysis (room-scheduling risk, the fixed rotation table) before the full simulator existed.
- **`assets/`** — reference figures from the original rules document (item tiers, conversion chart, guild list).
- The written analysis went through 5 revisions and 4 rounds of independent review (errors found and fixed each round — see §0 of the analysis for the full changelog) before being judged mature enough to move to simulation.
- The simulator went through 3 rounds of independent code review on its first version before merging, and the loan-interest/coin-purchase tuning pass above went through the same review process before being adopted — see the "Review history" section at the bottom of [`simulation/README.md`](simulation/README.md).
