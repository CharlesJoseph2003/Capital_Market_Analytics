from dash import html
from dash import dcc
import dash_mantine_components as dmc
from StockData import symbols_dict
from CryptoData import crypto_symbols
from CryptoData import crypto_dict
from Crypto_Graphs import tree_map_crypto

# print(symbols_dict)
data=[{'value': key, 'label': value} for key, value in symbols_dict.items()]
value=list(symbols_dict.keys())[1]

# print(data)
# print(value)
# print(crypto_symbols[0])
# print(symbols_list[0])

data = [["5d", "5 Days"], ["1mo", "1 Month"], ['1y', '1 Year'], ['max', 'Max']]

def create_layout_crypto():
    crypto_layout = html.Div(children=[
         dmc.Grid(
                children=[
                dmc.Col(html.Div([
                        html.P("Cryptocurrencies", style={'textAlign': 'center', 'fontSize': 24, 'margin-top': 10,}),
                        dmc.Select(
                                # data=crypto_symbols,
                                 data=[{'value': key, 'label': value} for key, value in crypto_dict.items()],
                                        id='crypto-dropdown', 
                                        value=crypto_symbols[0],
                                        searchable=True,
                                        nothingFound="No options found",
                                        clearable=True,
                                        style={'backgroundColor': 'lightgrey', 'position': 'absolute', 'z-index': '3', 'width': '49%'}    # Specify the desired width}
                                        
                        #dropdown
                        ),

                ]), span='auto'),
                ],
                gutter="sm",
                # style={'margin-bottom': -10}
        ),
                dmc.SimpleGrid(
                        cols=2,
                        spacing='lg',
                        children=[
                                html.Div([
                                     dcc.Interval(
                                        id='interval-component_crypto',
                                        interval=3*1000,  # in milliseconds
                                        n_intervals=0
        ),
                                dcc.Graph(  #current indicator
                                        id='current-crypto',
                                        style={'width': '15vh', 'height': '9vh', 'position': 'absolute', 'z-index': '2', 'margin-left': 65, 'margin-top':40}
                                ),

                                  dmc.RadioGroup( #radio_group
                                        [dmc.Radio(l, value=k) for k, l in data],
                                        id="crypto-time",
                                        value="5d",
                                        # label="Select your favorite framework/library",
                                        size="sm",
                                        mt=10,
                                        style={'margin-left':200, 'margin-top': 40, 'position': 'absolute', 'z-index': '2'}
                                ),
                                ]),
        ]
        ),



        dmc.SimpleGrid(
        cols=2,
        spacing='xs',
        children=[
                html.Div([         
                        dcc.Graph(  #scatter plot
                                id='scatter-crypto'
                        ),
  
                ],style={'width': '100%', 'height': '500px','margin-bottom':-100, 'z-index': '1', 'margin-top': 25}),

                html.Div([         
                        dcc.Graph(  #scatter plot
                                id='treemap-crypto',
                                figure = tree_map_crypto()
                        ),
  
                ],style={'width': '100%', 'height': '500px','margin-bottom':-100, 'z-index': '1', 'margin-top': 25}),
        ],
        # style={'width': '50%', 'height': '400px'}
          # style={'display': 'flex', 'justifyContent': 'center'}),
          style={'margin': '0 auto'}
        #   style={ 'margin-bottom': -80,'margin': '0 auto'}

        ),
        # html.Div(style={'margin-bottom': '-70x'}),
   

        dmc.Grid(
                children=[
                dmc.Col(html.Div([
                        dmc.Card(
                        children=[
                                dmc.CardSection(
                                children=[
                               
                                        dmc.SimpleGrid(
                                        cols = 2,
                                        spacing="sm",

                                        children=[
                                                
                                            
                                                dcc.Graph(
                                                id= 'crypto_table-right',
                                                style={'width': '70vh', 'height': '30vh', 'margin': '0 auto', 'z-index': '2'}
                                                ),

                        
                                        ]
                                        )
                                ]
                                )


                        ]
                        

                        ),

                ]), span="auto"),

                ])
    ])
    return crypto_layout