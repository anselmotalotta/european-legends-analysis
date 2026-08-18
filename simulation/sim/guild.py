"""Guild state during a simulated game."""
import math
from collections import Counter
from dataclasses import dataclass, field


@dataclass
class Guild:
    name: str
    specialty: str  # its Tier-1 production type
    coins: int
    inventory: Counter = field(default_factory=Counter)  # item name -> count
    loans: list = field(default_factory=list)  # list of principal amounts owed
    quest_coins_earned: int = 0  # metrics-only running total; already included in .coins
    rooms_visited: set = field(default_factory=set)
    opponents_faced: list = field(default_factory=list)
    trade_partners: set = field(default_factory=set)
    trade_count: int = 0  # barter + purchases combined (kept for backward compatibility)
    purchase_count: int = 0  # coin purchases only - subset of trade_count
    barter_count: int = 0  # item-for-item swaps only - subset of trade_count

    def has(self, item, qty=1):
        return self.inventory[item] >= qty

    def add(self, item, qty=1):
        self.inventory[item] += qty

    def remove(self, item, qty=1):
        if self.inventory[item] < qty:
            raise ValueError(f"{self.name} does not have {qty}x {item}")
        self.inventory[item] -= qty
        if self.inventory[item] == 0:
            del self.inventory[item]

    def take_loan(self, shortfall, multiplier):
        # Rounded up to the nearest whole coin (corrected-ruleset-v2.md §14)
        # - repayment must be payable in physical coins at a live event,
        # and rounding up (not down) means the bank is never undercharged.
        self.loans.append(math.ceil(shortfall * multiplier))

    def total_debt(self):
        return sum(self.loans)

    def liquidation_value(self, sell_price):
        return sum(sell_price[item] * count for item, count in self.inventory.items())

    def final_score(self, sell_price):
        return self.coins + self.liquidation_value(sell_price) - self.total_debt()
