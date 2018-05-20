from build import run_market


if __name__ == '__main__':
    random.seed(1)
    index, traders, stocks, market = run_market(stocks = 50, traders = 150, duration = 45000)
