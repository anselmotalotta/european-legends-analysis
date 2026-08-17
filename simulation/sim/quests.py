"""
Quest scoring. This first version deliberately does NOT simulate actual
quest content (musical excerpts, painting recognition, puzzle assembly,
etc.) - that's out of scope for an economy/access/trading simulator and
would just be noise dressed up as precision. Instead, each guild gets a
`quest_skill` in [0, 1] (drawn once per guild per game, representing that
guild's overall mixed-skill performance for a charity event with random
team composition), and quest scores are derived from it using each
quest's own stated scoring table (analysis §4 item 1: the per-quest
tables are used, not the generic 0/2/4/6/8/10 rule, since 3 of 4 rooms'
quests contradict that generic rule).

This is a real simplification, stated plainly so it isn't mistaken for
higher fidelity than it has - see simulation/README.md.
"""
import random

# Each room has two quests; scores are read off each quest's own table
# using `skill` in [0, 1] as a stand-in for "how well this guild does at
# this kind of task."
QUEST_TABLES = {
    "Room1": [
        lambda skill, rng: round(skill * 10),          # Music: 1 pt/correct, 0-10
        lambda skill, rng: 10 if skill > 0.85 else (6 if skill > 0.5 else 3),  # Map puzzle
    ],
    "Room2": [
        lambda skill, rng: round(skill * 10),          # Art Gallery
        lambda skill, rng: round(skill * 10),          # Hall of Languages
    ],
    "Room3": [
        lambda skill, rng: 10 if skill > 0.85 else (7 if skill > 0.6 else (5 if skill > 0.35 else 3)),  # Architect
        lambda skill, rng: round(skill * 10),          # Hall of Legends
    ],
    "Room4": [
        lambda skill, rng: 10 if skill > 0.8 else (8 if skill > 0.6 else (6 if skill > 0.4 else (4 if skill > 0.2 else 0))),  # Locksmith
        lambda skill, rng: round(skill * 10),          # Scribe's Observation
    ],
}


def draw_skill(rng: random.Random):
    return rng.random()


def score_room(room, guild_a, guild_b, skill_a, skill_b, rng, room_win_bonus, tie_bonus):
    """Returns (score_a, score_b) including the room-win/tie bonus (analysis §2.7)."""
    quests = QUEST_TABLES[room]
    total_a = sum(q(skill_a, rng) for q in quests)
    total_b = sum(q(skill_b, rng) for q in quests)
    if total_a > total_b:
        total_a += room_win_bonus
    elif total_b > total_a:
        total_b += room_win_bonus
    else:
        total_a += tie_bonus
        total_b += tie_bonus
    return total_a, total_b
