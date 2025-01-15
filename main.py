import requests
import pandas as pd
import time

API_KEY = "S68D5ZVBQ4JSXY2L"  
BASE_URL = "https://www.alphavantage.co/query"

def fetch_all_stocks_rsi():
    stocks = ["TCS", "INFY", "RELIANCE"]  
    all_data = []

    for symbol in stocks:
        print(f"Fetching RSI data for {symbol}...")
        params = {
            "function": "RSI",
            "symbol": symbol,
            "interval": "daily",
            "time_period": 14,
            "series_type": "close",
            "apikey": API_KEY
        }
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if "Technical Analysis: RSI" in data:
            rsi_data = data["Technical Analysis: RSI"]
            df = pd.DataFrame.from_dict(rsi_data, orient="index")
            df.reset_index(inplace=True)
            df.columns = ["date", "RSI"]
            df["RSI"] = df["RSI"].astype(float)
            df["symbol"] = symbol
            all_data.append(df)
        else:
            print(f"Error fetching RSI for {symbol}: {data}")

    if all_data:
        return pd.concat(all_data, ignore_index=True)
    else:
        return pd.DataFrame()

def filter_high_rsi_stocks(dataframe, threshold=65):
    return dataframe[dataframe["RSI"] > threshold]

def calculate_rsi_ma(dataframe, ma_period=5):
    dataframe["RSI_MA"] = dataframe["RSI"].rolling(window=ma_period).mean()
    return dataframe

def detect_bullish_crossover(dataframe):
    dataframe["bullish_crossover"] = (
        (dataframe["RSI"] > dataframe["RSI_MA"]) &  # RSI crosses above RSI-MA
        (dataframe["RSI"].shift(1) <= dataframe["RSI_MA"].shift(1)) &  # Previous RSI <= RSI-MA
        (dataframe["RSI"] >= 55)  # RSI is at least 55
    )
    return dataframe[dataframe["bullish_crossover"]]

def main():
    while True:
        print("Fetching RSI data for all stocks...")
        all_data = fetch_all_stocks_rsi()

        if not all_data.empty:
            # Filter stocks with RSI > 65
            high_rsi_stocks = filter_high_rsi_stocks(all_data)

            if not high_rsi_stocks.empty:
                print("Stocks with RSI > 65 detected. Checking for bullish crossovers...")

                # Detect bullish crossovers in high RSI stocks
                bullish_signals = []
                for symbol in high_rsi_stocks["symbol"].unique():
                    stock_data = high_rsi_stocks[high_rsi_stocks["symbol"] == symbol]
                    stock_data = calculate_rsi_ma(stock_data)
                    bullish_signal = detect_bullish_crossover(stock_data)

                    if not bullish_signal.empty:
                        bullish_signals.append(bullish_signal)

                # Combine all bullish signals into a single DataFrame
                if bullish_signals:
                    all_bullish_signals = pd.concat(bullish_signals, ignore_index=True)
                    print("Bullish crossovers detected for the following stocks:")
                    print(all_bullish_signals)
                else:
                    print("No bullish crossovers detected.")
            else:
                print("No stocks with RSI > 65 found.")
        else:
            print("No data retrieved.")

        print("Waiting 2 hours before the next check...")
        time.sleep(7200)  # Wait for 2 hours (7200 seconds)


if __name__ == "__main__":
    main()
