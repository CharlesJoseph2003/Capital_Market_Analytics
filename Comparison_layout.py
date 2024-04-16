from dash import html
from dash import dcc
import dash_mantine_components as dmc
from StockData import symbols_list
from StockData import symbols_dict
from CryptoData import crypto_symbols
from CryptoData import crypto_dict
# print(symbols_dict)
data=[{'value': key, 'label': value} for key, value in symbols_dict.items()]
value=list(symbols_dict.keys())[1]

# print(data)
# print(value)
# print(crypto_symbols[0])
# print(symbols_list[0])

data = [["5d", "5 Days"], ["1mo", "1 Month"], ['1y', '1 Year'], ['max', 'Max']]


def create_layout_comparison():
    comparison_layout = html.Div(children=[
        # dcc.Interval(
        #         id='interval-component',
        #         interval=1*100,  # in milliseconds
        #         n_intervals=0
        # ),
         dmc.Grid(
                children=[
                dmc.Col(html.Div([
                        html.P("Stocks",  style={'textAlign': 'center', 'fontSize': 24, 'margin-top': 10}),


                        dmc.Select(
                                # data=symbols_list, 
                                data=[{'value': key, 'label': value} for key, value in symbols_dict.items()],
                                        value=symbols_list[0],
                                        id='left-dropdown',
                                        searchable=False,
                                        nothingFound="No options found",
                                        clearable=False,
                                        style={'backgroundColor': 'lightgrey', 'position': 'absolute', 'z-index': '3', 'height': 'auto', 'width': '49%'}
                                # data=[{'value': key, 'label': value} for key, value in symbols_dict.items()],
                                # id =  'left-dropdown',
                                # value=list(symbols_dict.keys())[0],
                        
                                
                        ),
                        # dcc.Graph(
                        #         id= 'current-left',
                        #         style={'width': '15vh', 'height': '10vh'}),


                ]), span="auto"),



                dmc.Col(html.Div([
                        html.P("Cryptocurrencies", style={'textAlign': 'center', 'fontSize': 24, 'margin-top': 10,}),
                        dmc.Select(
                                # data=crypto_symbols,
                                 data=[{'value': key, 'label': value} for key, value in crypto_dict.items()],
                                        id='right-dropdown', 
                                        value=crypto_symbols[0],
                                        searchable=False,
                                        nothingFound="No options found",
                                        clearable=False,
                                        style={'backgroundColor': 'lightgrey', 'position': 'absolute', 'z-index': '3', 'width': '49%'}    # Specify the desired width}
                                        
                        
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
                                        id='interval-component',
                                        interval=3*1000,  # in milliseconds
                                        n_intervals=0
        ),
                                dcc.Graph(
                                        id='current-left',
                                        style={'width': '15vh', 'height': '9vh', 'position': 'absolute', 'z-index': '2', 'margin-left': 65, 'margin-top':40}
                                ),
                                
                                dmc.RadioGroup(
                                        [dmc.Radio(l, value=k) for k, l in data],
                                        id="left-time",
                                        value="5d",
                                        # label="Select your favorite framework/library",
                                        size="sm",
                                        mt=10,
                                        style={'margin-left':200, 'margin-top': 40, 'position': 'absolute', 'z-index': '2'}
                                ),

                                ]),
                                
                                html.Div([
                                dcc.Graph(
                                        id='current-right',
                                        style={'width': '15vh', 'height': '9vh', 'position': 'absolute', 'z-index': '2', 'margin-left': 65, 'margin-top':40}
                                ),

                                  dmc.RadioGroup(
                                        [dmc.Radio(l, value=k) for k, l in data],
                                        id="right-time",
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
                        dcc.Graph(
                                id='scatter-left'
                        ),

                ],style={'width': '100%', 'height': '500px','margin-bottom':-100, 'z-index': '1', 'margin-top': 25}),

                html.Div([         
                        dcc.Graph(
                                id='scatter-right'
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
                                        cols = 1,
                                        spacing="sm",

                                        children=[
                                                
                                            
                                                dcc.Graph(
                                                id= 'table-left',
                                                style={'width': '70vh', 'height': '30vh', 'margin': '0 auto', 'z-index': '2'}
                                                ),

                        
                                        ]
                                        )
                                ]
                                )


                        ]
                        

                        ),

                ]), span="auto"),


                dmc.Col(html.Div([
                        dmc.Card(
                        children=[
                                dmc.CardSection(
                                children=[
  
                                        dmc.SimpleGrid(
                                        cols = 1,
                                        spacing="sm",

                                        children=[
                                                dcc.Graph(
                                                id= 'table-right',
                                                style={'width': '70vh', 'height': '30vh', 'margin': '0 auto 0 auto', 'z-index': '2'}

                                                ),


                                        ]
                                        )
                                ]
                                )


                        ]
                        

                        ),
                        

                ]), span='auto'),
                ],
        # gutter="sm",
        ),

    ]
    )
    return comparison_layout