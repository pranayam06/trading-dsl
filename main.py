from ast import Strategy, CapitalRule, BuyRule, SellRule, Condition, SMA

s = Strategy(
    "momentum",
    [
        CapitalRule(10000),
        BuyRule(Condition(SMA(10), ">", SMA(30))),
        SellRule(Condition(SMA(10), "<", SMA(30))),
    ]
)

print(s.name)
