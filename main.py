import Indicator as ind # our module
import yfinance as yf 
import pandas as pd


# stock Download
Ticker="^NSEI"
# Ticker="^NSEBANK"
# Ticker="NIFTY_FIN_SERVICE.NS"
dataStock = yf.download(tickers=Ticker, start="2025-06-01",end="2025-07-06",interval="5m") 
dataStock.columns = dataStock.columns.droplevel(1)
#applied indictor
macd = ind.MACD(dataStock)
# vwap = ind.VWAP(dataStock)
st = ind.SuperTrend(dataStock)
macd = ind.MACD(dataStock)
vwap = ind.VWAP(dataStock)
# join indicator 
dataStock= dataStock.join([vwap,st,macd])

dataStock["Buy_Signal"] = ((dataStock["SUPERTd_10_3.0"]==1) & 
(dataStock["MACD_Line"] > dataStock["MACD_Hist"]) &
(dataStock["SUPERT_10_3.0"]< dataStock["Close"]))

trades = []
position = None


for i in range(1, len(dataStock)):
    row = dataStock.iloc[i]

    if position is None and row['Buy_Signal']:
        entry_price = row['Close']
        stop_loss = row['SUPERT_10_3.0']
        target_price = entry_price + 1.5 * (entry_price - stop_loss)

        position = {
            'entry_date': row.name,
            'entry_price': entry_price,
            'stop_loss': stop_loss,
            'target_price': target_price
        }

    elif position:
        low = row['Low']
        high = row['High']
        st_trend = row['SUPERTd_10_3.0']
        exit_reason = None

        # Exit by stoploss
        if low <= position['stop_loss']:
            exit_price = position['stop_loss']
            exit_reason = 'Stoploss'
        # Exit by target
        elif high >= position['target_price']:
            exit_price = position['target_price']
            exit_reason = 'Target'
        # Exit on supertrend flip
        elif st_trend == -1:
            exit_price = row['Close']
            exit_reason = 'Supertrend Flip'

        if exit_reason:
            position['exit_date'] = row.name
            position['exit_price'] = exit_price
            position['exit_reason'] = exit_reason
            trades.append(position)
            position = None

# --- Trades DataFrame ---
trades_df = pd.DataFrame(trades)
trades_df['PnL'] = trades_df['exit_price'] - trades_df['entry_price']

print("\nAll Trades:\n", trades_df)
print("\nTotal Trades:", len(trades_df))
print("Winning Trades:", (trades_df['PnL'] > 0).sum())
print("Win Rate: {:.2f}%".format((trades_df['PnL'] > 0).mean() * 100))
print("Total Profit: {:.2f}".format(trades_df['PnL'].sum()))

import matplotlib.pyplot as plt

# plt.axvline(x=5, color='red', linestyle='--', linewidth=1)
plt.plot(dataStock["Close"])
for x in  dataStock.index[dataStock["Buy_Signal"] == 1]:
    plt.axvline(x=x, color='red', linestyle='--', linewidth=1)
# plt.scatter(1,3,color='green', label='Buy Signal', marker='^', s=80)
plt.show()