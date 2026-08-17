"""Regression tests for review r1's findings on commit 1d80903."""
import dataclasses
import random

from sim.config import GameConfig
from sim.engine import GameEngine, resolve_room_winner
from sim.experiment import compare, run_batch, all_greedy_mix
from sim.guild import Guild
from sim.policies import POLICIES


def test_F1_compare_uses_common_random_numbers():
    """compare() must run both arms on the same seed range so the only
    difference between them is the design change, not sampling noise."""
    base = GameConfig()
    variant = dataclasses.replace(base, room_win_bonus=0)  # a no-op-ish variant for this test
    report = compare(base, variant, all_greedy_mix(base), n_trials=5, seed_start=777)
    base_results = run_batch(base, all_greedy_mix(base), n_trials=5, seed_start=777)
    variant_results = run_batch(variant, all_greedy_mix(base), n_trials=5, seed_start=777)
    # Same seed => same starting hands/skill draws => guild-slot completion
    # (which room_win_bonus doesn't affect) should match exactly.
    for a, b in zip(base_results, variant_results):
        for name in a.guilds:
            assert a.guilds[name].rooms_visited == b.guilds[name].rooms_visited


def test_F2_ties_are_won_by_a_and_b_with_roughly_equal_frequency():
    rng = random.Random(0)
    a_wins = sum(resolve_room_winner(5, 5, rng) for _ in range(2000))
    assert 800 < a_wins < 1200  # not exactly always-True (2000) or always-False (0)


def test_F2_non_ties_are_never_randomized():
    rng = random.Random(0)
    assert all(resolve_room_winner(10, 3, rng) is True for _ in range(50))
    assert all(resolve_room_winner(3, 10, rng) is False for _ in range(50))


def test_F3_coin_purchase_can_complete():
    """A guild with coins and a need should be able to buy an item from a
    guild that doesn't need it, via seek_purchase/accept_purchase."""
    config = GameConfig()
    buyer = Guild(name="Buyer", specialty="Wax", coins=20)
    seller = Guild(name="Seller", specialty="Flax", coins=0)
    seller.add("Candle", 1)
    policy = POLICIES["greedy"]
    rng = random.Random(0)

    proposal = policy.seek_purchase(buyer, ["Room4"], config, rng)
    assert proposal == ("Candle", config.room_coin_fallback_fee)

    accepted = policy.accept_purchase(seller, "Candle", config.room_coin_fallback_fee, [], config, rng)
    assert accepted is True


def test_F3_trade_volume_is_no_longer_zero_under_rational_play():
    """Before F3, all-greedy play produced exactly 0 trades over any batch
    size - now that coin purchases exist, it should not be zero."""
    config = GameConfig()
    results = run_batch(config, all_greedy_mix(config), n_trials=100, seed_start=0)
    total_trades = sum(g.trade_count for r in results for g in r.guilds.values())
    assert total_trades > 0


def test_F4_reward_pick_order_accepts_all_three_variants():
    for order in ("winner_first", "loser_first", "random"):
        config = dataclasses.replace(GameConfig(), reward_pick_order=order)
        engine = GameEngine(config, {n: POLICIES["greedy"] for n in config.guild_names}, seed=1)
        result = engine.run()  # should not raise
        assert result is not None


def test_F4_reward_pick_order_rejects_unknown_value():
    config = dataclasses.replace(GameConfig(), reward_pick_order="bogus")
    engine = GameEngine(config, {n: POLICIES["greedy"] for n in config.guild_names}, seed=1)
    try:
        engine.run()
        assert False, "expected ValueError"
    except ValueError:
        pass
