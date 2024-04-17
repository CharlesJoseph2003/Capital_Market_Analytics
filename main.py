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

