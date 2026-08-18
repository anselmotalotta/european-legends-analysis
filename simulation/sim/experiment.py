"""
Comparative experiment runner (analysis guardrail #3: "make the
simulator comparative, not predictive" - its strongest output is
"design A is robustly better than design B," not a point prediction
about the real event).
"""
import dataclasses

from .engine import GameEngine
from .metrics import summarize
from .policies import POLICIES


def run_batch(config, policy_mix, n_trials, seed_start=0):
    """policy_mix: either a dict guild_name -> policy name ('greedy' or
    'casual'), used unchanged for every trial, OR a callable
    seed -> dict, called fresh per trial so the assignment varies with
    the seed (see mixed_policy_per_trial). Found via investigating
    review R8 on PR #3: a *static* mixed policy_mix (the same 4 guilds
    always greedy, the same 4 always casual across an entire batch) was
    confounding every "mixed policy" result in this project with which
    SPECIFIC guilds happened to draw the better-performing policy - a
    37x win-rate spread that had nothing to do with rotation position
    and everything to do with a fixed random.Random(seed=0) call. Static
    dicts are kept working for all_greedy_mix/all_casual_mix, which are
    uniform and have nothing to confound."""
    results = []
    for i in range(n_trials):
        mix = policy_mix(seed_start + i) if callable(policy_mix) else policy_mix
        assignment = {name: POLICIES[mix[name]] for name in config.guild_names}
        engine = GameEngine(config, assignment, seed=seed_start + i)
        results.append(engine.run())
    return results


def compare(base_config, variant_config, policy_mix, n_trials, label_base="baseline", label_variant="variant", seed_start=0):
    """Paired comparison using common random numbers: both arms see the same
    seed for trial i, so the same skill draws, starting hands, and shuffle
    order hit both configs. This isolates the design-change effect from
    sampling noise (found missing in review r1/F1 - the two arms previously
    ran on disjoint seed ranges, which let noise masquerade as signal; e.g.
    an unpaired run showed a fully inverted specialty win-rate ranking that
    vanished under pairing)."""
    base_results = run_batch(base_config, policy_mix, n_trials, seed_start=seed_start)
    variant_results = run_batch(variant_config, policy_mix, n_trials, seed_start=seed_start)
    return {
        label_base: summarize(base_results),
        label_variant: summarize(variant_results),
    }


def all_greedy_mix(config):
    return {name: "greedy" for name in config.guild_names}


def all_casual_mix(config):
    return {name: "casual" for name in config.guild_names}


def mixed_policy(config, greedy_fraction=0.5, seed=0):
    """A single, fixed greedy/casual assignment. Useful when you
    deliberately want one static mix (e.g. asserting a property of
    'these 4 guilds greedy, these 4 casual'), but NOT for measuring
    anything about guilds or rotation fairness in aggregate across many
    trials - the same 4 guilds get the (much stronger) greedy policy
    every single trial, which will dominate any per-guild statistic.
    Use mixed_policy_per_trial for that instead."""
    import random
    rng = random.Random(seed)
    names = list(config.guild_names)
    rng.shuffle(names)
    n_greedy = round(len(names) * greedy_fraction)
    return {name: ("greedy" if i < n_greedy else "casual") for i, name in enumerate(names)}


def mixed_policy_per_trial(config, greedy_fraction=0.5):
    """Returns a callable seed -> dict, re-shuffling the greedy/casual
    assignment fresh for every trial (pass to run_batch/compare
    directly). This is what "mixed skill" should mean across a batch:
    which specific guilds are strong varies game to game, the way it
    would at a real event with random team assignment - not the same 4
    colleagues being uniformly better than the other 4 every single
    game."""
    def make_mix(seed):
        return mixed_policy(config, greedy_fraction=greedy_fraction, seed=seed)
    return make_mix


def print_human_summary(report, mix_name):
    """Plain-English summary of one compare() report, for readers who
    don't want to parse the raw numbers themselves. Pass --json on the
    command line instead to see the full data."""
    print(f"\n===================================================")
    print(f" Policy mix: {mix_name}")
    print(f"===================================================")
    for label, summary in report.items():
        print(f"\n  --- {label} ---")
        print(f"  Ran {summary['n_games']} practice games.")
        print(f"  Average final score across all guilds: {summary['score']['mean']:.1f} coins "
              f"(lowest game: {summary['score']['min']}, highest: {summary['score']['max']}).")
        print(f"  All 8 guilds visited all 4 rooms in {summary['pct_games_all_guilds_complete']:.0f}% of games.")
        # "Trades" here is swaps and coin purchases combined (metrics.py
        # doesn't separate them yet - see simulation/README.md's
        # not-yet-done list) - worded as "exchanges" so it doesn't read
        # as bartering specifically (review r1(PR#2)/F3).
        print(f"  On average, each guild made {summary['mean_trades_per_guild']:.1f} exchanges with other guilds "
              f"- swaps or coin purchases - ({summary['pct_guilds_zero_trades']:.0f}% of guilds made none at all).")
        print(f"  On average, each guild took out {summary['mean_loans_per_guild']:.1f} loan(s), "
              f"ending the game owing {summary['mean_debt_per_guild']:.1f} coins in debt.")
    print()


if __name__ == "__main__":
    import sys
    from .config import GameConfig

    show_raw_json = "--json" in sys.argv

    base = GameConfig()
    free_choice = dataclasses.replace(base, use_fixed_rotation=False, coordinate_starting_hands=False)

    for mix_name, mix in [("all-greedy", all_greedy_mix(base)), ("all-casual", all_casual_mix(base)),
                          ("mixed", mixed_policy_per_trial(base))]:
        report = compare(base, free_choice, mix, n_trials=500,
                          label_base="fixed_rotation", label_variant="free_choice")
        if show_raw_json:
            import json
            print(f"\n=== policy mix: {mix_name} ===")
            print(json.dumps(report, indent=2, default=str))
        else:
            print_human_summary(report, mix_name)
