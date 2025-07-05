#author: Prajwal
import pandas_ta as ta
import pandas as pd

def SuperTrend(df:pd.DataFrame, Confict=False ):
    df.columns = df.columns.droplevel(0)  # Drop the ticker level
    df.dropna(inplace=True)
    sup = ta.supertrend(high=df["High"], low=df["Low"], close=df["Close"])
    if Confict==True :
        return  df.join(sup)
    return df



