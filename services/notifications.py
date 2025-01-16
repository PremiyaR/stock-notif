def notify(symbol, signals, df):
    """
    Notify the user about detected signals.
    """
    print(f"Notifications for {symbol}:")
    for signal in signals:
        print(f"- {signal}")
    print("Latest Indicators:")
    print(df.tail(1)[['close', 'RSI_14', 'RSI_MA', 'EMA_10', 'EMA_20', 'EMA_50']])
