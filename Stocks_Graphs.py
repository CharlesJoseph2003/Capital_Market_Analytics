import yfinance as yf
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
from Index import Index_market_metrics
from StockData import treemap
from StockData import market_metrics
from StockData import income_statement_table

_,df_info_result = market_metrics()
new_df = pd.DataFrame(df_info_result)
new_df_2 = new_df.copy()
new_df.set_index('symbol', inplace=True)

_,df_info_index = Index_market_metrics()
new_index_df = pd.DataFrame(df_info_index)
new_index_df.set_index('symbol', inplace=True)
# print(new_index_df)

df_info_treemap = treemap()
new_treemap_df = pd.DataFrame(df_info_treemap)
# print('new_treemap2',new_treemap_df)
new_treemap_df_2 = new_treemap_df[['symbol','sector','delta','marketCap']].copy()
color_group = [-1,-0.02,-0.01,0, 0.01, 0.02,1]
new_treemap_df_2['colors'] = pd.cut(new_treemap_df['delta'], bins=color_group, labels=['red','indianred','forestgreen','lightgreen','lime','green'])

incomestatement = income_statement_table()



indicator_title_text_size = 15
paper_bgcolor = 'white'
paper_bgcolor2 = 'white'

def generate_graphs_DOW(dropdown,time): 
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
    

    fig.update_yaxes(visible=True, secondary_y=True, )
    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.0,xanchor="right",x=1))

    fig.update_xaxes(showspikes=True, spikecolor="black", spikesnap="cursor", spikemode="across", tickangle = 0,)
    fig.update_yaxes(showspikes=True, spikecolor="black", spikethickness=2)
    fig.update_layout(spikedistance=1000, hoverdistance=100)
    fig.update_layout(showlegend=True, paper_bgcolor=paper_bgcolor)
    return fig


def data_table_Index(dropdown):
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
        ['<b>Open</b>',             '<b>Day High</b>',           '<b>Day Low</b>',              '<b>Previous Close</b>',],
        ["${:,.2f}".format(new_index_df.loc[dropdown, 'open']), "${:,.2f}".format(new_index_df.loc[dropdown, 'dayHigh']), "${:,.2f}".format(new_index_df.loc[dropdown, 'dayLow']), 
         "${:,.2f}".format(new_index_df.loc[dropdown, 'previousClose'])],
        ['<b>Fifty Day Avg</b>',     '<b>Fifty-two Week Low</b>', '<b>Fifty-two Week High</b>', '<b>Two-Hundred Day</b>'],
        ["${:,.2f}".format(new_index_df.loc[dropdown, 'fiftyDayAverage']), "${:,.2f}".format(new_index_df.loc[dropdown, 'fiftyTwoWeekLow']), 
         "${:,.2f}".format(new_index_df.loc[dropdown, 'fiftyTwoWeekHigh']), "${:,.2f}".format(new_index_df.loc[dropdown, 'twoHundredDayAverage'])]],
        # 2-D list of colors for alternating rows
      
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


def current_indicator_left_stock(dropdown):
    stock_data = market_metrics()[0].loc[market_metrics()[0]['symbol'] == dropdown]
    # print(stock_data)
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


def update_indicator_stock(n, dropdown):
    return current_indicator_left_stock(dropdown)



def current_indicator_Dow(dropdown):
    Index_data = Index_market_metrics()[0].loc[Index_market_metrics()[0]['symbol'] == dropdown]
    # print(Index_data)
    fig = go.Figure(go.Indicator(
        mode="number+delta",
        value=Index_data['open'].iloc[0],  # Assuming df is defined somewhere before this function
        number={"font":{"size":20}, 'valueformat': '.2f'},
        title= {'text': "Opening Index", "font":{"size":indicator_title_text_size}},
        delta={'position': "bottom", 'reference': Index_data['previousClose'].iloc[0]},
        # domain={'x': [0, 1], 'y': [0, 0.5]}
    ))

    fig.update_layout(paper_bgcolor=paper_bgcolor2)

    return fig

def tree_map():
    fig = px.treemap(new_treemap_df_2, path=[px.Constant("all"), 'sector','symbol'], values = 'marketCap', color='colors', height=700,
        color_discrete_map ={'(?)':'#bae4f7', 'red':'red', 'indianred':'indianred','gray':'gray', 'lightgreen':'lightgreen','lime':'lime','green':'green'},
        hover_data = {'delta':':.2p'},
        custom_data=['delta','sector'])
    fig.update_traces(
        hovertemplate="<br>".join([
        "Stock: %{label}",
        "Market Cap(M): %{value}",
        "Delta: %{customdata[0]:.2p}",
        "Sector: %{customdata[1]}",
        ])
    )
    fig.data[0].texttemplate = "<b>%{label}</b><br>%{customdata[0]:.2p}"
    return fig

def income_statement_graph(dropdown):
    selected_row = incomestatement.loc[dropdown]
    selected_row = selected_row.transpose()
    new_row = selected_row.dropna()
    df2 = new_row.transpose()
    rowEvenColor = 'lightgrey'
    rowOddColor = 'white'
    fig = go.Figure(data=[go.Table(
    header=dict(
        values=['']+ list(df2.columns),
        line_color='white',
        fill_color='#bae4f7',
        align=['left', 'center'],
        font=dict(color='white', size=12),
        height=40
    ),
    cells=dict(
        values=[df2.index] + [df2[col].astype(str) for col in df2.columns],
        line_color='white',
        fill_color = [[rowOddColor,rowEvenColor]*len(df2.index)],
        # fill=dict(color=['#bae4f7'] * len(df2.index)),
        align=['left'] + ['center'] * len(df2.columns),
        font_size=12,
        height=50)
    )]
    )

    # Update layout for better visibility
    fig.update_layout(
    margin=dict(l=0, r=0, t=0, b=0,),width=600, height=1000

    )
    return fig



