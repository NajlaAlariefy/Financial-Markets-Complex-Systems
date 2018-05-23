'''
    File name: trader.py
    Author: Najla Alariefy
    Date created: 8/APR/2018
    Date last modified: 18/MAY/2018
    Python Version: 3.0
'''


import random
from stock import Stock

class InvalidOperation(Exception):
    pass


class Trader:
    def __init__(self, id, wallet, appetite, stocks):
        self.id = id
        self.wallet = wallet
        self.portfolio = {stock.id: [0, stock.value] for stock in stocks}
        self.appetite = appetite



    def assess(self, stock):
        # a trader has a chance of
        if random.random() < 0.2 and stock.risk <= self.appetite + 0.1:
            if stock.price <= stock.value:
                self.buy(stock)
            else:
                 self.sell(stock)
        stock.change()



    def buy(self, stock):
        if self.wallet > stock.price and stock.count > 0:
            i = str('[ trader ' +  str(self.id + 1) + ']' + ' buying ' + str(stock))
            #print(i)
            self.wallet -= stock.price
            self.portfolio[stock.id][0] += 1
            stock.buy()


    def sell(self, stock):
        if self.portfolio[stock.id][0] > 0:
            i = str('[ trader ' +  str(self.id + 1) + ']' + ' selling ' + str(stock))
            #print(i)
            self.wallet += stock.price
            self.portfolio[stock.id][0] -= 1
            stock.sell()

    # this function no longer in use
    def liquidity(self):
        if random.random() < 0.1:
            self.wallet += random.gauss(500, 20)

    def __repr__(self):
        return f'{self.__class__.__name__}(ID: {self.id}, Wallet: {self.wallet}, Risk: {self.appetite}, Portfolio: {self.portfolio})'
