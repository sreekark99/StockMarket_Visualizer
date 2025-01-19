import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import webbrowser
from threading import Timer

# Initialize the app
app = dash.Dash(__name__)
df = pd.read_csv("backtest_results.csv", parse_dates=["date_in", "date_out"])

# Create Bar Plot (Profit Percentage by Ticker)
bar_fig = px.bar(df, 
                 x="token", 
                 y="profit_percentage", 
                 title="Profit Percentage by Ticker",
                 labels={"profit_percentage": "Profit Percentage (%)", "token": "Ticker"})
bar_fig.update_layout(
    xaxis_title="Ticker",
    yaxis_title="Profit Percentage (%)",
    template="plotly_dark",
    plot_bgcolor="#212121", 
    paper_bgcolor="#212121",
    font=dict(color="white")
)

# Create Scatter Plot (Buy Price vs Sell Price)
scatter_fig = px.scatter(df, 
                         x="buy_price", 
                         y="sell_price", 
                         color="token", 
                         title="Buy Price vs Sell Price for Each Trade",
                         labels={"buy_price": "Buy Price ($)", "sell_price": "Sell Price ($)"})
scatter_fig.update_layout(
    xaxis_title="Buy Price ($)",
    yaxis_title="Sell Price ($)",
    template="plotly_dark",
    plot_bgcolor="#212121",
    paper_bgcolor="#212121",
    font=dict(color="white")
)

app.layout = html.Div(
    children=[
        # Header
        html.Div(
            children=[
                html.H1(
                    children="Stock Backtest Visualization",
                    style={
                        'textAlign': 'center',
                        'color': '#FFD700',
                        'font-family': 'Arial, sans-serif',
                        'margin-bottom': '30px',
                    }
                ),
            ]
        ),
        
        # Bar Plot Section
        html.Div(
            children=[
                html.H3(
                    "Profit Percentage by Ticker",
                    style={
                        'color': '#FFD700',
                        'font-family': 'Arial, sans-serif',
                        'margin-bottom': '20px',
                    }
                ),
                dcc.Graph(
                    id="bar-plot",
                    figure=bar_fig
                )
            ],
            style={
                'padding': '20px',
                'backgroundColor': '#333333',
                'border-radius': '10px',
                'margin-bottom': '30px'
            }
        ),
        
        # Scatter Plot Section
        html.Div(
            children=[
                html.H3(
                    "Buy Price vs Sell Price for Each Trade",
                    style={
                        'color': '#FFD700',
                        'font-family': 'Arial, sans-serif',
                        'margin-bottom': '20px',
                    }
                ),
                dcc.Graph(
                    id="scatter-plot",
                    figure=scatter_fig
                )
            ],
            style={
                'padding': '20px',
                'backgroundColor': '#333333',
                'border-radius': '10px'
            }
        )
    ],
    style={
        'font-family': 'Arial, sans-serif',
        'backgroundColor': '#212121',
        'color': 'white',
        'padding': '50px',
        'margin': '0',
    }
)

def open_browser():
    webbrowser.open("http://127.0.0.1:8050/")

Timer(1, open_browser).start()
app.run_server(debug=True, use_reloader=False)
