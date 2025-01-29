import pandas as pd
import yfinance as yf
import numpy as np
import datetime
import matplotlib.pyplot as plt

# Define index components (Sample Stocks & Weights)
index_components = {
    "AAPL": 0.3,  # Apple - 30%
    "MSFT": 0.3,  # Microsoft - 30%
    "GOOGL": 0.2,  # Google - 20%
    "AMZN": 0.2   # Amazon - 20%
}

# Define date range (Past 1 Year)
start_date = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime('%Y-%m-%d')
end_date = datetime.datetime.now().strftime('%Y-%m-%d')

# Fetch historical stock price data
data = yf.download(list(index_components.keys()), start=start_date, end=end_date)['Adj Close']

# Handle missing values (Forward-fill)
data.fillna(method='ffill', inplace=True)

# Normalize prices to start from 100 (Base value)
normalized_data = data / data.iloc[0] * 100

# Calculate Weighted Index
index_values = (normalized_data * pd.Series(index_components)).sum(axis=1)

# Create DataFrame for Index Summary
index_summary = pd.DataFrame({
    'Date': index_values.index,
    'Index Value': index_values.values
})
index_summary.set_index('Date', inplace=True)

# Save Index Summary as CSV
index_summary.to_csv("index_summary.csv")
print("Index Summary saved as 'index_summary.csv'. Open the file to view the data.")

# Fetch corporate actions (Dividends & Stock Splits)
corporate_actions = {}
for ticker in index_components.keys():
    stock = yf.Ticker(ticker)
    splits = stock.splits
    dividends = stock.dividends

    corporate_actions[ticker] = {
        "Stock Splits": splits if not splits.empty else "No splits recorded",
        "Dividends": dividends if not dividends.empty else "No dividends recorded"
    }

# Print Corporate Actions for review
for ticker, actions in corporate_actions.items():
    print(f"\nCorporate Actions for {ticker}:")
    print("Stock Splits:\n", actions["Stock Splits"])
    print("Dividends:\n", actions["Dividends"])

# Plot the Index Performance Over Time
plt.figure(figsize=(12, 6))
plt.plot(index_summary.index, index_summary["Index Value"], label="Index Performance", linewidth=2, color='blue')
plt.xlabel("Date")
plt.ylabel("Index Value")
plt.title("Index Performance Over Time")
plt.legend()
plt.grid()
plt.show()
