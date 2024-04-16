from dash import html
import dash_mantine_components as dmc
from Stocks_layout import create_layout_stocks
from Comparison_layout import create_layout_comparison
from Crypto_layout import create_layout_crypto

def create_layout():
    layout1 = html.Div(children=[
        html.H1(children='Capital Market Analytics', style={'textAlign': 'center'}),


    dmc.Tabs( 
    [
        dmc.TabsList(
            
            [
                dmc.Tab("Comparison", value="comparison"),
                dmc.Tab("Stocks", value="stocks"),
                dmc.Tab("Crypto", value="crypto"),
            ],
            position="center",
            grow=True,
        ),
        dmc.TabsPanel([create_layout_comparison()], value="comparison"),
        dmc.TabsPanel([create_layout_stocks()] , value='stocks'),
        dmc.TabsPanel([create_layout_crypto()], value='crypto'),
    ],
    color="blue",
    orientation="horizontal",
    value= 'comparison'
),

    ])
        

    return layout1
