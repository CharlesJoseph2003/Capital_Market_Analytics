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

  # market_cap = entry['market_cap']
  # percent_change_1h = entry['percent_change_1h']
  # percent_change_24h = entry['percent_change_24h']
  # price = entry['price']
  # volume = entry['volume']
  # circulating_supply = entry['circulating_supply']

  crypto_name.append(name)
  crypto_symbols.append(symbol)
  crypto_price.append(price)
  crypto_max_supply.append(max_supply)

crypto_dict = {}
Crypto_name_ticker = pd.DataFrame({'Company': crypto_name, 'Ticker': crypto_symbols})
# print(Crypto_name_ticker)

crypto_dict = dict(zip(Crypto_name_ticker['Ticker'].iloc[0:total_crypto], Crypto_name_ticker['Company'].iloc[0:total_crypto]))
# print(crypto_dict)# for max_supply in crypto_max_supply:
#     if max_supply is None:
#         crypto_max_supply.append("infinite")
#     else:
#         crypto_max_supply.append(max_supply)
# print(crypto_symbols)
# print(crypto_price)
# print(crypto_max_supply)
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
    # Crypto_df['percentChange'] = ((Crypto_df['open'] - Crypto_df['previousClose']) / Crypto_df['previousClose']) * 100
    # print(Crypto_df['previousClose'])
    # print(Crypto_df)
    # return Crypto_df
    return Crypto_df, percent_change(Crypto_df)
crypto_metrics()


def percent_change(df):
    df['percentChange'] = ((df['open'] - df['previousClose']) / df['previousClose']) * 100
    # df['delta'] = df['percentChange'] / df['previousClose']
    # print(df)
    return df
# crytpo_metrics()


def treemap_crypto():
    _,df_info = crypto_metrics()
    tree_df = df_info[['symbol', 'currentPrice','marketCap', 'previousClose']].copy()  # Select relevant columns for the treemap
    tree_df['marketCap'] = tree_df['marketCap'].astype(float)
    # print(tree_df)
    return tree_df
treemap_crypto()


# def percent_change(df):
#     global df_info_crypto
#     df_info_crypto = df.copy()
#     df_info_crypto.loc[:, 'percentChange'] = (((df['open'] - df['previousClose'])) / df['previousClose']) * 100
#     print(df_info_crypto['percentChange'])
#     # print(df)
    
#     # columns_to_print = ['shortName', 'previousClose', 'open', 'percentChange']
#     # for column in columns_to_print:
#     #     print(df[column])  
#     # top_list(df_info)
#     # print(df_info)
#     return df_info_crypto

# crytpo_metrics()



# def history_crytp():
#     hist_list = []
#     for symbol_str in crypto_list: 
#         symbol = yf.Ticker(str(symbol_str))
#         hist = symbol.history(period="1mo")
#         hist_list.append(symbol_str)
#         hist_list.append(hist)
#     # print(hist_list)
    
# def market_metrics_crypto ():
#     list_of_metrics = ['symbol','shortName','marketCap']
#     # list_of_metrics = ['symbol','shortName','marketCap','currentPrice', 'circulatingSupply','volume','volumeAllCurrencies','averageVolume','previousClose','open','dayLow','dayHigh',
#     #         'fiftyDayAverage','fiftyTwoWeekLow','fiftyTwoWeekHigh', 'maxAge','trailingPegRatio', 'description']
#     lst2 = []
#     for symbol_str in crypto_list:
#         # print(symbol_str)
#         symbol = yf.Ticker(str(symbol_str))
#         crypto_info = symbol.info
#         crypto_dict = {}
#         for metric in list_of_metrics:
#             if metric in crypto_info:
#                 crypto_dict[metric] = crypto_info[metric]
#         lst2.append(crypto_dict)
#     sorted_list = sorted(lst2, key=lambda x: x['marketCap'], reverse=True) #can use this to sort by other metrics, the callback will use the 
#     #x['marketCap]
#     # print(sorted_list)
#     Crypto_df = pd.DataFrame(sorted_list, columns=[i for i in list_of_metrics])
#     top_crypto = Crypto_df.head(10)
#     # print(top_stocks)

#     return percent_change(top_crypto)

# def percent_change(df):
#     df_info = df.copy()
#     df_info.loc[:, 'percentChange'] = (((df['open'] - df['previousClose'])) / df['previousClose']) * 100
#     top_list(df_info)
#     print(df_info)
#     return df_info
# def top_list(df):
#     # top_symbols.clear()
#     global top_crypto_symbols
#     for symbol in df['symbol']:
#         top_crypto_symbols.append(symbol)
#     print('from data_analysis',top_crypto_symbols)
#     return top_crypto_symbols

# market_metrics_crypto()

