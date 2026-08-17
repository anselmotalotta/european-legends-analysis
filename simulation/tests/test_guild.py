from sim.guild import Guild
from sim import items as I


def make_guild(coins=10, **kwargs):
    return Guild(name="Test", specialty="Wax", coins=coins, **kwargs)


def test_loan_covers_shortfall_only_and_repays_double():
    """Analysis §2.4 correction: a guild with 10 coins facing a 15-coin fee
    borrows only the 5-coin shortfall, owing 10 (not 15 -> 30) at the end."""
    g = make_guild(coins=10)
    fee = 15
    shortfall = fee - g.coins
    g.coins = 0
    g.take_loan(shortfall, multiplier=2)
    assert g.total_debt() == 10


def test_zero_coin_guild_takes_full_loan():
    g = make_guild(coins=0)
    fee = 15
    g.take_loan(fee, multiplier=2)
    assert g.total_debt() == 30


def test_add_remove_inventory():
    g = make_guild()
    g.add("Flax", 2)
    assert g.has("Flax", 2)
    g.remove("Flax", 1)
    assert g.inventory["Flax"] == 1
    g.remove("Flax", 1)
    assert "Flax" not in g.inventory


def test_remove_more_than_held_raises():
    g = make_guild()
    g.add("Flax", 1)
    try:
        g.remove("Flax", 2)
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_final_score_liquidation_and_debt():
    g = make_guild(coins=20)
    g.add("Candle", 2)  # Tier-2, worth 4 each = 8
    g.take_loan(5, multiplier=2)  # owes 10
    assert g.final_score(I.SELL_PRICE) == 20 + 8 - 10
