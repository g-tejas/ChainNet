import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import date
from math import sqr
import black_box as bb

#### Backtest Parameters
DCA_FREQUENCY = 'W' # M for monthly, W for weekly
START_DATE = date(2017,1,1)
END_DATE = date(2021,10,30)

df = pd.read_csv("data/riskmetric.csv", usecols=['Date', 'Value', 'avg'])
df['Date'] = pd.to_datetime(df['Date'])
df = df[df['Date'] > pd.to_datetime(START_DATE)]
df = df[df['Date'] <= pd.to_datetime(END_DATE)]
df = df.set_index("Date").resample(DCA_FREQUENCY).mean()

def buy_multiplier(risk):
    multiple = -0.5 + (2.5 + 0.5)/(1 + (risk/0.1)**1) 
    return multiple

def sell_multiplier(risk):
    multiple = 1.07328 + (0.1038428 - 1.07328)/(1 + (risk/0.8148592)**13.41005) 
    return multiple

def buy(buy_order_in_usd, price, USDbalance, BTCbalance):
    buy_order_in_btc = buy_order_in_usd / price
    USDbalance -= buy_order_in_usd
    BTCbalance += buy_order_in_btc
    return USDbalance, BTCbalance

def sell(sell_order_in_btc, price, USDbalance, BTCbalance):
    sell_order_in_usd = sell_order_in_btc * price
    USDbalance += sell_order_in_usd
    BTCbalance -= sell_order_in_btc
    return USDbalance, BTCbalance

def strategy(risk, signal, price, USDbalance, BTCbalance):
    multiplier = 0
    if signal == 's':
        if BTCbalance > 0:
           sellAmountinBTC = sell_multiplier(risk) * BTCbalance
           multiplier = sell_multiplier(risk)
           USDbalance, BTCbalance = sell(sellAmountinBTC, price, USDbalance, BTCbalance)
            
    elif signal == 'b':
        if USDbalance > 0:
            buyAmount = buy_multiplier(risk) * USDbalance
            multiplier = buy_multiplier(risk)
            USDbalance, BTCbalance = buy(buyAmount, price, USDbalance, BTCbalance)

    elif signal == 'n':
        pass # don't do anything in the neutral zone to avoid over trading

    return USDbalance, BTCbalance, multiplier


df['USDbalance'] = ''
df['USDbalance'].iloc[0] = 10000 # start off with 10, 000 US dollars

df['BTCbalance'] = ''
df['BTCbalance'].iloc[0] = 0

df['Portfolio'] = ''
df['Portfolio'].iloc[0] = df['Value'].iloc[0] * df['BTCbalance'].iloc[0] + df['USDbalance'].iloc[0]

df['Multiplier'] = ''

for i in range(1, df.shape[0]): # you dont want to execute strategy on first day
    if df["avg"][i] < 0.4:
        signal='b'
    elif df["avg"][i] > 0.6:
        signal='s'
    else:
        signal='n' # neutral

    df['USDbalance'][i], df['BTCbalance'][i], df['Multiplier'][i] = strategy(risk=df['avg'][i],
                                                                            signal=signal,
                                                                            price=df['Value'][i],
                                                                            USDbalance=df['USDbalance'][i-1],
                                                                            BTCbalance=df['BTCbalance'][i-1])
    df['Portfolio'][i] = df['Value'][i] * df['BTCbalance'][i] + df['USDbalance'][i]

# Make the plots
fig = make_subplots(specs=[[{"secondary_y": True}]])
xaxis=df.index

fig.add_trace(go.Scatter(x=xaxis, y=df['Portfolio'], name="Portfolio Value", line=dict(color="green")), secondary_y=False)
fig.add_trace(go.Scatter(x=xaxis, y=df['Value'], name="Bitcoin Price", line=dict(color="gold")), secondary_y=False)

fig.show()

df.to_csv(f'backtest_results/model_1_{START_DATE} - {END_DATE}.csv')
print(df)
