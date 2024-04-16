import pandas as pd
import plotly.express as px
from CryptoData import treemap_crypto


df_info_treemap = treemap_crypto()
new_treemap_df = pd.DataFrame(df_info_treemap)
new_treemap_df_2 = new_treemap_df[['symbol','marketCap']].copy()
color_group = [-1,-0.02,-0.01,0, 0.01, 0.02,1]

def tree_map_crypto():
    fig = px.treemap(new_treemap_df_2, path=[px.Constant("all"), 'symbol'], values = 'marketCap', height=700,
        hover_data = {'marketCap'})
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