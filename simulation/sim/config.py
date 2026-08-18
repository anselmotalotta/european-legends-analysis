"""
Frozen rules interpretation for the simulator (analysis guardrail #1:
"anything still ambiguous in §4 should be a parameter or clearly marked
default, not silently hard-coded").

Every field below is either directly stated in the source rules
(marked ESTABLISHED) or a specific resolution of a §4 ambiguity
(marked ASSUMPTION, with the §4 item number it resolves). Assumptions
are exactly the things design-variant experiments should vary.
"""
from dataclasses import dataclass, field


@dataclass(frozen=True)
class GameConfig:
    # --- ESTABLISHED ---
    n_guilds: int = 8
    n_rooms: int = 4
    n_rounds: int = 4
    starting_coins: int = 10
    room_coin_fallback_fee: int = 15
    room_win_bonus: int = 5
    room_tie_bonus: int = 2
    # 1.5x, not the original 2x: lowered by the tuning sweep in
    # simulation/README.md, which found double interest measurably
    # widened the game's overall score spread compared to 1.5x, for a
    # roughly proportional increase in average debt. See corrected-
    # ruleset-v2.md §14, which reflects this as the adopted rule.
    loan_interest_multiplier: float = 1.5
    production_per_break: tuple = (1, 2, 3)  # Tier-1 units/round at breaks 1-3

    # --- ASSUMPTION: §4 item 1 (generic 0/2/4/6/8/10 rule contradicts
    # several per-quest tables). Default resolution: use each quest's own
    # stated scoring table/range, since it's more specific and the generic
    # rule is inconsistent with 3 of the 4 rooms' quests. ---
    use_generic_scoring_scale: bool = False

    # --- ASSUMPTION: §4 item 2. Default: coin-paying guilds DO receive a
    # reward Tier-2 card, same as item-paying guilds (the text's "different
    # than the one they paid" phrasing is read as describing the reward
    # mechanic generally, not conditioning it on payment method). ---
    coin_payment_grants_reward_card: bool = True

    # --- ASSUMPTION: §4 item 3. Default: the "3 available items" reward is
    # one pool shared by both guilds in the room, cards removed as each
    # guild picks (the reading analysis §2.5's scarcity argument assumes). ---
    shared_reward_pool: bool = True

    # --- ASSUMPTION: §1 recommendation. Default: use the fixed, verified
    # room/opponent rotation (analysis §1) rather than free-choice
    # scheduling. The free-choice variant is what simulation/toy_scheduling_model.py
    # already measures in isolation (38.2% completion) - this flag lets the
    # full engine reproduce that as one design variant among others. ---
    use_fixed_rotation: bool = True

    # --- ASSUMPTION: analysis §2.1 recommendation, only meaningful when
    # use_fixed_rotation is True. Default: starting hands are coordinated
    # with each guild's Round-1 room assignment (analysis §2.1 table)
    # rather than dealt purely at random. ---
    coordinate_starting_hands: bool = True

    # --- ASSUMPTION: analysis §2.7 / §8. Default: room winner picks their
    # reward card first (as stated). A plain bool can't express the 3-way
    # variant §8 actually lists (winner-first / loser-first / random) -
    # "random" is also the source rule's own tie-break for which item is
    # chosen (not who picks), so it's a real case, not hypothetical.
    # One of "winner_first", "loser_first", "random". ---
    reward_pick_order: str = "winner_first"

    # --- ESTABLISHED (source doc: "Guilds may freely exchange items for
    # coins or other items"), but exposed as a toggle so the tuning sweep
    # can test what happens if coin-for-item purchases between guilds are
    # disabled and only barter (item-for-item) trades remain - a live
    # question raised by simulation findings: under rational play, almost
    # all guild-to-guild exchange turns out to be coin purchases rather
    # than barter, which is a weaker fit for the event's stated networking
    # purpose than an actual two-sided swap. Default True (matches the
    # current ruleset as written). ---
    allow_coin_purchases: bool = True

    # --- Not yet modeled at all (analysis §2.6): guild-special Tier-3
    # items (20-coin sell price) and unique per-guild quests are still
    # "in elaboration" in the source and are out of scope for this first
    # version (guardrail: "before adding every guild-specific special
    # quest"). Every guild's Tier-3 items sell at the plain 14-coin price. ---

    guild_names: tuple = (
        "Lisbon", "Bursa", "Stockholm", "Ghent",
        "Gdansk", "Venice", "Prague", "Vienna",
    )
    guild_specialty: dict = field(default_factory=lambda: {
        "Lisbon": "Wax", "Bursa": "Wax",
        "Stockholm": "Flax", "Ghent": "Flax",
        "Gdansk": "Saltpetre", "Venice": "Saltpetre",
        "Prague": "Charcoal", "Vienna": "Charcoal",
    })
