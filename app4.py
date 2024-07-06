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
    html.H1('Stock Prices and SMA'),
    dcc.Dropdown(
        id='symbol-dropdown',
        options=[{'label': key, 'value': value} for key, value in symbols.items()],
        value='AMZN',  # Default symbol (AWS)
        clearable=False
    ),
    dcc.Graph(id='stock-sma-graph')
])

# Define callback to update graph based on dropdown selection
@app.callback(
    Output('stock-sma-graph', 'figure'),
    [Input('symbol-dropdown', 'value')]
)
def update_graph(symbol):
    # Fetch data from AlphaVantage API based on selected symbol
    url_ma = f'https://www.alphavantage.co/query?function=SMA&symbol={symbol}&interval=daily&time_period=10&series_type=open&apikey={API_KEY}'
    url_stock = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}'

    response_ma = requests.get(url_ma)
    data_ma = response_ma.json()['Technical Analysis: SMA']

    response_stock = requests.get(url_stock)
    data_stock = response_stock.json()['Time Series (Daily)']

    # Prepare data for graph
    stock_trace = {
        'x': list(data_stock.keys()),
        'y': [data_stock[date]['4. close'] for date in data_stock.keys()],
        'type': 'line',
        'name': symbol
    }

    sma_trace = {
        'x': list(data_ma.keys()),
        'y': [float(data_ma[date]['SMA']) for date in data_ma.keys()],
        'type': 'line',
        'name': 'SMA'
    }

    # Return updated graph figure
    return {
        'data': [stock_trace, sma_trace],
        'layout': {
            'title': f'{symbol} Stock Price and SMA'
        }
    }

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
