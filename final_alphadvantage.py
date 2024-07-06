import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import requests

# Retrieve API key securely from environment variables
API_KEY = os.getenv('ALPHAVANTAGE_API_KEY')

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
        url_stock = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}'
        response_stock = requests.get(url_stock)

        if response_stock.status_code != 200:
            print(f"Error fetching data for {symbol}: {response_stock.status_code}")
            continue

        try:
            data_stock = response_stock.json()['Time Series (Daily)']

            stock_trace = {
                'x': list(data_stock.keys()),
                'y': [float(data_stock[date]['4. close']) for date in data_stock.keys()],
                'type': 'line',
                'name': symbol
            }

            data_traces.append(stock_trace)

        except KeyError:
            print(f"Error: 'Time Series (Daily)' not found for {symbol}")
            continue

    return {
        'data': data_traces,
        'layout': {'title': 'Stock Price Comparison'}
    }

# Run the Dash app if running as main module
if __name__ == '__main__':
    app.run_server(debug=True)
