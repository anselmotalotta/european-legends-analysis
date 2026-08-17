"""Item types and the conversion recipe graph (analysis §2.1, Fig. 2)."""

TIER1 = ("Flax", "Wax", "Charcoal", "Saltpetre")
TIER2 = ("Candle", "Cloth", "Dye", "BlackPowder")
TIER3 = ("Lantern", "Firework", "DyedCloth", "Ink")

# Tier-1 pair -> Tier-2 item. The 4-cycle from analysis §2.1: each Tier-1
# type appears in exactly two recipes; diagonal pairs (Flax+Charcoal,
# Wax+Saltpetre) don't convert to anything.
TIER1_RECIPES = {
    frozenset({"Flax", "Wax"}): "Candle",
    frozenset({"Wax", "Charcoal"}): "Dye",
    frozenset({"Charcoal", "Saltpetre"}): "BlackPowder",
    frozenset({"Saltpetre", "Flax"}): "Cloth",
}

# Tier-2 pair -> Tier-3 item, from the source conversion chart (Fig. 2).
TIER2_RECIPES = {
    frozenset({"Candle", "Cloth"}): "Lantern",
    frozenset({"Candle", "BlackPowder"}): "Firework",
    frozenset({"Cloth", "Dye"}): "DyedCloth",
    frozenset({"Dye", "BlackPowder"}): "Ink",
}

# Room -> its Tier-2 entry prerequisite (analysis §1/§2.1).
ROOM_PREREQUISITE = {
    "Room1": "Cloth",
    "Room2": "Dye",
    "Room3": "BlackPowder",
    "Room4": "Candle",
}

SELL_PRICE = {
    **{t: 1 for t in TIER1},
    **{t: 4 for t in TIER2},
    **{t: 14 for t in TIER3},
}


def tier1_options(missing: str):
    """The two Tier-2 items craftable from a starting hand missing `missing`
    (analysis §2.1 table) — always exactly two, sharing the hub ingredient."""
    hand = [t for t in TIER1 if t != missing]
    options = []
    for a, b in ((hand[0], hand[1]), (hand[0], hand[2]), (hand[1], hand[2])):
        recipe = TIER1_RECIPES.get(frozenset({a, b}))
        if recipe:
            options.append(recipe)
    return options
