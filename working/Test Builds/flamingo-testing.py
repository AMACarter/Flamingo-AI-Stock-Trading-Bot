import alpaca_trade_api as tradeapi # Alpaca API
import sys 
import datetime
import os
import time
import webbrowser
import importlib
import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from numpy.lib.utils import source
import pandas as pd
import numpy as np
import talib # Techincal Analysis
import logging # Data logging
import tkinter as tk # GUI elements
import multiprocessing # Thread management
import yfinance as yf
from datetime import timedelta


# import flamingoAI # AI module

from alpaca_trade_api.rest import REST
from alpaca_trade_api.rest import TimeFrame
from matplotlib import pyplot
from pandas import read_csv
from multiprocessing import Process
from re import T
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from ttkthemes import ThemedTk
from ttkthemes import ThemedStyle
from colorama import Fore, Back, Style
from functools import partial
from datetime import datetime
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from matplotlib import style
from scipy.signal import argrelextrema


# CONNECTION TO API AND ACCOUNT

def flamingo_startup():
   
    # Setup Alpaca API 
    api_key = 'PKPVWUKI5H0UBVALQUXM'
    api_secret = 'QQrNRzBk5RTfVoRX8ISdYrWeQwHh51XmDb6LVSBh'
    base_url = 'https://paper-api.alpaca.markets'
    data_url = 'wss://data.alpaca.markets'

    # Initiate REST API
    api = tradeapi.REST(
        api_key, 
        api_secret, 
        base_url, 
        api_version='v2')
    
    # Initiate WebSocket
    conn = tradeapi.stream2.StreamConn(
	    api_key,
	    api_secret,
	    base_url=base_url,
	    data_url=data_url,
	    data_stream='alpacadatav1',
    )

    # Get our account information.
    account = api.get_account()
    
    # Checks account: Equity, value and buying power    
    print ('${} Equity worth.'.format (account.equity))
    print ('${} Portfolio value.'.format(account.portfolio_value))
    print ('${} is available as buying power.'.format(account.buying_power))
    
    # Check our current balance vs. our balance at the last market close
    balance_change = float(account.equity) - float(account.last_equity)
    
    if (balance_change <= 0):
        
        print (Fore.RED + f'Today\'s portfolio balance change: ${round (balance_change, 2)}')
    else:
        print (Fore.GREEN + f'Today\'s portfolio balance change: +${round (balance_change, 2)}')
    
    balance_percentage = (balance_change / float(account.last_equity)) * 100
    
    if (balance_percentage <= 0):
        
        print (Fore.RED + f'{round (balance_percentage, 2)}%')
    else:
        print (Fore.GREEN + f'{round (balance_percentage, 2)}%')
    
    print (Style.RESET_ALL)

    # Get a list of all of our positions.
    portfolio = api.list_positions()

    # Print the quantity of shares for each position.
    for position in portfolio:
        print ("{} shares of {}".format(position.qty, position.symbol))
 
    # Checking market times
    clock = api.get_clock()
    print(Fore.YELLOW + 'The market is {}'.format('open.' if clock.is_open else 'closed.'))
    print (Style.RESET_ALL)
    
    # Logging different components
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
       
    print (Fore.GREEN + "Flamingo Bot Initialised.")
    print (Style.RESET_ALL)
    
    # Open broker dashboard
    # webbrowser.open('https://app.alpaca.markets/brokerage/dashboard/overview', new=2, autoraise=True)
    
    def get_data(symbol, lookback):
    
        all_data = pd.DataFrame()
        for x in range(lookback):
            if x == 0:
                data = api.polygon.historic_agg('minute', symbol, limit=None).df
            else:
                data = api.polygon.historic_agg('minute', symbol, _from = (data.index.min() - timedelta(days=5)).strftime('%x %X'), to = start, limit = None).df
        start = data.index.min().strftime('%x %X')
        end = data.index.max().strftime('%x %X')
        all_data = pd.concat([data, all_data], axis=0)
        all_data.drop(columns=['volume'], inplace=True)
        all_data.dropna(inplace=True)
        all_data = all_data[~all_data.index.duplicated()]
        all_data.replace(0, method='bfill', inplace=True)
        return all_data   
     
    data = get_data('CAT', 3) 
    data   
    
    resampled_data = data.resample('60T', closed='right', label='right').agg({'open': 'first',
                                                                         'high': 'max',
                                                                         'low': 'min',
                                                                         'close': 'last'}).dropna()
    resampled_data
    
    def get_max_min(prices, smoothing, window_range):
        smooth_prices = prices['close'].rolling(window=smoothing).mean().dropna()
        local_max = argrelextrema(smooth_prices.values, np.greater)[0]
        local_min = argrelextrema(smooth_prices.values, np.less)[0]
        price_local_max_dt = []
        for i in local_max:
            if (i>window_range) and (i<len(prices)-window_range):
                price_local_max_dt.append(prices.iloc[i-window_range:i+window_range]['close'].idxmax())
        price_local_min_dt = []
        for i in local_min:
            if (i>window_range) and (i<len(prices)-window_range):
                price_local_min_dt.append(prices.iloc[i-window_range:i+window_range]['close'].idxmin())  
        maxima = pd.DataFrame(prices.loc[price_local_max_dt])
        minima = pd.DataFrame(prices.loc[price_local_min_dt])
        max_min = pd.concat([maxima, minima]).sort_index()
        max_min.index.name = 'date'
        max_min = max_min.reset_index()
        max_min = max_min[~max_min.date.duplicated()]
        p = prices.reset_index()   
        max_min['day_num'] = p[p['timestamp'].isin(max_min.date)].index.values
        max_min = max_min.set_index('day_num')['close']
    
        return max_min

    smoothing = 3
    window = 10

    minmax = get_max_min(resampled_data, smoothing, window)
    minmax    
    
# STRATEGY
  

# MAIN THREAD

if __name__ == '__main__': 
    
    p1 = multiprocessing.Process(target=flamingo_startup)
#    p2 = multiprocessing.Process(target=get_data)

    p1.start()
#    p2.start()

    p1.join()
#    p2.join()
    

