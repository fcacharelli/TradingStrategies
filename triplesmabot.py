#from bot import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')


#class SMA(bot.Bot):
#	def __init__(self):
#		pass

df = pd.read_csv('../data/btc.csv')
shortEMA=df.Close.ewm(span=5,adjust=False).mean()
mediumEMA=df.Close.ewm(span=21,adjust=False).mean()
longEMA=df.Close.ewm(span=63,adjust=False).mean()
df['Short']=shortEMA
df['Medium']=mediumEMA
df['Long']=longEMA

def buy_sell(data):
	buy_list=[]
	sell_list=[]
	flag_long=False
	flag_short=False

	for i in range(0,len(data)):
		if data['Medium'][i] < data['Long'][i] and data['Short'][i] < data['Medium'][i] and flag_short==False and flag_long==False:
			buy_list.append(data['Close'][i])
			sell_list.append(np.nan)
			flag_short=True
		elif flag_short==True and data['Short'][i] > data['Medium'][i]:
			sell_list.append(data['Close'][i])
			buy_list.append(np.nan)
			flag_short=False
		elif data['Medium'][i] > data['Long'][i] and data['Short'][i] > data['Medium'][i] and flag_long==False and flag_short==False:
			buy_list.append(data['Close'][i])
			sell_list.append(np.nan)
			flag_long=True
		elif flag_long==True and data['Short'][i] < data['Medium'][i]:
			sell_list.append(data['Close'][i])
			buy_list.append(np.nan)
			flag_long=False
		else:
			buy_list.append(np.nan)
			sell_list.append(np.nan)
	return (buy_list,sell_list)

df['Buy'], df['Sell'] = buy_sell(df)


plt.figure(figsize=(12.2,4.5))
plt.title('BTC Price')
plt.plot(df['Close'], label='Close Price', color='blue',alpha=0.5)
plt.plot(shortEMA, label='Short', color='red', alpha=0.35)
plt.plot(mediumEMA, label='Medium', color='orange', alpha=0.35)
plt.plot(longEMA, label='Long', color='green', alpha=0.35)
plt.scatter(df.index,df['Buy'],color='green',marker='^',alpha=1)
plt.scatter(df.index,df['Sell'],color='red',marker='v',alpha=1)
plt.xlim([2400,2600])
plt.show()