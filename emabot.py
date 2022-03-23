from interfaz import Bot
from pruebaapi import PruebaAPI
import time
import pandas_ta as ta

class EMA(Bot):
	def __init__(self, API):
		self.API = API
		self.historial = API.getPriceHistory()
	def updatePrice(self):
		self.API.updatePrice()
		self.historial = API.getPriceHistory()
		self.getEMAs(self.historial)
	def getEMAs(self,data):
		data.ta.ema(length=20, append=True)
		data.ta.ema(length=70, append=True)
		data.ta.ema(length=150, append=True)
	def funcion(self):
		self.getEMAs(self.historial)
		leng = 0
		flag_short=False
		flag_long=False
		while self.isRunning()==True and leng != len(self.historial):
			leng=len(self.historial)
			if self.historial['EMA_70'].iloc[-1] < self.historial['EMA_150'].iloc[-1] and self.historial['EMA_20'].iloc[-1] < self.historial['EMA_70'].iloc[-1] and flag_short==False and flag_long==False:
				self.API.buy(self.historial['Close'].iloc[-1])
				flag_short=True
			elif flag_short==True and self.historial['EMA_20'].iloc[-1] > self.historial['EMA_70'].iloc[-1]:
				self.API.sell(self.historial['Close'].iloc[-1])
				flag_short=False
			elif self.historial['EMA_70'].iloc[-1] > self.historial['EMA_150'].iloc[-1] and self.historial['EMA_20'].iloc[-1] > self.historial['EMA_70'].iloc[-1] and flag_long==False and flag_short==False:
				self.API.buy(self.historial['Close'].iloc[-1])
				flag_long=True
			elif flag_long==True and self.historial['EMA_20'].iloc[-1] < self.historial['EMA_70'].iloc[-1]:
				self.API.sell(self.historial['Close'].iloc[-1])
				flag_long=False
			self.updatePrice()
		print(self.API.netValue(self.historial['Close'].iloc[-1]))

API = PruebaAPI()
bot = EMA(API)


bot.startBot()
x=0
while x==0:
	x=input("1 to exit: ")   #Mejorar forma de matar el bot
bot.endBot()
