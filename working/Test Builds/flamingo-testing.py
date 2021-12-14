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
    
# STRATEGY

def flamingo_teststrat():
    
    sample_data = [
  ['Mon', 20, 28, 38, 45],
  ['Tue', 31, 38, 39, 50],
  ['Wed', 50, 55, 56, 62],
  ['Thu', 77, 70, 71, 60],
  ['Fri', 68, 66, 22, 15],
 ]

    sample_data = pd.DataFrame(sample_data,
                               columns=["Day","Open","High","Low","Close"])

    open = sample_data['Open']
    high = sample_data['High']
    low = sample_data['Low']
    close = sample_data['Close']
    
    talib.CDLBELTHOLD(open, high, low, close)        
    talib.CDLBREAKAWAY(open, high, low, close)    
    talib.CDL3BLACKCROWS(open, high, low, close)
    talib.CDL3STARSINSOUTH(open, high, low, close)
    talib.CDLRISEFALL3METHODS(open, high, low, close)
    

# MAIN THREAD

if __name__ == '__main__': 
    
    p1 = multiprocessing.Process(target=flamingo_startup)
    p2 = multiprocessing.Process(target=flamingo_teststrat)

    p1.start()
    p2.start()

    p1.join()
    p2.join()
    

