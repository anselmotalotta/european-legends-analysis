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
    loan_interest_multiplier: int = 2  # repaid at double
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

    # --- ASSUMPTION: analysis §2.7. Default: room winner picks their
    # reward card first (as stated). The rubber-banding alternative
    # (loser picks first) is an explicit design variant to compare. ---
    winner_picks_reward_first: bool = True

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
