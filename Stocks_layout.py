from dash import html
from dash import dcc
import dash_mantine_components as dmc
from StockData import symbols_list
from StockData import symbols_dict
from Index import index_list
from Index import index_dict
from Stocks_Graphs import tree_map
# print(symbols_dict)
data=[{'value': key, 'label': value} for key, value in symbols_dict.items()]
value=list(symbols_dict.keys())[1]

data = [["5d", "5 Days"], ["1mo", "1 Month"], ['1y', '1 Year'], ['max', 'Max']]

def create_layout_stocks():
    stock_layout = html.Div(children=[
        dmc.Grid(
                children=[
                dmc.Col(html.Div([
                        html.P("Stocks",  style={'textAlign': 'center', 'fontSize': 24, 'margin-top': 10}),


                        dmc.Select(
                                # data=symbols_list, 
                                data=[{'value': key, 'label': value} for key, value in symbols_dict.items()],
                                        value=symbols_list[0],
                                        id='left-dropdown_stocks',
                                        searchable=False,
                                        nothingFound="No options found",
                                        clearable=False,
                                        style={'backgroundColor': 'lightgrey', 'position': 'absolute', 'z-index': '3', 'height': 'auto', 'width': '49%'}

                                
                        ),


                ]), span="auto"),



                dmc.Col(html.Div([
                        html.P("Index", style={'textAlign': 'center', 'fontSize': 24, 'margin-top': 10,}),
                        dmc.Select(
                                # data=crypto_symbols,
                                 data=[{'value': key, 'label': value} for key, value in index_dict.items()],
                                        id='Dow-dropdown', 
                                        value=index_list[0],
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
                                        id='interval-component-stocks',
                                        interval=3*1000,  # in milliseconds
                                        n_intervals=0
        ),
                                dcc.Graph(
                                        id='current-left_stocks',
                                        style={'width': '15vh', 'height': '9vh', 'position': 'absolute', 'z-index': '2', 'margin-left': 65, 'margin-top':40}
                                ),
                                
                                dmc.RadioGroup(
                                        [dmc.Radio(l, value=k) for k, l in data],
                                        id="left-time_stocks",
                                        value="5d",
                                        # label="Select your favorite framework/library",
                                        size="sm",
                                        mt=10,
                                        style={'margin-left':200, 'margin-top': 40, 'position': 'absolute', 'z-index': '2'}
                                ),

                                ]),
                                
                                html.Div([
                                dcc.Graph(
                                        id='current-DOW',
                                        style={'width': '15vh', 'height': '9vh', 'position': 'absolute', 'z-index': '2', 'margin-left': 65, 'margin-top':40}
                                ),

                                  dmc.RadioGroup(
                                        [dmc.Radio(l, value=k) for k, l in data],
                                        id="DOW_time-stocks",
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
                                id='scatter-left_stocks'
                        ),

                ],style={'width': '100%', 'height': '500px','margin-bottom':-100, 'z-index': '1', 'margin-top': 25}),

                html.Div([         
                        dcc.Graph(
                                id='DOW_stock'
                        ),
  
                ],style={'width': '100%', 'height': '500px','margin-bottom':-100, 'z-index': '1', 'margin-top': 25}),
        ],

          style={'margin': '0 auto'}

        ),
   

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
                                                id= 'table-left_stocks',
                                                style={'width': '70vh', 'height': '30vh','margin': '0 auto', 'z-index': '2', }
                                                #'margin': '0 auto',
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
                                                id= 'table-right_Dow',
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
        gutter="sm",
        ),
        
        dmc.SimpleGrid(
        cols=2,
        spacing='xs',
        children=[
                html.Div([
                        dcc.Graph(
                                id='income_statement_table'
                                
                        ),

                ],style={'width': '100%', 'height': '500px','margin-top':15, 'z-index': '3', 'margin-left': 100}),

                html.Div([         
                        dcc.Graph(
                                
                                id='tree_map',
                                figure = tree_map()
                        ),
  
                ],style={'width': '100%', 'height': '500px','margin-top':-50, 'z-index': '3', 'margin-right': -200}),
        ],

          style={'margin-top':-50,'margin': '0 auto'}

        ),



    ])
    return stock_layout