from fbprophet import Prophet
import warnings

warnings.simplefilter(action ='ignore', category=FutureWarning)

end1 = dt.date(end.year - 1, end.month,end.day)
end2 = dt.date(end.year, end.month - 6, end.day)

start1 = dt.date(end1.year -6, end.month, end.day)

df1 = reader.get_data_yahoo(cripto,start1,end1)['Adj Close']
df2 = reader.get_data_yahoo(cripto,start1,end2)['Adj Close']

modelfb1 = Prophet()

df1 = df1.reset_index()
df1[['ds', 'y']] = df1[['Date', 'BTC-USD']]
modelfb1.fit(df1)


modelfb2 = Prophet()

df2 = df2.reset_index()
df2[['ds', 'y']] = df2[['Date', 'BTC-USD']]
modelfb2.fit(df2)

future = modelfb1.make_future_dataframe(periods=365)

future2 = modelfb2.make_future_dataframe(periods=365)

forecast1 = modelfb1.predict(future)
forecast2 = modelfb2.predict(future2)

modelfb1.plot(forecast1)
plt.show()
##Or a another model

##modelfb2.plot(forecast2)
##plt.show()
