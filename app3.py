import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import requests

API_KEY = 'T2UDKND5LW5VJBOG'
symbol = 'AAPL'  # Example stock symbol
url_ma = f'https://www.alphavantage.co/query?function=SMA&symbol={symbol}&interval=daily&time_period=10&series_type=open&apikey={API_KEY}'
url_stock = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}'

response_ma = requests.get(url_ma)
data_ma = response_ma.json()['Technical Analysis: SMA']

response_stock = requests.get(url_stock)
data_stock = response_stock.json()['Time Series (Daily)']

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1(f'Stock Prices and SMA for {symbol}'),
    dcc.Graph(
        id='stock-sma-graph',
        figure={
            'data': [
                {
                    'x': list(data_stock.keys()),
                    'y': [data_stock[date]['4. close'] for date in data_stock.keys()],
                    'type': 'line',
                    'name': symbol
                },
                {
                    'x': list(data_ma.keys()),
                    'y': [float(data_ma[date]['SMA']) for date in data_ma.keys()],
                    'type': 'line',
                    'name': 'SMA'
                }
            ],
            'layout': {
                'title': f'{symbol} Stock Price and SMA'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
