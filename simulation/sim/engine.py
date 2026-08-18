"""
Game engine: runs one simulated game end-to-end. Deliberately scoped
per the analysis's guardrail to keep the first version small - models
the core economy, room access, trading, rewards, loans, and scoring
cleanly, WITHOUT guild-special Tier-3 items or unique per-guild quests
(analysis §2.6 - still "in elaboration" in the source).
"""
import random

from . import items as I
from . import quests as Q
from . import rotation as R
from .guild import Guild


def resolve_room_winner(score_a, score_b, rng):
    """Who actually won a room's combined quest score, tie broken
    randomly (source doc: "In case of a tie the item is chosen
    randomly"). Pulled out as a pure function per review r1/F2, which
    found the inline version (`score_a >= score_b`) silently made guild_a
    win every tie - and guild_a is whichever guild is listed first in
    FIXED_ROTATION's tuples, not evenly distributed across guilds."""
    if score_a > score_b:
        return True
    if score_b > score_a:
        return False
    return rng.random() < 0.5


def resolve_pick_order(a_won, reward_pick_order, rng):
    """Who picks their reward card first - a separate, configurable
    question (analysis §2.7/§8) from who actually won the room."""
    if reward_pick_order == "winner_first":
        return a_won
    if reward_pick_order == "loser_first":
        return not a_won
    if reward_pick_order == "random":
        return rng.random() < 0.5
    raise ValueError(f"unknown reward_pick_order: {reward_pick_order!r}")


class GameResult:
    def __init__(self, guilds, config):
        self.guilds = guilds
        self.config = config

    def scores(self):
        return {g.name: g.final_score(I.SELL_PRICE) for g in self.guilds.values()}


class GameEngine:
    def __init__(self, config, policy_assignment, seed=None):
        """policy_assignment: dict guild_name -> AgentPolicy instance."""
        self.config = config
        self.policies = policy_assignment
        self.rng = random.Random(seed)

    def _new_guild(self, name):
        return Guild(name=name, specialty=self.config.guild_specialty[name],
                     coins=self.config.starting_coins)

    def _deal_starting_hand(self, guild):
        if self.config.coordinate_starting_hands and self.config.use_fixed_rotation:
            missing = R.COORDINATED_MISSING_MATERIAL[guild.name]
        else:
            missing = self.rng.choice(I.TIER1)
        for t in I.TIER1:
            if t != missing:
                guild.add(t, 1)
        return missing

    def _craft_round1(self, guild, missing):
        options = I.tier1_options(missing)
        policy = self.policies[guild.name]
        chosen = policy.choose_round1_craft(guild, options, self.rng)
        a, b = [pair for pair in I.TIER1_RECIPES if I.TIER1_RECIPES[pair] == chosen][0]
        guild.remove(a, 1)
        guild.remove(b, 1)
        guild.add(chosen, 1)

    def _unvisited_rooms(self, guild):
        return [f"Room{i}" for i in range(1, self.config.n_rooms + 1)
                if f"Room{i}" not in guild.rooms_visited]

    def _pay_room_fee(self, guild, room):
        needed = I.ROOM_PREREQUISITE[room]
        if guild.has(needed):
            guild.remove(needed, 1)
            return "item"
        fee = self.config.room_coin_fallback_fee
        if guild.coins >= fee:
            guild.coins -= fee
        else:
            shortfall = fee - guild.coins
            guild.coins = 0
            guild.take_loan(shortfall, self.config.loan_interest_multiplier)
        return "coin"

    def _run_room(self, round_index, room, guild_a_name, guild_b_name, guilds):
        ga, gb = guilds[guild_a_name], guilds[guild_b_name]
        ga.rooms_visited.add(room)
        gb.rooms_visited.add(room)
        ga.opponents_faced.append(gb.name)
        gb.opponents_faced.append(ga.name)

        method_a = self._pay_room_fee(ga, room)
        method_b = self._pay_room_fee(gb, room)

        skill_a, skill_b = Q.draw_skill(self.rng), Q.draw_skill(self.rng)
        score_a, score_b = Q.score_room(room, ga, gb, skill_a, skill_b, self.rng,
                                         self.config.room_win_bonus, self.config.room_tie_bonus)
        ga.coins += score_a
        ga.quest_coins_earned += score_a
        gb.coins += score_b
        gb.quest_coins_earned += score_b

        # Reward pool excludes the room's Tier-2 prerequisite ("the one
        # they paid") regardless of payment method - so a coin-paying
        # guild is treated the same as an item-paying one here. Noted by
        # review r1 as a second, unflagged reading of the same §4 item 2
        # that coin_payment_grants_reward_card already flags explicitly;
        # kept as-is (harmless per that review) rather than adding a
        # second config flag for a very similar assumption.
        paid_item = I.ROOM_PREREQUISITE[room]
        pool = [t for t in I.TIER2 if t != paid_item]

        a_won = resolve_room_winner(score_a, score_b, self.rng)
        a_first = resolve_pick_order(a_won, self.config.reward_pick_order, self.rng)
        order = [(ga, method_a), (gb, method_b)] if a_first else [(gb, method_b), (ga, method_a)]

        if self.config.shared_reward_pool:
            available = list(pool)
            for guild, method, in order:
                if method == "coin" and not self.config.coin_payment_grants_reward_card:
                    continue
                if not available:
                    continue
                policy = self.policies[guild.name]
                card = policy.choose_reward_card(guild, available, self._unvisited_rooms(guild), self.config, self.rng)
                available.remove(card)
                guild.add(card, 1)
        else:
            for guild, method in order:
                if method == "coin" and not self.config.coin_payment_grants_reward_card:
                    continue
                policy = self.policies[guild.name]
                card = policy.choose_reward_card(guild, list(pool), self._unvisited_rooms(guild), self.config, self.rng)
                guild.add(card, 1)

    def _craft_and_trade(self, guilds, allow_production, break_index):
        # Production
        if allow_production:
            qty = self.config.production_per_break[break_index]
            for guild in guilds.values():
                guild.add(guild.specialty, qty)

        # Crafting: Tier1->Tier2, then Tier2->Tier3, greedily where a
        # guild's policy says to (Tier1->2 is always worth it - it's a
        # pure conversion with no downside modeled here; Tier2->3 is
        # policy-gated per analysis §2.2's shadow-value point). Noted by
        # review r1: converting Tier-1 unconditionally also converts away
        # the Tier-1 surplus that would otherwise sit in inventory as
        # tradeable stock - a second, quiet contributor (beyond the
        # missing coin-purchase path) to why trade volume is low under
        # rational play. Left unconditional for v1 since it's the
        # economically correct move in isolation (2 coins of input yields
        # 4 of output); worth revisiting if trade volume is investigated
        # further.
        for guild in guilds.values():
            unvisited = self._unvisited_rooms(guild)
            changed = True
            while changed:
                changed = False
                for pair, product in I.TIER1_RECIPES.items():
                    # sorted(), not tuple(): frozenset iteration order is
                    # hash-seed-dependent per process; a/b order doesn't
                    # change behavior here (removal is symmetric) but an
                    # explicit deterministic order removes any doubt.
                    a, b = sorted(pair)
                    if guild.has(a) and guild.has(b):
                        guild.remove(a, 1)
                        guild.remove(b, 1)
                        guild.add(product, 1)
                        changed = True
            policy = self.policies[guild.name]
            changed = True
            while changed:
                changed = False
                for pair, product in I.TIER2_RECIPES.items():
                    # sorted(), not tuple(): frozenset iteration order is
                    # hash-seed-dependent per process; a/b order doesn't
                    # change behavior here (removal is symmetric) but an
                    # explicit deterministic order removes any doubt.
                    a, b = sorted(pair)
                    if guild.has(a) and guild.has(b):
                        if policy.should_craft_up(guild, a, b, unvisited, self.config):
                            guild.remove(a, 1)
                            guild.remove(b, 1)
                            guild.add(product, 1)
                            changed = True

        # Trading: one pass, random guild order. Each guild tries an
        # item-for-item swap first, then - if that doesn't clear - a
        # coin purchase (source doc: "exchange items for coins or other
        # items"; added per review r1/F3, which correctly noted a pure
        # item-swap can't bridge a needed item's shadow value against a
        # seller's lower liquidation valuation of it, but a coin
        # side-payment can).
        order = list(guilds.keys())
        self.rng.shuffle(order)
        for name in order:
            guild = guilds[name]
            policy = self.policies[name]
            unvisited = self._unvisited_rooms(guild)
            partners = [n for n in order if n != name]
            self.rng.shuffle(partners)

            traded = False
            proposal = policy.seek_trade(guild, unvisited, self.config, self.rng)
            if proposal:
                wanted, offered = proposal
                if guild.has(offered):
                    for pname in partners:
                        partner = guilds[pname]
                        if not partner.has(wanted):
                            continue
                        partner_policy = self.policies[pname]
                        partner_unvisited = self._unvisited_rooms(partner)
                        if partner_policy.accept_trade(partner, offered, wanted, partner_unvisited, self.config, self.rng):
                            guild.remove(offered, 1)
                            partner.remove(wanted, 1)
                            guild.add(wanted, 1)
                            partner.add(offered, 1)
                            guild.trade_count += 1
                            partner.trade_count += 1
                            guild.trade_partners.add(pname)
                            partner.trade_partners.add(name)
                            traded = True
                            break

            if traded:
                continue

            purchase = policy.seek_purchase(guild, unvisited, self.config, self.rng)
            if not purchase:
                continue
            wanted, coins_offered = purchase
            if guild.coins < coins_offered:
                continue
            for pname in partners:
                partner = guilds[pname]
                if not partner.has(wanted):
                    continue
                partner_policy = self.policies[pname]
                partner_unvisited = self._unvisited_rooms(partner)
                if partner_policy.accept_purchase(partner, wanted, coins_offered, partner_unvisited, self.config, self.rng):
                    guild.coins -= coins_offered
                    partner.coins += coins_offered
                    partner.remove(wanted, 1)
                    guild.add(wanted, 1)
                    guild.trade_count += 1
                    partner.trade_count += 1
                    guild.trade_partners.add(pname)
                    partner.trade_partners.add(name)
                    break

    def _assign_rooms_free_choice(self, round_index, guilds):
        """Free-choice scheduling variant: reuses the toy-scheduling-model
        policy (random order, pick uniformly among unvisited rooms with a
        free slot) so it's directly comparable to simulation/toy_scheduling_model.py."""
        capacity = {f"Room{i}": 2 for i in range(1, self.config.n_rooms + 1)}
        order = list(guilds.keys())
        self.rng.shuffle(order)
        assignment = {}
        pending = []
        for name in order:
            guild = guilds[name]
            eligible = [r for r, cap in capacity.items() if cap > 0 and r not in guild.rooms_visited]
            if not eligible:
                continue
            room = self.rng.choice(eligible)
            capacity[room] -= 1
            pending.append((room, name))
        by_room = {}
        for room, name in pending:
            by_room.setdefault(room, []).append(name)
        pairs = []
        for room, names in by_room.items():
            if len(names) == 2:
                pairs.append((room, names[0], names[1]))
            # a room with only 1 guild that round has no opponent - skip
            # (matches "two other guilds already paid" lockout in the rules)
        return pairs

    def run(self):
        guilds = {name: self._new_guild(name) for name in self.config.guild_names}
        missing = {name: self._deal_starting_hand(g) for name, g in guilds.items()}
        for name, g in guilds.items():
            self._craft_round1(g, missing[name])

        for round_index in range(self.config.n_rounds):
            if self.config.use_fixed_rotation:
                pairs = [(room, a, b) for room, (a, b) in R.FIXED_ROTATION[round_index].items()]
            else:
                pairs = self._assign_rooms_free_choice(round_index, guilds)
            for room, a, b in pairs:
                self._run_room(round_index, room, a, b, guilds)

            if round_index < 3:
                self._craft_and_trade(guilds, allow_production=True, break_index=round_index)

        # Final trading window: no production, one more craft/trade pass.
        self._craft_and_trade(guilds, allow_production=False, break_index=None)

        return GameResult(guilds, self.config)
