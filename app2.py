import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import requests

API_KEY = 'T2UDKND5LW5VJBOG'
symbol = 'AAPL'  # Example stock symbol
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={API_KEY}'

response = requests.get(url)
data = response.json()['Time Series (5min)']

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1(f'Intraday Stock Prices for {symbol}'),
    dcc.Graph(
        id='intraday-stock-graph',
        figure={
            'data': [{
                'x': list(data.keys()),
                'y': [data[date]['4. close'] for date in data.keys()],
                'type': 'line',
                'name': symbol
            }],
            'layout': {
                'title': f'{symbol} Intraday Stock Price'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
