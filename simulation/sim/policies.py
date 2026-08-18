"""
Agent behavior policies (analysis §8: "rational vs. casual play needs
concrete behavioral models, not a label"). Every policy must implement
all five decision points: craft choice, room-access valuation, trade
initiation/acceptance, reward-card selection, and (implicitly, via
room_access_value) reasoning about its own future needs. Neither policy
reasons about what OTHER guilds hold - that's a possible future
extension, not modeled here.
"""
from abc import ABC, abstractmethod

from . import items as I
from . import rotation as R


class AgentPolicy(ABC):
    name = "base"

    @abstractmethod
    def choose_round1_craft(self, guild, options, rng):
        """Which of the (always exactly 2) starting-hand Tier-2 options to craft."""

    @abstractmethod
    def room_access_value(self, guild, item, unvisited_rooms, config):
        """Estimated value (coins) of holding one unit of `item` right now."""

    @abstractmethod
    def should_craft_up(self, guild, tier2_a, tier2_b, unvisited_rooms, config):
        """Whether to convert two held Tier-2 items into their Tier-3 product now."""

    @abstractmethod
    def seek_trade(self, guild, unvisited_rooms, config, rng):
        """Returns (item_wanted, item_offered) or None."""

    @abstractmethod
    def accept_trade(self, guild, item_offered_to_me, item_they_want, unvisited_rooms, config, rng):
        """Whether to accept a proposed swap (I give item_they_want, get item_offered_to_me)."""

    @abstractmethod
    def seek_purchase(self, guild, unvisited_rooms, config, rng):
        """Buying with coins, not items (source doc: 'exchange items for
        coins or other items' - found missing in review r1/F3, which noted
        it's the one instrument that can bridge a needed item's shadow
        value (up to 15) against what a seller who doesn't need it values
        it at in liquidation (at most 14), a gap plain item-for-item
        bartering can't cross. Returns (item_wanted, coins_offered) or None."""

    @abstractmethod
    def accept_purchase(self, guild, item_wanted, coins_offered, unvisited_rooms, config, rng):
        """Whether to sell item_wanted for coins_offered."""

    @abstractmethod
    def choose_reward_card(self, guild, available_cards, unvisited_rooms, config, rng):
        """Pick one card from the pool of available Tier-2 reward cards."""


def _unvisited_room_items(unvisited_rooms):
    return {I.ROOM_PREREQUISITE[r] for r in unvisited_rooms}


def _most_urgent(needed_items, unvisited_rooms):
    """The item needed for the nearest upcoming room, among needed_items.
    Falls back to a fixed deterministic order if none matches (shouldn't
    happen in practice, but keeps this total)."""
    for room in unvisited_rooms:
        item = I.ROOM_PREREQUISITE[room]
        if item in needed_items:
            return item
    return min(needed_items)


class GreedyPolicy(AgentPolicy):
    """Rational: values items by shadow value (analysis §2.2), reasons
    about upcoming room needs, only crafts up when it doesn't sacrifice
    room access, actively seeks trades to fill gaps."""
    name = "greedy"

    def choose_round1_craft(self, guild, options, rng):
        room = R.ROUND1_ROOM_BY_GUILD.get(guild.name)
        needed = I.ROOM_PREREQUISITE.get(room) if room else None
        if needed in options:
            return needed
        return options[0]

    def room_access_value(self, guild, item, unvisited_rooms, config):
        if item in _unvisited_room_items(unvisited_rooms):
            return config.room_coin_fallback_fee
        return I.SELL_PRICE[item]

    def should_craft_up(self, guild, tier2_a, tier2_b, unvisited_rooms, config):
        needed = _unvisited_room_items(unvisited_rooms)
        return tier2_a not in needed and tier2_b not in needed

    def seek_trade(self, guild, unvisited_rooms, config, rng):
        needed_items = _unvisited_room_items(unvisited_rooms) - set(guild.inventory)
        if not needed_items:
            return None
        spare = [item for item, qty in guild.inventory.items()
                 if qty > 0 and self.room_access_value(guild, item, unvisited_rooms, config) == I.SELL_PRICE[item]]
        if not spare:
            return None
        # Offer the highest-value spare item as bait - a Tier-1 surplus
        # (worth 1) is rarely enough to interest a partner holding a
        # needed Tier-2 card (worth up to 15 to them); a spare Tier-2
        # item they don't need is a fairer, more credible offer.
        best_bait = max(spare, key=lambda item: I.SELL_PRICE[item])
        # Which needed item to go after first: the one needed for the
        # nearest upcoming room (see _most_urgent) when that ordering is
        # available, otherwise a fixed deterministic fallback. Originally
        # picked via Python's per-process string-hash order (review
        # r1(PR#2)/F1, fixed to alphabetical), then refined to actual
        # urgency (review R8 on PR#3, once room order became available).
        return (_most_urgent(needed_items, unvisited_rooms), best_bait)

    def accept_trade(self, guild, item_offered_to_me, item_they_want, unvisited_rooms, config, rng):
        my_cost = self.room_access_value(guild, item_they_want, unvisited_rooms, config)
        my_gain = self.room_access_value(guild, item_offered_to_me, unvisited_rooms, config)
        return my_gain >= my_cost

    def seek_purchase(self, guild, unvisited_rooms, config, rng):
        needed_items = _unvisited_room_items(unvisited_rooms) - set(guild.inventory)
        if not needed_items:
            return None
        price = config.room_coin_fallback_fee  # never worse than just paying the GM
        if guild.coins < price:
            return None
        return (_most_urgent(needed_items, unvisited_rooms), price)

    def accept_purchase(self, guild, item_wanted, coins_offered, unvisited_rooms, config, rng):
        my_cost = self.room_access_value(guild, item_wanted, unvisited_rooms, config)
        return coins_offered >= my_cost

    def choose_reward_card(self, guild, available_cards, unvisited_rooms, config, rng):
        # Prioritize by ROOM URGENCY (unvisited_rooms is chronologically
        # ordered when the fixed rotation is used - see engine.py's
        # _unvisited_rooms), not by an arbitrary card order. Found via
        # review R8 on PR #3: the old version checked `card in needed`
        # against an unordered set, so it could grab an item needed for
        # a LATER room while missing the one needed next, forcing an
        # avoidable coin fallback - a real, structural cause of the
        # per-guild win-rate gap that review found.
        for room in unvisited_rooms:
            needed_item = I.ROOM_PREREQUISITE[room]
            if needed_item in available_cards:
                return needed_item
        return max(available_cards, key=lambda c: I.SELL_PRICE[c])


class CasualPolicy(AgentPolicy):
    """Casual: treats every Tier-2 item as an interchangeable liquidation
    value (the naive treatment analysis §2.2 corrected), crafts up
    greedily whenever possible regardless of upcoming rooms, rarely
    trades, and picks reward cards at random."""
    name = "casual"

    def choose_round1_craft(self, guild, options, rng):
        return rng.choice(options)

    def room_access_value(self, guild, item, unvisited_rooms, config):
        return I.SELL_PRICE[item]

    def should_craft_up(self, guild, tier2_a, tier2_b, unvisited_rooms, config):
        return True

    def seek_trade(self, guild, unvisited_rooms, config, rng):
        if rng.random() > 0.15 or not guild.inventory:
            return None
        have = [i for i, q in guild.inventory.items() if q > 0]
        want = rng.choice(I.TIER2)
        offered = rng.choice(have)
        return (want, offered)

    def accept_trade(self, guild, item_offered_to_me, item_they_want, unvisited_rooms, config, rng):
        return rng.random() < 0.5

    def seek_purchase(self, guild, unvisited_rooms, config, rng):
        if rng.random() > 0.15 or guild.coins < 5:
            return None
        want = rng.choice(I.TIER2)
        offer = rng.randint(5, min(guild.coins, config.room_coin_fallback_fee))
        return (want, offer)

    def accept_purchase(self, guild, item_wanted, coins_offered, unvisited_rooms, config, rng):
        return rng.random() < 0.5

    def choose_reward_card(self, guild, available_cards, unvisited_rooms, config, rng):
        return rng.choice(available_cards)


POLICIES = {"greedy": GreedyPolicy(), "casual": CasualPolicy()}
