# European Legends Office Adventure Game — Ruleset v2

*Corrected and completed version of the original document (v. 16 August 2026), incorporating the actionable recommendations from the independent balance & design review ([full analysis](game-balance-analysis.md)). Everything below is meant to be usable directly — print it, hand it to helpers, done. A short summary of what changed and why follows immediately below; the ruleset itself starts at §1.*

---

## What changed from the original, and why

| Change | Why |
|---|---|
| **Room visits now follow a fixed, pre-assigned rotation** (§7) instead of open scheduling | The original left room choice to guilds racing for slots with zero spare capacity (4 rooms × 2 slots = exactly 8 guilds); unmanaged, that fails to complete for a meaningful fraction of guilds. The fixed rotation guarantees every guild visits every room exactly once, against a different opponent each round. |
| **Starting Tier-1 kits are now assigned, not fully random** (§6) | Coordinated so every guild's opening hand can pay its Round-1 room fee without needing a loan on turn one. Still looks and feels random to players — they don't know in advance which two of their three items they'll get, only which one they won't. |
| **The quest scoring section no longer contradicts itself** (§9) | The original had a generic "0/2/4/6/8/10" scoring rule that conflicted with several individual quests' own scoring tables. This version scores every quest by its own stated table only. |
| **Loan mechanics are stated precisely, and the interest rate is lowered** (§8) | Clarified that a loan covers only the coin *shortfall* for a room fee, not the full 15-coin fee. The repayment rate is also lowered from double the shortfall to **one and a half times** it, based on a [tuning comparison](../simulation/README.md#tuning-sweep-what-the-numbers-actually-support) run after the ruleset was otherwise finalized: at double interest, weaker-playing guilds carried measurably more debt and the game's overall score spread (a proxy for how much the game is decided by an early stumble rather than the rest of the game) was highest of the three rates tested. 1.5× keeps a real penalty — it is not free to borrow — while reducing both effects without a rules change needed anywhere else. |
| **Reward-card and payment-method questions are resolved** (§8) | Paying a room's fee in coins now explicitly still earns a reward Tier-2 card, same as paying in items. The reward pool of 3 cards is explicitly one pool shared by both guilds in the room, cards removed as each guild picks. |
| **Common Quest 3B now has a fixed clue count** (§7, Room 3) | Set to 10 clues, matching the other four "identify N things" quests, for consistent scoring ranges. |
| **A recoverable time buffer is built into the schedule** (§4) | The original schedule filled all 100 minutes with no contingency. 10 minutes of flexible buffer is now built in. |
| **Guildhall staffing is now specified** (§10, new) | The original didn't say how many people staff conversions/fees/loans. This version specifies a minimum and a self-service option for simple conversions. |

Two things are deliberately **not** changed here, and still need your input before the event:

- **Guild special items and unique quests** (§6, §11) are still placeholders — same as the original, these need to be finalized.
- **Whether the game's trading incentives serve the event's networking purpose specifically** is still open. Testing found that skilled play satisfies most of its need to trade through coin purchases rather than genuine item-for-item barter — but also found that simply disallowing coin purchases doesn't convert that into more barter, it mostly just removes the exchange altogether for skilled guilds. So this ruleset keeps coin purchases between guilds as written; no rule change here is currently supported by the evidence, though the underlying concern (does the game actually get colleagues from different guilds talking to each other) remains open. See the [simulation](../simulation/) for the detail.

---

## 1. Date

17 September 2026

## 2. Place

Ground level of the Bloque C of the PKI building (further as Game Area, consisting of the central game location – the Mezzanine of the 1st floor Bloque C (as the briefing area and the Guildhall) and the four activities rooms at the ground 0).

## 3. Purpose

Charity, Networking, Team-building, Entertainment.

## 4. Participation and participants

The game is to be held in up to 8 teams of 5 EIB Group participants with a total number of players not exceeding 40 people (on first registration basis). Ideally the teams would be randomly mixed to allow colleagues for networking. Team members would be identifiable by different colour wristbands provided for the time of the game and provided with an accessible rules summary customized for each team, including one unique guild quest. The teams are referred to as guilds in the game. The game is run by the Game Master with help of the group of helpers/volunteers (ideally ca. 10 people — see §10 for suggested allocation).

## 5. Condition of participation

Registration will be confirmed only upon making a minimum 20 euro donation to one of the participating charities chosen among the existing EIB Volunteering Hub approved charities. The event would be used, among other purposes, to promote EIB Group's collaboration with these charities and explain their activities. As the participation "ticket" constitutes a charity donation, no reimbursement for colleagues who could not participate despite donating and registering is foreseen.

## 6. Duration and structure of the game

Approximately 80 minutes plus 20 minutes for final trading phase and final briefing taking place exclusively at Mezzanine-Guildhall. There will be a clock visible to players in the Guildhall, the central location of the game and the exact time will be announced.

The game lasts 100 minutes, structured as follows. **10 minutes of flexible buffer is built into the opening briefing** — if it runs shorter than planned, that time carries forward as slack for the rest of the schedule; the Game Master should feel free to compress it live rather than treat every phase as fixed-length.

| # | Phase | Length |
|---|---|---|
| 1 | Opening Briefing (general instructions, concluded with starting-item conversions allowing participants to move to the First Round of Activities) — **includes 5–10 min flexible buffer** | 10 min incl. moving around |
| 2 | Activities First Round | 10 min |
| 3 | Trading break one | 10 min incl. moving around |
| 4 | Activities Second Round | 10 min |
| 5 | Trading break two | 10 min incl. moving around |
| 6 | Activities Third Round | 10 min |
| 7 | Trading break three | 10 min incl. moving around |
| 8 | Activities Fourth Round | 10 min |
| — | *(after c.a. 80 minutes, participants return to the Mezzanine)* | |
| 9 | Last trading opportunities | 10 min |
| 10 | End of game and final briefing | 10 min |

## 7. Room rotation (new — replaces open scheduling)

Each round, 2 guilds compete in each of the 4 activity rooms — exactly 8 guild-slots per round, matching all 8 guilds exactly. To guarantee every guild visits every room exactly once, against a **different opponent every round**, and never against its own same-specialty counterpart, follow this fixed rotation. Print each guild's row on their team sheet.

| Round | Room 1 — *Of Maps and Music* (Cloth) | Room 2 — *Of Words and Images* (Dye) | Room 3 — *Of the Ones That Built Legacy* (Black Powder) | Room 4 — *Of the Devil in the Details* (Candle) |
|---|---|---|---|---|
| 1 | Lisbon, Stockholm | Bursa, Ghent | Gdansk, Prague | Venice, Vienna |
| 2 | Gdansk, Vienna | Venice, Prague | Lisbon, Ghent | Bursa, Stockholm |
| 3 | Ghent, Venice | Stockholm, Gdansk | Bursa, Vienna | Lisbon, Prague |
| 4 | Bursa, Prague | Lisbon, Vienna | Stockholm, Venice | Ghent, Gdansk |

*(Reproducible from [`simulation/rotation_schedule.py`](../simulation/rotation_schedule.py). Note: this rotation does not guarantee every guild meets all three other guilds' production specialties — every guild meets two of the three. Full specialty coverage would require each guild meeting its own twin once, a different tradeoff not adopted here.)*

## 8. Goal of the game

The winning guild is the guild that possesses the highest number of coins at the end of the game. Coins are gained by converting and trading items, fulfilling objectives of common quests as well as special guilds' quests.

## 9. Items

Items are represented by cards printed specifically for the game. They exist in three tiers, from tier 1 (basic guild supply cards), through tier 2 (crafting cards) to tier 3 (final products).

Each tier 2 and tier 3 item requires two different items of lower level to be made (meaning that two cards are exchanged for one more valuable). One item can only belong to one team – if two teams would like to create a tier 2 or tier 3 item jointly, they need to trade items between them before they do so.

Items are produced and converted **at the Guildhall only**. Peer-to-peer trading (exchanging items or items-for-coins between guilds) may happen anywhere, at any time during the game, not only at the Guildhall — see §8.

Guilds can produce Tier 1 items depending on their unique availability (each Guild can produce exactly one type of tier 1 item), in the following quantities: one tier 1 item in the first trading round, 2 in the second, 3 in the third.

Items would be also required to participate in the common quests (and more items would be offered as a reward for their fulfilment).

## 10. Starting items and coins (corrected)

Each guild receives 3 random Tier-1 items and 10 coins at the beginning of the game, as well as a scoresheet for quests and a small bag for items.

**The 3 starting items are not fully random** — each guild's kit always includes 3 of the 4 Tier-1 types (always missing exactly one type), and *which* type is missing is chosen so that every guild can craft, from its own opening hand, the exact Tier-2 item its Round-1 room requires (§7). This still looks and plays as a random deal to guilds — they aren't told in advance which one material they'll be missing, only that they have three of the four.

| Guild(s) | Round-1 room needs | Starting hand should be missing |
|---|---|---|
| Lisbon, Stockholm | Cloth (Flax+Saltpetre) | Wax or Charcoal |
| Bursa, Ghent | Dye (Wax+Charcoal) | Flax or Saltpetre |
| Gdansk, Prague | Black Powder (Charcoal+Saltpetre) | Flax or Wax |
| Venice, Vienna | Candle (Flax+Wax) | Charcoal or Saltpetre |

## 11. Trading items and selling prices

Big part of the scoring in the game will come from selling the items at the Guildhall at the end of the game at the following prices:

- Tier 1 item – 1 coin
- Tier 2 item – 4 coins
- Tier 3 item – 14 coins
- Guild special item (one type of Tier 3 item for each guild that they specially benefit from selling – 20 coins) — *still to be finalized; see the "still open" note above.*

Guilds may freely exchange items for coins or other items, anywhere and at any time during the game (§9). Whenever an agreement is made between the guild members about the price and items to be traded it has to be honoured on the spot. Any promises of future exchanges are not binding unless such future contract would be concluded before the Game Master (bear in mind that the game is foreseen for 100 minutes only).

## 12. Guilds' unique quests

Each guild starts the game with a unique quest that they will be trying to fulfil requiring to look for places and information within the Game Area. Completion of the quest is rewarded by 15 to 20 coins depending on the complexity of the quest. *Still to be finalized for each guild — see the "still open" note above.*

## 13. Common quests

In accordance with the Game theme of European legends, there are multiple locations within the Game Area where volunteers run quests in form of activities for participants which require certain tier 2 items to participate (see below). Each guild is eligible to participate in common quests and score coins depending on the level of success. Room assignment follows the fixed rotation in §7 — not open scheduling — so no guild can be shut out of a room by other guilds arriving first. Each quest can be done once per guild. The information about the type of activity and requirements to partake in it is included in the form of a poster on the wall/door next to the location, and is also available at the Guildhall.

## 14. Quest participation fee (corrected)

You need to pay one Tier 2 item per guild per activity room to the Game Master in the Guildhall in order to participate (see names of required items next to names of competitions). Instead of a Tier 2 item, a guild can pay 15 coins.

If a guild has neither the required Tier 2 item nor 15 coins, the Game Master issues a loan covering **only the coin shortfall** — e.g. a guild with 10 coins facing the 15-coin fee is loaned 5 coins, not 15. The loan is repaid at the end of the game at **one and a half times the loaned amount, rounded up to the nearest coin** (in the example, a 5-coin loan is repaid as 8 coins). Rounding up keeps every repayment a whole number of physical coins and consistently favors the bank, so it never accidentally undercharges.

Before leaving the activities room, guilds choose a new Tier 2 item, different from the one they paid to participate — **this applies whether the fee was paid in items or in coins.** The 3 available reward items are one pool shared by both guilds in the room: the winners choose first, the losers choose second, and each choice removes that card from the shared pool for that room-round.

## 15. Quest scoring (corrected)

Each quest is scored according to its own table below — there is no separate generic scoring scale; scores range from 0 up to each quest's own stated maximum. Whichever guild scores more combined coins across the two quests in a room scores an additional 5 coins (in case of a tie, both guilds receive 2 additional coins each).

Guilds do the two quests in a room in parallel — it is entirely up to them how they want to split for that purpose.

### Activity room 1 — Of Maps and Music (The Cloth Room)

**Prerequisite:** 1 × Cloth per participating guild

**Common Quest 1A — European Music Hall.** Guilds listen to 10 musical excerpts (15–20 seconds each) and must identify the country associated with the composer (if classical) or artist (if modern music). Examples: Mozart → Austria; Sibelius → Finland; Chopin → Poland; Verdi → Italy; Albéniz → Spain.
*Scoring: 1 coin for each correct answer (0–10).*

**Common Quest 1B — Cartographer's Workshop.** Guilds solve a puzzle map of Europe (to be tested whether 50 or 100 pieces is appropriate within the time limit). Time: strict 7 minutes.
*Scoring: Complete puzzle = 10 coins; 80% complete = 6 coins; good effort = 3 coins.*

### Activity room 2 — Of Words and of Images (The Dye Room)

**Prerequisite:** 1 × Dye per participating guild

**Common Quest 2A — Art Gallery.** Guilds are shown prints of 10 famous European paintings and must identify the country of origin of the painter. Examples: Girl with a Pearl Earring → Netherlands; Guernica → Spain; The Kiss → Austria; Wanderer Above the Sea of Fog → Germany; Impression, Sunrise → France.
*Scoring: 1 coin for each correct answer (0–10).*

**Common Quest 2B — Hall of Languages.** Guilds listen to 10 recordings of spoken European languages (approximately 20 seconds each) and identify the language. Examples of languages: Italian, Greek, Hungarian, Finnish, Portuguese.
*Scoring: 1 coin for each correct answer (0–10).*

### Activity room 3 — Of the Ones That Built Legacy (The Black Powder Room)

**Prerequisite:** 1 × Black Powder per participating guild

**Common Quest 3A — Architect's Challenge.** Time: strict 7 minutes. Guilds build a structure using provided playing cards with as many layers of standing cards as possible (no objects other than cards to support the construction). Participants may hold the cards during construction, but for scoring the cards must stand unassisted. It's irrelevant for scoring whether cards stand on their shorter or longer edges.
*Scoring: at least one card standing = 3 coins; 2 layers = 5 coins; 3 layers = 7 coins; more than 3 layers = 10 coins.*

**Common Quest 3B — Hall of Legends.** Guilds identify historical European figures from **10 clues** (matching the other rooms' clue count for consistent scoring). Examples: "I conquered much of Europe and was crowned Emperor in 1804." → Napoleon; "I discovered a sea route to India." → Vasco da Gama; "I composed the Ninth Symphony." → Beethoven; "I was Queen of England during the Spanish Armada." → Elizabeth I; "I was a physicist who developed relativity." → Einstein.
*Scoring: 1 coin for each correct answer (0–10).*

### Activity room 4 — Of the Devil in the Details (The Candle Room)

**Prerequisite:** 1 × Candle per participating guild

**Common Quest 4A — The Locksmith's Secret.** Guilds solve a chain of riddles. Each clue provides a letter that ultimately reveals a five-letter password needed to unlock a padlock.
*Scoring, based on completion time: within 2 min = 10 coins; within 3 min = 8 coins; within 4 min = 6 coins; within 5 min = 4 coins; not solved = 0 coins.*

**Common Quest — Scribe's Observation.** Time: 7 minutes. Guilds compare two illustrations (10 differences hidden between them) and write down the differences.
*Scoring: 1 coin for each correctly identified difference (0–10).*

The Game Master's decisions on rules, scoring, disputes, and interpretation of quests are final.

## 16. Guildhall staffing (new)

Conversions, quest-fee payments, and loans all happen at the Guildhall, concentrated into the 10-minute trading breaks for up to 8 guilds at once. To avoid this becoming a bottleneck:

- Staff **2–3 dedicated helpers at the Guildhall** during every trading break (separate from the Game Master and separate from the helpers staffing the 4 activity rooms).
- Consider a **self-service swap table** for straightforward 2-cards-for-1 conversions (guilds physically exchange cards themselves, no helper needed) so Guildhall staff can focus on fee payments, loans, and disputes.
- If possible, time a short rehearsal beforehand to check how many transactions 8 guilds actually generate per 10-minute window, and adjust staffing if needed.

## Annex

**Fig. 1** — list of items with icons (to be used to prepare item tokens)
**Fig. 2** — item conversion table
**Fig. 3** — names and symbols for different guilds

*(See [`../assets/`](../assets/) for the figures.)*

8 different guilds present in the game, with 4 different specializations and with a different special objective each (still in elaboration):

| Guild | Produces |
|---|---|
| Lisbon | Wax |
| Bursa | Wax |
| Stockholm | Flax |
| Ghent | Flax |
| Gdansk | Saltpetre |
| Venice | Saltpetre |
| Prague | Charcoal |
| Vienna | Charcoal |

**Still open, same as the original document:** confirming the list of volunteers, confirming the list of charities and details for the ticket payment system, determining the scope of possible participation of the European Investment Bank Group Board Gaming Club in the activity or as a side event (e.g. as a board game night for participants following the termination of the main Adventure Game), and finalizing each guild's special item and unique quest.
