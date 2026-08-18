import dataclasses

from sim.config import GameConfig
from sim.engine import GameEngine
from sim.experiment import run_batch, all_greedy_mix
from sim.policies import POLICIES


def test_disabling_coin_purchases_eliminates_purchase_transactions():
    config = dataclasses.replace(GameConfig(), allow_coin_purchases=False)
    policies = {n: POLICIES["greedy"] for n in config.guild_names}

    purchases = 0
    orig = POLICIES["greedy"].accept_purchase

    def traced(self, *a, **k):
        nonlocal purchases
        result = orig(self, *a, **k)
        if result:
            purchases += 1
        return result

    type(POLICIES["greedy"]).accept_purchase = traced
    try:
        for seed in range(20):
            GameEngine(config, policies, seed=seed).run()
    finally:
        type(POLICIES["greedy"]).accept_purchase = orig

    assert purchases == 0


def test_allow_coin_purchases_default_matches_current_ruleset():
    assert GameConfig().allow_coin_purchases is True


def test_loan_interest_multiplier_accepts_non_integer_values():
    config = dataclasses.replace(GameConfig(), loan_interest_multiplier=1.5)
    policies = {n: POLICIES["greedy"] for n in config.guild_names}
    result = GameEngine(config, policies, seed=1).run()  # should not raise
    assert result is not None


def test_lower_loan_interest_reduces_mean_debt():
    base = GameConfig()
    capped = dataclasses.replace(base, loan_interest_multiplier=1.0)
    mix = {n: "casual" for n in base.guild_names}  # casual play generates the most loans
    from sim.metrics import summarize

    base_results = run_batch(base, mix, n_trials=100, seed_start=0)
    capped_results = run_batch(capped, mix, n_trials=100, seed_start=0)
    base_debt = summarize(base_results)["mean_debt_per_guild"]
    capped_debt = summarize(capped_results)["mean_debt_per_guild"]
    assert capped_debt < base_debt
