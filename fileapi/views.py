from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

# from .models import FileApi
# from fileapi.serializers import FileApiSerializer

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

import matplotlib.pyplot as plt
import tensorflow as tf
# from tensorflow.keras.preprocessing import image
# from tensorflow.keras.preprocessing.image import img_to_array
# import keras
# from keras.models import load_model 


# @api_view(['GET',])
# def api_get_file_view(request,id):
# 	try:
# 		file_api = FileApi.objects.get(id=id)
# 	except FileApi.DoesNotExist:
# 		return Response(status=status.HTTP_404_NOT_FOUND)

# 	if(request.method == "GET"):
		
# 		serializer = FileApiSerializer(file_api)
# 		return Response(serializer.data)
		
		
# @api_view(['POST',])
# def api_post_file_view(request):
# 	file_api = FileApi()
# 	if(request.method == "POST"):
# 		serializer = FileApiSerializer(file_api,data=request.data)
		
# 		scanner(request.data['file2']) 
# 		if(serializer.is_valid()):
# 			serializer.save()
# 			return Response(serializer.data,status=status.HTTP_201_CREATED)
# 		return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)

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
		if w >= 1000 and h >= 400 and ar > 0.5:
			questionCnts.append(c)
			
		# bubble
		if w >= 124 and h >= 131 and ar >= 0.8 and ar <= 1.5:
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
			answer = development(cnts,thresh,paper)
		answersArray.append(answer)
		i = i + 1

	# grab the test taker
	
	# print ("################SALIO DE SCANNER###############")
	# print (answersArray)
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
	validCheck = 50000 
	for (j, c) in enumerate(cnts):
		mask = np.zeros(thresh.shape, dtype="uint8")
		cv2.drawContours(mask, [c], -1, 255, -1)
		mask = cv2.bitwise_and(thresh, thresh, mask=mask)
		total = cv2.countNonZero(mask)
		if total > validCheck:
			answers.append(j)
	return answers

def development(cnts,thresh,paper):
	textAnswer = ""
	textLine = ""

	
	#DENSE Model
	print("ESTE ES LA RUTA")
	print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
	# new_model = tf.keras.models.load_model(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/fileapi/emnist_trained_dense.h5')

	# NUEVO MODELO
	new_model = tf.keras.models.load_model(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/fileapi/letras_y_nn_final.h5')

	
	# new_model = tf.keras.models.load_model('C:/Users/oswal/Documents/UCAB/Tesis/Proyecto/Scanner/API_PYTHON/fileapi/new.h5')


	# # #CNN Model
	# new_model = tf.keras.models.load_model('C:/Users/oswal/Documents/UCAB/Tesis/Proyecto/Scanner/API_PYTHON/fileapi/emnist_trained.h5')
	
	# #CNN YUCA Model
	# new_model = tf.keras.models.load_model('C:/Users/oswal/Documents/UCAB/Tesis/Proyecto/Scanner/API_PYTHON/fileapi/emnist_trained_yuca.h5')


	# letters ={0:0,1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9,
	# 10:'A',11:'B',12:'C',13:'D',14:'E',15:'F',16:'G',17:'H',18:'I',19:'J',
	# 20:'K',21:'l',22:'M',23:'N',24:'O',25:'P',26:'Q',27:'R',28:'S',29:'T',
	# 30:'u',31:'V',32:'W',33:'X',34:'Y',35:'Z',36:'a',37:'b',38:'d',39:'e',
	# 40:'f',41:'g',42:'h',43:'n',44:'q',45:'r',46:'t',47:'அ',48:'ஆ'}


	letters = {
		0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',6:'G',7:'H',8:'I',9:'J',
		10:'K',11:'L',12:'M',13:'N',14:'O',15:'P',16:'Q',17:'R',
		18:'S',19:'T',20:'U',21:'V',22:'W',23:'X', 24:'Y',25:'Z', 26: 'Ñ'
	}


	x,y,w,h = cv2.boundingRect(cnts[0])

	# cuadrito = thresh[y+4 : y+27 , x + 4: x + 27] #tamano del cuadrito

	box = thresh[y+3 : y+h -3 , x+3 : x + w - 3] #tamano de la caja de la respuesta de desarrollo
	boxPaper = paper[y+3 : y+h -3 , x+3 : x + w - 3] #tamano de la caja de la respuesta de desarrollo

	
	# cv2.imshow("box", box)
	# cv2.waitKey(0)
	

	#####################################################CODIGO MEDIUM PARA DETECTAR CUADRADOS#########################################################

	ctnsBox = getCntsBoxs(box,boxPaper)
	
	idx = 0

	print(len(ctnsBox))
	startBox = 0
	stopBox = startBox + 19

	textAnswer1 = ""
	textAnswer2 = ""

	while idx < 4:
		
		partCtnsBox = contours.sort_contours(ctnsBox[startBox : stopBox ])[0]

		startBox = stopBox
		stopBox = startBox+19
		for c in partCtnsBox:

			xBoxito, yBoxito, wBoxito, hBoxito = cv2.boundingRect(c)
			# print(xBoxito, yBoxito, wBoxito, hBoxito)
			if (wBoxito > 17 and hBoxito > 17):
				
				# idx += 1
				new_img = boxPaper[yBoxito + 10 :yBoxito+wBoxito - 10, xBoxito + 10 :xBoxito+wBoxito - 10]
				
				####################INVENTO DE CORTAR LA LETRA######################
										
				grey = cv2.cvtColor(new_img.copy(), cv2.COLOR_BGR2GRAY)	
				ret, threshLetter = cv2.threshold(grey.copy(), 75, 255, cv2.THRESH_BINARY_INV)

				
				blurredLetter = cv2.GaussianBlur(threshLetter, (5, 5), 0)
				

				ctnsLetter, _ = cv2.findContours(blurredLetter.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
				# print("STR(LEN(ctnsLetter))" , len(ctnsLetter))
				
				# cv2.imshow("new_img", new_img)
				# cv2.waitKey(0)

				# for ctLetter in ctnsLetter:
				# 		xi2, yi2, wi2, hi2 = cv2.boundingRect(ctij)
				# 		ar = w / float(h)
				# 		print(xi2, yi2, wi2, hi2, ar)
				# 		if(hi2 > biggerCtn[0]):
				# 			biggerCtn = ( hi2 , ctij)

				if(len(ctnsLetter) == 0):
					# no letter / space
					print("space normal")
					textAnswer1 = textAnswer1 + " "


				elif(len(ctnsLetter) > 1):
					# letter i or j
					print("letter i or j")
					ij = threshLetter.copy()
					rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 7))
					dilation = cv2.dilate(ij, rect_kernel, iterations = 1)
					
					 
					contoursSpecial, _ = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

					biggerCtn = (0 , [])
					#Get the bigger contour
					for ctij in contoursSpecial:
						xi2, yi2, wi2, hi2 = cv2.boundingRect(ctij)
						print("xi2, yi2, wi2, hi2")
						print(xi2, yi2, wi2, hi2)
						ar = w / float(h)
						print(xi2, yi2, wi2, hi2, ar)
						if(hi2 > biggerCtn[0]):
							biggerCtn = ( hi2 , wi2, ctij)

					xi, yi, wi, hi = cv2.boundingRect(biggerCtn[2])
					
					if(wi < 20 or hi < 20):
						print("espacio ij")
						textAnswer1 = textAnswer1 + " "
					else:

						
						digit = threshLetter[yi:yi+hi, xi:xi+wi]

						height, width = digit.shape
						percent = (18* 100) /height 

						# height = int(height * percent / 100)
						height = 18
						width = int(width * percent / 100)
						if(width % 2 != 0):
							width = width + 1

						resized_digit = cv2.resize(digit, (width,height))

						paddingX = abs(int((28 - width) / 2))

						# print("STR(LEN(ctnsLetter))" , len(ctnsLetter))

						
						# cv2.imshow("digit i j", digit)
						
						# # Resizing that digit to (18, 18)
						# resized_digit = cv2.resize(digit, (18,18))
						
						# # Padding the digit with 5 pixels of black color (zeros) in each side to finally produce the image of (28, 28)
						padded_digit = np.pad(resized_digit, ((5,5),(paddingX,paddingX)), "constant", constant_values=0)
						# print("padded_digit.shape ",padded_digit.shape)
						height, width = padded_digit.shape
						if(height > 28 or width > 28):
							padded_digit = cv2.resize(digit, (28,28))
					

						# cv2.imshow("padded_digit", padded_digit)
						# cv2.waitKey(0)

						# NUEVO MODELO
						prediction = new_model.predict(digit.reshape(1, 28, 28, 1)) 

						# En caso de usar el model de DENSE
						# prediction = new_model.predict(padded_digit.flatten().reshape(-1, 28*28))  
						
						# # En caso de usar el model de CNN
						# prediction = new_model.predict(padded_digit.reshape(1, 28, 28, 1))
						
						textAnswer1 = textAnswer1 + str(letters[int(np.argmax(prediction))])

						textLine = textLine + str(letters[int(np.argmax(prediction))])
						#PRUEBA HACIENDO LA PREDICITION CON ESTA IMAGEN
						# print(str(letters[int(np.argmax(prediction))]), np.argmax(prediction))
						
						# cv2.imshow("padded_digit i j final", padded_digit)
						# cv2.waitKey(0)

				else:	
					#Normal letter
					# print("normal")

					# (ctnsLetter, boundingBoxes) = contours.sort_contours(ctnsLetter, method="top-to-bottom")
					# print("STR(LEN(ctnsLetter))" , len(ctnsLetter))
					cLetter = ctnsLetter[0]
					xL,yL,wL,hL = cv2.boundingRect(cLetter)
					
					print("xL,yL,wL,hL")
					print(xL,yL,wL,hL)

					if(wL < 20 or hL < 20):
						print("espacio letter")
						textAnswer1 = textAnswer1 + " "
					else:
						# Cropping out the digit from the image corresponding to the current contours in the for loop
						digit = threshLetter[yL:yL+hL, xL:xL+wL]

						height, width = digit.shape
						percent = (18* 100) /height 

						# height = int(height * percent / 100)
						height = 18
						width = int(width * percent / 100)
						if(width % 2 != 0):
							width = width + 1

						resized_digit = cv2.resize(digit, (width,height))

						paddingX = abs(int((28 - width) / 2))
						# # Resizing that digit to (18, 18)
						# resized_digit = cv2.resize(digit, (18,18))
						
						# # Padding the digit with 5 pixels of black color (zeros) in each side to finally produce the image of (28, 28)
						padded_digit = np.pad(resized_digit, ((5,5),(paddingX,paddingX)), "constant", constant_values=0)
						# print("padded_digit.shape ",padded_digit.shape)
						height, width = padded_digit.shape
						if(height > 28 or width > 28):
							padded_digit = cv2.resize(digit, (28,28))


						# NUEVO MODELO
						prediction = new_model.predict(digit.reshape(1, 28, 28, 1)) 

						# En caso de usar el model de DENSE
						# prediction = new_model.predict(padded_digit.flatten().reshape(-1, 28*28))  

						
						# cv2.imshow("padded_digit", padded_digit)
						# cv2.waitKey(0)
						# # En caso de usar el model de CNN
						# prediction = new_model.predict(padded_digit.reshape(1, 28, 28, 1))


						textAnswer1 = textAnswer1 + str(letters[int(np.argmax(prediction))])


						# print(str(letters[int(np.argmax(prediction))]), np.argmax(prediction))
							
						# cv2.imshow("padded_digit letter", padded_digit)
						# cv2.waitKey(0)

						# Adding the preproces
				####################INVENTO DE CORTAR LA LETRA######################

		idx = idx + 1





		# for c in ctnsBox:
			# Returns the location and width,height for every contour
			


		# print("textAnswer: " + textAnswer)
		# print("textAnswer1: " + textAnswer1)
		# answersArray.append(textAnswer1)
		
	return textAnswer1.lower()


def getCntsBoxs(box,boxPaper):

	# height, width = box.shape
	# percent = (300* 100) /height 

	# # height = int(height * percent / 100)
	# height = int(height * percent / 100)
	# width = int(width * percent / 100)

	# resized = cv2.resize(box.copy(), (width,height))

	# cv2.imshow("boxnormal", resized)
	# cv2.waitKey(0)

	box = cv2.GaussianBlur(box, (21,21), 0)

	
	# height, width = box.shape
	# percent = (300* 100) /height 

	# # height = int(height * percent / 100)
	# height = int(height * percent / 100)
	# width = int(width * percent / 100)

	# resized = cv2.resize(box.copy(), (width,height))

	# cv2.imshow("boxblurred", resized)
	# cv2.waitKey(0)

	# Defining a kernel length
	kernel_length = np.array(box).shape[1]//80
	
	# A verticle kernel of (1 X kernel_length), which will detect all the verticle lines from the image.
	verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))
	# A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
	hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
	# A kernel of (3 X 3) ones.
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))


	# Morphological operation to detect vertical lines from an image
	img_temp1 = cv2.erode(box, verticle_kernel, iterations=3)
	verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=3)
	# Morphological operation to detect horizontal lines from an image
	img_temp2 = cv2.erode(box, hori_kernel, iterations=3)
	horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=3)
	

	# Weighting parameters, this will decide the quantity of an image to be added to make a new image.
	alpha = 0.5
	beta = 1.0 - alpha
	# This function helps to add two image with specific weight parameter to get a third image as summation of two image.
	img_final_bin = cv2.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
	img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=2)
	(threshFinal, img_final_bin) = cv2.threshold(img_final_bin, 128,255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

	# # Find contours for image, which will detect all the boxes
	ctnsBox, hierarchy = cv2.findContours(img_final_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	
	# FILTER CONTOURS WITH WIDT > 50 AND HEIGTH > 50
	ctnsBoxTemp = []
	
	print("before len(ctnsBox): " , len(ctnsBox))

	for ct in ctnsBox:
		pass
		xBoxito, yBoxito, wBoxito, hBoxito = cv2.boundingRect(ct)
		
		if(wBoxito > 50 and hBoxito > 50):
			ctnsBoxTemp.append(ct)
			# cv2.drawContours(boxPaper, [ct], -1, (random.randint(1,254),random.randint(1,254),random.randint(1,254)), -1)
	
	ctnsBox = ctnsBoxTemp
	print("after  len(ctnsBox): " ,len(ctnsBox))



	# height, width = box.shape
	# percent = (300* 100) /height 

	# # height = int(height * percent / 100)
	# height = int(height * percent / 100)
	# width = int(width * percent / 100)

	# resized = cv2.resize(boxPaper.copy(), (width,height))

	# cv2.imshow("boxpinted", resized)
	# cv2.waitKey(0)
	# Sort all the contours by top to bottom.
	(ctnsBox, boundingBoxes) = contours.sort_contours(ctnsBox, method="top-to-bottom")

	
	###############################CODIGO MEDIUM PARA DETECTAR CUADRADOS#########################################################
				
	


	return ctnsBox