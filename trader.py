'''
    File name: trader.py
    Author: Najla Alariefy
    Date created: 8/APR/2018
    Date last modified: 23/MAY/2018
    Python Version: 3.0
'''
import random
from stock import Stock

class InvalidOperation(Exception):
    pass

# The Trader agent class responsible for trading decisions
class Trader:
    def __init__(self, id, wallet, appetite, stocks):
        self.id = id
        self.wallet = wallet
        self.portfolio = {stock.id: [0, stock.value] for stock in stocks}
        self.appetite = appetite

    # main decision making function
    def assess(self, stock):
        # a trader has a 20% chance of assessing the stock
        # if the stock is convenient for the trader's risk appetite
        if random.random() < 0.2 and stock.risk <= self.appetite + 0.1:
            if stock.price <= stock.value:
                self.buy(stock)
            else:
                 self.sell(stock)
        # external factors affect the stock everytime it is traded
        stock.change()

    # when a trader attempts to buy a stock
    def buy(self, stock):
        # if the trader can afford it, and there are outstanding shares
        if self.wallet > stock.price and stock.count > 0:
            i = str('[ trader ' +  str(self.id + 1) + ']' + ' buying ' + str(stock))
            #print(i)
            self.wallet -= stock.price
            self.portfolio[stock.id][0] += 1
            stock.buy()


    # when a trader attempts to sell a stock
    def sell(self, stock):
        # if the trader has the stock
        if self.portfolio[stock.id][0] > 0:
            i = str('[ trader ' +  str(self.id + 1) + ']' + ' selling ' + str(stock))
            #print(i)
            self.wallet += stock.price
            self.portfolio[stock.id][0] -= 1
            stock.sell()


    # this function was created to add more value entry mechanism
    # it is no longer in use
    def liquidity(self):
        if random.random() < 0.1:
            self.wallet += random.gauss(500, 20)


    def __repr__(self):
        return f'{self.__class__.__name__}(ID: {self.id}, Wallet: {self.wallet}, Risk: {self.appetite}, Portfolio: {self.portfolio})'
