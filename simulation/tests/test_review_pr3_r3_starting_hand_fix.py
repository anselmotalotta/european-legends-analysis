"""Regression tests for PR #3's r7 finding: R8's 7.2x per-guild win-rate
gap traces to COORDINATED_MISSING_MATERIAL leaving 4 of 8 guilds with
only 1 usable Tier-1 recipe partner in their starting hand (instead of
2), and the fix is a different, still-Round-1-valid choice of missing
material per guild - not a policy or rotation change."""
from sim.config import GameConfig
from sim.experiment import run_batch, all_greedy_mix
from sim.metrics import summarize
from sim.rotation import COORDINATED_MISSING_MATERIAL, ROUND1_ROOM_BY_GUILD
from sim import items as I


def _partners_in_hand(own, missing):
    hand = [t for t in I.TIER1 if t != missing]
    return [h for h in hand if h != own and I.TIER1_RECIPES.get(frozenset({own, h}))]


def test_every_guild_has_two_usable_recipe_partners_in_its_starting_hand():
    """The root cause, pinned directly: every guild's own Tier-1 specialty
    must pair with 2 of the 3 types in its starting hand, not 1. Before
    the fix, Bursa/Stockholm/Gdansk/Venice had only 1 (review r7 on
    PR #3)."""
    config = GameConfig()
    for guild, own in config.guild_specialty.items():
        missing = COORDINATED_MISSING_MATERIAL[guild]
        partners = _partners_in_hand(own, missing)
        assert len(partners) == 2, (guild, own, missing, partners)


def test_round1_room_prerequisite_is_still_craftable_from_the_starting_hand():
    """The fix must not break the original guarantee this table exists
    for: every guild can still pay its Round-1 room's Tier-2 fee straight
    from its opening 3-item hand, with no loan or trade needed."""
    config = GameConfig()
    for guild in config.guild_specialty:
        missing = COORDINATED_MISSING_MATERIAL[guild]
        room = ROUND1_ROOM_BY_GUILD[guild]
        needed_item = I.ROOM_PREREQUISITE[room]
        needed_pair = next(pair for pair, item in I.TIER1_RECIPES.items() if item == needed_item)
        hand = {t for t in I.TIER1 if t != missing}
        assert needed_pair <= hand, (guild, missing, room, needed_item)


def test_per_guild_win_rate_spread_drops_sharply_after_the_fix():
    """The whole point of the fix: measured spread should land well
    within noise range for 8 roughly-equal guilds, not the 3.4x-7.2x
    range measured before it (see test_review_pr3_r2_fidelity_audit.py)."""
    config = GameConfig()
    results = run_batch(config, all_greedy_mix(config), n_trials=400, seed_start=0)
    s = summarize(results)
    rates = list(s["win_rate_by_guild"].values())
    assert max(rates) / max(min(rates), 1e-9) < 3.0


def test_leftover_tier1_inventory_is_now_uniform_across_guilds():
    """Before the fix, leftover Tier-1 inventory split cleanly into two
    groups (5.0 vs. 7.0 units/guild) tracking the 1-vs-2-partner split.
    After the fix, every guild has 2 partners, so leftover should be
    uniformly low variance across guilds, not bimodal."""
    config = GameConfig()
    results = run_batch(config, all_greedy_mix(config), n_trials=100, seed_start=0)
    per_guild = {}
    for r in results:
        for name, g in r.guilds.items():
            leftover = sum(qty for item, qty in g.inventory.items() if item in I.TIER1)
            per_guild.setdefault(name, []).append(leftover)
    means = {name: sum(vals) / len(vals) for name, vals in per_guild.items()}
    assert max(means.values()) - min(means.values()) < 0.5
