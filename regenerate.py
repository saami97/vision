import cv2
import numpy as np

import os

eyeCascade = cv2.CascadeClassifier("haarcascade_eye.xml")
faceCascade = cv2.CascadeClassifier("face_cascade.xml")

currentDir = os.path.dirname(os.path.realpath(__file__))

def detectFaces(grayImg):
	faces = faceCascade.detectMultiScale(grayImg,1.1,5)
	print(faces)
	if not np.any(faces):
		return False
	return True

def regenerateImg(imgPath):
	shifts = [0,5,10,20,25,30,32,35]
	for j in  range(0,2):
		i=0
		while(i<len(shifts)):
			imageGray = cv2.imread(imgPath)
			if(j==1):
				imageGray = cv2.flip(imageGray,1)
			eyes = eyeCascade.detectMultiScale(imageGray,1.2,8)
			if(np.any(eyes)):
				height = imageGray.shape[0]
				width = imageGray.shape[1]
				imageCrop = imageGray[0:height,0:(eyes[0][0]+eyes[0][2]+shifts[i])]
				imageFlip = cv2.flip(imageCrop,1)
				newimage = np.concatenate((imageCrop,imageFlip),1)
				if detectFaces(newimage):
					cv2.imwrite("regenerated-images/regenerated"+str(i)+".jpg",newimage)
			i += 1
