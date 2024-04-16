from Stocks_Graphs import *
from Comparison_Graphs import *
from dash.dependencies import Input, Output

def Crypto_Callbacks(app): 

    app.callback(
        Output("scatter-crypto", "figure"),
        Input('crypto-dropdown', 'value'),       #Crypto Scatter Plot
        Input('crypto-time', 'value')
        # prevent_initial_call=True
    )(generate_graphs2)


    app.callback(Output('current-crypto', 'figure'),
                Input('interval-component_crypto', 'n_intervals'), #Crypto Indicator
                Input('crypto-dropdown', 'value')
    )(update_indicator_crypto)

    app.callback(
        Output('crypto_table-right','figure'),         #Crypto Data Table
        Input('crypto-dropdown', 'value')
    )(data_table2)



    # app.callback(
    #     Output()
    # )
        