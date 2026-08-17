import dataclasses

from sim.config import GameConfig
from sim.engine import GameEngine
from sim.experiment import run_batch, all_greedy_mix, all_casual_mix
from sim.metrics import summarize
from sim.policies import POLICIES
from sim import items as I


def _greedy_engine(seed, config=None):
    config = config or GameConfig()
    policies = {name: POLICIES["greedy"] for name in config.guild_names}
    return GameEngine(config, policies, seed=seed)


def test_game_runs_without_error_and_produces_all_guilds():
    result = _greedy_engine(seed=1).run()
    assert set(result.guilds.keys()) == set(GameConfig().guild_names)


def test_fixed_rotation_every_guild_visits_all_rooms():
    result = _greedy_engine(seed=2).run()
    for guild in result.guilds.values():
        assert len(guild.rooms_visited) == 4


def test_scores_are_deterministic_given_seed():
    r1 = _greedy_engine(seed=42).run()
    r2 = _greedy_engine(seed=42).run()
    assert r1.scores() == r2.scores()


def test_different_seeds_usually_give_different_scores():
    r1 = _greedy_engine(seed=1).run()
    r2 = _greedy_engine(seed=2).run()
    assert r1.scores() != r2.scores()


def test_no_negative_inventory_ever_reachable():
    # A guild's inventory Counter should never go negative - Guild.remove()
    # raises rather than allowing that, so a clean run implies this held.
    result = _greedy_engine(seed=3).run()
    for guild in result.guilds.values():
        assert all(qty > 0 for qty in guild.inventory.values())


def test_fixed_rotation_gives_full_room_completion():
    config = GameConfig()
    mix = all_greedy_mix(config)
    results = run_batch(config, mix, n_trials=20, seed_start=0)
    summary = summarize(results)
    assert summary["pct_games_all_guilds_complete"] == 100.0


def test_free_choice_gives_incomplete_room_completion():
    """Sanity check against the standalone toy model's ~38% figure
    (simulation/toy_scheduling_model.py) - not an exact match expected,
    since this engine additionally requires 2 guilds per room to award a
    visit (see simulation/README.md), but it should be well below 100%."""
    config = dataclasses.replace(GameConfig(), use_fixed_rotation=False, coordinate_starting_hands=False)
    mix = all_greedy_mix(config)
    results = run_batch(config, mix, n_trials=100, seed_start=0)
    summary = summarize(results)
    assert summary["pct_games_all_guilds_complete"] < 90.0


def test_casual_policy_produces_more_loans_than_greedy():
    config = GameConfig()
    greedy_results = run_batch(config, all_greedy_mix(config), n_trials=100, seed_start=0)
    casual_results = run_batch(config, all_casual_mix(config), n_trials=100, seed_start=0)
    greedy_summary = summarize(greedy_results)
    casual_summary = summarize(casual_results)
    assert casual_summary["mean_debt_per_guild"] > greedy_summary["mean_debt_per_guild"]


def test_liquidation_value_uses_sell_price_table():
    result = _greedy_engine(seed=5).run()
    guild = next(iter(result.guilds.values()))
    expected = sum(I.SELL_PRICE[item] * qty for item, qty in guild.inventory.items())
    assert guild.liquidation_value(I.SELL_PRICE) == expected
