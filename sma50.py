import pandas as pd
import yfinance as yf
import datetime
import time

symbols = ['BTC-USD','ETH-USD','BNB-USD','XRP-USD','ADA-USD','LUNA1-USD','SOL-USD','HEX-USD','AVAX-USD','DOT-USD','DOGE-USD','SHIB-USD','MATIC-USD','CRO-USD','NEAR-USD','LTC-USD','ATOM-USD','LINK-USD','UNI1-USD','TRX-USD','BCH-USD','FTT-USD','ETC-USD','ALGO-USD','XLM-USD','LEO-USD','WAVES-USD','MANA-USD','BTCB-USD','HBAR-USD','FIL-USD','ICP-USD','VET-USD','EGLD-USD','AXS-USD','RUNE-USD','SAND-USD','XMR-USD','THETA-USD','APE3-USD','FTM-USD','XTZ-USD']
posframe = pd.DataFrame(symbols)
posframe.columns = ["Currency"]
posframe['Position'] = 0
posframe['Invest'] = 10
posframe['Quantity'] = 0

def getHourlyData(symbol):
	data = pd.DataFrame(yf.download(symbol, start=datetime.datetime.now()-datetime.timedelta(days = 3), interval="1h"))
	return data

def applyTechnicals(df):
	df['FastSMA'] = df.Close.rolling(5).mean()
	df['SlowSMA'] = df.Close.rolling(72).mean()

def changepos(curr,price,buy):
	if buy:
		posframe.loc[posframe.Currency==curr,'Position']=1
		posframe.loc[posframe.Currency==curr,'Quantity']=posframe.loc[posframe.Currency==curr,'Invest']/price
		posframe.loc[posframe.Currency==curr,'Invest']=0
	else:
		posframe.loc[posframe.Currency==curr,'Position']=0
		posframe.loc[posframe.Currency==curr,'Invest']=posframe.loc[posframe.Currency==curr,'Quantity']*price
		posframe.loc[posframe.Currency==curr,'Quantity']=0

def get_current_price(symbol):
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period='1d')
    return todays_data['Close'][0]

def netValue():
	value=0
	for i in range(len(posframe)):
		value=value+posframe.iloc[i]['Invest']+posframe.iloc[i]['Quantity']*get_current_price(posframe.iloc[i]['Currency'])
	return value


def trader():
	for coin in posframe[posframe.Position==1].Currency:
		df = getHourlyData(coin)
		applyTechnicals(df)
		lastrow=df.iloc[-1]
		if lastrow.SlowSMA > lastrow.FastSMA:
			changepos(coin,lastrow.Close,buy=False)
			print(f'Sell {coin}')
	for coin in posframe[posframe.Position==0].Currency:
		df = getHourlyData(coin)
		applyTechnicals(df)
		lastrow=df.iloc[-1]
		if lastrow.FastSMA > lastrow.SlowSMA:
			changepos(coin,lastrow.Close,buy=True)
			print(f'Buy {coin}')
	print(posframe)
while True:
	trader()
	print(netValue())
	time.sleep(3600)

