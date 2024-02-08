import pandas as pd
import yfinance as yf
index_list = ['^DJI','^GSPC','^IXIC'] 
index_dict={}

def Index_market_metrics():
    global index_dict
    list_of_metrics = ['symbol','shortName','volume','averageVolume','previousClose','open','dayLow','dayHigh',
            'fiftyDayAverage','fiftyTwoWeekLow','fiftyTwoWeekHigh','quoteType', 'twoHundredDayAverage']
    lst2 = []
    for symbol_str in index_list:
        # print(symbol_str)
        symbol = yf.Ticker(str(symbol_str))
        stock_info = symbol.info
        stock_dict = {}
        for metric in list_of_metrics:
            if metric in stock_info:
                stock_dict[metric] = stock_info[metric]
            if 'shortName' in stock_info:
                index_dict[symbol_str] = stock_info['shortName']  # Assign shortName to index_dict directly
        
        lst2.append(stock_dict)
    Stock_df = pd.DataFrame(lst2, columns=[i for i in list_of_metrics])
    # print(Stock_df)
    # print(index_dict)
    return Stock_df,percent_change(Stock_df)


def percent_change(df):
    global df_info
    df_info = df.copy()
    df_info.loc[:, 'percentChange'] = (((df['open'] - df['previousClose'])) / df['previousClose']) * 100
    # print(df)
    
    # columns_to_print = ['shortName', 'previousClose', 'open', 'percentChange']
    # for column in columns_to_print:
    #     print(df[column])  
    # top_list(df_info)
    # print(df_info)
    return df_info

Index_market_metrics()

# msft = yf.Ticker("^DJI")

# # get all stock info
# print(msft.info)