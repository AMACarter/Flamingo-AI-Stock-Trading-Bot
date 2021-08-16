import alpaca_trade_api as tradeapi # Alpaca API
import sys 
import datetime
import time
import webbrowser
import importlib
import logging # Data logging
import tkinter as tk # GUI elements
import multiprocessing # Thread management
from colorama import Fore, Back, Style


import flamingoAI # AI module

from alpaca_trade_api.rest import REST
from alpaca_trade_api.rest import TimeFrame
from matplotlib import pyplot
from pandas import read_csv
from multiprocessing import Process
from re import T
    
# LAUNCH GUI

def flamingo_gui():
    
    window = tk.Tk()
    window.title("Flamingo Trading Bot")

    label = tk.Label(text="")
    label.pack()
    window.mainloop() 

# CONNECTION TO API AND ACCOUNT

def flamingo_startup():
    
    # Setup Alpaca API 
    api_key = 'PKPVWUKI5H0UBVALQUXM'
    api_secret = 'QQrNRzBk5RTfVoRX8ISdYrWeQwHh51XmDb6LVSBh'
    base_url = 'https://paper-api.alpaca.markets'
    data_url = 'wss://data.alpaca.markets'

    # Initiate REST API
    api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')
    
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
    print (f'Today\'s portfolio balance change: ${round (balance_change, 2)}')
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
    
    # Logging different components
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    
    print ("Flamingo Bot Initialised.")
    
    # Open broker dashboard
    webbrowser.open('https://app.alpaca.markets/brokerage/dashboard/overview', new=2, autoraise=True)

# MAIN THREAD

if __name__ == '__main__': 
    
    p1 = multiprocessing.Process(target=flamingo_startup)
    p2 = multiprocessing.Process(target=flamingo_gui)

    p1.start()
    p2.start()

    p1.join()
    p2.join()
