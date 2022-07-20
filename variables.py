# You can view your trades at https://exchange.sandbox.gemini.com/ and fees
# at https://www.gemini.com/fees/api-fee-schedule#section-api-fee-schedule

# You need sandbox public keys / private keys
public_key = "<redacted>"  
private_key = "<redacted>"
api_maker_fee = 0.002 # 0.20%

# Use "gusd_sell = 'all'" to transfer all GUSD to USD (leaving zero balance).
# Replace gusd_balance below to transfer a static amount.
gusd_sell = 'all'

# Update symbol based on what crypto/fiat pair you want to buy. Update tick 
# size and quote currency price increment based on what crypto-pair you are 
# buying. The last number is the dollar amount of the coin that you want to 
# buy. Check the API documentation to see what you need for a given pair (i.e.;
# in the documentation if it says "1e-8" you want to use the number after "e-" 
# which would be 8; in the case of .01 you want 2 because .01 is 1e-2).
# https://docs.gemini.com/rest-api/#symbols-and-minimums
crypto = [
    ['BTCUSD', 8, 2, 8],
    ['ETHUSD', 6, 2, 8],
    ['SOLUSD', 6, 3, 2],
    ['DOTUSD', 6, 4, 2]
    ]

# Set up a buy for 0.999 times the current price. Add more decimals for a 
# higher price and faster fill. If the price is too close to spot your order 
# won't post. Lower factor makes the order cheaper but fills quickly (0.5 
# would set an order for half the price and so your order could take 
# months/years/never to fill)
factor = 0.999
