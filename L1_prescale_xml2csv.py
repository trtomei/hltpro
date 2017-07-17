### L1_prescale_xml2csv.py
# Author: Thiago R. F. P. Tomei
# Date: 2017-06-29
# Version: v1

# This script takes two XMLs as input: the RunSettings key (i.e. the L1 prescales)
# and the L1Menu. It outputs into stdout the same information as the XML but in CSV
# format. We pad out unused bits with empty names and columns of zeros.
# This can then be pasted back into the GoogleDocs for book-keeping.
# Mostly useful for when the L1 menu changes.
# The logic is: L1 Menu maps numbersToNames, RunSettings key maps namesToColumns

import xml.etree.ElementTree as ET

L1PrescalesName = "UGT_RS_CLOBS_ugt_rs_algo_prescale_circulating_v2_CONF.xml"
L1MenuName = "L1Menu_Collisions2017_v1_m6.xml"

numbersToNames = dict()
namesToColumns = dict()

# L1 Prescales
L1PrescalesTree = ET.parse(L1PrescalesName)
L1Prescales = L1PrescalesTree.getroot()
columnsrow = L1Prescales[0][1][0].text.split(",")
columnNames = [x.split(":")[1] for x in columnsrow[1:]]
nColumns = len(columnNames)
defaultColumn = int(L1Prescales[0][0].text)

listOfPrescales = L1Prescales.findall(".//row") #Using XPath, find everything named "row" in the tree
for row in listOfPrescales:
	row2 = row.text.split(',')
	bitName = row2[0].strip() # We strip whitespace at the beginning and end of the bitName 
	prescaleRow = [int(ps) for ps in row2[1:]] 
	namesToColumns[bitName] = prescaleRow
	
# L1 Menu
L1MenuTree = ET.parse(L1MenuName)
L1Menu = L1MenuTree.getroot()
listOfAlgos = L1Menu.findall("algorithm")
for algo in listOfAlgos:
	bitNumber = int(algo.find("index").text)
	bitName = algo.find("name").text
	numbersToNames[bitNumber] = bitName

# We need to prepend the column names with a single quote to ensure that GoogleDocs doesn't transform strings like "2.0E34" into numbers...
maxAlgo = max(numbersToNames.keys())	
print "Default"+","+columnNames[defaultColumn]
print "Bit"+","+"Algo name"+","+(",".join(["'"+cn for cn in columnNames]))

# We print into stdout
for bit in range(0,maxAlgo+1):
	if bit in numbersToNames.keys(): # This bit is defined in the L1 menu
		bitName = numbersToNames[bit]
		if bitName in namesToColumns: # We have prescales for this bit
			prescaleRow = namesToColumns[bitName]
			print str(bit)+","+bitName+","+(",".join([str(ps) for ps in prescaleRow]))
		else: # We don't have prescales for this bit. Put 0 for the time being
			print str(bit)+","+bitName+","+(",".join(["0"]*nColumns))
	else: # L1 doesn't define this bit. Put 0
		print str(bit)+","+' '+","+(",".join(["0"]*nColumns))
		
