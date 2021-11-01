import streamlit as st
import pandas as pd
import numpy as np
import quandl as quandl
from datetime import date
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf
from annotated_text import annotated_text, annotation
from htbuilder import h1
st.set_page_config(layout="wide")

@st.cache(allow_output_mutation=True)
def load_data():
    df = quandl.get("BCHAIN/MKPRU", api_key="FYzyusVT61Y4w65nFESX").reset_index()

    btcdata = yf.download(tickers='BTC-USD', period="1d", interval="1m")["Close"]
    lastprice = btcdata.iloc[-1]
    df.loc[len(df)] = [date.today(), lastprice]

    df = df[df["Value"] > 0]
    df["Date"] = pd.to_datetime(df["Date"])
    df.sort_values(by="Date", inplace=True)
    f_date = pd.to_datetime(date(2010, 1, 1))
    E_date = pd.to_datetime(date(2009, 1, 3))  # genesis
    delta = f_date - E_date
    df = df[df.Date > f_date]
    df.reset_index(inplace=True)

    return df, delta

def normalization(data):
    normalized = (data - data.min()) / (data.max() - data.min())
    return normalized


def ossValue(days):
    X = np.array(np.log10(df.ind[:days])).reshape(-1, 1)
    y = np.array(np.log10(df.Value[:days]))
    reg = LinearRegression().fit(X, y)
    values = reg.predict(X)
    return values[-1]

def normalizationhalving(Normlist):
    global df
    df1 = df[df["Date"] <= "2011-10-19"]
    df2 = df[(df["Date"] > "2011-10-19") & (df["Date"] <= "2015-01-14")]
    df3 = df[(df["Date"] > "2015-01-14") & (df["Date"] <= "2018-12-15")]
    df4 = df[df["Date"] > "2018-12-15"]
    for item in Normlist:
        df1[item].update(normalization(df1[item]))
        df2[item].update(normalization(df2[item]))
        df3[item].update(normalization(df3[item]))
        df4[item].update(normalization(df4[item]))
    df = pd.concat([df1, df2, df3, df4])
    return df

df, delta = load_data()

############## 400MA ########################################
df['400MA'] = 0
for i in range(0, df.shape[0]):
    df['400MA'][i] = df['Value'][0 if i < 400 else (i - 400): i].dropna().mean()

df['400MArisk'] = 0
for i in range(0, df.shape[0]):
    df['400MArisk'][i] = (df['Value'][i] / df['400MA'][i])

############## Mayer Multiple ########################################
df["Mayer"] = df["Value"] / df["Value"].rolling(200).mean()

############## Puell Multiple ########################################
df["btcIssuance"] = 7200 / 2 ** (np.floor(df["index"] / 1458))
df["usdIssuance"] = df["btcIssuance"] * df["Value"]
df["MAusdIssuance"] = df["usdIssuance"].rolling(window=365).mean()
df["PuellMultiple"] = df["usdIssuance"] / df["MAusdIssuance"]

############### Price/52W MA ########################################
df["Price/52w"] = df["Value"] / df["Value"].ewm(span=365).mean()

############## Sharpe Ratio ########################################
df["Return%"] = df["Value"].pct_change() * 100
df["Sharpe"] = (df["Return%"].rolling(365).mean() - 1) / df["Return%"].rolling(365).std()

############# Sortino #############################################
dfs = df[df["Return%"] < 0]
df["Sortino"] = (df["Return%"].rolling(365).mean() - 1) / dfs["Return%"].rolling(365).std()

############# Power Law ###########################################
df["ind"] = [x + delta.days for x in range(len(df))]
df["PowerLaw"] = np.log10(df.Value) - [ossValue(x + 1) for x in range(len(df))]

#################### avg ################################
df.update(normalizationhalving(["PuellMultiple", "Price/52w", "PowerLaw", "Sharpe", "Sortino", "Mayer","400MArisk"]))

metric_list = ["PuellMultiple", "Price/52w", "PowerLaw", "Sharpe", "Mayer", "400MArisk"]


# Title of dashboard
st.markdown("<h1 style='text-align: center; color: white;'>Chain Net</h1>", unsafe_allow_html=True)

# sidebar title
st.sidebar.title("Oscillator Config")
st.sidebar.caption("Select the metrics you would like to include in the Oscillator")

metric_selection = st.sidebar.multiselect(label='Metrics',
                                            options=metric_list)

#coin = st.sidebar.selectbox(label='Cryptocurrency', options=['Bitcoin', 'Ethereum'])
df["avg"] = df[metric_selection].mean(axis=1)
#################### Plot ################################
fig = make_subplots(specs=[[{"secondary_y": True}]])
xaxis = df.Date

fig.add_trace(go.Scatter(x=xaxis, y=df.Value, name="Price", line=dict(color="gold")), secondary_y=False)
fig.add_trace(go.Scatter(x=xaxis, y=df["avg"], name="Risk", mode="lines", line=dict(color="white")), secondary_y=True)

fig.add_hrect(y0=0.4, y1=0.3, line_width=0, fillcolor="green", opacity=0.2, secondary_y=True)
fig.add_hrect(y0=0.3, y1=0.2, line_width=0, fillcolor="green", opacity=0.3, secondary_y=True)
fig.add_hrect(y0=0.2, y1=0.1, line_width=0, fillcolor="green", opacity=0.4, secondary_y=True)
fig.add_hrect(y0=0.1, y1=0, line_width=0, fillcolor="green", opacity=0.5, secondary_y=True)
fig.add_hrect(y0=0.6, y1=0.7, line_width=0, fillcolor="red", opacity=0.3, secondary_y=True)
fig.add_hrect(y0=0.7, y1=0.8, line_width=0, fillcolor="red", opacity=0.4, secondary_y=True)
fig.add_hrect(y0=0.8, y1=0.9, line_width=0, fillcolor="red", opacity=0.5, secondary_y=True)
fig.add_hrect(y0=0.9, y1=1.0, line_width=0, fillcolor="red", opacity=0.6, secondary_y=True)


risk = round(df['avg'].iloc[-1],2)
bitcoin_price = round(df['Value'].iloc[-1])
st.sidebar.markdown("<h3>" + 'Latest BTC price:     ' + str(annotation(f"{bitcoin_price}", background="#fea")) + "</h3>", unsafe_allow_html=True)
if df['avg'].iloc[-1] < 0.4:
    st.sidebar.markdown("<h3>" + 'Risk:     ' + str(annotation(f"{risk}", background="#afa")) + "</h3>", unsafe_allow_html=True)
elif df['avg'].iloc[-1] > 0.6:
    st.sidebar.markdown("<h3>" + 'Risk:     ' + str(annotation(f"{risk}", background="#faa")) + "</h3>", unsafe_allow_html=True)
else:
    st.sidebar.markdown("<h3>" + 'Risk:     ' + str(annotation(f"{risk}", background="#8ef")) + "</h3>", unsafe_allow_html=True)

fig.update_layout(xaxis_title='Date', yaxis_title='Price',
                  yaxis2_title='Risk',
                  yaxis1=dict(type='log', showgrid=False),
                  yaxis2=dict(showgrid=True, tickmode='linear', tick0=0.0, dtick=0.1),
                  template="plotly_dark",
                  )

st.plotly_chart(fig, use_container_width=True)

annotated_text(
    ("This", "", "#afa"),
    " is low risk, while ",
    ("this", "", "#faa"),
    " is high risk and lastly, ",
    ("this", "", "#8ef"),
    " is neutral risk ",
)
print(df[['Date', 'PuellMultiple']])