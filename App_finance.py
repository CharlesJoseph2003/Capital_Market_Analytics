import dash
from Stocks_Graphs import *
from Comparison_Graphs import *
from App_layout import create_layout
from Comparison_Callbacks import Comparison_Callbacks
from Stocks_Callbacks import Stocks_Callbacks
from Crypto_Callbacks import Crypto_Callbacks


app = dash.Dash(__name__)

layout = create_layout()

app.layout = layout  # Set the initial layout

Comparison_Callbacks(app)
Stocks_Callbacks(app)
Crypto_Callbacks(app)


if __name__ == '__main__':
    app.run_server(debug=True)


# app.callback(
#     Output("current-right", "figure"),
#     Input('right-dropdown', 'value'),
# )(current_indicator_right)

# #MARKETCAP-------------------------------------------------------------------
# app.callback(
#     Output("marketCap-left", "figure"),
#     Input('left-dropdown', 'value'),
# )(marketCap_indicator_left)


# app.callback(
#     Output("marketCap-right", "figure"),
#     Input('right-dropdown', 'value'),
# )(marketCap_indicator_right)

# #PREVIOUSCLOSE-----------------------------------------------------------------

# app.callback(
#     Output("prevClose-left", "figure"),
#     Input('left-dropdown', 'value'),
# )(previousClose_indicator_left)


# app.callback(
#     Output("prevClose-right", "figure"),
#     Input('right-dropdown', 'value'),
# )(previousClose_indicator_right)

# #VOLUME-------------------------------------------------------------------------
# app.callback(
#     Output("volume-left", "figure"),
#     Input('left-dropdown', 'value'),
# )(volume_indicator_left)


# app.callback(
#     Output("volume-right", "figure"),
#     Input('right-dropdown', 'value'),
# )(volume_indicator_right)


# #FIFTYDAYAVERAGE---------------------------------------------------------------
# app.callback(
#     Output("fiftydayaverage-left", "figure"),
#     Input('left-dropdown', 'value'),
# )(fiftyDayAverage_indicator_left)


# app.callback(
#     Output("fiftydayaverage-right", "figure"),
#     Input('right-dropdown', 'value'),
# )(fiftyDayAverage_indicator_right)



