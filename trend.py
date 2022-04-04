import pandas as pd
import yfinance as yf
import datetime
import matplotlib.pyplot as plt
import numpy as np

def getMMs(df):
	Mins = pd.DataFrame(columns=["Date","Price"])
	Maxs = pd.DataFrame(columns=["Date","Price"])
	for i in range(1,len(df)-1):
		anterior,valor,siguiente=df['Close'].iloc[i-1],df['Close'].iloc[i],df['Close'].iloc[i+1]
		if (anterior<valor) and (valor>siguiente):
			Maxs = Maxs.append({'Date': df.index[i], 'Price': valor}, ignore_index=True)
		elif (anterior>valor) and (valor<siguiente):
			Mins = Mins.append({'Date': df.index[i], 'Price': valor}, ignore_index=True)
	return Mins,Maxs

def getTrend(Mins,Maxs):
	Trend = pd.DataFrame(columns=['Date','Trend'])
	for i in range(1,min(len(Mins),len(Maxs))-1):
		minAn,minAc,maxAn,maxAc,date=Mins['Price'].iloc[i-1],Mins['Price'].iloc[i],Maxs['Price'].iloc[i-1],Maxs['Price'].iloc[i],Mins['Date'].iloc[i]
		if (minAc<minAn) and (maxAc<maxAn):
			#print(f'DOWN: {date}')
			Trend = Trend.append({'Date': date,'Trend': 'DOWN'}, ignore_index=True)
		elif (minAc>minAn) and (maxAc>maxAn):
			#print(f'UP: {date}')
			Trend = Trend.append({'Date': date,'Trend': 'UP'}, ignore_index=True)
		else:
			#print(f'VOLATILE: {date}')
			Trend = Trend.append({'Date': date,'Trend': 'VOLATILE'}, ignore_index=True)
	return Trend


symbol="ETH-BTC"

data = pd.DataFrame(yf.download(symbol, start=datetime.datetime.now()-datetime.timedelta(days = 90), interval="1h"))

mins,maxs=getMMs(data)
Trend = getTrend(mins,maxs)

df = pd.concat([data,Trend.set_index('Date')],axis=1)
print(df)

plt.figure(figsize=(12.2,4.5))
plt.title('BTC Price')
plt.plot(df['Close'], label='Close Price', color='blue',alpha=0.5)
up = df.apply(lambda x: x['Close'] if (x['Trend']=='UP') else np.nan,axis=1)
down = df.apply(lambda x: x['Close'] if (x['Trend']=='DOWN') else np.nan,axis=1)
plt.scatter(df.index, up,color='green',marker='^',alpha=1)
plt.scatter(df.index, down,color='red',marker='v',alpha=1)
plt.show()