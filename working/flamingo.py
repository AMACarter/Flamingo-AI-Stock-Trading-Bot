import alpaca_trade_api as tradeapi # Alpaca API
import sys 
import datetime
import time
import webbrowser
import importlib
import threading
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import logging # Data logging
import tkinter as tk # GUI elements
import multiprocessing # Thread management
import flamingoAI # AI module

from alpaca_trade_api.rest import REST
from alpaca_trade_api.rest import TimeFrame
from matplotlib import pyplot
from pandas import read_csv
from multiprocessing import Process
from re import T
from tkinter import *
from colorama import Fore, Back, Style
from functools import partial
from datetime import datetime
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

# CONNECTION TO API AND ACCOUNT

global api

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
        print (Fore.GREEN + f'Today\'s portfolio balance change: ${round (balance_change, 2)}')
    
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

# LAUNCH GUI

def flamingo_gui():
    
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
    
    histtf={}
    for tf in ['15Min']:
        hist = api.get_portfolio_history(
            date_start='2021-08-15',
            period="7D",
            extended_hours=True,
            timeframe=tf
        ).df
        histtf[tf] = hist
    
    root = Tk()
    root.title("Flamingo Trading Bot")
    root.geometry("1920x1080")
    
    fig, (ax1,ax2) = plt.subplots(2)
    fig.suptitle('Portfolio')
    ax1.plot(hist.equity)
    ax2.plot(hist.profit_loss)
    
    canvas = FigureCanvasTkAgg(fig, root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
        
    # Get users API keys
    
    # UserApiKeyLabel = tk.Label(window, text="API Key").grid(row=0, column=0)
    # UserApiKey = StringVar()
    # UserApiEntry = Entry(window, textvariable=UserApiKey).grid(row=0, column=1)
    
    # UserSecretKeyLabel = tk.Label(window, text="Secret key").grid(row=1, column=0)
    # UserSecretKey = StringVar()
    # UserSecretKeyEntry = Entry(window, textvariable=UserSecretKey).grid(row=1, column=1)
    
    # validateAPI = partial(validateAPI, UserApiKey, UserSecretKey)
    
    # AuthButton =Button(window, text="Validate", command=validateAPI).grid(row=3, column=1)
      
    root.mainloop() 


# MAIN THREAD

if __name__ == '__main__': 
    
    p1 = multiprocessing.Process(target=flamingo_startup)
    p2 = multiprocessing.Process(target=flamingo_gui)

    p1.start()
    p2.start()

    p1.join()
    p2.join()
