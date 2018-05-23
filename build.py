'''
    File name: util.py
    Author: Najla Alariefy
    Date created: 8/APR/2018
    Date last modified: 18/MAY/2018
    Python Version: 3.0
'''

import random
import threading
import pandas as pd
import numpy as np
from util import represent, printProgressBar
from stock import Stock
from trader import Trader
from time import sleep

# Simulation run function
def run_market(stock_options= 20, traders= 40, duration= 100000):
    """ Runs the simulation and returns the market state (including trader
             portfolios, stock prices, and market index)

        Args:
            stock_options (int): Number of stock options in this simulation.
            traders       (int): Number of traders in this simulation.
            duration      (int): Number of duration.

        Returns:
            index    (list[int]): The market's index throughout the duration.
            traders  (list[Trader]): List of Trader objects & their updated
                                     portfolios.
            stocks   (list[Stock]): A list of Stock objects after price changes.
            market   (pandas.DataFrame): Consolidated trader portfolios
                                         with their total assets.
    """

    assert type(stock_options) and type(traders) and type(duration) == int

    mutex = threading.Lock()
    barrier = threading.Barrier(traders)

    # initialising stocks
    stocks = init_stocks(stock_options)

    # initialising index
    index = init_index(stocks)

    # initialising traders
    traders = init_traders(traders, stocks)

    # Initial call to print 0% progress
    printProgressBar(0, duration, prefix = 'Progress:',
                        suffix = 'Complete', length = 50)

    # run the simulation
    for time in range(duration):
        # print('time: ', time, 'starting trade hour')
        traders_threads = [
                threading.Thread(
                    target=run_trader,
                    args=(trader, stocks, barrier, mutex),
                ) for trader in traders
        ]
        for thread in traders_threads:
            thread.start()
        for thread in traders_threads:
            thread.join()
        # print('time: ', time, 'ending trade hour')

        # calculate the market index after each hour
        calculate_index(stocks, index)

        # Update Progress Bar
        sleep(0.1)
        printProgressBar(time + 1, duration, prefix = 'Progress:',
                         suffix = 'Complete', length = 50)


    # visualise the market index, traders and stocks
    market = represent(traders, stocks, index, duration)
    print('Market simulation done. ', duration, ' time steps, ', len(stocks),
          ' stock options, ', len(traders), ' traders.')
    return index, traders, stocks, market


def init_stocks(stocks=20):
    """ Returns a list of Stock objects of Price, Value, Shares,
        and Risk Beta Parameter. """
    return [
            Stock(
                i,
                # stock price variation
                random.normalvariate(100, 4),
                # stock value variation
                random.normalvariate(150, 20),
                # stock outstanding shares
                random.randint(200, 200),
                # stock beta parameter for risk profiling
                random.uniform(0.1,1),
            ) for i in range(stocks)
    ]

def init_traders(traders, stocks):
    """ Returns a list of Trader objects of Wallet, Risk appetite,
        and Portfolio. """
    return [
            Trader(
                i,
                # trader initial 'cash' / wallet.
                random.normalvariate(1000, 50),
                # trader's risk tolerence / appetite.
                random.uniform(0.1,1),
                # initialise portfolio of stocks (all 0 initially).
                stocks
            ) for i in range(traders)
    ]

def run_trader(trader, stocks, barrier, mutex):
    """ Runs all traders against all stocks. """
    for stock in stocks:
        with mutex:
            # All traders will assess this stock options
            trader.assess(stock)

        # All traders will wait for each other
        # before moving on to the next stock option
        barrier.wait()


def init_index(stocks):
    """ Initialise stock market index using the 'price_weighted_average'
        method. """
    index = []
    price = 0

    for stock in stocks:
        price += stock.price

    index.append(price / len(stocks))
    return index


def calculate_index(stocks, index, method = 'price_weighted_average'):
    """ Calculate market average price and append it to the index. """
    if method == 'price_weighted_average':
        prices = 0

        for stock in stocks:
             prices += stock.price

        ind = prices / len(stocks)
        index.append(ind)
