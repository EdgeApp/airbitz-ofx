#####################################################################
#																	#
#	File: qbo.py													#
#	Developer: Justin Leto											#
#																	#
#	qbo class provides an interface from main csv iterator method	#
#	to handle qbo formatting, validations, and writing to file.		#
#																	#
#	Usage: python csvtoqbo.py <options> <csvfiles>					#
#																	#
#####################################################################

import sys, traceback
import os
from datetime import datetime
import logging
import qboconst

class qbo:

	#	Holds a list of valid transactions via the addTransaction() method
	__transactions = list()

	#	The full QBO document build from constants and transactions
	__document = None

	#	Flag indicating whether the QBO document is valid
	__isValid = None

	#	constructor
	def __init__(self):
		#	Reads in constant values from file, set to private (const) variables
		self.__HEADER = qboconst.HEADER
		self.__FOOTER = qboconst.FOOTER
		self.__DATE_START = qboconst.DATE_START
		self.__DATE_END = qboconst.DATE_END
		self.__BANKTRANLIST_START = qboconst.BANKTRANLIST_START
		self.__BANKTRANLIST_END = qboconst.BANKTRANLIST_END
		self.__TRANSACTION_START = qboconst.TRANSACTION_START
		self.__TRANSACTION_END = qboconst.TRANSACTION_END

		#	Set document to valid
		self.__isValid = True
	

	# PUBLIC GET METHODS for constant values - used in unit testing.
	#
	#
	def getHEADER(self):
		return self.__HEADER

	def getFOOTER(self):
		return self.__FOOTER

	def getDATE_START(self):
		return self.__DATE_START

	def getDATE_END(self):
		return self.__DATE_END
	
	def getBANKTRANLIST_START(self):
		return self.__BANKTRANLIST_START

	def getBANKTRANLIST_END(self):
		return self.__BANKTRANLIST_END

	def getTRANSACTION_START(self):
		return self.__TRANSACTION_START

	def getTRANSACTION_END(self):
		return self.__TRANSACTION_END
	
	#	method to validate paramters used to submit transactions
	def validateTransaction(self, status, date_posted, txn_type, to_from_flag, txn_amount, txn_exrate, name):

		# if str.lower(status) != 'completed':
		# 	#log status failure
		# 	logging.info("Transaction status [" + status + "] invalid.")
		# 	raise Exception("Transaction status [" + status + "] invalid.")
        #
		#if type(datetime.strptime(str(date_posted), '%m/%d/%Y')) is not datetime:
		#	logging.info("Transaction posted date [" + date_posted + "] invalid.")
		#	raise Exception("Transaction posted date [" + date_posted + "] invalid.")

		# if str.lower(txn_type) not in ('payment','refund','withdrawal', 'withdraw funds', 'send', 'receive'):
		# 	logging.info("Transaction type [" + str(txn_type) + "] not 'Payment', 'Refund', 'Withdraw Funds', or 'Withdrawal'.")
		# 	raise Exception("Transaction type [" + str(txn_type) + "] not 'Payment', 'Refund', 'Withdraw Funds', or 'Withdrawal'.")
        #
		# if str.lower(to_from_flag) not in ('to', 'from'):
		# 	logging.info("Transaction 'To/From' field [" + to_from_flag + "] invalid.")
		# 	raise Exception("Transaction 'To/From' field [" + to_from_flag + "] invalid.")
        #
		# #logical test of txn_type and to_from_flag
		# if ((str.lower(txn_type) == 'refund' and str.lower(to_from_flag) != 'to') or (str.lower(txn_type) == 'payment' and str.lower(to_from_flag) != 'from')):
		# 	logging.info("Transaction type inconsistent with 'To/From' field.")
		# 	raise Exception("Transaction type inconsistent with 'To/From' field.")
        #
		if len(name) == 0 or not name:
			logging.info("Transaction name empty or null.")
			raise Exception("Transaction name empty or null.")

		return True

	#	Add transaction takes in param values uses the required formatting QBO transactions
	#	and pushes to list
	def addTransaction(self, denom, date_posted, txn_memo, txn_id, txn_amount, txn_curamt, txn_category, name):
		
		# try:
		# 	#	Validating param values prior to committing transaction
		# 	self.validateTransaction(status, date_posted, txn_type, txn_id, txn_amount, name)
		# except:
		# 	raise Exception

		#	Construct QBO formatted transaction
		transaction = ""

		day = ""
		month = ""
		date_array = date_posted.split('-')
		day = date_array[2]
		month = date_array[1]
		year  = date_array[0]
		if len(day) == 1:
			day = "0"+day
		if len(month) ==1:
			month = "0"+month
			
		rec_date = datetime.strptime(year+"/"+month+"/"+day, '%Y/%m/%d')
		rec_date = rec_date.strftime('%Y%m%d%H%M%S') + '.000'

		dtposted = '  <DTPOSTED>' + rec_date

		if float(txn_amount) > 0:
			trtype = '  <TRNTYPE>CREDIT'
		else:
			trtype = '  <TRNTYPE>DEBIT'
		#
		# if str.lower(txn_type) == 'receive':
		# 	trtype = '<TRNTYPE>CREDIT'
		# elif str.lower(txn_type) == 'send':
		# 	trtype = '<TRNTYPE>DEBIT'

		# if str.lower(txn_type) in ('refund', 'withdrawal', 'withdraw funds'):
		# 	tramt = '<TRNAMT>-' + str(txn_amount).replace('$','')
		# else:
		# 	tramt = '<TRNAMT>' + str(txn_amount).replace('$','')

		tramtbits = float(txn_amount) * denom
		tramt = '  <TRNAMT>' + str(tramtbits)

		if name:
			trname = '  <NAME>' + str(name) + "\n"
		else:
			trname = ''

		exrate = float(txn_curamt) / (tramtbits)
		curamt = "{0:0.2f}".format(abs(float(txn_curamt)))
		fmtexrate = "{0:0.6f}".format(float(exrate))

		rawmemo = 'Rate=' + fmtexrate + " USD=" + curamt + " category=\"" + str(txn_category) + "\" memo=\"" + str(txn_memo)
		memo = '  <MEMO>' + rawmemo[:253] + "\"\n"

		fitid = '  <FITID>' + str(txn_id)
		exrate = '    <CURRATE>' + fmtexrate

		transaction = ("" + self.__TRANSACTION_START + "\n"
						"" + trtype + "\n"
						"" + dtposted + "\n"
						"" + tramt + "\n"
						"" + fitid + "\n"
						"" + trname +
						"" + memo +
						"" + "  <CURRENCY>" + "\n"
						"" + exrate + "\n"
						"" + "    <CURSYM>USD" + "\n"
						"" + "  </CURRENCY>" + "\n"
						"" + self.__TRANSACTION_END + "\n")

		#	Commit transaction to the document by adding to private member list object
		self.__transactions.append(transaction)

		logging.info("Transaction [" + str(self.getCount())  + "] Accepted.")
		return True

	#	get the current number of valid committed transactions
	def getCount(self):
		return len(self.__transactions)

	#	get the valid status of the document
	def isValid(self):
		#	If number of valid transactions are 0 document is invalid
		if self.getCount() == 0:
			self.__isValid = False
		return self.__isValid

	#	get the text of the document
	def getDocument(self):
		self.Build()
		return self.__document

	#	Construct the document, add the transactions
	#	save str into private member variable __document
	def Build(self):
		if not self.isValid():
			logging.info("Error: QBO document is not valid.")
			raise Exception("Error: QBO document is not valid.")

		self.__document = ("" + self.__HEADER + "\n"
					"" + self.__BANKTRANLIST_START + "\n"
					"" + self.__DATE_START + "\n"
					"" + self.__DATE_END + "\n")

		for txn in self.__transactions:
			self.__document = self.__document + str(txn)
		
		self.__document = self.__document + ("" + self.__BANKTRANLIST_END + "\n"
							   "" + self.__FOOTER + "")

	#	Write QBO document to file
	def Write(self, filename):

		try:

			with open(filename, 'w') as f:
				#	getDocument method will build document
				#	test for validity and return string for write
				f.write(self.getDocument())

			return True

		except:
			#log io error return False
			exc_type, exc_value, exc_traceback = sys.exc_info()
			lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
			print(''.join('!! ' + line for line in lines))
			logging.info('qbo.Write() method: '.join('!! ' + line for line in lines))
			return False
