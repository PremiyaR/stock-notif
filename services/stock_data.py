from nsepython import nse_quote_ltp

def fetch_realtime_data(symbol):
    """
    Fetch real-time price data for a given stock symbol using nsepython.
    """
    try:
        print(f"Fetching real-time data for {symbol}...")
        data = nse_quote_ltp(symbol)
        return data
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

def read_stock_list(filename):
    """
    Reads a list of stock symbols from a file.
    """
    try:
        with open(filename, 'r') as file:
            symbols = [line.strip() for line in file if line.strip()]
        return symbols
    except Exception as e:
        print(f"Error reading stock list: {e}")
        return []
