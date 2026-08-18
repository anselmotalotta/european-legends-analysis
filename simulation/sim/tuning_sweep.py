"""
Tuning sweep: tests specific rule-tuning questions raised by early
findings from this simulator (see simulation/README.md's "Findings"
section), each as a genuine paired comparison (guardrail #3 -
comparative, not predictive) rather than a single run's symptom.

Run: python3 -m sim.tuning_sweep
"""
import dataclasses

from .config import GameConfig
from .experiment import run_batch, all_greedy_mix, all_casual_mix, mixed_policy_per_trial
from .metrics import summarize

N_TRIALS = 400


def _row(label, config, mix):
    results = run_batch(config, mix, n_trials=N_TRIALS, seed_start=0)
    s = summarize(results)
    guild_rates = list(s["win_rate_by_guild"].values())
    guild_spread = (max(guild_rates) / max(min(guild_rates), 1e-9)) if guild_rates else 0.0
    print(f"{label:38s} mean_score={s['score']['mean']:6.1f}  score_stdev={s['score']['stdev']:5.1f}  "
          f"stdev_excl_debt={s['score']['stdev_excluding_debt']:5.1f}  "
          f"complete%={s['pct_games_all_guilds_complete']:5.1f}  mean_debt={s['mean_debt_per_guild']:5.1f}  "
          f"barters={s['mean_barters_per_guild']:4.1f}  purchases={s['mean_purchases_per_guild']:4.1f}  "
          f"per_guild_win_ratio={guild_spread:5.2f}x")
    return s


def sweep_loan_interest():
    """Reports stdev_excluding_debt alongside plain score stdev, because
    the two can diverge misleadingly: multiplying a fixed debt
    distribution by a bigger constant necessarily widens plain score
    stdev even if guild BEHAVIOR is completely unchanged (review
    r1(PR#3)/F1 - none of this simulator's policies read the interest
    rate when deciding anything, so there is no behavioral channel for
    it to act through). Per review r5: even "mean debt scales with the
    multiplier" is the same identity one level removed - the number and
    size of loans taken is identical across multipliers (confirmed:
    total loan COUNT is pinned by a regression test), so debt is just
    that fixed total times different constants. Neither number is
    independent evidence for choosing one rate over another; 1.5x is a
    values choice, not a simulation finding. See simulation/README.md."""
    print("\n=== Sweep A: loan interest multiplier (mixed policy, per-trial random assignment) ===")
    base = GameConfig()
    mix = mixed_policy_per_trial(base)
    for multiplier in (1.0, 1.5, 2.0):
        config = dataclasses.replace(base, loan_interest_multiplier=multiplier)
        _row(f"multiplier={multiplier}", config, mix)


def sweep_coin_purchases():
    print("\n=== Sweep B: coin purchases allowed vs. barter-only ===")
    base = GameConfig()
    for mix_name, mix in (("all-greedy", all_greedy_mix(base)), ("all-casual", all_casual_mix(base)),
                           ("mixed", mixed_policy_per_trial(base))):
        for allow in (True, False):
            config = dataclasses.replace(base, allow_coin_purchases=allow)
            _row(f"{mix_name}, allow_coin_purchases={allow}", config, mix)


def sweep_reward_pick_order():
    print("\n=== Sweep C: reward pick order (mixed policy, per-trial random assignment) ===")
    base = GameConfig()
    mix = mixed_policy_per_trial(base)
    for order in ("winner_first", "loser_first", "random"):
        config = dataclasses.replace(base, reward_pick_order=order)
        _row(f"reward_pick_order={order}", config, mix)


def sweep_per_guild_fairness():
    """Review R8 on PR #3: win_rate_by_specialty averages away a large,
    real, per-guild disparity. Reports the actual per-guild win rates
    under identical (all-greedy) play directly, since that's the
    cleanest read on whether the rotation/starting-hand design (§7/§10)
    itself is fair - no policy or skill-mix confound. Originally a 7.2x
    spread with no explanation; review r7 traced it to
    COORDINATED_MISSING_MATERIAL leaving 4 of 8 guilds with only 1 usable
    Tier-1 recipe partner instead of 2 - fixed in sim/rotation.py (see
    test_review_pr3_r3_starting_hand_fix.py). What's printed below is
    what's left after that fix - expected to be noise-level, not the old
    3.4x-7.2x range."""
    print("\n=== Sweep D: per-guild win rate under identical policy (all-greedy) ===")
    config = GameConfig()
    mix = all_greedy_mix(config)
    results = run_batch(config, mix, n_trials=N_TRIALS, seed_start=0)
    s = summarize(results)
    for name, rate in sorted(s["win_rate_by_guild"].items(), key=lambda kv: -kv[1]):
        print(f"  {name:10s} {rate:.3f}  ({config.guild_specialty[name]})")
    rates = list(s["win_rate_by_guild"].values())
    print(f"  max/min ratio: {max(rates)/max(min(rates), 1e-9):.2f}x")
    print("  Was 7.2x before the starting-hand fix (see review r7 on PR #3); now")
    print("  consistent with ordinary sampling noise for an 8-way outcome.")


if __name__ == "__main__":
    sweep_loan_interest()
    sweep_coin_purchases()
    sweep_reward_pick_order()
    sweep_per_guild_fairness()
