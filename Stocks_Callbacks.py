from Stocks_Graphs import *
from Comparison_Graphs import *
from dash.dependencies import Input, Output, State

def Stocks_Callbacks(app): 
    app.callback(   
    Output("scatter-left_stocks", "figure"),
    Input('left-dropdown_stocks', 'value'),
    Input('left-time_stocks', 'value')
    # prevent_initial_call=True
    
    )(generate_graphs1)

    app.callback(
        Output('table-left_stocks','figure'),
        Input('left-dropdown_stocks', 'value')
    )(data_table)


    app.callback(Output('current-left_stocks', 'figure'),
                Input('interval-component-stocks', 'n_intervals'),
                Input('left-dropdown_stocks', 'value')
    )(update_indicator_stock)



    app.callback(Output('current-DOW', 'figure'),
                Input('Dow-dropdown', 'value')
    )(current_indicator_Dow)


    app.callback(   
        Output("DOW_stock", "figure"),
        Input('Dow-dropdown', 'value'),
        Input('DOW_time-stocks', 'value')
    )(generate_graphs_DOW)


    app.callback(
        Output('table-right_Dow','figure'),
        Input('Dow-dropdown', 'value')
    )(data_table_Index)


    app.callback(
        Output('income_statement_table', 'figure'),
        Input('left-dropdown_stocks', 'value')
    )(income_statement_graph)
