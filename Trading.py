import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Define the list of ticker symbols and the period for historical data
ticker_symbols = ['AAPL', 'MSFT', 'GOOGL', 'INVALID_TICKER']  # Including an invalid ticker for demonstration
period = '1mo'  # One month of data

# Initialize a DataFrame to store the bid-ask spreads
bid_ask_spreads = pd.DataFrame()

for ticker_symbol in ticker_symbols:
    try:
        # Download historical data
        ticker = yf.Ticker(ticker_symbol)
        historical_data = ticker.history(period=period)

        # Ensure data is available
        if historical_data.empty:
            print(f"No data available for ticker: {ticker_symbol}")
            continue

        # Note: yfinance does not provide bid and ask prices directly.
        # This example assumes 'Open' as bid and 'Close' as ask
        historical_data['bid_price'] = historical_data['Open']
        historical_data['ask_price'] = historical_data['Close']

        # Calculate bid-ask spread
        historical_data[f'{ticker_symbol}_bid_ask_spread'] = historical_data['ask_price'] - historical_data['bid_price']

        # Append the bid-ask spread to the DataFrame
        bid_ask_spreads = pd.concat([bid_ask_spreads, historical_data[f'{ticker_symbol}_bid_ask_spread']], axis=1)

    except Exception as e:
        print(f"Error processing ticker {ticker_symbol}: {e}")


# Display first few rows to verify
print(bid_ask_spreads.head())

# Plot the bid-ask spreads
plt.figure(figsize=(12, 8))

for ticker_symbol in ticker_symbols:
    if f'{ticker_symbol}_bid_ask_spread' in bid_ask_spreads.columns:
        plt.plot(bid_ask_spreads.index, bid_ask_spreads[f'{ticker_symbol}_bid_ask_spread'], marker='o', linestyle='-', label=ticker_symbol)

plt.title('Bid-Ask Spread Comparison')
plt.xlabel('Date')
plt.ylabel('Bid-Ask Spread')
plt.legend()
plt.grid(True)
plt.show()
