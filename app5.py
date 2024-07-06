import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import requests

API_KEY = 'T2UDKND5LW5VJBOG'

# Define options for dropdown menu
symbols = {
    'AWS': 'AMZN',
    'GCP': 'GOOGL',
    'Azure': 'MSFT',
    'IBM Cloud': 'IBM',
    'Snowflake': 'SNOW'
}

# Create Dash app
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
    # Initialize empty list to store traces for each selected symbol
    data_traces = []

    # Loop through selected symbols and fetch data from AlphaVantage API
    for symbol in selected_symbols:
        url_stock = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}'
        response_stock = requests.get(url_stock)
        data_stock = response_stock.json()['Time Series (Daily)']

        # Prepare trace for each symbol
        stock_trace = {
            'x': list(data_stock.keys()),
            'y': [data_stock[date]['4. close'] for date in data_stock.keys()],
            'type': 'line',
            'name': symbol
        }

        # Append trace to data_traces list
        data_traces.append(stock_trace)

    # Return updated graph figure with all selected symbols
    return {
        'data': data_traces,
        'layout': {
            'title': 'Stock Price Comparison'
        }
    }

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
