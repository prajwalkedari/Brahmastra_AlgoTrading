import pandas as pd

def MACD(df, Confict=False, External_Lib=True):
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(0)

    if External_Lib:
        import pandas_ta as ta
        macd = ta.macd(df["Close"])
        if Confict:
            return macd
        return df.join(macd)

    short_ema = df["Close"].ewm(span=12, adjust=False).mean()
    long_ema = df["Close"].ewm(span=26, adjust=False).mean()
    df["MACD_Line"] = short_ema - long_ema
    df["Signal_Line"] = df["MACD_Line"].ewm(span=9, adjust=False).mean()
    df["MACD_Hist"] = df["MACD_Line"] - df["Signal_Line"]

    if Confict:
        return df[["MACD_Line", "Signal_Line", "MACD_Hist"]]

    return df
