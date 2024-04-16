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

