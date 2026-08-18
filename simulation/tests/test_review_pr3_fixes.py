"""Regression tests for PR #3 review findings."""
import dataclasses

from sim.config import GameConfig
from sim.engine import GameEngine
from sim.experiment import run_batch, all_greedy_mix, mixed_policy
from sim.guild import Guild
from sim.metrics import summarize
from sim import items as I


def test_F2_barter_and_purchase_counts_are_tracked_separately():
    """review r1(PR#3)/F2: trade_count alone can't distinguish barter from
    coin purchases, which produced a materially wrong claim ("0 completed
    transactions either way") in the PR that introduced allow_coin_purchases.
    barter_count and purchase_count must be trackable independently."""
    config = GameConfig()
    results = run_batch(config, all_greedy_mix(config), n_trials=100, seed_start=0)
    total_purchases = sum(g.purchase_count for r in results for g in r.guilds.values())
    total_barters = sum(g.barter_count for r in results for g in r.guilds.values())
    # Purchases dominate under all-greedy play; barter is rare but no
    # longer strictly zero after the R8 fix (choose_reward_card/seek_trade
    # now target the guild's actual next need instead of an arbitrary
    # one, which occasionally lets a barter clear that couldn't before).
    assert total_purchases > 0
    assert total_purchases > total_barters * 10  # purchases still dominate heavily
    # trade_count must still equal the sum of the two (backward compatible).
    for r in results:
        for g in r.guilds.values():
            assert g.trade_count == g.barter_count + g.purchase_count


def test_F2_disabling_purchases_actually_removes_transactions_not_zero_either_way():
    """The corrected claim: purchases-off has 0 transactions, purchases-on
    does not (it was wrongly described as "0 either way")."""
    config_on = GameConfig()
    config_off = dataclasses.replace(config_on, allow_coin_purchases=False)
    mix = all_greedy_mix(config_on)

    results_on = run_batch(config_on, mix, n_trials=50, seed_start=0)
    results_off = run_batch(config_off, mix, n_trials=50, seed_start=0)

    total_on = sum(g.trade_count for r in results_on for g in r.guilds.values())
    total_off = sum(g.trade_count for r in results_off for g in r.guilds.values())

    assert total_on > 0
    assert total_off == 0


def test_F1_score_stdev_excluding_debt_is_unaffected_by_loan_interest():
    """review r1(PR#3)/F1: raw score stdev widens with the loan interest
    multiplier purely because a fixed debt distribution is being scaled by
    a bigger constant - not because guild behavior changes (no policy
    reads the interest rate). stdev_excluding_debt must be stable across
    multipliers while plain stdev is not, proving the effect is
    arithmetic, not behavioral."""
    base = GameConfig()
    mix = mixed_policy(base)
    stdevs = []
    stdevs_excl_debt = []
    for multiplier in (1.0, 1.5, 2.0):
        config = dataclasses.replace(base, loan_interest_multiplier=multiplier)
        results = run_batch(config, mix, n_trials=100, seed_start=0)
        s = summarize(results)
        stdevs.append(s["score"]["stdev"])
        stdevs_excl_debt.append(s["score"]["stdev_excluding_debt"])

    assert stdevs[0] < stdevs[2]  # raw stdev does widen with the multiplier
    # stdev excluding debt is identical (same seeds, same behavior, only
    # the final debt subtraction differs) - allow only float rounding noise.
    assert max(stdevs_excl_debt) - min(stdevs_excl_debt) < 0.01


def test_scores_excluding_debt_equals_score_plus_total_debt():
    g = Guild(name="Test", specialty="Wax", coins=20)
    g.add("Candle", 2)  # liquidation value 8
    g.take_loan(5, multiplier=1.5)  # debt = ceil(7.5) = 8
    score = g.final_score(I.SELL_PRICE)
    assert score + g.total_debt() == g.coins + g.liquidation_value(I.SELL_PRICE)
