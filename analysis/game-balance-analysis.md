# European Legends — Office Adventure Game: Balance & Design Analysis

**Reviewed document:** *European Legends Office Adventure Game*, v. 16 August 2026
**Event:** EIB Group charity game, 17 September 2026, up to 8 guilds × 5 players
**Revision 5** — see [§0](#s0) for what changed and why, and a note on document conventions used from revision 3 on.

**Reference figures from the source document:**

![Items by tier](../assets/items-and-tiers.jpg)
![Conversion chart](../assets/conversion-chart.png)
![Guilds](../assets/guilds.jpg)

---

## <a id="s0"></a>0. What changed in this revision

An independent reviewer found three reasoning errors in the first draft, one of which invalidated a central recommendation, plus several important dynamics the first draft didn't examine at all. Rather than patch around them, this revision reworks the affected sections from scratch. In order of how much they change the conclusions:

1. **§2.1 was mathematically wrong.** The claim that a guild's starting hand *determines* which single Tier‑2 item it can craft is false — every starting hand supports **two** feasible recipes, not one. This breaks the original "deal starting kits to control room demand" recommendation. Corrected below, with a working replacement.
2. **§2.2's loan math overstated the penalty** in the typical case (guilds start with 10 coins, so most loans cover a shortfall of a few coins, not the full 15) and the "eliminated by round 2" line was an unsupported claim, now downgraded to an explicit open question for the simulation.
3. **The whole economic framing was too simple.** Sale prices (1/4/14/20 coins) are not the same as strategic value — a Tier‑2 item is also an admission ticket, and the reward mechanic (pay one Tier‑2, receive a *different* one) changes the real cost of room entry substantially. New §2.2–§2.4 below.
4. **A likely rules contradiction was missed** (generic quest scoring says even numbers only; several individual quests can score odd numbers) — now in §4, ranked near the top per the reviewer's suggestion.
5. **The "unmanaged scheduling is the default outcome" claim in §1 was asserted, not measured.** It's now backed by a toy Monte Carlo model (§7) instead of assertion, and the fixed-rotation recommendation now comes with a concrete, checked schedule instead of just "use a Latin square."
6. **A new central question is now the headline of the whole document**: does this game actually require cross-guild trading, given guilds can self-produce, craft, and exchange Tier‑2 items at rooms without ever dealing with another guild? See §2.5 — networking is a stated purpose of the event, so this is not a side issue.
7. Timing analysis (§3) now leads with the fact that the 100-minute schedule has **zero global slack**, which is a bigger operational risk than any single room's internal buffer.
8. §5 (Guildhall) reframed around throughput/protocol design rather than headcount.

**Revision 3 adds two things a second independent review caught that revision 2 had genuinely missed** (the rest of that review's comments turned out to be about revision 1 — see the note below):

9. **§2.7 is new**: loans aren't the only positive/negative-feedback mechanism in this game. The room-winner picking their Tier‑2 reward first, and the +5 room-win bonus itself, both compound in favor of guilds that are already ahead — arguably a bigger snowball risk than loans, and previously unexamined.
10. **Confidence labels added throughout** — claims are now tagged `[Established]`, `[Derived]`, `[Risk — plausible, not yet measured]`, or `[Open — needs simulation]` so the document doesn't read as more settled than it is. See the convention note just below.

> **A note on document versions:** a second independent review of this document was received, but it quoted several passages (e.g. the original, incorrect starting-hand claim, and the "forces cross-guild trading" line) that revision 2 had already removed or corrected. The most likely explanation is a GitHub Pages build delay during a GitHub-wide outage on 2026‑08‑17, which left the published page briefly showing revision 1 after revision 2 had already been committed. If you're reviewing this document, please check you're reading the current commit on `main`, not a cached copy of the page.

> **Confidence labels used from here on:** `[Established]` = stated directly in the source rules. `[Derived]` = follows deductively from the rules (shown with the derivation). `[Risk — plausible, not yet measured]` = a credible concern that hasn't been quantified. `[Open — needs simulation]` = a question the written rules genuinely cannot settle either way. Not every sentence is labeled — only the load-bearing claims — but the goal is that no claim in this document should read as more certain than it actually is.

**Revision 4 fixes a real, high-priority flaw a third review found in the §1 rotation, plus several precision issues — this time all against the actual current document, not a stale one:**

11. **The §1 rotation was a real design mistake, now fixed.** The original fixed rotation solved room capacity by construction, but it also — unintentionally — paired every guild with the *same* opponent in all 4 rounds (Lisbon always vs. Bursa, etc.), which directly undercuts the event's networking purpose and lets a stronger guild repeatedly claim the winner's-first-pick advantage (§2.7) against the same weaker guild four times running. Replaced with a schedule, verified in code, where every guild still visits all 4 rooms once but faces a **different opponent every round with zero repeats**.
12. **The toy scheduling model's description was imprecise.** It does *not* model "no visibility" — the code gives each guild perfect knowledge of which rooms still have capacity before it chooses. Corrected to "sequential random choice with full knowledge of current availability, no negotiation or anticipation." The 38.2% result itself is unchanged and still valid for the model as actually implemented; only its description and interpretation were wrong.
13. **"Lower-bound-ish worst case" was an unsupported framing** — real players could do better (negotiation) or worse (confusion, concurrent decisions, imperfect queue visibility) than the toy model. Reworded as a policy-specific baseline, not a bound in either direction.
14. Smaller precision fixes: the starting-hand section overstated the players' residual randomness (§2.1); §2.3's "net asset loss ≈ 0" now explicitly separates liquidation value from strategic value; the "shared 3-card reward pool" reading is now flagged as an interpretation to confirm (§4); §8 gained an opponent/interaction-diversity metric, since "number of trades" alone doesn't measure networking; §9's priority order now leads with the rotation fix.

**Revision 5 fixes a fourth review's findings — this one caught a claim in revision 4 that was itself checked and found false, not just imprecise:**

15. **§1's claim that the corrected rotation gives opponents "spanning both other production specialties" was wrong**, verified computationally: under this table every guild meets only 2 of the other 3 specialty-pairs, never all 3 (e.g. Lisbon meets flax and charcoal guilds, never saltpetre). Full 3-specialty coverage turns out to be reachable only by allowing each guild to meet its own twin exactly once — a genuine design tradeoff, not adopted here — so the false claim is corrected rather than the schedule redesigned again.
16. **§2.3's coin-admission accounting mixed up cash outflow (−15) with net wealth change (−11)**, inconsistent with the section's own liquidation-vs-strategic-value framing — corrected.
17. **§2.5 overstated that a reward-pool collision makes trading "necessary"** — a guild could instead craft the needed item itself later. Softened to "creates pressure to," not "requires."
18. **"Verified by exhaustive search" overstated what the rotation script actually does** — it's a constraint search that stops at the first valid schedule, then checks that one schedule exhaustively, not an enumeration of every possible schedule. Corrected in both the analysis and the script's own docstring.
19. **§8's "rational vs. casual" agent behavior needed concrete specification, not a label** — added explicit requirements for craft-choice, room-access valuation, trade initiation/acceptance, inventory reasoning, and reward-card selection policies before the full simulation can be implemented meaningfully.

---

## 1. Structural risk: room scheduling has no coordination mechanism

`[Established]` Each round, 4 activity rooms × 2 guild slots = exactly 8 slots — one per guild. Over 4 rounds that's 32 slots, exactly enough for all 8 guilds to visit all 4 rooms once each.

`[Derived]` Nothing in the rules guarantees that ideal matching happens on its own — guilds choose/race for rooms, constrained only by "two other guilds already paid their participation fee" locking a room. The system therefore has **zero spare capacity**: one bad allocation early can leave a guild locked out of a room it still needs for the rest of the game.

`[Derived from a toy model — a policy-specific baseline, not a bound in either direction]` (see §7 for method): under a model where guilds pick, one at a time in random order, uniformly at random among rooms they haven't visited that still have a free slot — i.e. sequential random choice **with full knowledge of current room availability**, but no negotiation and no anticipation of what happens later in the round — only **38% of games** end with all 8 guilds having visited all 4 rooms, and **18% of individual guild-slots end up missing a room**, even though total capacity exactly matches total demand. This isn't a lower or upper bound on the real event (real players might do better via negotiation, or worse from concurrent decisions and imperfect queue visibility) — it's evidence that **an allocation problem exists under this policy**, not an estimate of how often it will actually occur on the day. An independent reviewer's quick check using the same approach landed within 1 point of this figure (38% vs. 38.4%).

### Recommendation: a rotation that solves capacity *and* keeps opponents varied

A fixed, pre-printed 4-round rotation removes the coordination problem entirely, guaranteed by construction (not a probabilistic improvement). **A first version of this table had a real flaw**, caught in review: splitting the 8 guilds into two groups of 4 and cycling each group through the rooms independently does guarantee capacity, but it also pairs every guild against the *same* opponent in all 4 rounds (e.g. Lisbon vs. Bursa every single time) — bad for the event's stated networking purpose, and it lets a stronger guild repeatedly claim the winner's-first-pick advantage (§2.7) against the same weaker guild four times running, compounding rather than varying.

The table below fixes that: every guild still visits each room exactly once, but **no guild ever faces the same opponent twice**, and no guild ever faces its own same-specialty "twin" (Lisbon/Bursa, Stockholm/Ghent, Gdansk/Venice, Prague/Vienna both make the same Tier‑1 material) — found by constraint search and programmatically verified (a depth-first search that stops at the first schedule satisfying all constraints, then checks that schedule exhaustively — not an enumeration of every possible schedule), not eyeballed. Generated by, and reproducible with, [`simulation/rotation_schedule.py`](../simulation/rotation_schedule.py):

| Round | Room 1 (Cloth) | Room 2 (Dye) | Room 3 (Black Powder) | Room 4 (Candle) |
|---|---|---|---|---|
| 1 | Lisbon, Stockholm | Bursa, Ghent | Gdansk, Prague | Venice, Vienna |
| 2 | Gdansk, Vienna | Venice, Prague | Lisbon, Ghent | Bursa, Stockholm |
| 3 | Ghent, Venice | Stockholm, Gdansk | Bursa, Vienna | Lisbon, Prague |
| 4 | Bursa, Prague | Lisbon, Vienna | Stockholm, Venice | Ghent, Gdansk |

Every guild's 4 opponents across the game are 4 distinct guilds. **Correction:** an earlier version of this paragraph claimed those opponents "span both other production specialties" — checked computationally, that's false as this table stands: `rotation_schedule.py` only enforces room-once-per-guild, opponent-distinctness, and no-twin-pairing, not full specialty coverage, and in fact every guild here meets only 2 of the 3 non-own specialty-pairs across its 4 opponents (e.g. Lisbon meets both Stockholm/flax and Ghent/flax, plus both Prague/charcoal and Vienna/charcoal, but never Gdansk or Venice/saltpetre). Achieving full 3-specialty coverage turns out to require each guild to meet its own twin exactly once (using one of the 4 opponent slots on the twin, leaving exactly one slot for each of the other 3 specialties) — a real design option, but a different tradeoff than "never meet your twin," so it isn't adopted here without that being a deliberate choice. What this table *does* still guarantee, verified: room-once-per-guild, no repeated opponent, and no guild meeting its own twin at all.

This table is also the input the starting-hand fix in §2.1 needs — the two have to be designed together, or fixing one can force loans via the other.

---

## 2. Economic balance

### 2.1 Starting hands: two feasible recipes, not one — corrected

`[Established]` The four Tier‑1 materials form a 4-cycle: **Flax–Wax → Candle, Wax–Charcoal → Dye, Charcoal–Saltpetre → Black Powder, Saltpetre–Flax → Cloth.** Diagonal pairs (Flax+Charcoal, Wax+Saltpetre) don't convert to anything.

`[Derived]` Each guild starts with 3 random *different* Tier‑1 items — missing exactly one of the four types. **The first draft of this analysis claimed the missing type determines which single Tier‑2 item the guild can craft. That's wrong.** Removing one node from a 4-cycle leaves a 3-node path with a shared middle ("hub") item — which means the guild can only *manufacture* one card (it holds only one unit of the hub item), but it has a **choice of two** possible recipes, both using that hub item:

| Missing material | Starting materials | Tier‑2 choices (pick one) |
|---|---|---|
| Flax | Wax, Charcoal, Saltpetre | Dye **or** Black Powder |
| Wax | Flax, Charcoal, Saltpetre | Black Powder **or** Cloth |
| Charcoal | Flax, Wax, Saltpetre | Candle **or** Cloth |
| Saltpetre | Flax, Wax, Charcoal | Candle **or** Dye |

This matters because it **invalidates the original recommendation** to deal starting kits so exactly 2 guilds are missing each Tier‑1 type. That controls the *aggregate opportunity set* (which items exist to be crafted, symmetrically), but it does not control *what guilds actually choose to craft* — four guilds could all independently choose Candle from four different starting hands and none choose the other options. Controlled dealing produces **symmetrical opportunity, not balanced demand.**

**The actual deterministic fix** is to design starting hands *against the room rotation* (§1), not against aggregate symmetry: guarantee each guild's starting hand supports crafting the specific Tier‑2 item its **assigned first room** requires. Since each of the four possible "missing" choices supports exactly two Tier‑2 outputs, and each Tier‑2 output is supported by exactly two possible "missing" choices, this is always achievable — e.g. for the corrected rotation in §1, Round‑1 assignments require:

| Guild | Round‑1 room needs | Guild's hand must **not** be missing | So the hand should be missing |
|---|---|---|---|
| Lisbon, Stockholm | Cloth (Flax+Saltpetre) | Flax, Saltpetre | Wax or Charcoal |
| Bursa, Ghent | Dye (Wax+Charcoal) | Wax, Charcoal | Flax or Saltpetre |
| Gdansk, Prague | Black Powder (Charcoal+Saltpetre) | Charcoal, Saltpetre | Flax or Wax |
| Venice, Vienna | Candle (Flax+Wax) | Flax, Wax | Charcoal or Saltpetre |

This guarantees every guild can pay its Round‑1 room fee from its opening hand — removing the "10 coins isn't enough for the 15-coin fallback" problem entirely for round 1. Note this doesn't remove randomness from the player's point of view: the organizer is choosing which one of the four materials to withhold, but the deal can still look and feel arbitrary to players, since the specific 3 items they end up with are still whatever's left after that one omission is fixed and haven't been announced or predictable in advance.

### 2.2 Tier‑2 items are admission rights, not 4-coin commodities

The original draft compared items purely by end-game sale price (Tier 1 = 1, Tier 2 = 4, Tier 3 = 14) and concluded crafting up the chain is "strictly worth doing." **That conflates sale price with strategic value, and it's the biggest conceptual gap in the first draft.**

`[Derived]` A Tier‑2 item is also the entry ticket to a room that otherwise costs **15 coins** in cash. Its *shadow value* right before a guild's next required room visit is much closer to "the coins it saves" than to its 4-coin liquidation price. Concretely: a guild holding two Tier‑2 cards can either (A) craft them into a Tier‑3 card — nominal gain 8→14, +6 coins — or (B) hold one back to pay for an unvisited room's entry, avoiding a 15-coin cash cost. Depending on which rooms are still unvisited, (B) can be worth far more than (A). **Crafting up the chain before a guild's room obligations are satisfied can be a mistake, not a free win.**

The general point: this game has **time-dependent, endogenous item values**, not a fixed price ladder — value depends on the round, which rooms remain unvisited, future recipe needs, and how many coins the guild has on hand as a substitute. That's a more interesting design than a flat price sheet, and it's something the simulation needs to model at the level of individual item identity, not aggregate item counts (see §2.5, §8).

### 2.3 The room reward loop makes item-based and coin-based admission very unequal

Room entry isn't just "spend one Tier‑2 item." After completing a room, the guild **exchanges** it: *"guilds choose a new tier 2 item, different than the one they paid to participate."* So paying with an item is closer to a swap than a cost:

- **Item admission:** surrender a card worth 4 (liquidation) → receive a different card worth 4. Net *liquidation* value is unchanged (4 → 4), plus the guild earns quest coins and possibly the 5-coin room-win bonus.
- **Coin admission:** surrender 15 real coins → (apparently) receive the same reward card worth 4 in liquidation. Cash outflow is 15 coins, but net *wealth* change (coins spent minus the value of what's received) is **−11, not −15** — worth being precise here since the rest of this section is explicitly about not confusing different quantities.

That's a large asymmetry, and it means **holding the correct Tier‑2 prerequisite going into a room may be one of the strongest strategic assets in the game** — a much bigger deal than the original draft's framing of items as interchangeable "4-coin" units. Worth being precise here, given §2.2's point about shadow value just above: "net liquidation loss ≈ 0" is true in sale-price terms, but the *strategic* swing can be large in either direction — surrendering an item you no longer need for one you desperately need next is a big win, and the reverse (forced into a card you don't need, per §2.5's reward-pool collision case) is a real loss even though the liquidation arithmetic nets to zero either way.

Two open questions this surfaces: **does a guild that pays the 15-coin fallback also receive a reward Tier‑2 card afterward?** The rule text ("different than the one they paid") reads as if it assumes item-based payment. If coin-payers get no reward card, the 15-coin path is even worse than the comparison above; if they do, it's exactly as described. And: **is the "3 available items" reward genuinely one pool shared by both guilds in the room, with cards removed as each guild picks** (the reading §2.5's scarcity argument depends on), or does each guild separately see its own set of 3? Both added to §4's ambiguity list and should be resolved before simulating.

### 2.4 Loans: the shortfall is usually much smaller than 15 coins — corrected

`[Derived]` The original draft assumed a "round‑1 loan of 15 coins costs 30 at the end," implying every loan is a 15-coin loan. The rule text says the GM lends **the missing amount**, not the full fee. Guilds start with 10 coins, so a guild needing the 15-coin fallback and still holding its starting coins needs a loan of only **5**, repaid at double = **10** at game end — not 30. A 15-coin loan only happens if a guild has already spent down to zero coins by the time it needs the fallback, which is a real possibility later in the game but not the round‑1 default case.

`[Open — needs simulation]` The stronger claim in the first draft — *"a guild can be mathematically eliminated from contention by round 2 without any player mistake"* — was asserted without supporting math and should be treated as an open hypothesis, not a finding. The honest version: **loans can create negative feedback (weaker guilds risk taking on more debt, which weakens them further), but how severe that feedback loop actually is depends on quantities the written rules don't fully pin down (whether coin-payers get reward items, how often the 15-coin path is actually needed) and needs to come from the simulation, not from reading the rules alone.** Loans are also not the only such mechanism — see §2.7.

### 2.5 The central open question: does this economy actually require trading?

`[Open — needs simulation]` This is arguably the most important thing the first draft missed, and it cuts against one of its own "what's working well" claims (that the recipe cycle "forces genuine cross-guild trading").

`[Derived]` Consider a guild that never trades with anyone: it crafts one Tier‑2 item from its starting hand (§2.1), pays into its Round‑1 room, and receives a *different* Tier‑2 item as a reward (§2.3). If that reward happens to be the item needed for an unvisited room, it can pay into that room next, receive yet another new Tier‑2 item, and so on — potentially chaining through all four rooms using only its own starting hand and the reward mechanic, without ever needing another guild's items. Guilds also self-produce increasing quantities of their own Tier‑1 specialty each round, giving them raw material for further crafting entirely in-house.

This isn't guaranteed to work every time, though, and the reason why is itself an interesting design detail: **each room seats 2 guilds sharing one reward pool of 3 cards.** The winner picks first. If both guilds in a room happen to want the same next-room item, the loser is forced to take something else — which creates pressure to trade or fall back to a coin payment, though not strictly a requirement to: the guild could instead craft the needed item itself later from its own Tier‑1 production, if time and materials allow. So scarcity, and therefore the incentive to trade, may be concentrated entirely in these two-guild reward collisions, rather than being a constant pressure created by the recipe graph itself as originally claimed.

Given that networking is an explicit stated purpose of the event, **whether the current rules create enough scarcity to make trading necessary — or whether a self-sufficient "solo chaining" strategy can win without ever talking to another guild — should be one of the first things the simulation measures**, ahead of any tuning of loan interest or Tier‑3 prices. The "recipe graph forces trading" claim is removed from §6 below pending that result.

### 2.6 Guild special items and unique quests are marked "in elaboration"

`[Established]` The 20-coin guild-special-item bonus and each guild's unique 15–20 coin quest aren't defined yet in this draft. They're relevant to §2.4's catch-up question and to guild identity — worth finishing before final simulation runs, since guild-specific asymmetries will shift the results.

### 2.7 Loans aren't the only snowball mechanism — two more that compound in favor of guilds already ahead

The first draft treated loan debt as *the* negative-feedback mechanism in this game. It isn't the only one, and the other two arguably matter more because they reward guilds for *winning*, not just penalize guilds for *losing* — meaning they could compound with loans rather than offset them.

`[Derived]` **1. The room winner picks their Tier‑2 reward first.** *"The winners choose first from 3 available items, the losers choose second."* A guild that's already ahead on quest skill doesn't just bank more coins — it also gets first pick of its next strategic asset (§2.3), which can determine whether it can chain straight to its next room (§2.5) or has to trade/pay coins instead. That's a second, compounding advantage stacked on top of the score itself.

`[Derived]` **2. The +5 room-win bonus is positively correlated with quest skill, not independent of it.** The bonus goes to whichever guild already scored more coins in that room's two quests — i.e. it's added on top of an existing lead, not distributed independently. A guild strong at the specific skills a room tests (music knowledge, spatial puzzles, trivia) gets rewarded twice for the same underlying advantage.

`[Open — needs simulation]` Together with loan debt, this gives the game **three separate mechanisms that could each push in the same direction**: quest-skilled/lucky guilds get more coins (+5 bonus), better future inventory (first pick), and avoid debt (no loans needed) — while weaker guilds get none of those and *also* accrue loan interest. Whether these compound into a runaway lead for whichever guild does well early, or are damped out by the game's other randomness (starting hands, room rotation, quest variety), is exactly the kind of question the written rules can't answer and the simulation should measure directly (added to §8).

`[Derived]` This is also why the §1 rotation fix mattered beyond just capacity: the original (flawed) rotation paired every guild against the same opponent all 4 rounds, which would have let this compounding advantage snowball against one specific weaker guild all game — win once, get the bonus and first pick, arrive stronger at the rematch, win again. The corrected rotation (different opponent every round) doesn't eliminate the compounding mechanism itself, but at least stops it from concentrating repeatedly against a single guild.

One concrete, testable alternative worth including in the simulation rather than just flagging: **a rubber-banding variant where the room-losing guild picks its reward card first instead of the winner.** This wouldn't need to be adopted, but comparing final-score variance under winner-first vs. loser-first vs. random-order selection (§8) would directly measure how much of this snowball is attributable to this one rule, versus the +5 bonus or loans.

---

## 3. Timing

### 3.1 The schedule has zero global slack — the bigger risk

Opening (10) + 4×activities (40) + 3×trading breaks (30) + final trading (10) + final briefing (10) = **100 minutes exactly**, with no built-in contingency anywhere for a briefing running long, a puzzle needing a reset, a scoring dispute, AV trouble, or simple congestion. For a live 40-person event, this is a bigger operational risk than any single room's internal timing margin. **Recommend building in 5–10 minutes of recoverable slack** — e.g. a deliberately loose opening briefing that can be trimmed live, or a short buffer folded into the final trading window — rather than treating 100 minutes as a hard, fully-packed schedule.

### 3.2 Per-room timing (secondary, but still worth checking)

Each room's two sub-quests run in parallel (guild splits in half), bounded by the longer one:

| Room | Longer sub-quest | Bound | Buffer in 10 min |
|---|---|---|---|
| 1 – Cloth Room | Cartographer's Workshop (strict) | 7 min | ~3 min |
| 2 – Dye Room | Hall of Languages (est.) | ~6 min | ~4 min |
| 3 – Black Powder Room | Architect's Challenge (strict) | 7 min | ~3 min |
| 4 – Candle Room | Scribe's Observation | 7 min | ~3 min |

These buffers are workable on paper but, per §3.1, there's no cushion elsewhere in the schedule to absorb it if one room runs over.

---

## 4. Rules ambiguities and gaps worth resolving before the simulation

Reordered from the first draft — the scoring contradiction is promoted to the top since it directly affects simulation parameters, not just clarity.

1. **Quest scoring scale contradicts itself.** The generic rule states *"Each quest scores 0, 2, 4, 6, 8 or 10 coins"* (even numbers only), but several individual quests explicitly allow odd totals: the "1 coin per correct answer" quests (European Music Hall, Art Gallery, Hall of Languages) can score any value 0–10, and the Cartographer's Workshop and Architect's Challenge scoring tables both include odd values (3, 5, 7). Only the Locksmith's Secret table is actually consistent with the generic even-only rule. This needs a resolution before the simulation can model expected quest income or room-winner-bonus frequency correctly.
2. **Does the 15-coin fallback also grant a reward Tier‑2 item afterward?** (§2.3) — changes the relative cost of the two admission paths substantially.
3. **Is the "3 available items" reward one pool shared by both guilds in a room (cards removed as each guild picks), or does each guild see its own separate set of 3?** (§2.3, §2.5) — the reading that it's one shared, depleting pool is the most natural and is what §2.5's scarcity/trading argument assumes, but it isn't stated outright.
4. **Room assignment mechanism** — is it free choice/racing (as implied by "two other guilds already paid"), GM-directed, or (per the §1 recommendation) a fixed rotation?
5. **Where/when can peer-to-peer trading happen?** Crafting is explicitly Guildhall-only; general trades aren't location-restricted in the text — mid-activity-room, or only during trading breaks?
6. **Common Quest 3B (Hall of Legends)** doesn't state its clue count, unlike the other four "identify 10 things" quests.
7. **Fallback for a guild that never completes all 4 rooms** — any end-game recourse, or is that quest income simply lost? (Now known to be a real risk at ~18% of guild-slots under one unmanaged-scheduling policy — §7; note that's a policy-specific baseline, not an event forecast.)

---

## 5. Operational risk: the Guildhall needs a designed, throughput-tested protocol

Conversions, quest-fee payments, and loans all funnel through the Guildhall/GM. During a single 10-minute trading break it may need to simultaneously handle: Tier‑1 production for up to 8 guilds, Tier‑1→Tier‑2 and Tier‑2→Tier‑3 crafting, room-fee payment and booking for the next round, loan issuance, disputes, and player questions — while guilds are also trying to negotiate trades with each other in the same window. Peer-to-peer trades look self-administered (no GM sign-off implied by the text), which helps, but everything else is a real queue.

**"Add 2–3 more helpers" is a reasonable start but isn't the actual fix** — the real question is throughput, not headcount. Recommend designing an explicit transaction protocol (e.g. a marked self-service swap table for straightforward 2-cards-for-1 conversions, GM only for loans/disputes) and, if possible, timing it in a rehearsal: seconds per transaction type, transactions needed per guild per round, and the probability a guild fails to complete its intended actions in 10 minutes. That number should feed directly into whether more staff, a simpler protocol, or both are needed.

---

## 6. What's working well

- The tier price ladder (§2.2) makes crafting a genuinely interesting decision rather than an obviously-always-correct one, once you account for shadow value — that's better design than "crafting is always good," not worse.
- Per-room quest timing comfortably fits the 10-minute slots when run in parallel (§3.2).
- The room-level win/tie handling is simple to administer — 5 coins to the winner, 2/2 on a tie, no ambiguous edge cases in the arithmetic itself. (But see §2.7: simple to run is not the same as balance-neutral — this bonus compounds with quest skill rather than being independent of it.)
- Charity ticket design (fixed €20 donation, no refund) is clean and doesn't interact with the in-game economy.
- The two-guilds-per-room reward pool (§2.5) is a subtle, probably-intentional scarcity mechanism worth preserving — it may be doing more balancing work than the recipe graph itself.

*(Removed from this list since the first draft: "the recipe graph forces cross-guild trading" — see §2.5, now an open question — and the room-win bonus is no longer described as consequence-free — see §2.7.)*

---

## 7. Appendix: toy scheduling model (supporting §1, not the full simulation)

**Method (precisely, per review correction):** 8 guilds, 4 rooms, 4 rounds, capacity 2 guilds/room/round. Each round, guilds are processed in a random order; each guild picks **uniformly at random among rooms it hasn't visited yet that currently have a free slot** — i.e. the guild has full, accurate knowledge of remaining capacity at the moment it chooses (this is not a "no visibility" model), but no negotiation with other guilds and no ability to anticipate choices later in the round. 200,000 simulated games, seeded for reproducibility. Code: [`simulation/toy_scheduling_model.py`](../simulation/toy_scheduling_model.py).

**Results:**

| Metric | Result |
|---|---|
| Games where all 8 guilds visit all 4 rooms | 38.2% |
| Individual guild-slots that complete all 4 rooms | 82.3% |
| Guild-slots missing exactly 1 room | 17.6% |
| Guild-slots missing 2+ rooms | ~0% |

An independent check by a reviewer using the same approach landed at 38.4% — consistent to within simulation noise.

**Reading these numbers:** this is **not a prediction or a bound on the real event's performance** — real players might do better than this policy (via negotiation and seeing what others are doing) or worse (concurrent decisions, imperfect queue visibility, time pressure, confusion), and nothing here establishes which direction dominates. What it *does* establish: under one explicit, simple, fully-specified decentralized-choice policy, exact capacity-equals-demand is not enough to guarantee a successful allocation — the risk is measurable, not just a plausible-sounding assertion. It's also worth being disciplined about scope: this model only tests the pure scheduling mechanic in isolation. The real game entangles room choice with which Tier‑2 item a guild happens to hold, coin availability, loans, and the previous room's reward card (§2.1–§2.5) — none of that is in this toy model, deliberately, so its 38.2% shouldn't be read as an estimate of the full economy's behavior. It exists to convert "this is a real risk" from an assertion into a checked claim, and to give the §1 rotation recommendation a concrete baseline to compare against (the fixed rotation gets this to 100% by construction — no simulation needed for that half).

---

## 8. Simulation plan (methodology, before any code for the full model)

Per the independent review: a simulation isn't useful design evidence unless the questions it needs to answer, and the variants it needs to compare, are specified before it's built. Proposed scope for the next phase:

**Core questions to measure:**
1. Probability every guild completes all 4 rooms, under realistic (not worst-case) scheduling behavior.
2. Distribution of final scores across guilds — how much of the spread is starting-hand luck vs. room-assignment luck vs. play quality.
3. Number of loans per guild and resulting debt distribution at game end.
4. Number of inter-guild trades that actually occur, and the fraction of guilds that could plausibly finish competitively without trading at all (§2.5 — the central question).
5. Tier‑1/Tier‑2/Tier‑3 inventory levels over time, per guild.
6. Shadow value of each Tier‑2 item type by round (§2.2) — i.e., what it's actually worth to a guild holding it at a given point, not its sale price.
7. Marginal expected-score value of a single room visit, including its reward card and downstream effects — not just its quest coins (corrects §7's "~20–25 coins lost" framing from the first draft, which only counted quest income).
8. Win-rate differences by guild/specialty, once §2.6's guild-specific content is finalized.
9. Sensitivity to player skill/behavior — rational optimizers vs. casual play — since this is a mixed-skill charity event, not a competitive tournament.
10. **Compounding of the three snowball mechanisms (§2.7)** — loan debt, winner's-first-pick, and the +5 room bonus — measured together, not separately: how much of the final-score spread traces back to an early lead in one or two rooms versus genuinely independent luck/skill later in the game.
11. **Opponent and interaction diversity** — distinct opposing guilds encountered per guild across the game, distinct trading partners, and cross-specialty interactions. "Number of trades" alone doesn't measure networking: ten trades with one guild is a very different outcome from six trades spread across six different guilds, and the event's stated purpose is the latter.

**Before implementation: item 9 needs concrete agent behavior specs, not just a label.** "Rational optimizers vs. casual play" isn't yet something a simulation can run — without pinning down the actual decision rules, a full simulator can produce precise-looking output that's really just an artifact of whatever behavior got implemented, not a finding about the game. At minimum, each agent policy needs explicit rules for:
- **Craft choice** — when to convert Tier‑1→2 and Tier‑2→3 vs. hold items back (§2.2's shadow-value tradeoff).
- **Room-access valuation** — how an agent estimates whether it's worth holding an item for an unvisited room vs. liquidating/trading it now.
- **Trade initiation and acceptance** — what price/exchange an agent will offer or accept, and how it decides whether a trade is worth pursuing at all vs. self-sufficient chaining (§2.5).
- **Reasoning about other guilds' inventories** — how much (if anything) an agent infers or assumes about what other guilds hold when deciding whether to trade.
- **Reward-card selection** — how a winner picks among the 3 available cards (§2.3), and how a loser chooses given what's left.

A "rational" policy and a "casual" policy should be two different concrete implementations of all five, not two labels applied to the same logic.

**Design variants to compare against the current ruleset:**
- Fixed room rotation with repeated opponents (the original, flawed §1 table) vs. the corrected varied-opponent rotation vs. free-choice scheduling — this should make the opponent-repetition cost from §2.7/§1 directly visible in the score-variance numbers, not just argued from principle.
- Coordinated starting hands (§2.1) vs. purely random.
- Current loan interest (double) vs. capped/first-loan-only interest.
- Current Tier‑3 sale values vs. alternatives.
- Mandatory vs. optional trading windows (to directly probe §2.5).
- Winner-picks-reward-first (current rule) vs. loser-picks-first vs. random order (§2.7's rubber-banding test).

Building the full agent-based model against this plan is the next step once §4's ambiguities are resolved (particularly the scoring-scale contradiction and the coin-payment reward-card question, both of which change simulation parameters directly).

---

## 9. Priority order for fixes

Revised to reflect the corrections above:

1. **Use the corrected room/opponent rotation** (§1) — it satisfies room capacity *and* opponent diversity together; the first version only did the former, and shouldn't be implemented as originally written.
2. **Correct understanding of starting hands** (§2.1) before designing any kit-dealing rule, and coordinate the deal with the rotation from #1 — the two-recipe choice changes what "controlling" the starting deal can and can't achieve.
3. **Model Tier‑2 items as admission rights, not 4-coin commodities** (§2.2–§2.3) — this changes the crafting economics substantially and should shape how the simulation values inventory.
4. **Determine whether trading is actually necessary** (§2.5) — directly relevant to the event's stated networking purpose, and should be one of the first simulation outputs, not an afterthought.
5. **Model the three snowball mechanisms together** (§2.7) — loans, winner's-first-pick, and the +5 bonus — before deciding whether any single one (e.g. loan interest) needs rebalancing in isolation.
6. **Resolve the quest-scoring contradiction** (§4.1) — needed before quest income can be modeled at all.
7. **Clarify the loan rule, the coin-payment reward question, and the shared-reward-pool question** (§2.4, §4) before touching the interest rate or the scarcity argument in §2.5.
8. **Add global schedule slack** (§3.1) — the 100-minute program currently has none.
9. **Design and throughput-test the Guildhall transaction protocol** (§5) rather than just adding volunteers.
10. **Finalize guild special items and unique quests** (§2.6) so they can be included in the simulation.
11. **Build the full simulation** against the plan in §8, only once 1–10 above are settled.

---

*Next: build the agent-based simulation described in §8.*
