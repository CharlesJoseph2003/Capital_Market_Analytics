from Stocks_Graphs import *
from Comparison_Graphs import *
from dash.dependencies import Input, Output

def Comparison_Callbacks(app):

    app.callback(   
        Output("scatter-left", "figure"),
        Input('left-dropdown', 'value'),        #Stock Scatter Plot
        Input('left-time', 'value')
        # prevent_initial_call=True
        
    )(generate_graphs1)

    app.callback(
        Output("scatter-right", "figure"),
        Input('right-dropdown', 'value'),       #Crypto Scatter Plot
        Input('right-time', 'value')
        # prevent_initial_call=True

    )(generate_graphs2)
        
        
    app.callback(
        Output('table-left','figure'),
        Input('left-dropdown', 'value')         #Stock Data Table
    )(data_table)


    app.callback(
        Output('table-right','figure'),         #Crypto Data Table
        Input('right-dropdown', 'value')
    )(data_table2)


#CURRENT INDICATORS----------------------------------------------------------

    app.callback(Output('current-left', 'figure'),
                Input('interval-component', 'n_intervals'), #Stock Indicator
                Input('left-dropdown', 'value')
    )(update_indicator)

    app.callback(Output('current-right', 'figure'),
                Input('interval-component', 'n_intervals'), #Crypto Indicator
                Input('right-dropdown', 'value')
    )(update_indicator_crypto)
