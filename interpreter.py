import pandas as pd 
import yfinance as yf
from astdefs import Strategy, CapitalRule, BuyRule, SellRule, Condition, SMA
from parser import parse_strategy

class Portfolio:
    def __init__(self, cash):
        self.cash = cash
        self.shares = 0

def compute_sma(prices, window):
    return prices.rolling(window=window).mean()

def evaluate_condition(cond, prices, day):
    left = compute_sma(prices, cond.left.window).iloc[day]
    right = compute_sma(prices, cond.right.window).iloc[day]

    if pd.isna(left) or pd.isna(right):
        return False
    if cond.op == ">":
        return left > right
    else:
        return left < right

def run_strategy(strategy, ticker="AAPL", start="2022-01-01", end="2023-01-01"):
    data = yf.Ticker(ticker)
    prices = data.history(start=start, end=end)["Close"]

    cap_rule = None
    for r in strategy.rules: 
        if isinstance(r, CapitalRule):
            cap_rule = r
            break 
    portfolio = Portfolio(cash=float(cap_rule.amount))

    for day in range(len(prices)):
        for rule in strategy.rules:
            if isinstance(rule, BuyRule):
                if evaluate_condition(rule.condition, prices, day):
                    price = float(prices.iloc[day])
                    shares_to_buy = portfolio.cash // price
                    portfolio.shares += shares_to_buy
                    portfolio.cash -= shares_to_buy * prices.iloc[day]
            elif isinstance(rule, SellRule):
                if evaluate_condition(rule.condition, prices, day):
                    portfolio.cash += portfolio.shares * prices.iloc[day]
                    portfolio.shares = 0

    final_value = portfolio.cash + portfolio.shares * prices.iloc[-1]
    print(f"Initial capital: {cap_rule.amount}")
    print(f"Final portfolio value: {final_value:.2f}")
    print(f"Return: {((final_value - cap_rule.amount)/cap_rule.amount*100):.2f}%")



if __name__ == "__main__":
    strategy = parse_strategy("examples/momentum.dsl")
    run_strategy(strategy, ticker="AAPL")