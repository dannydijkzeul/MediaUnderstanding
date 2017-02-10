import sys
import dlib
import os
import time
import openface
from skimage import io 
import shutil
import cv2
import csv
from collections import defaultdict

def makeSeperateDir():
	if not os.path.exists("./allPortraits/"):
		os.makedirs("./allPortraits/")

	if not os.path.exists("./croppedPortraits/"):
		os.makedirs("./croppedPortraits/")

def seperatePortraits():
	path = "./" + raw_input('Give directory of of bookcovers: ')

	showWindow = raw_input('Do you want to show the images [y/N]: ') or "N"

	image_paths = [os.path.join(path, f) for f in os.listdir(path)]

	face_detector = dlib.get_frontal_face_detector()

	if showWindow == "y":
		win = dlib.image_window()

	for j in image_paths:
		image = io.imread(j)

		detected_faces = face_detector(image, 1)

		print("I found {} faces in the file {}".format(len(detected_faces), j))

		PADDING = len(image)/20
		for i, face_rect in enumerate(detected_faces):
			# Detected faces are returned as an object with the coordinates 
			# of the top, left, right and bottom edges
			print("- Face #{} found at Left: {} Top: {} Right: {} Bottom: {}".format(i, face_rect.left(), face_rect.top(), face_rect.right(), face_rect.bottom()))
			image_face = image[face_rect.top()-PADDING:face_rect.bottom()+PADDING,face_rect.left()-PADDING:face_rect.right()+PADDING]	

			if  showWindow == "y":
				win.set_image(image)
				win.add_overlay(face_rect)
				time.sleep(1)
				win.clear_overlay()

			if len(detected_faces) == 1:

				dirImg = j.split("/")
   				nameImg = "./croppedPortraits/cropped-" + dirImg[-1]

   				image_to_write = cv2.cvtColor(image_face, cv2.COLOR_RGB2BGR)

				shutil.move(j,"./allPortraits/")
				cv2.imwrite(nameImg, image_to_write)
				if  showWindow == "y":
					win.set_image(image_face)

					# Draw the face landmarks on the screen.				
					time.sleep(1)



def makeAuthorDirFromFile():
	showWindow = raw_input('Do you want to show the images [y/N]: ') or "N"

	pathArray = []
	authorArray = []

	with open('authordict.csv','rb') as csvfile:
		read = csv.reader(csvfile, delimiter=',')
		for row in read:
			pathArray.append(row[1])
			authorArray.append(row[0])

	face_detector = dlib.get_frontal_face_detector()

	classArray = defaultdict(list)
	predictor_model = "shape_predictor_68_face_landmarks.dat"

	face_detector = dlib.get_frontal_face_detector()
	face_pose_predictor = dlib.shape_predictor(predictor_model)

	if showWindow == "y":
		win = dlib.image_window()

	for idx, i in enumerate(pathArray):
		try:
			image = io.imread(i)

			detected_faces = face_detector(image, 1)

			print("I found {} faces in the file {}".format(len(detected_faces), i))

		 	if len(detected_faces) == 1:
		 		classArray[authorArray[idx]].append(i)

		 	if showWindow == "y":
		 		win.set_image(image)

		 		for i, face_rect in enumerate(detected_faces):

					# Detected faces are returned as an object with the coordinates 
					# of the top, left, right and bottom edges
					print("- Face #{} found at Left: {} Top: {} Right: {} Bottom: {}".format(i, face_rect.left(), face_rect.top(), face_rect.right(), face_rect.bottom()))

					pose_landmarks = face_pose_predictor(image, face_rect)

					win.set_image(image)

					# Draw the face landmarks on the screen.
					win.add_overlay(pose_landmarks)
					win.add_overlay(face_rect)
				
				time.sleep(1)	
				win.clear_overlay()
		except IOError:
			print "A corrupt image has been found and has been skipped"

	with open('onlyAuthor.csv', 'w') as f:
		for key, value in classArray.iteritems():
			for item in value:
				f.write(key + "," + item + "\n")
