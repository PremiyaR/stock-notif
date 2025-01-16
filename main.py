from services.stock_data import read_stock_list, fetch_realtime_data
from services.indicators import calculate_indicators, detect_signals
from services.notifications import notify
import time

def monitor_stocks():
    stock_list_file = "stocks_list.txt"
    symbols = read_stock_list(stock_list_file)

    if not symbols:
        print("No stocks to monitor. Check your stock list file.")
        return

    historical_data = {symbol: [] for symbol in symbols}

    while True:
        print("Monitoring stocks...")
        for symbol in symbols:
            try:
                # Fetch real-time price
                price = fetch_realtime_data(symbol)
                if price is None:
                    continue

                # Update historical data
                historical_data[symbol].append(price)

                # Ensure sufficient data for calculations
                if len(historical_data[symbol]) >= 14:
                    df = calculate_indicators(historical_data[symbol])
                    signals = detect_signals(df)
                    if signals:
                        notify(symbol, signals, df)
            except Exception as e:
                print(f"Error processing {symbol}: {e}")

        print("Waiting 2 hours before the next check...")
        time.sleep(7200)

if __name__ == "__main__":
    monitor_stocks()
