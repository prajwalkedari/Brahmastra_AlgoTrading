#author: Prajwal
import pandas_ta as ta
import pandas as pd

def SuperTrend(df:pd.DataFrame, Confict=True , length=10, multiplier=3):
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)
    df.dropna(inplace=True)
    sup = ta.supertrend(high=df["High"], low=df["Low"], close=df["Close"], length=length, multiplier=multiplier)
    if Confict==True :
        return  sup
    return df.join(sup)



