'''
    File name: stock.py
    Author: Najla Alariefy
    Date created: 8/APR/2018
    Date last modified: 18/MAY/2018
    Python Version: 3.0
'''
import random


class InvalidOperation(Exception):
    # print('No outstanding shares available.')
    pass

# The Stock class partially acts as the "external factors" agent as the change()
# function
class Stock:
    def __init__(self, id, price, value, count, risk):
        self.id = id
        self.price = value * random.gauss(1,0.0001)
        self.value = value
        self.count = count
        self.risk = risk
        # for logging trends of stock price and value
        self.price_trend = [self.price]
        self.value_trend = [value]

    # When an acquisition operation occurs, one less outstanding share is available
    def buy(self):
        if not self.count:
            raise InvalidOperation
        self.count -= 1
        self.price *= 1.001
        self.price_trend.append(self.price)
        self.value_trend.append(self.value)

    # When a sale operation occurs, one more outstanding share is available
    def sell(self):
        self.count += 1
        self.price *= 0.99999
        self.price_trend.append(self.price)
        self.value_trend.append(self.value)

    # The 'external factors' agent, values change with a bias towards inflation
    def change(self):
        if random.random() < self.risk and self.value > 1:
            flate = random.gauss(1.0000001,0.001)
            self.value *= flate if flate >0 else 1
            self.price = self.value * random.gauss(0.9999999,0.0001)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id}, {self.price}, {self.value}, {self.count})'
