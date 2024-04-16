import yfinance as yf
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
# url =  'https://stockanalysis.com/list/biggest-companies/'
# r = requests.get(url)
# # print(r)
# soup  =  BeautifulSoup(r.text, 'lxml')
# # table = soup.find('table', class_= 'default-table table marketcap-table dataTable')
# table = soup.find('table', class_= 'symbol-table svelte-132bklf') #might have to update html tag because website changes it 


total_stock=20
url = 'https://stockanalysis.com/list/biggest-companies/'

# Fetch the webpage content
response = requests.get(url)
html_content = response.text

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find the table with id="main-table"
desired_table = soup.find('table', {'id': 'main-table'})

# Extract the class attribute from the table tag
if desired_table:
    table_classes = desired_table.get('class')
    if table_classes:
        combined_classes = ' '.join(table_classes)

        # Use the combined_classes variable to find the table
        table = soup.find('table', class_=combined_classes)

        # Check if the table was found
        if table:
            print("Table found with the desired class:", combined_classes)
        else:
            print("Table not found with the desired class.")
    else:
        print("No class attribute found for the table.")
else:
    print("Table not found.")


# if table:
#     headers = table.find_all('th')
#     titles = [header.text for header in headers]
#     print(titles)
# else:
#     print("Table not found")

headers = table.find_all('th')
titles = []
for i in headers:
    title = i.text
    titles.append(title)
df = pd.DataFrame(columns=titles)
rows =  table.find_all('tr')
for i in rows[1:]:
    data = table.find_all('td')
    # print(data)
    row = [tr.text for tr in data]
# print(row)
rows = [row[i:i+7] for i in range(0, len(row), 7)]

# Convert to DataFrame
df = pd.DataFrame(rows, columns=['Rank', 'Ticker', 'Company', 'Market Cap', 'Price', 'Change', 'Volume'])
df['Ticker'] = df['Ticker'].str.replace(".", "-")


symbols_dict = {}
symbols_dict = dict(zip(df['Ticker'].iloc[0:total_stock], df['Company'].iloc[0:total_stock]))

# print('this is symbols dict', symbols_dict)
symbols_list = list(df.iloc[0:total_stock, 1])
for i in range(len(symbols_list)):
    symbols_list[i] = symbols_list[i].replace(".", "-")  # Replaces all "." with "-" in the string 
# print('symbols list', symbols_list)
list_of_metrics = ['symbol','shortName','marketCap','currentPrice', 'dividendYield','volume','averageVolume',
                       'previousClose','open','dayLow','dayHigh','fiftyDayAverage','fiftyTwoWeekLow','fiftyTwoWeekHigh', 
                       'profitMargins','totalRevenue','pegRatio', 'longBusinessSummary','sector']

selected_rows = ['Total Revenue', 'Total Expenses', 'Operating Revenue',  'Operating Expense','Research And Development ', 
                 'Operating Income', 'Net Income','Net Income Common Stockholders', 'Gross Profit', 'EBITDA',
                  'Tax Rate For Calcs']

# selected_rows = ['Total Revenue', 'Net Income', 'Gross Profit', 'EBITDA', 'Total Expenses', 'Operating Expense', 'Tax Rate For Calcs']

    
def market_metrics():
    lst2 = []
    for symbol_str in symbols_list:
        # print(symbol_str)
        symbol = yf.Ticker(str(symbol_str))
        stock_info = symbol.info
        stock_dict = {}
        for metric in list_of_metrics:
            if metric in stock_info:
                stock_dict[metric] = stock_info[metric]
        
        lst2.append(stock_dict)
    # print(lst2)
    Stock_df = pd.DataFrame(lst2, columns=[i for i in list_of_metrics])
    print(Stock_df)
    return Stock_df, percent_change(Stock_df)



def percent_change(df):
    df['percentChange'] = ((df['open'] - df['previousClose']) / df['previousClose']) * 100
    df['delta'] = df['percentChange'] / df['previousClose']
    # print(df)
    return df
market_metrics()


def treemap():
    _,df_info = market_metrics()
    tree_df = df_info[['symbol', 'currentPrice','marketCap', 'delta', 'percentChange', 'previousClose', 'sector']].copy()  # Select relevant columns for the treemap
    tree_df['marketCap'] = tree_df['marketCap'].astype(float)
    # print(tree_df)
    return tree_df
treemap()


def income_statement_table():
    lst = []
    for symbol_str in symbols_list:
        stock = yf.Ticker(symbol_str)
        df = pd.DataFrame(stock.income_stmt)
        missing_rows = [row for row in selected_rows if row not in df.index]
        present_rows = [row for row in selected_rows if row in df.index]
        
        if missing_rows:
            new_df = df.loc[present_rows].set_index([[symbol_str] * len(present_rows), present_rows])
        else:
            new_df = df.loc[present_rows].set_index([[symbol_str] * len(present_rows), present_rows])
        new_df.columns = new_df.columns.astype(str)
        lst.append(new_df)

    income_statement = pd.concat(lst, axis=1)
    return income_statement


# def incomestatement():
#     lst2 = []
#     for symbol_str in symbols_list:
#         symbol = yf.Ticker(str(symbol_str))
#         stock_income = pd.DataFrame(symbol.income_stmt)
#         stock_dict = {}
#         print(symbol_str)
        
#         for metric in selected_rows:
#             value = stock_income.get(metric)
#             if value is not None:
#                 print(metric)
#                 stock_dict[metric] = value
#             else:
#                 # Handle missing metric, e.g., set it to NaN or any default value
#                 stock_dict[metric] = None
        
#         lst2.append(stock_dict)

#     Stock_df = pd.DataFrame(lst2, columns=[i for i in selected_rows])
#     print(Stock_df)



# def incomestatement():
#     lst2 = []
#     # _,df_info = market_metrics()
#     for symbol_str in symbols_list:
#         symbol = yf.Ticker(str(symbol_str))
#         stock_income = pd.DataFrame(symbol.income_stmt)
#         # print(stock_income.index)
#         # stock_income = symbol.income_stmt
#         # print(stock_income)
#         stock_dict = {}
#         print(symbol_str)
#         for metric in selected_rows:
#             if metric in stock_income.index:
#                 print(metric)
#                 stock_dict[metric] = stock_income[metric]
#             else:
#                 continue
#         lst2.append(stock_dict)
#     # print(lst2)
#     Stock_df = pd.DataFrame(lst2, columns=[i for i in selected_rows])
#     print(Stock_df)

#     missing_rows = [row for row in selected_rows if row not in stock_income]
#     if missing_rows:
#         print(symbol_str)
#         print('missing_row',missing_rows)
            
#         present_rows = [ row for row in selected_rows if row in stock_income]
#         if present_rows:
#             print(symbol_str)
#             print(present_rows)
#         for metric in selected_rows:
        #     pass

# incomestatement()












# def incomestatement():

#     lst = []
#     empty_df = pd.DataFrame()
#     _,df_info = market_metrics()
#     for symbol_str in df_info['symbol']:
#         symbol = yf.Ticker(str(symbol_str))
#         df = pd.DataFrame(symbol.income_stmt)
#         missing_rows = [row for row in selected_rows if row not in df.index]
#         present_rows = [ row for row in selected_rows if row in df.index]
#         if missing_rows:
#             # print(f"Rows {missing_rows} not present in the income statement data for {symbol_str}. Skipping.")
#             # print(f"Rows {present_rows}  present in the income statement data for {symbol_str}")
#             new_df = df.loc[present_rows]
#         else:
#             new_df = df.loc[selected_rows]
#         new_df['ticker'] = symbol_str
#         # new_df.set_index('ticker', inplace=False)
#         # lst.append(new_df)
#     # print(lst)
#         new_df.index = new_df.index.astype(str)  # Convert index to strings
#         # print(new_df.index)
#         new_df.columns = new_df.columns.astype(str)
#         new_df_columns = list(new_df.columns)
#         table_data = new_df[new_df_columns]
      

#     # print(empty_df)
#         # empty_df.append(table_data)
#         # print(symbol)
#         # print(table_data)
#         lst.append(table_data)
#     print(lst)

#     return lst
# incomestatement()

        # _,df_info = market_metrics()


    # # # _,df_info = market_metrics()
    # # lst=[]
    # # for symbol_str in symbols_list:
    # #     symbol = yf.Ticker(str(symbol_str))
    # #     df = pd.DataFrame(symbol.income_stmt)
    # #     new_df = df.loc[['Total Revenue','Net Income', 'Gross Profit', 'EBITDA', 'Total Expenses', 'Operating Expense','Tax Rate For Calcs']]
    # #     new_df.index = new_df.index.astype(str)  # Convert index to strings
    # #     new_df.columns = new_df.columns.astype(str)
    # #     new_df_columns = list(new_df.columns)
    # #     table_data = new_df[new_df_columns]
    # #     lst.append(table_data)
    # # print(lst)


        # stock_income_statement = symbol.income_stmt
        # stock_dict = {}
        # for statement in list_of_statements:
        
        # print(stock_income_statement)
        







# resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
# soup = bs.BeautifulSoup(resp.text, 'lxml')
# table = soup.find('table', {'class': 'wikitable sortable'})

# tickers = []
# for row in table.findAll('tr')[1:]:
#     ticker = row.findAll('td')[0].text
#     tickers.append(ticker)
# tickers = [s.replace('\n', '') for s in tickers]

# start = datetime.datetime(2020, 1, 1)
# end = date.today()
# data = yf.download(tickers, start=start, end=end)
# # print(data)

# df = data.stack().reset_index().rename(index=str, columns={"level_1": "Symbol"}).sort_values(['Symbol','Date'])
# df.set_index('Date', inplace=True)
# pd.DataFrame(df)

# # print(df)
# symbols_list = list(df['Symbol'].unique())
# print(symbols_list)
# top_symbols = []


# class Stock: 
#     def __init__(self, list_of_symbols = symbols_list):
#         if list_of_symbols is None:
#             self.list_of_symbols = []
#         else:
#             self.list_of_symbols = list_of_symbols
        
    #put into dataframe
    # def history(self):
    #     hist_list = []
    #     for symbol_str in self.list_of_symbols: 
    #         symbol = yf.Ticker(str(symbol_str))
    #         hist = symbol.history(period="1mo")
    #         hist_list.append(symbol_str)
    #         hist_list.append(hist)
    #     # print(hist_list)
    
    # def market_metrics(self):
    #     list_of_metrics = ['symbol','shortName','marketCap','currentPrice', 'dividendYield','volume','averageVolume','previousClose','open','dayLow','dayHigh',
    #            'fiftyDayAverage','fiftyTwoWeekLow','fiftyTwoWeekHigh', 'profitMargins','totalRevenue','pegRatio']
    #     lst2 = []
    #     for symbol_str in self.list_of_symbols:
    #         # print(symbol_str)
    #         symbol = yf.Ticker(str(symbol_str))
    #         stock_info = symbol.info
    #         stock_dict = {}
    #         for metric in list_of_metrics:
    #             if metric in stock_info:
    #                 stock_dict[metric] = stock_info[metric]
    #         lst2.append(stock_dict)
    #     sorted_list = sorted(lst2, key=lambda x: x['marketCap'], reverse=True) #can use this to sort by other metrics, the callback will use the 
    #     #x['marketCap]
    #     # print(sorted_list)
    #     Stock_df = pd.DataFrame(sorted_list, columns=[i for i in list_of_metrics])
    #     top_stocks = Stock_df.head(10)
    #     # print(top_stocks)

    #     self.percent_change(top_stocks)

    # def percent_change(self, df):
    #     df = df.copy()
    #     df.loc[:, 'percentChange'] = (((df['open'] - df['previousClose'])) / df['previousClose']) * 100
    #     # print(df)
        
    #     # columns_to_print = ['shortName', 'previousClose', 'open', 'percentChange']
    #     # for column in columns_to_print:
    #     #     print(df[column])  
    #     # self.generate_graphs(df)  
    #     self.top_list(df)
    #     return df
    # def top_list(self,df):
    #     for symbol in df['symbol']:
    #         top_symbols.append(symbol)
    #     print(top_symbols)

# def history():
#     hist_list = []
#     for symbol_str in symbols_list: 
#         symbol = yf.Ticker(str(symbol_str))
#         hist = symbol.history(period="1mo")
#         hist_list.append(symbol_str)
#         hist_list.append(hist)
#     # print(hist_list)


# def top_list(df):
#     # top_symbols.clear()
#     global top_symbols
#     top_symbols.clear()
#     for symbol in df['symbol']:
#         top_symbols.append(symbol)
#     # for index, (symbol, shortname) in enumerate(zip(df['symbol'], df['shortname'])):
#     #     top_symbols[symbol] = shortname
 
#     print('from data_analysis',top_symbols)
#     return top_symbols

