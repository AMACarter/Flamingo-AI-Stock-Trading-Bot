import alpaca_trade_api as tradeapi # Alpaca API
import sys 
import datetime
import time
import threading
import webbrowser
import logging # Data logging
import scipy # Linear algebra
import numpy # Arrays and Matrices
import matplotlib # Plotting
import pandas # Data manipulation
import sklearn # Machine learning
import tkinter as tk # GUI elements
import multiprocessing # Thread management


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
    
    api = tradeapi.REST(
        'PKPVWUKI5H0UBVALQUXM',
        'QQrNRzBk5RTfVoRX8ISdYrWeQwHh51XmDb6LVSBh',
        'https://paper-api.alpaca.markets', api_version='v2'
    )
    # Get our account information.
    account = api.get_account()

    # Check if our account is restricted from trading.
    if account.trading_blocked:
        print('Account is currently restricted from trading.')

    # Check how much money we can use to open new positions.
        print('${} is available as buying power.'.format(account.buying_power))

    # Get a list of all of our positions.
    portfolio = api.list_positions()

    # Print the quantity of shares for each position.
    for position in portfolio:
        print("{} shares of {}".format(position.qty, position.symbol))
    
    # Check our current balance vs. our balance at the last market close
    balance_change = float(account.equity) - float(account.last_equity)
    print(f'Today\'s portfolio balance change: ${balance_change}')

    # Logging different components
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    
    print("Flamingo Bot Initialised.")
    
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