# Program Title: Stock Price Analyzer using Pandas and Moving Averages
# Author: Lydia S. Makiwa
# Date: June 5, 2026
# Description: This program simulates historical stock prices, calculates
#              20-day and 50-day Simple Moving Averages (SMA), computes
#              daily returns, and detects MA crossover buy/sell signals.
#              Great for AIML students entering quantitative finance.

import numpy as np
import pandas as pd

# 1. Simulating Stock Price Data (Geometric Brownian Motion)
def simulate_stock_prices(ticker, days=100, start_price=150.0, seed=42):
    np.random.seed(seed)
    # Daily returns: mean = 0.0005, std = 0.015
    daily_returns = np.random.normal(0.0005, 0.015, days)
    price_paths = start_price * np.exp(np.cumsum(daily_returns))
    dates = pd.date_range(end='2026-06-05', periods=days)
    df = pd.DataFrame({'Close': price_paths}, index=dates)
    return df

# 2. Calculate Technical Indicators
def analyze_stock(df):
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    df['Daily_Return'] = df['Close'].pct_change()
    
    # Generate Buy/Sell Signals (MA Crossover)
    # Buy when SMA_20 > SMA_50 (Golden Cross)
    # Sell when SMA_20 < SMA_50 (Death Cross)
    df['Signal'] = 0.0
    df['Signal'] = np.where(df['SMA_20'] > df['SMA_50'], 1.0, -1.0)
    df['Position'] = df['Signal'].diff()
    return df

# 3. Running demo
if __name__ == "__main__":
    print("=== Stock Price Analyzer Demo ===")
    ticker = "AAPL"
    df = simulate_stock_prices(ticker, days=100, start_price=150.0)
    analyzed_df = analyze_stock(df)
    
    print(f"\nAnalyzing synthetic stock data for {ticker} over last 100 days:")
    print(analyzed_df.tail(10))
    
    # Find buy/sell trigger points
    buys = analyzed_df[analyzed_df['Position'] == 2.0]
    sells = analyzed_df[analyzed_df['Position'] == -2.0]
    
    print("\n--- Detected Trading Signals ---")
    print(f"Buy triggers (SMA_20 crossed above SMA_50):")
    for date, row in buys.iterrows():
        print(f"  Date: {date.strftime('%Y-%m-%d')} at Price: ${row['Close']:.2f}")
    
    print(f"\nSell triggers (SMA_20 crossed below SMA_50):")
    for date, row in sells.iterrows():
        print(f"  Date: {date.strftime('%Y-%m-%d')} at Price: ${row['Close']:.2f}")
