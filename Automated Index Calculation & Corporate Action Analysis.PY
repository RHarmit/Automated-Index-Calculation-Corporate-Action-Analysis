import pandas as pd
import yfinance as yf
import numpy as np
import datetime
import plotly.graph_objects as go

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

# Fetch historical stock price data (including Adjusted Close)
data = yf.download(list(index_components.keys()), start=start_date, end=end_date, auto_adjust=False)

# Use Adjusted Close prices
adj_close_data = data['Adj Close']

# Handle missing values (Forward-fill)
adj_close_data.fillna(method='ffill', inplace=True)

# Normalize prices to start from 100 (Base value)
normalized_data = adj_close_data / adj_close_data.iloc[0] * 100

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

# Plot the Index Performance Over Time using Plotly
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=index_summary.index,
    y=index_summary["Index Value"],
    mode='lines',
    name='Index Performance'
))

# Add range slider for interactivity
fig.update_layout(
    title="Index Performance Over Time",
    xaxis_title="Date",
    yaxis_title="Index Value",
    xaxis=dict(
        rangeslider=dict(visible=True),  # Enable range slider
        type="date"
    ),
    template="plotly_white"
)

fig.show()
