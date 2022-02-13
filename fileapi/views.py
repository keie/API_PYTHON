from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import argparse
import imutils 
import cv2
import base64
import random
import os

#Import for neural network

def test():

	return Response("it works!")


def scanner(indexQuestion,file2,json_questions):

	
	# print ("################ENTRO EN SCANNER###############")
	
	ANSWER_KEY = {0: 1, 1: 4, 2: 0, 3: 3, 4: 1}
	answersArray = []
	img = base64.b64decode(file2); 
	npimg = np.fromstring(img, dtype=np.uint8); 
	image = cv2.imdecode(npimg, 1)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (5, 5), 0)
	edged = cv2.Canny(blurred, 75, 200)
	
	cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	docCnt = None

	if len(cnts) > 0:
		
		cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
		paperimage = []
		
		for c in cnts:
			
			peri = cv2.arcLength(c, True)
			approx = cv2.approxPolyDP(c, 0.02 * peri, True)

			if len(approx) == 4:
				docCnt = approx
				paperimage = c
				break

	paper = four_point_transform(image, docCnt.reshape(4, 2))
	warped = four_point_transform(gray, docCnt.reshape(4, 2))

	paper = image
	warped = gray

	
	blurredWarped = cv2.GaussianBlur(warped, (21,21), 0)
	
	blurredThresh = cv2.threshold(blurredWarped, 0, 255,
	cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
	thresh = cv2.threshold(warped, 0, 255,
		cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

	cnts = cv2.findContours(blurredThresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	questionCnts = []


		
	imS = cv2.resize(blurredThresh, (750,1000))   
	# cv2.imshow("paper", imS)
	# cv2.waitKey(0)

	for c in cnts:
		
		(x, y, w, h) = cv2.boundingRect(c)
		ar = w / float(h)
		# print(h,w,ar)
		# box
		if w >= 1000 and h >= 250 and ar > 0.5:
			questionCnts.append(c)
			
		# bubble
		if w >= 80 and h >= 80 and ar >= 0.8 and ar <= 1.5:
			questionCnts.append(c)

	questionCnts = contours.sort_contours(questionCnts,
		method="top-to-bottom")[0]
	correct = 0

	
	p = paper.copy()
	for ct in questionCnts:
		pass
		cv2.drawContours(p, [ct], -1, (random.randint(1,254),random.randint(1,254),random.randint(1,254)), -1)

		
	# imS = cv2.resize(p, (750,1000))   
	# cv2.imshow("paper", imS)
	# cv2.waitKey(0)
	

	#armo el array de longitudes de las respuestas
	array_lenght = []
	totalAnswers = 0
	iq = indexQuestion
	# print(json_questions    )
	# print("len(questionCnts): " + str(len(questionCnts)))
	while ( totalAnswers < len(questionCnts) ):
		# print("entro " + str(iq) + " totalAnswers " + str(totalAnswers))
		lenAnswers = len(json_questions['questions'][iq]['answers'])
		if(lenAnswers == 0):
			lenAnswers = 1 
		array_lenght.append(lenAnswers)
		totalAnswers = totalAnswers + lenAnswers
		if (iq != (len(questionCnts)-1)):
			iq = iq + 1

	# print(array_lenght)
	stop = 0
	i = 0
	start = 0
	while i < len(array_lenght):
		# print("array_lenght[i] ",array_lenght[i])
		#Preguntas de seleccion simple, seleccion multiple, escala
		stop = stop + array_lenght[i] 
		actualcnts = questionCnts[start : stop]
		# print("i, start, stop")
		# print(i, start, stop)
		cnts = contours.sort_contours(questionCnts[start : stop])[0]
		bubbled = None
		start = stop 
		answer = None
		# print("entro (i+indexQuestion)" + str(i+indexQuestion) + " " + str(json_questions['questions'][i+indexQuestion]['type']))
		if(str(json_questions['questions'][i+indexQuestion]['type']) == "ssimple" or str(json_questions['questions'][i+indexQuestion]['type'] == "scala") ):
			answer = simple(cnts, thresh)
		if(str(json_questions['questions'][i+indexQuestion]['type']) == "smultiple"):
			answer = multiple(cnts, thresh)
		if(str(json_questions['questions'][i+indexQuestion]['type']) == "development"):
			answer = ""
		answersArray.append(answer)
		i = i + 1

	# grab the test taker
	
	return (answersArray)


def simple(cnts, thresh):
	bubbled = None
	for (j, c) in enumerate(cnts):
		mask = np.zeros(thresh.shape, dtype="uint8")
		cv2.drawContours(mask, [c], -1, 255, -1)
		mask = cv2.bitwise_and(thresh, thresh, mask=mask)
		total = cv2.countNonZero(mask)
		if bubbled is None or total > bubbled[0]:
			bubbled = (total, j)
	return bubbled[1]


def multiple(cnts, thresh):
	answers = []
	validCheck = 4000
	for (j, c) in enumerate(cnts):
		mask = np.zeros(thresh.shape, dtype="uint8")
		cv2.drawContours(mask, [c], -1, 255, -1)
		mask = cv2.bitwise_and(thresh, thresh, mask=mask)
		total = cv2.countNonZero(mask)
		if total > validCheck:
			answers.append(j)
	return answers
