open('__init__.py', 'a')
import os
import csv
import cv2
from skimage import io
from getAuthors import makeSeperateDir, seperatePortraits, makeAuthorDirFromFile
from readtsv import addAuthorToImage
from makeDir import createAuthorFolders
from affine import makeAffine


if __name__ == '__main__':

	# Start
	print "Welcome to the book cover parser \nChoose one of the following options \n1: Seperate the portrets \n2: Sort authors into files with their name"
	print "3: Do an afine transformation and place in folders\n4: Generate embeddings for neural net"
	print "5: Train neural net\n6: Test neural net"

	choose = raw_input()
	if choose == "1":
		makeSeperateDir()
		seperatePortraits()
	elif choose == "2":
		addAuthorToImage()
		makeAuthorDirFromFile()
		createAuthorFolders()
	elif choose == "3":
		if not os.path.exists("./aligned-images/"):
			os.makedirs("./aligned-images/")
		with open('onlyAuthor.csv','rb') as csvfile:
			read = csv.reader(csvfile, delimiter=',')
			for row in read:
				img = io.imread(row[1])
				afineImg = makeAffine(img)

				authorDir = "./aligned-images/" + row[0]
				if not os.path.exists(authorDir):
					os.makedirs(authorDir)

				dirImg = row[1].split("/")
   				nameImg = authorDir + "/aligned-" + dirImg[-1]

   				image_to_write = cv2.cvtColor(afineImg, cv2.COLOR_RGB2BGR)

   				print nameImg
				cv2.imwrite(nameImg, image_to_write)

	elif choose == "4":
		if not os.path.exists('./generated-embeddings'):
			os.mkdir('generated-embeddings')
		os.system('./batch-represent/main.lua' +
                  ' -outDir ./generated-embeddings/' +
                  ' -data ./aligned-images/ ')
	elif choose == '5':
		os.system('./demos/classifier.py train ./generated-embeddings/')
	elif choose == '6':
		print "what is the name of the folder containting the test cases?"
		directory = raw_input()
		if os.path.exists('./{}/'.format(directory)):
			image_paths = \
			[os.path.join(directory, f) for f in os.listdir('./{}/'\
                                                           .format(directory))]
			for photo in image_paths:
				os.system("./demos/classifier.py infer ./generated-embeddings/classifier.pkl " + photo)
		else:
			print "Directory does not exist"