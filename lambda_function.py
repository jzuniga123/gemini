import json
import gemini
import variables

public_key = variables.public_key
private_key = variables.private_key
gusd_sell = variables.gusd_sell
factor = variables.factor
trader = gemini.PrivateClient(public_key, private_key)
portfolio = trader.get_balance()

def _convertGUSDtoUSD(gusd_sell):

    # If no GUSD, then nothing to convert. Otherwise, convert amount held or,
    # if amount stated, lesser of stated amount and available amount.
    gusd = list(coin['available'] for coin in portfolio if coin['currency'] == 'GUSD')
    if len(gusd) == 0:
        print('No GUSD to convert.')
        return
    # else:

    if gusd_sell == 'all':
        gusd_balance = gusd[0]
    else:
        gusd_balance = str(min(float(gusd_sell), float(gusd[0])))

    # Use "buy" to convert USD to GUSD and "sell" to convert GUSD into USD
    results = trader.wrap_order(gusd_balance, "sell")


def _buyCrypto(symbol, tick_size, increment, buy_amount):

    # Check if there is any fiat available to make purchases.
    usd = list(coin['available'] for coin in portfolio if coin['currency'] == 'USD')
    if len(usd) == 0:
        print('No USD available to make purchases.')
        return

    # Set up a buy for the current price
    symbol_spot_price = float(trader.get_ticker(symbol)['ask'])

    # To set a limit order at a fixed price (ie. $55,525) set 
    # execution_price = "55525.00" or execution_price = str(55525.00)
    execution_price = str(round(symbol_spot_price*factor, increment))

    # Determine fee offset necessary for given purchase amount and then set
    # amount to the most precise rounding (tick_size) such that an order for
    # $20.00 should buy $19.96 coin and pay $0.04 (0.20%) fee. Must round 
    # down because Gemini rounds up and purchase can exceed stated amount.
    fee_offset = 1 - variables.api_maker_fee
    buy_size = (buy_amount * fee_offset) / float(execution_price)
    amount = int(buy_size * 10 ** tick_size) / 10 ** tick_size
		
    # Execute maker buy for given symbol, amount, and calculated price.
    buy = trader.new_order(symbol, str(amount), execution_price, "buy", ["maker-or-cancel"])
    print(f'Maker Buy: {buy}')

    
def lambda_handler(event, context):

    # Recurring buys of GUSD have no fee so account is funded with automatic
    # purchases of GUSD. To fund purchases, GUSD is then converted to USD.
    _convertGUSDtoUSD(gusd_sell)

    # Place orders for each asset listed in variables file
    for asset in variables.crypto:
        _buyCrypto(asset[0], asset[1], asset[2], asset[3])

    return {
        'statusCode': 200,
        'body': json.dumps('End of script')
    }
