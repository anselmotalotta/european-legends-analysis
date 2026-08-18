"""
Aggregate metrics across many simulated games. Covers a subset of the
analysis §8 core-questions list - the ones a "deliberately small first
version" (per the review's guardrail) can answer well. Not covered yet,
left for a future iteration: shadow-value-by-round (needs price
inference, not just bookkeeping) and marginal per-room expected value
(needs a counterfactual "what if this room were skipped" re-run). Said
plainly rather than silently omitted.
"""
import statistics as stats
from collections import Counter

from . import items as I


def summarize(results):
    n = len(results)
    all_scores = []
    per_guild_scores = {}
    completion_flags = []
    guild_slots_complete = 0
    guild_slots_total = 0
    loans_per_guild = []
    debt_per_guild = []
    trades_per_guild = []
    barters_per_guild = []
    purchases_per_guild = []
    zero_trade_guilds = 0
    opponents_per_guild = []
    trade_partners_per_guild = []
    win_by_specialty = Counter()
    win_by_guild = Counter()
    games_by_specialty = Counter()
    scores_excluding_debt = []

    for result in results:
        scores = result.scores()
        all_scores.extend(scores.values())
        winner = max(scores, key=scores.get)
        win_by_specialty[result.guilds[winner].specialty] += 1
        win_by_guild[winner] += 1

        game_complete = True
        for name, guild in result.guilds.items():
            per_guild_scores.setdefault(name, []).append(scores[name])
            games_by_specialty[guild.specialty] += 1
            guild_slots_total += 1
            if len(guild.rooms_visited) == result.config.n_rooms:
                guild_slots_complete += 1
            else:
                game_complete = False
            loans_per_guild.append(len(guild.loans))
            debt_per_guild.append(guild.total_debt())
            trades_per_guild.append(guild.trade_count)
            barters_per_guild.append(guild.barter_count)
            purchases_per_guild.append(guild.purchase_count)
            if guild.trade_count == 0:
                zero_trade_guilds += 1
            opponents_per_guild.append(len(set(guild.opponents_faced)))
            trade_partners_per_guild.append(len(guild.trade_partners))
            # Isolates the loan-interest rate's effect on the score
            # distribution from the rest of the game (review r1(PR#3)/F1:
            # "score stdev" alone conflates a genuine behavioral effect
            # with the pure arithmetic of subtracting a bigger debt
            # number - this metric holds debt out so the two can be told
            # apart). See simulation/README.md's Tuning sweep section.
            scores_excluding_debt.append(scores[name] + guild.total_debt())
        completion_flags.append(game_complete)

    def mean(xs):
        return stats.mean(xs) if xs else 0.0

    return {
        "n_games": n,
        "score": {
            "mean": mean(all_scores),
            "stdev": stats.stdev(all_scores) if len(all_scores) > 1 else 0.0,
            "stdev_excluding_debt": stats.stdev(scores_excluding_debt) if len(scores_excluding_debt) > 1 else 0.0,
            "min": min(all_scores) if all_scores else 0,
            "max": max(all_scores) if all_scores else 0,
        },
        "score_by_guild": {name: mean(vals) for name, vals in per_guild_scores.items()},
        "pct_games_all_guilds_complete": 100 * sum(completion_flags) / n,
        "pct_guild_slots_complete": 100 * guild_slots_complete / guild_slots_total,
        "mean_loans_per_guild": mean(loans_per_guild),
        "mean_debt_per_guild": mean(debt_per_guild),
        "mean_trades_per_guild": mean(trades_per_guild),
        "mean_barters_per_guild": mean(barters_per_guild),
        "mean_purchases_per_guild": mean(purchases_per_guild),
        "pct_guilds_zero_trades": 100 * zero_trade_guilds / guild_slots_total,
        "mean_distinct_opponents_per_guild": mean(opponents_per_guild),
        "mean_distinct_trade_partners_per_guild": mean(trade_partners_per_guild),
        "win_rate_by_specialty": {
            spec: win_by_specialty[spec] / n for spec in games_by_specialty
        },
        # Per-guild win rate, not just per-specialty (review R8 on PR#3):
        # averaging by specialty can hide a large gap between two guilds
        # that happen to share one, since they don't share a starting
        # hand, Round-1 room, or room-visit order - specialty and
        # rotation position are independent variables here.
        "win_rate_by_guild": {
            name: win_by_guild[name] / n for name in per_guild_scores
        },
    }


def score_variance_from_early_lead(results):
    """Approximate answer to analysis §2.7/§8 item 10: correlation between
    a guild's cumulative quest income (a proxy for "did well early/often")
    and its final score. Not a full compounding decomposition - a
    starting point a future iteration should refine."""
    xs, ys = [], []
    for result in results:
        for guild in result.guilds.values():
            xs.append(guild.quest_coins_earned)
            ys.append(guild.final_score(I.SELL_PRICE))
    if len(xs) < 2:
        return None
    try:
        return stats.correlation(xs, ys)
    except AttributeError:
        # Python < 3.10 fallback
        mean_x, mean_y = stats.mean(xs), stats.mean(ys)
        cov = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
        var_x = sum((x - mean_x) ** 2 for x in xs)
        var_y = sum((y - mean_y) ** 2 for y in ys)
        if var_x == 0 or var_y == 0:
            return 0.0
        return cov / (var_x ** 0.5 * var_y ** 0.5)
