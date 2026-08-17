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

# Starting-hand coordination (analysis §2.1): which Tier-1 type each
# guild's opening hand should be missing, so it can always craft its
# Round-1 room's Tier-2 prerequisite from its opening hand.
COORDINATED_MISSING_MATERIAL = {
    "Lisbon": "Wax", "Stockholm": "Wax",       # need Cloth = Flax+Saltpetre
    "Bursa": "Flax", "Ghent": "Flax",          # need Dye = Wax+Charcoal
    "Gdansk": "Flax", "Prague": "Flax",        # need BlackPowder = Charcoal+Saltpetre
    "Venice": "Charcoal", "Vienna": "Charcoal",  # need Candle = Flax+Wax
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
