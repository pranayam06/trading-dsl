strategy momentum {
  capital 10000
  buy when sma(10) > sma(30)
  sell when sma(10) < sma(30)
}