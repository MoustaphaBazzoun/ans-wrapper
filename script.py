
import yfinance as yf
import time
from datetime import datetime

def get_stock_price(ticker_symbol: str) -> float:
    """Fetch the current stock price using yfinance."""
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(period="1d", interval="1m")
    
    if data.empty:
        print("No data available.")
        return None

    latest_price = data['Close'].iloc[-1]
    return latest_price

def update_price_every_minute(ticker_symbol: str):
    """Update stock price every minute."""
    print(f"Tracking {ticker_symbol}... (Ctrl+C to stop)")
    try:
        while True:
            price = get_stock_price(ticker_symbol)
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if price:
                print(f"[{now}] {ticker_symbol}: ${price:.2f}")
            else:
                print(f"[{now}] Failed to fetch price.")
            time.sleep(60)
    except KeyboardInterrupt:
        print("\nStopped by user.")

if __name__ == "__main__":
    update_price_every_minute("AAPL")
