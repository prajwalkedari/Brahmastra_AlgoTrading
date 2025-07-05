#Author: Pratham Dubey
import pandas as pd
def VWAP(df,Confict=False,External_Lib=True):
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(0)
    if External_Lib:
        import pandas_ta as ta 
        t=ta.vwap(df["High"],df["Low"],df["Close"],df["Volume"])
        if Confict:
            return t
        return df.join(t)
    df["price"] =(df["High"]+df["Low"]+df["Close"])/3
    df["VWAP"] = (df["price"]*df["Volume"]).cumsum() /df["Volume"].cumsum()
    if Confict :
        return  df["VWAP"]
    df =df.drop("price", axis='columns')
    return df

