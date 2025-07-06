#author: Prajwal
import pandas_ta as ta
import pandas as pd

def SuperTrend(df:pd.DataFrame, Confict=False ):
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(0)
    df.dropna(inplace=True)
    sup = ta.supertrend(high=df["High"], low=df["Low"], close=df["Close"])
    if Confict==True :
        return  df.join(sup)
    return df



