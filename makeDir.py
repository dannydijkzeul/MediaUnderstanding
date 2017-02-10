import os
import csv
from shutil import copyfile

def createAuthorFolders():

	if not os.makedirs("./training-images/"):
		os.makedirs("./training-images/")

	with open('onlyAuthor.csv', 'rb') as inputFile:
	    inputFile = csv.reader(inputFile, delimiter=',')
	    for row in inputFile:
	   		pathDir = "./training-images/" + row[0]
	   		dirImg = row[1].split("/")
	   		newImg = pathDir + "/" + dirImg[-1]
	   		if os.path.exists(pathDir):
	   			copyfile(row[1], newImg)
	   		else:
	   			os.makedirs(pathDir)