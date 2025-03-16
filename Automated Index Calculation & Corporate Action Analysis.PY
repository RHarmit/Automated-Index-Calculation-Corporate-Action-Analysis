import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# Fetch historical bond yield data (Example: US 10-Year Treasury Bond)
bond_ticker = "^TNX"  # US 10-Year Treasury Yield
data = yf.download(bond_ticker, start="2023-01-01", end="2024-01-01")

if data.empty:
    print("No data fetched. Please check the ticker or date range.")
    exit()

# Inspect the data to ensure proper values
print(data.head())  # Check if 'Close' values are in percentage points

# Calculate daily returns for yield movements
data['Daily Return'] = data['Close'].pct_change()
data.dropna(inplace=True)

# Calculate Key Fixed Income Metrics
def calculate_metrics(data):
    # Average yield (already in percentage points, no need to multiply by 100)
    avg_yield = data['Close'].mean()
    # Convert to float in case it's a Series
    avg_yield = float(avg_yield)
    
    # Volatility of daily returns (standard deviation)
    yield_volatility = data['Daily Return'].std()
    yield_volatility = float(yield_volatility)
    
    # Value at Risk (VaR) at 95% confidence level
    var_95 = np.percentile(data['Daily Return'], 5)
    
    return avg_yield, yield_volatility, var_95

avg_yield, yield_volatility, var_95 = calculate_metrics(data)

# Visualizing Bond Yield Movements
plt.figure(figsize=(10, 5))
plt.plot(data.index, data['Close'], label='US 10Y Treasury Yield', color='blue')
plt.xlabel("Date")
plt.ylabel("Yield (%)")
plt.title("US 10-Year Treasury Yield Trends")
plt.legend()
plt.grid()
plt.show()

# Output the results
print(f"Average Yield: {avg_yield:.2f}%")
print(f"Yield Volatility: {yield_volatility * 100:.2f}%")
print(f"Value at Risk (95% Confidence): {var_95 * 100:.2f}%")

