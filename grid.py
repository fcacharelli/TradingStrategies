import pandas as pd
import yfinance as yf
import datetime
import math
import matplotlib.pyplot as plt
import numpy as np
import statistics

TOKEN=0.01
actual_price=0

def grid(df,grids,pct_range,wtime):
	times=0
	win=0
	for i in range(0,len(df)-wtime,24):
		entry_price=df['Close'].iloc[i]
		top_range = entry_price*(1+pct_range)
		bottom_range = entry_price*(1-pct_range)
		price_gap = (top_range - bottom_range)/grids
		Token2=TOKEN
		Token1=Token2/entry_price
		grid_gap = Token1/grids
		global actual_price
		for j in range(i+1,i+1+wtime):
			actual_price=df['Close'].iloc[j]
			if ((actual_price >= entry_price+price_gap) and (actual_price<top_range)):
				ngrids=math.floor((actual_price-entry_price)/price_gap)
				Token1=Token1-grid_gap*ngrids
				for n in range(1,ngrids+1):
					Token2=Token2+(grid_gap*(n*price_gap+entry_price))*0.999
				entry_price = entry_price+ngrids*price_gap
			elif ((actual_price <= entry_price-price_gap) and (actual_price>bottom_range)):	
				ngrids=math.floor((entry_price-actual_price)/price_gap)
				Token1=Token1+price_gap*ngrids
				for n in range(1,ngrids+1):
					Token2=Token2-(grid_gap*(entry_price-n*price_gap))*0.999
				entry_price = entry_price-ngrids*price_gap
		Result = Token2+Token1*actual_price
		times=times+1
		if Result>(TOKEN*2):
			win = win+1
		#
		#
		# Volver a plantear el grid con lista de precios 
		# Cuando los cruza compra o vende, como kucoin
		# el resultado no deberia poder dar negativo (si menor a la inversion pero no negativo)
		#
	return times,win

symbol="ETH-BTC"
data = pd.DataFrame(yf.download(symbol, start=datetime.datetime.now()-datetime.timedelta(days = 365), interval="1h"))
data['Date'] = data.index
data.reset_index(drop=True,inplace=True)

days = [1,2,5,10,15,30,45]
ranges = [5,10,15,20]
grids = [10,20,30,40,50,60,70,80]
f = open("myfile.csv", "a")
f.write('Day,Grid,Range,Tests,Wins\n')
for day in days:
	print(day)
	for gride in grids:
		print(gride)
		for rango in ranges:
			tests,wins = grid(data,gride,rango/100,day*24)
			f.write(str(day)+','+str(gride)+','+str(rango)+','+str(tests)+','+str(wins)+'\n')
f.close()


#
#
#for i in range(len(Days)):
#	f.write(str(data['Date'].iloc[Days[i]])+',1\n')
#f.close()


#
#f.write('Days,Grids,Range,MinP,MaxP,AvgP\n')
#f.write(str(i)+','+str(j)+','+str(n)+','+str(MinP)+','+str(MaxP)+','+str(AvgP)+'\n')
#f.close()