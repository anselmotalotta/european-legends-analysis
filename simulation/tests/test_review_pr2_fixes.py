"""Regression tests for PR #2 review findings."""
import os
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_SNIPPET = """
from sim.config import GameConfig
from sim.experiment import run_batch, all_greedy_mix
from sim.metrics import summarize
res = run_batch(GameConfig(), all_greedy_mix(GameConfig()), n_trials=50, seed_start=0)
s = summarize(res)
print(round(s["mean_trades_per_guild"], 6))
print(round(s["score"]["mean"], 6))
"""


def _run_with_hashseed(hashseed):
    env = dict(os.environ, PYTHONHASHSEED=str(hashseed))
    result = subprocess.run(
        [sys.executable, "-c", _SNIPPET],
        cwd=REPO_ROOT, env=env, capture_output=True, text=True, timeout=60,
    )
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def test_F1_results_are_identical_across_process_hash_seeds():
    """review r1(PR#2)/F1: GreedyPolicy.seek_trade/seek_purchase used
    `next(iter(a_set))` to pick which item to pursue, which depends on
    Python's per-process string-hash randomization - so the *same seeded
    model* played a different game in different processes. Fixed by
    switching to `min(needed_items)` (a fixed, deterministic order)."""
    outputs = {_run_with_hashseed(seed) for seed in (0, 1, 2, 3)}
    assert len(outputs) == 1, f"results differ across PYTHONHASHSEED values: {outputs}"
