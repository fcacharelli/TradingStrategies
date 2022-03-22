from abc import ABC, abstractmethod
import threading
import uuid

#-------------------------------------#
# Interfaz Bot
#
class Bot(ABC):
	def startBot(self):
		self.__botID = uuid.uuid4()
		self.__running = True
		x = threading.Thread(target=self.funcion)
		x.start()
	def getBotID(self):
		return self.__botID
	def funcion(self):
		pass
	def isRunning(self):
		return self.__running
	def endBot(self):
		self.__running = False

#-------------------------------------#
# Interfaz API
#
class API(ABC):
	def buy(self,price):
		pass
	def sell(self,price):
		pass
