import yfinance as yf
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from StockData import market_metrics
from CryptoData import crypto_metrics

# df_info_crypto_result = crypto_metrics()
_,df_info_crypto_result = crypto_metrics()
new_crypto_df = pd.DataFrame(df_info_crypto_result)
new_crypto_df.set_index('symbol', inplace=True)

_,df_info_result = market_metrics()
new_df = pd.DataFrame(df_info_result)
new_df_2 = new_df.copy()
new_df.set_index('symbol', inplace=True)

indicator_title_text_size = 15
paper_bgcolor = 'white'
paper_bgcolor2 = 'white'


# print(df_info_result)
# print('new Df', new_df)

def generate_graphs1(dropdown, time): 
    # selected_key = [key for key, value in symbols_dict.items() if value == dropdown][0]
    # print('this is the selected key', selected_key)
    # symbol = new_df_2.loc[dropdown, 'symbol']
    # print('this is the symbol',symbol)
    # print(f"Dropdown value: {dropdown}")

    fig = make_subplots(subplot_titles=[dropdown], specs=[[{"secondary_y": True}]],)
    # Stock = yf.Ticker(str(df_info_result.loc[dropdown, 'symbol']))
    Stock = yf.Ticker(dropdown)

    hist = Stock.history(period=time)
    df = pd.DataFrame(hist)
    df.reset_index(inplace=True)
    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
# Filter out weekends (Saturday and Sunday) and overwrite the original df


    # print(df['Date'])
    hist['diff'] = hist['Close'] - hist['Open']
    hist.loc[hist['diff']>=0, 'color'] = 'green'
    hist.loc[hist['diff']<0, 'color'] = 'red'

    fig.add_trace(go.Scatter(x=hist.index,y=hist['Close'].rolling(window=1).mean(),marker_color='blue',name='20 Day MA'),)
    fig.add_trace(go.Candlestick(x=hist.index,
            open=hist['Open'],
            high=hist['High'],
            low=hist['Low'],
            close=hist['Close'],
            name='Price'))
    
    if time == '5d':
        hist = hist.resample('H').last()
        fig.update_xaxes(tickformat = '%b-%d %H:%M', tickmode = 'linear')
    elif time == '1mo':
        hist = hist.resample('D').last()
    else:
        hist = hist.resample('M').last()
        fig.add_trace(go.Bar(x=hist.index, y=hist['Volume'], name='Volume', marker_color=hist['color']), secondary_y = True,)



    # fig.add_trace(go.Bar(x=hist.index, y=hist['Volume'], name='Volume', marker_color=hist['color']), secondary_y = True,)

    fig.update_yaxes(visible=True, secondary_y=True, )
    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.0,xanchor="right",x=1))
    
    fig.update_layout(showlegend=True, paper_bgcolor=paper_bgcolor)
    fig.update_xaxes(showspikes=True, spikecolor="black", spikesnap="cursor", spikemode="across", tickangle=0),
    fig.update_yaxes(showspikes=True, spikecolor="black", spikethickness=2)
    fig.update_layout(spikedistance=1000, hoverdistance=100)
    return fig




def generate_graphs2(dropdown, time): 
    fig = make_subplots(subplot_titles=[dropdown], specs=[[{"secondary_y": True}]],)
    Crypto = yf.Ticker(dropdown)
    hist = Crypto.history(period=time)
    df = pd.DataFrame(hist)
    df.reset_index(inplace=True)
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')


    # print(df['Date'])
    hist['diff'] = hist['Close'] - hist['Open']
    hist.loc[hist['diff']>=0, 'color'] = 'green'
    hist.loc[hist['diff']<0, 'color'] = 'red'

    fig.add_trace(go.Scatter(x=hist.index,y=hist['Close'].rolling(window=1).mean(),marker_color='blue',name='20 Day MA'),)
    fig.add_trace(go.Candlestick(x=hist.index,
            open=hist['Open'],
            high=hist['High'],
            low=hist['Low'],
            close=hist['Close'],
            name='Price'))
    
    
    if time == '5d':
        hist = hist.resample('D').last()
        fig.update_xaxes(tickformat = '%b-%d %H:%M', tickmode = 'linear')
    elif time == '1mo':
        hist = hist.resample('D').last()
    else:
        hist = hist.resample('M').last()
        fig.add_trace(go.Bar(x=hist.index, y=hist['Volume'], name='Volume', marker_color=hist['color']), secondary_y = True,)



    fig.update_yaxes(visible=True, secondary_y=True, )
    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.0,xanchor="right",x=1))

    fig.update_xaxes(showspikes=True, spikecolor="black", spikesnap="cursor", spikemode="across", tickangle = 0,)
    fig.update_yaxes(showspikes=True, spikecolor="black", spikethickness=2)
    fig.update_layout(spikedistance=1000, hoverdistance=100)
    fig.update_layout(showlegend=True, paper_bgcolor=paper_bgcolor)
    return fig



def current_indicator_left(dropdown):
    stock_data = market_metrics()[0].loc[market_metrics()[0]['symbol'] == dropdown]
    print(stock_data)
    fig = go.Figure(go.Indicator(
        mode="number+delta",
        value=stock_data['currentPrice'].iloc[0],  # Assuming df is defined somewhere before this function
        number={'prefix': "$", "font":{"size":20}, 'valueformat': '.2f'},
        title= {'text': "Current Price", "font":{"size":indicator_title_text_size}},
        delta={'position': "bottom", 'reference': stock_data['previousClose'].iloc[0]},
        # domain={'x': [0, 1], 'y': [0, 0.5]}
    ))

    fig.update_layout(paper_bgcolor=paper_bgcolor2)

    return fig


def update_indicator(n, dropdown):
    return current_indicator_left(dropdown)


def current_indicator_right(dropdown):
    crypto_data = crypto_metrics()[0].loc[crypto_metrics()[0]['symbol'] == dropdown]
    print(crypto_data)
    fig = go.Figure(go.Indicator(
        mode="number+delta",
        value=crypto_data['currentPrice'].iloc[0],  # Assuming df is defined somewhere before this function
        number={'prefix': "$", "font":{"size":20}, 'valueformat': '.2f'},
        title= {'text': "Current Price", "font":{"size":indicator_title_text_size}},
        delta={'position': "bottom", 'reference': crypto_data['previousClose'].iloc[0]},
        # domain={'x': [0, 1], 'y': [0, 0.5]}
    ))

    fig.update_layout(paper_bgcolor=paper_bgcolor2)

    return fig


def update_indicator_crypto(n, dropdown):
    return current_indicator_right(dropdown)




# def current_indicator_left(dropdown):
#     fig = go.Figure(go.Indicator(
#         mode="number+delta",
#         value= new_df.loc[dropdown,'currentPrice'],  # Assuming df is defined somewhere before this function
#         number={'prefix': "$", "font":{"size":20}, 'valueformat': '.2f'},
#         title= {'text': "Current Price", "font":{"size":indicator_title_text_size}},
#         delta={'position': "bottom", 'reference': new_df.loc[dropdown,'previousClose']},
#         # domain={'x': [0, 1], 'y': [0, 0.5]}
#     ))

#     fig.update_layout(paper_bgcolor=paper_bgcolor2)

#     return fig



# def current_indicator_right(dropdown):
#     fig = go.Figure(go.Indicator(
#         mode="number+delta",
#         value= new_crypto_df.loc[dropdown,'currentPrice'],  # Assuming df is defined somewhere before this function
#         number={'prefix': "$", "font":{"size":20}},
#         title= {'text': "Current Price", "font":{"size":indicator_title_text_size}},
#         delta={'position': "bottom", 'reference': new_crypto_df.loc[dropdown, 'previousClose']},
#         # domain={'x': [0, 1], 'y': [0, 1]}
#     ))

#     fig.update_layout(paper_bgcolor=paper_bgcolor)

#     return fig



def data_table(dropdown):
    rowEvenColor = 'lightgrey'
    rowOddColor = 'white'

    fig = go.Figure(data=[go.Table(
 
   header=dict(
    line_color='white',
    fill_color='white',
    align=['left','center'],
    font=dict(color='white', size=12)
  ),

    cells=dict(
        values=[
        ['<b>Open</b>',             '<b>Day High</b>',           '<b>Day Low</b>',              '<b>Previous Close</b>', '<b>Market Cap</b>'],
        ["${:,.2f}".format(new_df.loc[dropdown, 'open']), "${:,.2f}".format(new_df.loc[dropdown, 'dayHigh']), "${:,.2f}".format(new_df.loc[dropdown, 'dayLow']), 
        "${:,.2f}".format(new_df.loc[dropdown, 'previousClose']), "${:,.2f}".format(new_df.loc[dropdown, 'marketCap'])],
        ['<b>Fifty Day Avg</b>',     '<b>Fifty-two Week Low</b>', '<b>Fifty-two Week High</b>',  '<b>PEG Ratio</b>',  '<b>Dividend Yield</b>'],
        ["${:,.2f}".format(new_df.loc[dropdown, 'fiftyDayAverage']), "${:,.2f}".format(new_df.loc[dropdown, 'fiftyTwoWeekLow']),
        "${:,.2f}".format(new_df.loc[dropdown, 'fiftyTwoWeekHigh']), new_df.loc[dropdown, 'pegRatio'],  new_df.loc[dropdown, 'dividendYield']]],
        line_color='white',
        # 2-D list of colors for alternating rows
        fill_color = [[rowOddColor,rowEvenColor,rowOddColor, rowEvenColor,rowOddColor]*5],
        align = ['center'],
        font = dict(color = 'black', size = 12)
        ))

    ])
    fig.update_layout(paper_bgcolor=paper_bgcolor, margin=dict(t=5, r=5,b=5, l=5 ),
    width=600,height=1000) # margin=dict( t=20, b=0))
    
    return fig
    # fig.show()

def data_table2(dropdown):
    rowEvenColor = 'lightgrey'
    rowOddColor = 'white'

    fig = go.Figure(data=[go.Table(
 
   header=dict(
    line_color='white',
    fill_color='white',
    align=['left','center'],
    font=dict(color='white', size=12)
  ),

    cells=dict(
        values=[
        ['<b>Open</b>',             '<b>Day High</b>',           '<b>Day Low</b>',              '<b>Volume</b>', '<b>Market Cap</b>'],
        ["${:,.2f}".format(new_crypto_df.loc[dropdown, 'open']), "${:,.2f}".format(new_crypto_df.loc[dropdown, 'dayHigh']), "${:,.2f}".format(new_crypto_df.loc[dropdown, 'dayLow']), 
         "${:,.2f}".format(new_crypto_df.loc[dropdown, 'volume']), "${:,.2f}".format(new_crypto_df.loc[dropdown, 'marketCap'])],
        ['<b>Fifty Day Avg</b>',     '<b>Fifty-two Week Low</b>', '<b>Fifty-two Week High</b>',  '<b>Max Supply</b>',  '<b>Circulating Supply</b>'],
        ["${:,.2f}".format(new_crypto_df.loc[dropdown, 'fiftyDayAverage']), "${:,.2f}".format(new_crypto_df.loc[dropdown, 'fiftyTwoWeekLow']),
          "${:,.2f}".format(new_crypto_df.loc[dropdown, 'fiftyTwoWeekHigh']), new_crypto_df.loc[dropdown, 'maxSupply'],  new_crypto_df.loc[dropdown, 'circulatingSupply']]],

        fill_color = [[rowOddColor,rowEvenColor,rowOddColor, rowEvenColor,rowOddColor]*5],
        align = ['center'],
        font = dict(color = 'black', size = 12)
        ))

    ])
    fig.update_layout(paper_bgcolor=paper_bgcolor, margin=dict(t=5, r=5,b=5, l=5 ),
    width=600,height=1000) # margin=dict( t=20, b=0))

    return fig

    