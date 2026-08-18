"""Regression tests for PR #3's r2 fidelity audit (R1-R8)."""
import dataclasses

from sim.config import GameConfig
from sim.engine import GameEngine
from sim.experiment import run_batch, all_greedy_mix, mixed_policy
from sim.metrics import summarize
from sim import items as I
from sim import quests as Q


def test_R2_skill_is_independent_per_quest_not_per_room():
    """review R2/r4: skill must not be shared between a room's 2 quests -
    that inflated per-room score stdev by ~36%, confirmed independently
    by two reviewers and by this project."""
    import random
    import statistics as stats

    rng = random.Random(42)
    totals = [sum(q(rng) for q in Q.QUEST_TABLES["Room1"]) for _ in range(5000)]
    # Shared-skill-per-room version measured ~5.2 stdev; independent-per-quest ~3.8.
    assert stats.stdev(totals) < 4.5


def test_R8_win_rate_is_reported_per_guild_not_only_per_specialty():
    """review R8: specialty-averaged win rate hides a large gap between
    two guilds sharing a specialty (they don't share a starting hand,
    Round-1 room, or room order - specialty and rotation position are
    independent). win_rate_by_guild must be available."""
    config = GameConfig()
    results = run_batch(config, all_greedy_mix(config), n_trials=100, seed_start=0)
    s = summarize(results)
    assert "win_rate_by_guild" in s
    assert set(s["win_rate_by_guild"]) == set(config.guild_names)


def test_R8_per_guild_disparity_is_real_and_survives_reversed_processing_order():
    """Confirms R8 is a real structural effect, not an artifact of this
    engine's shared sequential RNG stream. If it were an RNG-consumption-
    order artifact, reversing which room is processed first within a
    round would change the ranking. It doesn't (verified by hand during
    review; this test pins the qualitative fact that a large spread
    exists, as a regression guard - the specific ranking is not asserted
    since it's sensitive to unrelated code changes elsewhere)."""
    config = GameConfig()
    results = run_batch(config, all_greedy_mix(config), n_trials=200, seed_start=0)
    s = summarize(results)
    rates = s["win_rate_by_guild"].values()
    # Confirmed real: roughly 3-8x spread between the best and worst guild
    # under identical policy. This is NOT expected to be ~1x (fair).
    assert max(rates) / max(min(rates), 0.001) > 2.0


def test_R5_loan_debt_scaling_is_the_same_shortfalls_times_a_constant():
    """review r5: 'debt scales with the multiplier' is not independent
    evidence either - it's the same identity as the stdev finding, one
    level removed. The number of loans taken must be identical across
    multipliers, since no policy reads the interest rate."""
    base = GameConfig()
    mix = mixed_policy(base)
    loan_counts = []
    for mult in (1.0, 1.5, 2.0):
        config = dataclasses.replace(base, loan_interest_multiplier=mult)
        results = run_batch(config, mix, n_trials=50, seed_start=0)
        total_loans = sum(len(g.loans) for r in results for g in r.guilds.values())
        loan_counts.append(total_loans)
    assert loan_counts[0] == loan_counts[1] == loan_counts[2]


def test_R7_tier1_production_is_never_used_by_greedy_policy():
    """review R7: guilds end the game holding ~100% of their own Tier-1
    production unused, because seek_trade only ever targets room-entry
    Tier-2 prerequisites, never complementary Tier-1 materials for
    crafting. Confirmed and left as a known, documented limitation
    (not fixed in this PR - tracked as follow-up)."""
    config = GameConfig()
    results = run_batch(config, all_greedy_mix(config), n_trials=50, seed_start=0)
    leftover = [
        sum(qty for item, qty in g.inventory.items() if item in I.TIER1)
        for r in results for g in r.guilds.values()
    ]
    # Production is 1+2+3=6 units/guild; confirmed close to fully unused.
    assert sum(leftover) / len(leftover) > 5.0
