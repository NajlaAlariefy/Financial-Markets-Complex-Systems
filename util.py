'''
    File name: util.py
    Author: Najla Alariefy
    Date created: 8/APR/2018
    Date last modified: 18/MAY/2018
    Python Version: 3.0
'''

import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt, mpld3
import matplotlib.mlab as mlab
import seaborn as sns
from sklearn import preprocessing
from scipy import stats
import powerlaw



def plot_index_powerlaw(index):
    fig = plt.figure(figsize=(10,7))
    fit = powerlaw.Fit(np.array(index)+1,xmin=1,discrete=True)
    fit.power_law.plot_pdf( color= 'b',linestyle='--',label='fit ccdf')
    plt.grid(True)
    plt.title('Power-Law Fit of Market Index')
    fit.plot_pdf( color= 'b')
    plt.savefig("figs/index_powerlaw.svg")
    plt.show()
    plt.clf()


def represent(traders, stocks, index, duration):
    # displaying traders' portfolios
    colnames = [ 'total_assets', 'wallet']
    rownames = [ 'shares','perceived_value','current_price']
    for i in range(len(stocks)):
        colnames.append('stock_' + str(i+1))
    for o in range(len(traders)):
        rownames.append('trader_' + str(o+1))

    market = pd.DataFrame(0, index= rownames, columns= colnames)

    for stock in stocks:
        market.loc[str('shares'), str('stock_' + str(stock.id + 1))] = stock.count
        market.loc[str('perceived_value'), str('stock_' + str(stock.id + 1))] = stock.value
        market.loc[str('current_price'), str('stock_' + str(stock.id + 1))] = stock.price

    for trader in traders:
        assets = 0
        for stock in stocks:
            market.loc[str('trader_' + str(trader.id + 1)),
                       str('stock_' + str(stock.id + 1))] = trader.portfolio[stock.id][0] * stock.price
            assets += trader.portfolio[stock.id][0] * stock.price
        # displaying traders' total values
        market.loc[str('trader_' + str(trader.id + 1)), str('total_assets')] = assets + trader.wallet
        # displaying trader wallets
        market.loc[str('trader_' + str(trader.id + 1)), str('wallet')] = trader.wallet

    return market


def plot_index(index):
    # plotting market index
    fig = plt.figure(figsize=(14,5))
    plt.plot(range(1,len(index)),index[1:])
    plt.title('Market Index', fontsize=18)
    plt.xlabel('Time', fontsize=12)
    plt.ylabel('Index', fontsize=12)
    plt.grid(True)
    plt.savefig("figs/index.svg")
    plt.show()
    plt.clf()


def plot_wealth_distribution(market):
    """ Plotting Trader Wealth Distribution. """
    wealth = market[3:]['total_assets']

    # plot normalised histogram
    fig = plt.figure(figsize=(7,7))
    plt.hist(wealth, normed=True)

    # Computing theoretical distribution, code excerpt from
    # https://elf11.github.io/2017/10/29/python-fitting-data.html
    xt = plt.xticks()[0]
    xmin, xmax = min(xt), max(xt)
    lnspc = np.linspace(xmin, xmax, len(wealth))
    ab,bb,cb,db = stats.beta.fit(wealth)
    pdf_beta = stats.beta.pdf(lnspc, ab, bb,cb, db)
    plt.plot(lnspc, pdf_beta, label="Beta")
    plt.grid(True)
    plt.title('Trader Wealth Distribution PDF', fontsize=18)
    plt.savefig("figs/wealth_distribution.svg")
    plt.show()
    plt.clf()

def plot_portfolios(market):
    # plotting trader portfolios
    fig = plt.figure(figsize=(14,14))
    r = sns.heatmap(market, cmap='BuPu', annot=False, fmt='.0f')
    r.set_title("Heatmap of Trader Portfolios", fontsize=14)
    plt.savefig("figs/portfolios.svg")
    plt.show()
    plt.clf()


def plot_wealth_risk(market, traders):
    # displaying trader risk appetites/tolerence
    for trader in traders:
            market.loc[str('trader_' + str(trader.id + 1)),
                       str('risk_tolerence')] = trader.appetite
    trader_summary = market[['total_assets','risk_tolerence']]

    # normalising total_assets to compare it with risk appetite
    trader_summary = trader_summary.iloc[3:]
    ts = trader_summary.values
    min_max_scaler = preprocessing.MinMaxScaler()
    ts_scaled = min_max_scaler.fit_transform(ts)
    rownames = []
    for o in range(len(traders)):
        rownames.append('trader_' + str(o+1))
    df = pd.DataFrame(ts_scaled, index = rownames)
    df = df.sort_values(0)
    df.columns = ['Total Assets', 'Risk Tolerence']

    # plotting normalised trader total_assets next to risk_tolerence
    plot_two(df)


def plot_two(df):
    fig = plt.figure(figsize=(8,14))
    wealth_risk_plot = sns.heatmap(df, cmap='YlGnBu', annot=False, fmt='.1f')
    wealth_risk_plot.set_title("Heatmap of Trader Wealth vs Trader Risk Tolerence", fontsize=12)
    plt.savefig("figs/wealth_risk_plot.svg")
    plt.show()
    plt.clf()


def plot_stocks(stocks):
    # plotting stock value
    fig = plt.figure(figsize=(14,6))
    for stock in stocks:
        plt.plot(range(0,len(stock.price_trend)),stock.price_trend)
        plt.plot(range(0,len(stock.value_trend)),stock.value_trend)
        plt.title(str('Stock ' + str(stock.id)))
        #plt.legend(['Price','Perceived Value'], loc='upper left')
    plt.title('Stocks Price Trends', fontsize=18)
    plt.xlabel('Number of Trades', fontsize=12)
    plt.ylabel('Price', fontsize=12)
    plt.savefig("figs/stocks.svg")
    plt.show() #mpld3.show()
    plt.clf()

# Print iterations progress, code excerpt from https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total:
        print()
