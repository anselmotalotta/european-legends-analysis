from sim import items as I


def test_tier1_options_always_exactly_two():
    for missing in I.TIER1:
        options = I.tier1_options(missing)
        assert len(options) == 2, f"missing={missing} gave {options}"


def test_tier1_options_match_analysis_table():
    # Analysis §2.1 table, verified independently in this repo's review history.
    expected = {
        "Flax": {"Dye", "BlackPowder"},
        "Wax": {"BlackPowder", "Cloth"},
        "Charcoal": {"Candle", "Cloth"},
        "Saltpetre": {"Candle", "Dye"},
    }
    for missing, options in expected.items():
        assert set(I.tier1_options(missing)) == options


def test_diagonal_pairs_have_no_recipe():
    assert frozenset({"Flax", "Charcoal"}) not in I.TIER1_RECIPES
    assert frozenset({"Wax", "Saltpetre"}) not in I.TIER1_RECIPES


def test_every_tier2_item_has_a_room():
    for room, prereq in I.ROOM_PREREQUISITE.items():
        assert prereq in I.TIER2

    assert set(I.ROOM_PREREQUISITE.values()) == set(I.TIER2)


def test_sell_prices_match_analysis():
    assert all(I.SELL_PRICE[t] == 1 for t in I.TIER1)
    assert all(I.SELL_PRICE[t] == 4 for t in I.TIER2)
    assert all(I.SELL_PRICE[t] == 14 for t in I.TIER3)
