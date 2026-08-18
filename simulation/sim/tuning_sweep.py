"""
Tuning sweep: tests specific rule-tuning questions raised by early
findings from this simulator (see simulation/README.md's "Findings"
section), each as a genuine paired comparison (guardrail #3 -
comparative, not predictive) rather than a single run's symptom.

Run: python3 -m sim.tuning_sweep
"""
import dataclasses
import statistics as stats

from .config import GameConfig
from .experiment import run_batch, all_greedy_mix, all_casual_mix, mixed_policy
from .metrics import summarize

N_TRIALS = 400


def _row(label, config, mix):
    results = run_batch(config, mix, n_trials=N_TRIALS, seed_start=0)
    s = summarize(results)
    win_rates = s["win_rate_by_specialty"].values()
    spread = (max(win_rates) - min(win_rates)) if win_rates else 0.0
    print(f"{label:38s} mean_score={s['score']['mean']:6.1f}  score_stdev={s['score']['stdev']:5.1f}  "
          f"complete%={s['pct_games_all_guilds_complete']:5.1f}  mean_debt={s['mean_debt_per_guild']:5.1f}  "
          f"mean_exchanges={s['mean_trades_per_guild']:4.1f}  specialty_spread={spread:.3f}")
    return s


def sweep_loan_interest():
    print("\n=== Sweep A: loan interest multiplier (mixed policy) ===")
    base = GameConfig()
    mix = mixed_policy(base)
    for multiplier in (1.0, 1.5, 2.0):
        config = dataclasses.replace(base, loan_interest_multiplier=multiplier)
        _row(f"multiplier={multiplier}", config, mix)


def sweep_coin_purchases():
    print("\n=== Sweep B: coin purchases allowed vs. barter-only ===")
    base = GameConfig()
    for mix_name, mix_fn in (("all-greedy", all_greedy_mix), ("all-casual", all_casual_mix), ("mixed", mixed_policy)):
        mix = mix_fn(base)
        for allow in (True, False):
            config = dataclasses.replace(base, allow_coin_purchases=allow)
            _row(f"{mix_name}, allow_coin_purchases={allow}", config, mix)


def sweep_reward_pick_order():
    print("\n=== Sweep C: reward pick order (mixed policy) ===")
    base = GameConfig()
    mix = mixed_policy(base)
    for order in ("winner_first", "loser_first", "random"):
        config = dataclasses.replace(base, reward_pick_order=order)
        _row(f"reward_pick_order={order}", config, mix)


if __name__ == "__main__":
    sweep_loan_interest()
    sweep_coin_purchases()
    sweep_reward_pick_order()
