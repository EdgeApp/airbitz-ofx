#####################################################################
#																	#
#	File: csvtoqbo.py												#
#	Developer: Paul Puey											#
#	Original Code by: Justin Leto									#
#	Forked from https://github.com/jleto/csvtoqbo					#
#																	#
#	main utility script file Python script to convert CSV files		#
#	of transactions exported from various platforms to QBO for		#
#	import into Quickbooks Online. 									#
#																	#
#	Usage: python csvtoqbo.py <options> <csvfiles>					#
#																	#
#####################################################################

import sys, traceback
import os
import logging
import csv
import qbo
import airbitzwallets

#	If only utility script is called
if len(sys.argv) <= 1:
	sys.exit("Usage: python %s <options> <csvfiles>\n"
		     "Where possible options include:\n"
			 "   -btc     Output bitcoin in full BTC denomination\n"
		     "   -mbtc    Output bitcoin in mBTC denomination\n"
		     "   -bits    Output bitcoin in bits (uBTC) denomination" % sys.argv[0]
			)
#	If help is requested
elif (sys.argv[1] == '--help'):
	sys.exit("Help for %s not yet implemented." % sys.argv[0])

#	Test for valid options, instantiate appropiate provider object
if sys.argv[1] == '-mbtc':
	denom = 1000
elif sys.argv[1] == '-btc':
	denom = 1
elif sys.argv[1] == '-bits':
	denom = 1000000

myProvider = airbitzwallets.airbitzwallets()

#	For each CSV file listed for conversion
for arg in sys.argv:
	if sys.argv.index(arg) >  1:
		
		try:
			with open(arg[:len(arg)-3] + 'log'): 
				os.remove(arg[:len(arg)-3] + 'log')
		except IOError:
		   pass

		logging.basicConfig(filename=arg[:len(arg)-3] + 'log', level=logging.INFO)
		logging.info("Opening '%s' CSV File" % myProvider.getName())

		try:

			with open(arg, 'r') as csvfile:

				# Open CSV for reading
				reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
				
				#instantiate the qbo object
				myQbo = None
				myQbo = qbo.qbo()
				txnCount = 0
				for row in reader:
					txnCount = txnCount+1
					sdata = str(row)

					#read in values from row of csv file
					date_posted = myProvider.getDatePosted(myProvider,row)
					txn_memo = myProvider.getTxnMemo(myProvider,row)
					txn_amount = myProvider.getTxnAmount(myProvider,row)
					txn_curamt = myProvider.getTxnCurAmt(myProvider,row)
					txn_category = myProvider.getTxnCategory(myProvider,row)
					txn_id = myProvider.getTxnId(myProvider,row)
					name = myProvider.getTxnName(myProvider,row)

					try:
                                                #Add transaction to the qbo document
                                                if myQbo.addTransaction(denom, date_posted, txn_memo, txn_id, txn_amount, txn_curamt, txn_category, name):
                                                        print('Transaction [' + str(txnCount) + '] added successfully!')
                                                        logging.info('Transaction [' + str(txnCount) + '] added successfully!')				

					except:
                                                #Error adding transaction			
                                                exc_type, exc_value, exc_traceback = sys.exc_info()
                                                lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                                                print(''.join('!! ' + line for line in lines))
                                                logging.info("Transaction [" + str(txnCount) + "] excluded!")
                                                logging.info('>> Data: ' + str(sdata))
                                                pass

		except:
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                        print(''.join('!! ' + line for line in lines))
                        logging.info("Trouble reading CSV file!")
                        
		# After transactions have been read, write full QBO document to file 
		try:
			filename = arg[:len(arg)-3] + 'qbo'
			if myQbo.Write('./'+ filename):
				print("QBO file written successfully!")
				#log successful write
				logging.info("QBO file %s written successfully!" % filename)

		except:
			#IO Error			
			exc_type, exc_value, exc_traceback = sys.exc_info()
			lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
			print(''.join('!! ' + line for line in lines))
			logging.info(''.join('!! ' + line for line in lines))
