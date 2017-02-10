import csv
import os
import dlib
import time
from skimage import io 
import glob
from collections import defaultdict


def addAuthorToImage():
	files = glob.glob("./bl2/*/*.jpg")
	autorDict = defaultdict(list)

	with open('ISBN+Authors.tsv','rb') as tsvin:
	    tsvin = csv.reader(tsvin, delimiter='\t')
	    for row in tsvin:
	    	for a in files:
	    		if row[0] in a:
	    			autorDict[row[1]].append([row[0], a])


	f = open('authordict.csv', 'w')
	for key, value in autorDict.iteritems():
		for item in value:
			f.write(key + "," + item[1] + "\n")
	f.close()
	
