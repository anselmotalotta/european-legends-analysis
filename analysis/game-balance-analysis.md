# European Legends — Office Adventure Game: Balance & Design Analysis

**Reviewed document:** *European Legends Office Adventure Game*, v. 16 August 2026
**Event:** EIB Group charity game, 17 September 2026, up to 8 guilds × 5 players
**Purpose of this document:** an independent design/balance review of the ruleset, ahead of an economic simulation of the trading and crafting system.

This is a written pass only — no code has been run yet. Findings are grouped by severity/type: structural risks (things that could break the event), economic balance (things that could make it unfair or unsatisfying), timing, rules gaps, operational risk, and what's already working well.

**Reference figures from the source document:**

![Items by tier](../assets/items-and-tiers.jpg)
![Conversion chart](../assets/conversion-chart.png)
![Guilds](../assets/guilds.jpg)

---

## 1. Structural risk: room scheduling has no coordination mechanism

This is the single largest risk in the current draft.

Each round, 4 activity rooms × 2 guild slots = exactly 8 slots — one for each guild. Over 4 rounds that's 32 slots, precisely enough for all 8 guilds to visit all 4 rooms once each. **But nothing in the rules guarantees this ideal matching actually happens.** Guilds choose (or race for) rooms themselves each round, constrained only by "two other guilds already paid their participation fee for the following round" locking a room. With 8 semi-informed teams converging on the Guildhall simultaneously every 10 minutes, under time pressure, decentralized self-scheduling can easily produce collisions — e.g., three guilds all wanting Room 3 in round 2, one gets shut out, and later in the game the rooms that guild still needs are already full every remaining round.

**Consequence if it happens:** a guild can end the game having visited only 2–3 of the 4 rooms, permanently missing ~20–25 coins of quest income per skipped room, on top of being funneled into avoidable loans (see §2). This isn't a rare edge case — it's the default outcome of unmanaged parallel demand on a hard 8-slots/round cap.

**Recommendations (pick one):**
- **Pre-assigned rotation (safest):** print each guild a fixed 4-round room order on their team sheet, designed as a Latin square so every room has exactly 2 guilds every round, guaranteed. This removes the coordination problem entirely and costs nothing to implement — you already control who gets which sheet.
- **Visible booking board:** a physical board at the Guildhall showing the 8 slots per round, guilds physically claim a slot. Lower design effort, but reintroduces the race/coordination risk and needs a helper to manage it.

I'd suggest the first option unless "who visits where" is meant to be a live strategic decision — it removes an entire failure mode for a two-line change.

## 2. Economic balance

### 2.1 Round-1 starting kits and the tier-2 recipe graph

The four Tier-1 materials form a 4-cycle in the conversion chart (Fig. 2): **Flax–Wax → Candle, Wax–Charcoal → Dye, Charcoal–Saltpetre → Black Powder, Saltpetre–Flax → Cloth.** Diagonal pairs (Flax+Charcoal, Wax+Saltpetre) don't convert to anything.

Each guild starts with 3 random *different* Tier-1 items — i.e., missing exactly one of the four types. Removing one node from a 4-cycle always leaves a 3-node path with a shared middle item, which means **a guild's starting hand can always craft exactly one Tier-2 item, never zero and never two** (they hold only 1 unit of the shared "hub" item, so only one of the two possible recipes is actually executable). This is a nice, deliberate-feeling structural property — worth confirming it was intentional, because it matters a lot for balance.

The problem: which Tier-2 item a guild *can* make is now determined by which Tier-1 type is missing from their random deal — but if the deal is *literally random* per guild rather than controlled, there's no guarantee the 8 guilds split evenly across the 4 possible outcomes. If, by chance, 5 guilds can only make Cloth and 1 guild can make Black Powder, Room 3 will be under-contested and Room 1 will have guilds shut out on turn one under §1's dynamics — compounding both problems.

**Recommendation:** don't leave the starting-kit missing-item to pure randomness. Deliberately deal starting kits so that exactly 2 guilds are missing each Tier-1 type (i.e., exactly 2 guilds can craft each Tier-2 item on turn one). This is a free fix — same "feels random to players" experience, but it makes the Round-1 room demand exactly match the Room-1 capacity (2 slots × 4 rooms), which also makes §1's Latin-square rotation trivial to design consistently with starting kits.

### 2.2 The loan mechanic can snowball without a catch-up path

A guild that can't pay a room's Tier-2 entry fee and doesn't have 15 coins takes a GM loan for the shortfall, repaid at **double** value at game end. This is a reasonable "the show must go on" safety valve, but as written it has no rubber-banding: a guild that's behind because of bad starting luck (§2.1) or bad room-timing luck (§1) is *more* likely to need loans in every subsequent round too (less time to craft, less to trade with), and each loan digs the final score deeper — with the penalty scaling as the game goes on (a round-1 loan of 15 costs 30 at the end; a round-4 loan is the same 30, but by round 4 there's no time left to earn it back). A guild that gets unlucky early can be mathematically eliminated from contention by round 2 without any player mistake.

This matters more for a charity/team-building event than a competitive game — a team that's locked out of winning by turn 30 (of 100 minutes) with no misplay of their own tends to check out early, which undercuts the "entertainment/team-building" purpose stated in the brief.

**Recommendation:** consider capping total loan interest (e.g., double only on the first loan, flat repayment on subsequent ones) or letting a guild's own unique quest (§2.4, worth 15–20 coins) function as an explicit catch-up lever regardless of Guildhall standing.

### 2.3 The crafting economy rewards conversion, which is good design

Selling prices (Tier 1 = 1, Tier 2 = 4, Tier 3 = 14, guild special Tier 3 = 20) mean converting two Tier-1 items (worth 2 coins raw) into one Tier-2 item (worth 4) is a "free" 100% value gain, and two Tier-2 into one Tier-3 (8 → 14) is another +75%. This is exactly the incentive structure you want: it makes crafting strictly worth doing whenever a guild has spare time and matching items, and it makes trading for the *right* second item valuable even at a coin cost. This part of the design is sound and doesn't need changing — flagging it here mainly so the simulation validates whether guilds realistically have *time* to climb the full chain (see §3), since the incentive only pays off if the chain is actually reachable within 100 minutes.

### 2.4 Guild special items and unique quests are marked "in elaboration"

The 20-coin "guild special item" bonus and each guild's unique 15–20 coin quest are central to both balance (§2.2's catch-up suggestion leans on them) and identity, but aren't defined yet in this draft. Worth finishing these before the simulation is built, since the simulation's results will shift once guild-specific asymmetries are added — I'd treat the current run as "core economy only" and re-run once these are final.

## 3. Timing

The per-room timing mostly works: each room's two sub-quests run in parallel (guild splits in half), and the room visit is bounded by the *longer* of the two sub-quests. Checking all four rooms against their 10-minute slot:

| Room | Longer sub-quest | Bound | Buffer left in 10 min |
|---|---|---|---|
| 1 – Cloth Room | Cartographer's Workshop (strict 7 min) | 7 min | ~3 min |
| 2 – Dye Room | Hall of Languages (~5–6 min est.) | ~6 min | ~4 min |
| 3 – Black Powder Room | Architect's Challenge (strict 7 min) | 7 min | ~3 min |
| 4 – Candle Room | Scribe's Observation (7 min) | 7 min | ~3 min |

The 3-minute buffers are tight but workable for fee payment, item selection, and walking within the room — **as long as the room isn't also where the 10-minute "moving around" between locations has to happen** (the rules assign movement time to the trading breaks and opening briefing explicitly, but not to activity rounds — worth double-checking that room-to-room transit is genuinely free/instant given "Ground level of Bloque C... four activities rooms," since if it's not, these buffers evaporate).

The bigger timing risk isn't inside a room, it's at the Guildhall (see §5).

## 4. Rules ambiguities and gaps worth resolving before the simulation

- **Room assignment mechanism** — is it guild free choice (races for slots), GM-directed, or a fixed rotation? The current text ("two other guilds already paid...") implies free choice/racing, which is what drives §1. Confirming this changes how the simulation should model it.
- **Where/when can peer-to-peer trading happen?** "Items are produced and converted at the Guildhall" is explicit; general item-for-item or item-for-coin trades between guilds aren't location-restricted in the text. Can two guilds trade mid-activity-room, or only during trading breaks at the Guildhall? This affects how much of the 10-minute activity rounds are usable for deal-making.
- **Common Quest 3B (Hall of Legends)** doesn't state how many clues/riddles are used, unlike the other four "identify 10 things" quests — presumably also 10 for consistency, but not stated.
- **Does a loan grant free entry, or just cover the coin shortfall for that room's fee?** — i.e., after taking a loan, does the guild still need to hand over the Tier-2 item if they later get one, or is the fee "coins-only" once converted to a loan?
- **What happens if a guild simply never manages to visit a room** (via §1) — is there an end-game fallback (buy access to missed quest coins some other way), or do they just lose that quest's income entirely?

## 5. Operational risk: the Guildhall is a single point of congestion

Conversions, quest-fee payments, and loans all funnel through the Guildhall/Game Master. Peer-to-peer trades appear to be self-administered (no GM sign-off implied by the text), which helps — but crafting and fee payment do not. With up to 8 guilds hitting the Guildhall simultaneously at the start of every 10-minute trading break, and only ~10 helpers total (most of whom are presumably staffing the 4×2 = 8 activity sub-quest stations), there may be only 1–2 people available to process conversions and fees for 8 teams in a 10-minute window. This is as much a live-event staffing question as a game-balance one, but it directly limits how much of the intended crafting economy actually gets used in practice.

**Recommendation:** explicitly staff 2–3 helpers at the Guildhall (not just the GM) during trading breaks, and consider a simple self-service mechanism for straightforward conversions (a marked table/box where guilds physically swap 2 cards for 1, no GM needed, GM only intervenes for loans/disputes) to remove the single-person bottleneck.

## 6. What's working well

- The 4-cycle recipe graph forces genuine cross-guild trading by design (§2.1) — nobody can craft alone, which directly serves the "networking" goal in the brief.
- The tier price ladder (§2.3) makes crafting strictly worth doing without needing to be mandatory — good incentive design.
- Per-room quest timing comfortably fits the 10-minute slots when run in parallel (§3).
- The win-bonus / tie-handling at the room level (5 coins to the room winner, 2/2 on a tie) is simple and won't produce weird edge cases.
- Charity ticket design (fixed €20 donation, no refund) is clean and doesn't interact with the in-game economy in a way that needs balancing.

## 7. Priority order for fixes

1. **Fix room scheduling** (§1) — highest risk of a genuinely broken event experience; cheapest fix (pre-printed rotation).
2. **Control starting-kit distribution** (§2.1) — free fix, and it also makes #1 easier to design correctly.
3. **Decide the loan catch-up question** (§2.2) — affects whether a losing guild can still have fun for the last 30 minutes.
4. **Resolve the open ambiguities** (§4) before the simulation is built, since several of them change what the simulation should assume.
5. **Guildhall staffing** (§5) — operational, but worth deciding before the event, not during it.

---

*Next: an agent-based simulation of guild economies (production, crafting, trading, quest income, loans) across the 100-minute timeline, to quantify how §1–§2's risks play out numerically and check whether the intended crafting chain (Tier 1 → 2 → 3) is realistically reachable in the time available.*
