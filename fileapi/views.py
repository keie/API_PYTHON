from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import FileApi
from fileapi.serializers import FileApiSerializer

from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import argparse
import imutils 
import cv2
import base64

@api_view(['GET',])
def api_get_file_view(request,id):
    try:
        file_api = FileApi.objects.get(id=id)
    except FileApi.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if(request.method == "GET"):
        
        serializer = FileApiSerializer(file_api)
        return Response(serializer.data)
        
        
@api_view(['POST',])
def api_post_file_view(request):
    file_api = FileApi()
    if(request.method == "POST"):
        serializer = FileApiSerializer(file_api,data=request.data)
        
        #print(request.data['file2'] )
        scanner(request.data['file2']) 
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)

def test():

    return Response("it works!")


def scanner(file2,json_questions):
    
    ANSWER_KEY = {0: 1, 1: 4, 2: 0, 3: 3, 4: 1}
    answersArray = []
    
    # filename = 'example.jpg'  # I assume you have a way of picking unique filenames
    # image= base64.b64decode(file2)
    # with open(filename, 'wb') as f:
    #     f.write(image)
    #     print("true") 


    img = base64.b64decode(file2); 
    npimg = np.fromstring(img, dtype=np.uint8); 
    image = cv2.imdecode(npimg, 1)


    # image = cv2.imread(filename)
    #image = cv2.imread("./test_04.png")
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

    thresh = cv2.threshold(warped, 0, 255,
        cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    questionCnts = []

    for c in cnts:
        
        (x, y, w, h) = cv2.boundingRect(c)
        ar = w / float(h)

        if w >= 15 and h >= 15 and ar >= 0.8 and ar <= 1.5:
            questionCnts.append(c)

    questionCnts = contours.sort_contours(questionCnts,
        method="top-to-bottom")[0]
    correct = 0

    #armo el array de longitudes de las respuestas
    array_lenght = []
    for object_question in json_questions['questions']:
        array_lenght.append(len(object_question['answers']))

    ARRAYS_LENGHT = [4 , 5, 6 , 2 , 5, 6 , 6, 6, 4]
    
    stop = 0
    i = 0
    start = 0

    while i < len(array_lenght):

        stop = stop + array_lenght[i] 
        actualcnts = questionCnts[start : stop]
        cnts = contours.sort_contours(questionCnts[start : stop])[0]
        bubbled = None
        start = stop 

        for (j, c) in enumerate(cnts):

            mask = np.zeros(thresh.shape, dtype="uint8")
            cv2.drawContours(mask, [c], -1, 255, -1)
            mask = cv2.bitwise_and(thresh, thresh, mask=mask)
            total = cv2.countNonZero(mask)
            if bubbled is None or total > bubbled[0]:
                bubbled = (total, j)
        answersArray.append(bubbled[1])
        i = i + 1

    # grab the test taker
    return (answersArray)