import pandas as pd
import pandas_ta as ta

def calculate_indicators(prices):
    """
    Calculate RSI and EMA indicators from price data.
    """
    df = pd.DataFrame(prices, columns=["close"])
    df['RSI_14'] = ta.rsi(df['close'], length=14)
    df['EMA_10'] = ta.ema(df['close'], length=10)
    df['EMA_20'] = ta.ema(df['close'], length=20)
    df['EMA_50'] = ta.ema(df['close'], length=50)
    df['EMA_100'] = ta.ema(df['close'], length=100)
    df['EMA_200'] = ta.ema(df['close'], length=200)
    df['RSI_MA'] = df['RSI_14'].rolling(window=5).mean()
    return df

def detect_signals(df):
    """
    Detect signals based on RSI and EMA conditions.
    """
    signals = []
    latest_rsi = df['RSI_14'].iloc[-1]

    # RSI Condition
    if latest_rsi >= 65:
        signals.append(f"RSI Alert: {latest_rsi:.2f}")

    # Bullish Crossover
    if latest_rsi > df['RSI_MA'].iloc[-1] and latest_rsi >= 65:
        signals.append("Bullish Crossover Alert")

    # EMA Proximity
    if (
        abs(df['EMA_10'].iloc[-1] - df['EMA_20'].iloc[-1]) < 1.0 and
        abs(df['EMA_20'].iloc[-1] - df['EMA_50'].iloc[-1]) < 1.0
    ):
        signals.append("EMA Proximity Alert")

    return signals
