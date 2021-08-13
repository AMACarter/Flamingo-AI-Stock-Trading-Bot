import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import REST
import logging

if __name__ == '__main__':

api = tradeapi.REST('PKPVWUKI5H0UBVALQUXM','QQrNRzBk5RTfVoRX8ISdYrWeQwHh51XmDb6LVSBh','https://paper-api.alpaca.markets/v2/account')

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


