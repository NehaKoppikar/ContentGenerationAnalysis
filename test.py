import requests

API_KEY = 'T2UDKND5LW5VJBOG'
symbol = 'AAPL'  # Example stock symbol
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}'

response = requests.get(url)
data = response.json()['Time Series (Daily)']

print(data)