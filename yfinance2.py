import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import yfinance as yf

# List of cloud computing companies and their stock symbols
companies = {
    'Amazon (AWS)': 'AMZN',
    'Microsoft (Azure)': 'MSFT',
    'Google (GCP)': 'GOOGL',
    'IBM': 'IBM',
    # 'Salesforce': 'CRM',
    'Snowflake': 'SNOW'
}

# Fetch stock data
def get_stock_data(tickers, start_date, end_date):
    data = yf.download(tickers, start=start_date, end=end_date)
    return data['Close']

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    html.H1("Cloud Computing Stock Price Comparison"),
    
    dcc.DatePickerRange(
        id='date-picker',
        start_date='2020-01-01',
        end_date=pd.Timestamp.now().strftime('%Y-%m-%d'),
        display_format='YYYY-MM-DD'
    ),
    
    dcc.Dropdown(
        id='company-dropdown',
        options=[{'label': company, 'value': symbol} for company, symbol in companies.items()],
        value=['AMZN', 'MSFT', 'GOOGL'],  # Default selected values
        multi=True
    ),
    
    dcc.Graph(id='stock-price-graph')
])

# Callback to update the graph
@app.callback(
    Output('stock-price-graph', 'figure'),
    [Input('company-dropdown', 'value'),
     Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def update_graph(selected_companies, start_date, end_date):
    df = get_stock_data(selected_companies, start_date, end_date)
    
    traces = []
    for company in selected_companies:
        traces.append(go.Scatter(
            x=df.index,
            y=df[company],
            name=list(companies.keys())[list(companies.values()).index(company)]
        ))
    
    return {
        'data': traces,
        'layout': go.Layout(
            title='Stock Prices Over Time',
            xaxis={'title': 'Date'},
            yaxis={'title': 'Stock Price (USD)'}
        )
    }

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)