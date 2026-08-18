"""
Quest scoring. This first version deliberately does NOT simulate actual
quest content (musical excerpts, painting recognition, puzzle assembly,
etc.) - that's out of scope for an economy/access/trading simulator and
would just be noise dressed up as precision. Instead, a fresh
`quest_skill` in [0, 1] is drawn independently for EVERY quest a guild
attempts (analysis §4 item 1: per-quest tables are used, not the
generic 0/2/4/6/8/10 rule, since 3 of 4 rooms' quests contradict it).

Correction (review r1/r4-r6 on PR #3): earlier versions of this file
and this docstring disagreed with each other and with the actual
engine about what was drawn when. What ships now, and what this
docstring now accurately describes: skill is independent per quest -
not shared across a room's 2 quests (that coupling inflated per-room
score spread by roughly a third, measured and confirmed independently
by two reviewers), and NOT persistent across a guild's 4 rooms either.
That means this model has NO persistent per-guild ability component at
all - a real team of 5 colleagues plausibly does carry some consistent
strength across the evening, and this model doesn't represent that.
Measured consequence: forcing one skill per guild for the whole game
instead produces roughly 70% higher score stdev (30.75 vs 17.86,
300-game sample) than the current per-quest-independent model - so
score-spread-based fairness claims in this project should be read as a
floor, not an estimate, until a persistent-skill variant is built
(tracked as follow-up, not implemented here per PR #3 scope).

This is a real simplification, stated plainly so it isn't mistaken for
higher fidelity than it has - see simulation/README.md.
"""
import random

# Each room has two quests; scores are read off each quest's own table
# using `skill` in [0, 1] as a stand-in for "how well this guild does at
# this kind of task." Each function draws its own skill independently.
QUEST_TABLES = {
    "Room1": [
        lambda rng: round(draw_skill(rng) * 10),          # Music: 1 pt/correct, 0-10
        lambda rng: _tiered(draw_skill(rng), [(0.85, 10), (0.5, 6), (0, 3)]),  # Map puzzle
    ],
    "Room2": [
        lambda rng: round(draw_skill(rng) * 10),          # Art Gallery
        lambda rng: round(draw_skill(rng) * 10),          # Hall of Languages
    ],
    "Room3": [
        lambda rng: _tiered(draw_skill(rng), [(0.85, 10), (0.6, 7), (0.35, 5), (0, 3)]),  # Architect
        lambda rng: round(draw_skill(rng) * 10),          # Hall of Legends
    ],
    "Room4": [
        lambda rng: _tiered(draw_skill(rng), [(0.8, 10), (0.6, 8), (0.4, 6), (0.2, 4), (0, 0)]),  # Locksmith
        lambda rng: round(draw_skill(rng) * 10),          # Scribe's Observation
    ],
}


def draw_skill(rng: random.Random):
    return rng.random()


def _tiered(skill, thresholds):
    for threshold, score in thresholds:
        if skill > threshold:
            return score
    return thresholds[-1][1]


def score_room(room, rng, room_win_bonus, tie_bonus):
    """Returns (score_a, score_b) including the room-win/tie bonus (analysis §2.7).
    Each guild's 2 quests each draw skill independently (see module docstring)."""
    quests = QUEST_TABLES[room]
    total_a = sum(q(rng) for q in quests)
    total_b = sum(q(rng) for q in quests)
    if total_a > total_b:
        total_a += room_win_bonus
    elif total_b > total_a:
        total_b += room_win_bonus
    else:
        total_a += tie_bonus
        total_b += tie_bonus
    return total_a, total_b
