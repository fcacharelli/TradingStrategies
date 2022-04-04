import pandas as pd
import yfinance as yf
import datetime
import math
import matplotlib.pyplot as plt

def grid(df,grids,pct_range,wtime):
	total=[]
	for i in range(0,len(df)-wtime,24):
		entry_price=df['Close'].iloc[i]
		top_range = entry_price*(1+pct_range)
		bottom_range = entry_price*(1-pct_range)
		grid_gap = (top_range - bottom_range)/grids
		price_gap = 100/grids
		pct_gain=pct_range/grids
		Token1=50
		Token2=50
		for j in range(i,i+wtime):
			actual_price=df['Close'].iloc[j]
			if ((actual_price >= entry_price+grid_gap) and (actual_price<top_range)):
				ngrids=math.floor((actual_price-entry_price)/grid_gap)
				Token1=Token1-price_gap*ngrids
				Token2=(Token2+price_gap*ngrids)*(1+pct_gain)
				entry_price = actual_price
			elif ((actual_price <= entry_price-grid_gap) and (actual_price>bottom_range)):	
				ngrids=math.floor((entry_price-actual_price)/grid_gap)
				Token1=(Token1+price_gap*ngrids)*(1+pct_gain)
				Token2=Token2-price_gap*ngrids
				entry_price = actual_price
		#print(f'Inicio={i/24} Token1={Token1:.2f} / Token2={Token2:.2f} / Total={Token1+Token2:.2f}')
		total.append(Token1+Token2)
	return total



symbol="ETH-BTC"
data = pd.DataFrame(yf.download(symbol, start=datetime.datetime.now()-datetime.timedelta(days = 90), interval="1h"))
res = []
for i in range(5,100):
	resultados = grid(data,i,0.3,5*24)
	res.append([i,sum(resultados)/len(resultados)])
res = pd.DataFrame(res, columns=["i","AVG"])
print(res)

plt.figure(figsize=(12.2,4.5))
plt.title('Grid Amount')
plt.plot(res['i'],res['AVG'], label='AVG gain', color='blue',alpha=0.5)
plt.show()