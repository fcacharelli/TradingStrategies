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
		data.ta.ema(length=5, append=True)
		data.ta.ema(length=21, append=True)
		data.ta.ema(length=63, append=True)
	def funcion(self):
		while self.isRunning()==True:
			self.getEMAs(bot.historial)
			print(self.historial)
			self.updatePrice()
			time.sleep(2)

API = PruebaAPI()
bot = EMA(API)


bot.startBot()
x=0
while x==0:
	x=input("1 to exit: ")   #Mejorar forma de matar el bot
bot.endBot()
