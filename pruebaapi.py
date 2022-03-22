import pandas as pd
import random
from interfaz import API

class PruebaAPI(API):
	def __init__(self):
		self.__USD=100
		self.__BTC=0
		self.datos=pd.read_csv("../data/btc.csv")
		inicio=random.randrange(2000)
		self.ahora=inicio+100
		self.historial = self.datos.iloc[inicio:self.ahora+1,:]
	def buy(self,price):
		self.__BTC=self.__USD/price
		self.__USD=0
	def sell(self,price):
		self.__USD=self.__BTC*price
		self.__BTC=0
	def getPriceHistory(self):
		return self.historial
	def updatePrice(self):
		self.ahora=self.ahora+1
		self.historial=pd.concat([self.historial,self.datos.iloc[[self.ahora]]], ignore_index=False,axis=0)
	def getCurrentPrice(self):
		return self.historial["Close"].iloc[-1]
	def netValue(self,price):
		return self.__USD+self.__BTC*price
