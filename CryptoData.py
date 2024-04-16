 #This example uses Python 2.7 and the python-request library.
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import yfinance as yf
import pandas as pd
import pprint

total_crypto = 20

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

parameters = {
  'sort': 'market_cap',
  # 'slug': 'bitcoin',
  'convert':'USD'
}
headers = { #need to give api the api key, functions as a passord and allows entry
  'Accepts': 'application/json', #letting us select which return format we want, returns a json format
  'X-CMC_PRO_API_KEY': 'c78b4a89-8c9f-4e0b-9f7c-1cb0c033a05d', #passes the api key
}

session = Session()
session.headers.update(headers) #adds headers to the session, every single request will use the headers
# and get access to api and get json response

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)#['data']['1']['quote']['USD']['price']
  # pprint.pprint(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)


crypto_symbols = []
crypto_price = []
crypto_max_supply = []
crypto_name = []
for entry in data['data'][:total_crypto]: 
  name = entry['name']
  symbol = entry['symbol'] + '-USD'
  price = entry['quote']['USD']['price']
  max_supply = entry['max_supply']
  crypto_name.append(name)
  crypto_symbols.append(symbol)
  crypto_price.append(price)
  crypto_max_supply.append(max_supply)

crypto_dict = {}
Crypto_name_ticker = pd.DataFrame({'Company': crypto_name, 'Ticker': crypto_symbols})
# print(Crypto_name_ticker)

crypto_dict = dict(zip(Crypto_name_ticker['Ticker'].iloc[0:total_crypto], Crypto_name_ticker['Company'].iloc[0:total_crypto]))
list_of_metrics = ['symbol','shortName','marketCap', 'circulatingSupply','volume','volumeAllCurrencies','averageVolume','previousClose','open','dayLow','dayHigh',
        'fiftyDayAverage','fiftyTwoWeekLow','fiftyTwoWeekHigh', 'maxAge','trailingPegRatio', 'description']

def percent_change(df):
    df['percentChange'] = ((df['open'] - df['previousClose']) / df['previousClose']) * 100
    # df['delta'] = df['percentChange'] / df['previousClose']
    # print(df)
    return df

def crypto_metrics():
    lst2 = []
    for symbol_str in crypto_symbols:
        # print(symbol_str)
        symbol = yf.Ticker(str(symbol_str))
        crypto_info = symbol.info
        stock_dict = {}
        for metric in list_of_metrics:
            if metric in crypto_info:
                stock_dict[metric] = crypto_info[metric]
        lst2.append(stock_dict)
    Crypto_df = pd.DataFrame(lst2, columns=[i for i in list_of_metrics])
    Crypto_df['currentPrice'] = crypto_price
    Crypto_df['maxSupply'] = crypto_max_supply
    return Crypto_df, percent_change(Crypto_df)
crypto_metrics()


def percent_change(df):
    df['percentChange'] = ((df['open'] - df['previousClose']) / df['previousClose']) * 100
    return df


def treemap_crypto():
    _,df_info = crypto_metrics()
    tree_df = df_info[['symbol', 'currentPrice','marketCap', 'previousClose']].copy()  # Select relevant columns for the treemap
    tree_df['marketCap'] = tree_df['marketCap'].astype(float)
    return tree_df
treemap_crypto()
