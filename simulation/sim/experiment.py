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
    """policy_mix: dict guild_name -> policy name ('greedy' or 'casual')."""
    assignment = {name: POLICIES[policy_mix[name]] for name in config.guild_names}
    results = []
    for i in range(n_trials):
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
    import random
    rng = random.Random(seed)
    names = list(config.guild_names)
    rng.shuffle(names)
    n_greedy = round(len(names) * greedy_fraction)
    return {name: ("greedy" if i < n_greedy else "casual") for i, name in enumerate(names)}


if __name__ == "__main__":
    from .config import GameConfig
    import json

    base = GameConfig()
    free_choice = dataclasses.replace(base, use_fixed_rotation=False, coordinate_starting_hands=False)

    for mix_name, mix_fn in [("all-greedy", all_greedy_mix), ("all-casual", all_casual_mix),
                              ("mixed", mixed_policy)]:
        mix = mix_fn(base)
        report = compare(base, free_choice, mix, n_trials=500,
                          label_base="fixed_rotation", label_variant="free_choice")
        print(f"\n=== policy mix: {mix_name} ===")
        print(json.dumps(report, indent=2, default=str))
