"""
The fixed room/opponent rotation from analysis §1, and the starting-hand
coordination from analysis §2.1. Both tables are reproduced here as data
(matching ../rotation_schedule.py's verified output) rather than
re-derived at runtime, so the engine doesn't depend on re-running the
constraint search on every simulation.
"""

# schedule[round_index][room] = (guild_a, guild_b)
FIXED_ROTATION = [
    {"Room1": ("Lisbon", "Stockholm"), "Room2": ("Bursa", "Ghent"),
     "Room3": ("Gdansk", "Prague"), "Room4": ("Venice", "Vienna")},
    {"Room1": ("Gdansk", "Vienna"), "Room2": ("Venice", "Prague"),
     "Room3": ("Lisbon", "Ghent"), "Room4": ("Bursa", "Stockholm")},
    {"Room1": ("Ghent", "Venice"), "Room2": ("Stockholm", "Gdansk"),
     "Room3": ("Bursa", "Vienna"), "Room4": ("Lisbon", "Prague")},
    {"Room1": ("Bursa", "Prague"), "Room2": ("Lisbon", "Vienna"),
     "Room3": ("Stockholm", "Venice"), "Room4": ("Ghent", "Gdansk")},
]

# Round-1 room assignment, per guild (derived from FIXED_ROTATION round 0).
ROUND1_ROOM_BY_GUILD = {
    guild: room
    for room, pair in FIXED_ROTATION[0].items()
    for guild in pair
}

# Starting-hand coordination (analysis §2.1, revised per review R8's root
# cause). Two constraints, both satisfiable simultaneously for every guild:
# (1) the guild must be able to craft its Round-1 room's Tier-2
# prerequisite from its opening hand, and (2) the guild's own Tier-1
# specialty (produced every round, 6 units total by game end) must pair
# with 2 of the 3 hand types under the recipe cycle, not just 1 - a
# guild that only has 1 usable partner in hand uses it up on the first
# conversion and then holds dead stock for the rest of the game.
# Previously only (1) was enforced; that left Bursa, Stockholm, Gdansk,
# and Venice with only 1 usable partner each, which review found
# accounted for a measured 7.2x per-guild win-rate spread under
# otherwise-identical play - see simulation/README.md's Findings.
# Each guild has exactly one Tier-1 type (its own specialty, or that
# specialty's non-recipe "diagonal" partner) that satisfies both
# constraints at once; see tests/test_review_pr3_r3_starting_hand_fix.py.
COORDINATED_MISSING_MATERIAL = {
    "Lisbon": "Wax", "Stockholm": "Charcoal",   # need Cloth = Flax+Saltpetre
    "Bursa": "Saltpetre", "Ghent": "Flax",      # need Dye = Wax+Charcoal
    "Gdansk": "Wax", "Prague": "Flax",          # need BlackPowder = Charcoal+Saltpetre
    "Venice": "Saltpetre", "Vienna": "Charcoal",  # need Candle = Flax+Wax
}


def rooms_for_guild(guild):
    """The 4 (round, room) assignments for a guild under the fixed rotation."""
    assignments = []
    for round_index, rooms in enumerate(FIXED_ROTATION):
        for room, pair in rooms.items():
            if guild in pair:
                assignments.append((round_index, room))
    return sorted(assignments)


def opponent_in_room(round_index, room, guild):
    a, b = FIXED_ROTATION[round_index][room]
    return b if a == guild else a
