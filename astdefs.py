
class Strategy:
    def __init__(self, name, rules):
        self.name = name
        self.rules = rules


class CapitalRule:
    def __init__(self, amount):
        self.amount = amount


class BuyRule:
    def __init__(self, condition):
        self.condition = condition


class SellRule:
    def __init__(self, condition):
        self.condition = condition


class Condition:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class SMA:
    def __init__(self, window):
        self.window = window
