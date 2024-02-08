import yfinance as yf
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
from Index import Index_market_metrics
from StockData import treemap
from StockData import market_metrics
from StockData import income_statement_table
from CryptoData import treemap_crypto


df_info_treemap = treemap_crypto()
new_treemap_df = pd.DataFrame(df_info_treemap)
# print('new_treemap2',new_treemap_df)
new_treemap_df_2 = new_treemap_df[['symbol','marketCap']].copy()
color_group = [-1,-0.02,-0.01,0, 0.01, 0.02,1]
# new_treemap_df_2['colors'] = pd.cut(new_treemap_df['delta'], bins=color_group, labels=['red','indianred','forestgreen','lightgreen','lime','green'])

def tree_map_crypto():
    fig = px.treemap(new_treemap_df_2, path=[px.Constant("all"), 'symbol'], values = 'marketCap', height=700,
        hover_data = {'marketCap'})
        # custom_data=['delta','sector'])
    fig.update_traces(
        hovertemplate="<br>".join([
        "Stock: %{label}",
        "Market Cap(M): %{value}",
        ])
    )
    fig.data[0].texttemplate = "<b>%{label}</b><br>%{customdata[0]}"
    # fig.show()
    return fig
tree_map_crypto()