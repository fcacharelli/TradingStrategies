import pandas as pd
import yfinance as yf
import datetime
import math
import matplotlib.pyplot as plt
import numpy as np
import statistics

TOKEN=0.02


def grid(df,grids,pct_range,wtime):
	Total_Gains=0
	for i in range(0,len(df)-wtime,24):
		entry_price=df['Close'].iloc[i]
		top_range = entry_price*(1+pct_range)
		bottom_range = entry_price*(1-pct_range)
		price_gap = (top_range - bottom_range)/grids
		Token2=TOKEN
		Token1=Token2*entry_price
		grid_gap = Token1/grids
		for j in range(i,i+wtime):
			actual_price=df['Close'].iloc[j]
			if ((actual_price >= entry_price+price_gap) and (actual_price<top_range)):
				ngrids=math.floor((actual_price-entry_price)/price_gap)
				Token1=Token1-grid_gap*ngrids
				for n in range(1,ngrids+1):
					Token2=Token2+(grid_gap*(ngrids*price_gap+entry_price))*0.999
				entry_price = actual_price
			elif ((actual_price <= entry_price-price_gap) and (actual_price>bottom_range)):	
				ngrids=math.floor((entry_price-actual_price)/price_gap)
				Token1=Token1+price_gap*ngrids
				for n in range(1,ngrids+1):
					Token2=Token2-(grid_gap*(entry_price-ngrids*price_gap))*0.999
				entry_price = actual_price
		Total = Token2+Token1*actual_price
		Gain = Total-TOKEN
		Total_Gains=Total_Gains+Gain
	return Total_Gains

symbol="ETH-BTC"
data = pd.DataFrame(yf.download(symbol, start=datetime.datetime.now()-datetime.timedelta(days = 365), interval="1h"))
data['Date'] = data.index
data.reset_index(drop=True,inplace=True)

gains=[]
pct=[]
APR=[]
for n in range(101):
	inicio = np.random.randint(0,330*24)
	df = data.iloc[inicio:inicio+32*24]
	gain = grid(df,80,0.1,2*24)
	gains.append(gain)
	pct.append((gain*100)/TOKEN)
	APR.append((gain*1200)/TOKEN)



print(f'Ganancias Mes: {statistics.mean(gains)}')
print(f'Porcentaje: {statistics.mean(pct)}')
print(f'APR: {statistics.mean(APR)}')




#f = open("myfile.csv", "a")
#f.write('Date,Best\n')
#for i in range(len(Days)):
#	f.write(str(data['Date'].iloc[Days[i]])+',1\n')
#f.close()


#
#f.write('Days,Grids,Range,MinP,MaxP,AvgP\n')
#f.write(str(i)+','+str(j)+','+str(n)+','+str(MinP)+','+str(MaxP)+','+str(AvgP)+'\n')
#f.close()