import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import yfinance as yf
# import pandas as pd

# Define options for dropdown menu
symbols = {
    'AWS': 'AMZN',
    'GCP': 'GOOGL',
    'Azure': 'MSFT',
    'IBM Cloud': 'IBM',
    'Snowflake': 'SNOW'
}

# Initialize Dash app
app = dash.Dash(__name__)

# Define layout of the app
app.layout = html.Div([
    html.H1('Compare Stock Prices'),
    dcc.Dropdown(
        id='symbol-dropdown',
        options=[{'label': key, 'value': value} for key, value in symbols.items()],
        value=['AMZN'],  # Default symbols (AWS)
        multi=True  # Allow multiple selection
    ),
    dcc.Graph(id='stock-comparison-graph')
])

# Define callback to update graph based on dropdown selection
@app.callback(
    Output('stock-comparison-graph', 'figure'),
    [Input('symbol-dropdown', 'value')]
)
def update_graph(selected_symbols):
    if not selected_symbols:
        return {'data': [], 'layout': {'title': 'Select symbols to compare'}}

    data_traces = []

    for symbol in selected_symbols:
        # Fetch historical data using yfinance
        ticker = yf.Ticker(symbol)
        stock_data = ticker.history(period="1y")['Close']

        stock_trace = {
            'x': stock_data.index,
            'y': stock_data.values,
            'type': 'line',
            'name': symbol
        }

        data_traces.append(stock_trace)

    return {
        'data': data_traces,
        'layout': {'title': 'Stock Price Comparison'}
    }

# Run the Dash app if running as main module
if __name__ == '__main__':
    app.run_server(debug=True)
