import time
import random
import pandas as pd
import numpy as np
from flask import Flask
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

server = Flask(__name__)

app = dash.Dash(__name__, server=server)

df = pd.DataFrame(columns=["Timestamp", "Stock Price"])
start_time = pd.Timestamp.now()

app.layout = html.Div([
    html.H1("Real-Time Stock Price Tracker", style={'textAlign': 'center'}),
    dcc.Graph(id='live-graph', style={"height": "70vh"}),
    dcc.Interval(id='interval-component', interval=1000, n_intervals=0)  
])

def get_live_data():
    global df
    new_time = pd.Timestamp.now()
    new_price = round(100 + np.sin(time.time()) * 5 + random.uniform(-2, 2), 2)  
    new_data = pd.DataFrame({"Timestamp": [new_time], "Stock Price": [new_price]})
    df = pd.concat([df, new_data]).tail(100)  
    return df

@app.callback(Output('live-graph', 'figure'), Input('interval-component', 'n_intervals'))
def update_graph(n):
    data = get_live_data()
    fig = {
        'data': [{
            'x': data["Timestamp"],
            'y': data["Stock Price"],
            'type': 'line',
            'mode': 'lines+markers',
            'name': 'Stock Price'
        }],
        'layout': {
            'title': 'Live Stock Price Data',
            'xaxis': {'title': 'Time'},
            'yaxis': {'title': 'Price (USD)'},
        }
    }
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
