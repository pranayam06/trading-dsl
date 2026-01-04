from ast import Strategy, CapitalRule, BuyRule, SellRule, Condition, SMA

def parse_condition(text):
    text = text.strip()
    if ">" in text:
        left_text, right_text = text.split(">")
        op = ">"
    elif "<" in text:
        left_text, right_text = text.split("<")
        op = "<"
    else:
        raise ValueError(f"Unknown comparator in {text}")

    def parse_indicator(ind):
        ind = ind.strip()
        if ind.startswith("sma(") and ind.endswith(")"):
            window = int(ind[4:-1])
            return SMA(window)
        else:
            raise ValueError(f"Unknown indicator: {ind}")

    left = parse_indicator(left_text)
    right = parse_indicator(right_text)
    return Condition(left, op, right)

def parse_rule(line): 
    rule = line.strip()
    if rule.startswith("capital"):
        tokens = rule.split()
        if len(tokens) == 2: 
            amount = tokens[1]
            return CapitalRule(amount)
        else:
            raise ValueError("capital line malformed");
    elif line.startswith("buy when"):
        cond = line[len("buy when "):]
        return BuyRule(parse_condition(cond))
    elif line.startswith("sell when"):
        cond = line[len("sell when "):]
        return SellRule(parse_condition(cond))
    else:
        raise ValueError(f"Unknown rule: {line}")

def parse_strategy(filename): 
    with open(filename, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    first = lines[0]
    if not first.startswith("strategy") or not first.endswith("{"):
        raise ValueError("Strategy line malformed")
    name = first.split()[1] 

    if lines[-1] != "}":
        raise ValueError("Strategy must end with }")

    rules = []
    for line in lines[1:-1]:
        rules.append(parse_rule(line))

    return Strategy(name, rules)

if __name__ == "__main__":
    s = parse_strategy("examples/momentum.dsl")
    print(s.name)
    for r in s.rules:
        print(type(r), vars(r))