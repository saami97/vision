import openface
import numpy as np
import os
import cv2
import time

np.set_printoptions(precision=2)

rootDir = os.path.dirname(os.path.realpath(__file__))
dlibFileDir = os.path.join(rootDir,'shape_predictor_68_face_landmarks.dat')
torchDir = os.path.join(rootDir,'nn4.small2.v1.t7');

start = time.time()

align = openface.AlignDlib(dlibFileDir)
net = openface.TorchNeuralNet(torchDir,96)

def getScore(imagePath):
	bgrimage = cv2.imread(imagePath)
	if bgrimage is None:
		raise Exception("Unable to load the image path.")
	rgbImg = cv2.cvtColor(bgrimage, cv2.COLOR_BGR2RGB)
	start = time.time()
    	bb = align.getLargestFaceBoundingBox(rgbImg)
	if bb is None:
        	return 0
	alignedFace = align.align(96, rgbImg, bb, landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
	if alignedFace is None:
        	return 0
	start = time.time()
    	rep = net.forward(alignedFace)
	return rep

def calculateScore(imgPath1,imgPath2):
	d = getScore(imgPath1) - getScore(imgPath2)
	d = format(np.dot(d, d))
	d = float(d)
	return d

def batchCompare(score1,score2):
	d = score1 - score2
	d = format(np.dot(d, d))
	d = float(d)
	return d
