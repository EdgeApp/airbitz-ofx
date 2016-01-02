#concrete provider class for handling amazon payments csv

from abstractprovider import AbstractProvider

class airbitzwallets(AbstractProvider):

	__providerID = ''
	__providerName = ''

	def __init__(self):
			self.__providerID = 'airbitz'
			self.__providerName = 'Airbitz Wallets'

	def getID(self):
		return self.__providerID

	def getName(self):		
		return self.__providerName

	@staticmethod
	def getDatePosted(self, row):
		return row.get('DATE')

	@staticmethod
	def getTxnMemo(self, row):
		return row.get('NOTES')

	@staticmethod
	def getTxnCurAmt(self, row):
		return row.get('USD')

	@staticmethod
	def getTxnCategory(self, row):
		return row.get('CATEGORY')

	@staticmethod
	def getTxnId(self, row):
		return row.get('TXID')

	@staticmethod
	def getTxnAmount(self,row):
		return row.get('AMT_BTC')

	@staticmethod
	def getTxnName(self,row):
		return row.get('PAYEE_PAYER_NAME')

