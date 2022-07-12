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

MIN_WIDTH_BUBBLE=70
MAX_WIDTH_BUBBLE=110
MIN_HEIGHT_BUBBLE=70
MAX_HEIGHT_BUBBLE=110
MIN_AR_BUBBLE=0.8
MAX_AR_BUBBLE=1.5
MIN_WIDTH_BOX=1000
MAX_WIDTH_BOX=1700
MIN_HEIGHT_BOX=250
MAX_HEIGHT_BOX=950
MIN_AR_BOX=0.5

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
	
	# imS = cv2.resize(image, (750,1000))   
	# cv2.imshow("paper", imS)
	# cv2.waitKey(0)
	
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
	# paper = four_point_transform(image, docCnt.reshape(4, 2))
	# warped = four_point_transform(gray, docCnt.reshape(4, 2))

	paper = image
	warped = gray
	
	thresh = cv2.threshold(warped, 0, 255,
		cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

	
	blurredWarped = cv2.GaussianBlur(warped, (21,21), 0)

	# imS = cv2.resize(blurredWarped, (750,1000))   
	# cv2.imshow("blurredWarped", imS)
	# cv2.waitKey(0)
	
	blurredThresh = cv2.threshold(blurredWarped, 0, 255,
	cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

	
		
	# imS = cv2.resize(blurredThresh, (750,1000))   
	# cv2.imshow("blurredThresh", imS)
	# cv2.waitKey(0)

	cnts = cv2.findContours(blurredThresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	questionCnts = []


	for c in cnts:
		
		(x, y, w, h) = cv2.boundingRect(c)
		ar = w / float(h)
		# print(w,h,ar)
		# box
		if w >= MIN_WIDTH_BOX and w <= MAX_WIDTH_BOX and h >= MIN_HEIGHT_BOX and h <= MAX_HEIGHT_BOX and ar > MIN_AR_BOX:
			questionCnts.append(c)
			
		# bubble
		if w >= MIN_WIDTH_BUBBLE and w <= MAX_WIDTH_BUBBLE and h >= MIN_HEIGHT_BUBBLE and h <= MAX_HEIGHT_BUBBLE and ar >= MIN_AR_BUBBLE and ar <= MAX_AR_BUBBLE:
			questionCnts.append(c)

	if (len(questionCnts) == 0):
		print('NO HAY CONTORNOS O HAY UN ERROR EN LA IMAGE')
		return None

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
		if(str(json_questions['questions'][i+indexQuestion]['type']) == "ssimple" or str(json_questions['questions'][i+indexQuestion]['type']) == "scala" ):
			answer = simple(cnts, thresh)
		if(str(json_questions['questions'][i+indexQuestion]['type']) == "smultiple"):
			answer = multiple(cnts, thresh)
		if(str(json_questions['questions'][i+indexQuestion]['type']) == "development"):
			answer = ""
		answersArray.append(answer)
		i = i + 1
	
	# imS = cv2.resize(p3, (750,1000))   
	# cv2.imshow("paper", imS)
	# cv2.waitKey(0)

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
			bubbled = (total, j, c)
	# cv2.drawContours(p3, [bubbled[2]], -1, (255 ,0 ,0 ), -1)
	return bubbled[1]


def multiple(cnts, thresh):
	answers = []
	# CTNLIST = []
	validCheck = 4000
	for (j, c) in enumerate(cnts):
		mask = np.zeros(thresh.shape, dtype="uint8")
		cv2.drawContours(mask, [c], -1, 255, -1)
		mask = cv2.bitwise_and(thresh, thresh, mask=mask)
		total = cv2.countNonZero(mask)
		if total > validCheck:
			answers.append(j)
			# CTNLIST.append(c)
	# for ct in CTNLIST:
	# 	pass
	# 	cv2.drawContours(p3, [ct], -1, (0,255,0), -1)
	return answers
