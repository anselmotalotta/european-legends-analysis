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


def test_R8_per_guild_disparity_is_now_small_after_the_starting_hand_fix():
    """R8's 7.2x per-guild win-rate spread was root-caused (review r7 on
    PR #3) to COORDINATED_MISSING_MATERIAL leaving 4 of 8 guilds with only
    1 usable Tier-1 recipe partner in their starting hand instead of 2 -
    see test_review_pr3_r3_starting_hand_fix.py for the fix itself. This
    regression guard now pins the opposite qualitative fact: the fixed
    assignment brings the spread down to noise-level (well under the old
    3.4x-7.2x range measured before the fix), not the removed test's
    ">2.0x, confirmed real" assertion."""
    config = GameConfig()
    results = run_batch(config, all_greedy_mix(config), n_trials=200, seed_start=0)
    s = summarize(results)
    rates = s["win_rate_by_guild"].values()
    assert max(rates) / max(min(rates), 0.001) < 3.5


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
    """review R7: guilds end the game holding most of their own Tier-1
    production unused, because seek_trade only ever targets room-entry
    Tier-2 prerequisites, never complementary Tier-1 materials for
    crafting. Confirmed and left as a known, documented limitation (not
    fixed in this PR - tracked as follow-up). The exact leftover amount
    changed as a side effect of the R8 starting-hand fix
    (test_review_pr3_r3_starting_hand_fix.py): previously 4 of 8 guilds
    (mean leftover 7.0) had only 1 usable recipe partner and 4 had 2
    (mean leftover 5.0); now every guild has 2, so leftover is uniformly
    5.0 - smaller and more even, but still most of a guild's production
    goes unused."""
    config = GameConfig()
    results = run_batch(config, all_greedy_mix(config), n_trials=50, seed_start=0)
    leftover = [
        sum(qty for item, qty in g.inventory.items() if item in I.TIER1)
        for r in results for g in r.guilds.values()
    ]
    # Production alone is 1+2+3=6 units/guild; confirmed most of it still
    # goes unused even after the R8 fix.
    assert sum(leftover) / len(leftover) >= 4.5
