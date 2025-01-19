#!/usr/bin/env python
# coding: utf-8

# In[151]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
from io import StringIO
import yfinance as yf
import os


# In[152]:


pwd = os.getcwd()
print(f"Present working directory: {pwd}")


# In[153]:


# Scrape the S&P 500 tickers from Wikipedia
def get_sp500_tickers():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = requests.get(url).text  # Fetch the HTML content of the page
    dfs = pd.read_html(StringIO(html))  # Wrap the HTML in StringIO to pass to read_html
    tickers = dfs[0]['Symbol'].tolist()  # Extract the 'Symbol' column
    return tickers

# Get the list of S&P 500 tickers
tickers = get_sp500_tickers()

# Limit to the first 50 tickers
tickers = tickers[:50]

# Print the list of tickers
print(tickers)


# In[154]:


import yfinance as yf
import os

# Get current directory and define folder path
folder_path = os.path.join(os.getcwd(), "saved_ticker_data_folder")

# Create directory if it doesn't exist (using makedirs with exist_ok=True)
os.makedirs(folder_path, exist_ok=True)
print("Folder:", folder_path)

saved_file_arr = []

# Download and save data for each ticker
for i in tickers:
    data = yf.download(i, period='1y', interval='1d')
    data.columns = [col[0] for col in data.columns]
    save_path = os.path.join(folder_path, f"{i}_Candlestick_data.csv")
    data.to_csv(save_path)
    saved_file_arr.append(save_path)
    print(f"Data for {i} saved at {save_path}")


# In[165]:


class BollingerBandBacktester:
    def __init__(self, data, investment_per_trade=100):
        self.data = data
        self.investment_per_trade = investment_per_trade
        self.trades = []
        self.positions = []

    def calculate_bollinger_bands(self, window=20, num_std_dev=2):
        self.data['MA'] = self.data['Close'].rolling(window=window).mean()
        self.data['STD'] = self.data['Close'].rolling(window=window).std()
        self.data['UpperBand'] = self.data['MA'] + (num_std_dev * self.data['STD'])
        self.data['LowerBand'] = self.data['MA'] - (num_std_dev * self.data['STD'])

    def simulate_trades(self):
        entry_date = None
        buy_price = None
        tokens_bought = None

        for index, row in self.data.iterrows():
            price = row['Close']
            lower_band = row['LowerBand']
            upper_band = row['UpperBand']

            # Check for buy condition (price falls 3% below lower band)
            if price < 0.97 * lower_band and not self.positions:
                tokens_bought = self.investment_per_trade / price
                self.positions.append(tokens_bought)
                entry_date = index
                buy_price = price

            # Check for sell condition (price touches upper band)
            elif price >= upper_band and self.positions:
                tokens_sold = sum(self.positions)
                sell_price = price
                profit = (sell_price - buy_price) * tokens_sold
                profit_percentage = (profit / (buy_price * tokens_sold)) * 100

                self.trades.append({
                    'token': None,
                    'date_in': entry_date,
                    'buy_price': round(buy_price, 2),
                    'date_out': index,
                    'sell_price': round(sell_price, 2),
                    'profit_percentage': round(profit_percentage, 2)
                })

                self.positions.clear()

        # Sell remaining positions at the end of the period
        if self.positions:
            final_price = self.data['Close'].iloc[-1]
            tokens_sold = sum(self.positions)
            sell_price = final_price
            profit = (sell_price - buy_price) * tokens_sold
            profit_percentage = (profit / (buy_price * tokens_sold)) * 100

            self.trades.append({
                'token': None,
                'date_in': entry_date,
                'buy_price': round(buy_price, 2),
                'date_out': self.data.index[-1],
                'sell_price': round(sell_price, 2),
                'profit_percentage': round(profit_percentage, 2)
            })

            self.positions.clear()

    def run_backtest(self, token):
        self.calculate_bollinger_bands()
        self.simulate_trades()
        for trade in self.trades:
            trade['token'] = token
        return self.trades


def backtest_all_stocks(file_paths, investment_per_trade=100):
    all_trades = []

    for file_path in file_paths:
        ticker = file_path.split('\\')[-1].split('_')[0]
        data = pd.read_csv(file_path, index_col='Date', parse_dates=True)
        backtester = BollingerBandBacktester(data, investment_per_trade)
        trades = backtester.run_backtest(ticker)
        all_trades.extend(trades)

    trades_df = pd.DataFrame(all_trades)
    return trades_df



trades_df = backtest_all_stocks(saved_file_arr)
trades_df = trades_df[['token', 'date_in', 'buy_price', 'date_out', 'sell_price', 'profit_percentage']]
trades_df.to_csv("backtest_results.csv", index=False)
print(f"Results .csv file is saved in {pwd}\\backtest_results.csv")

