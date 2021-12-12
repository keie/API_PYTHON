from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from . import models
# from .models import Forms
# from .models import Response_Form
from . import serializers
from fileapi.views import (
    test,
    scanner
    ) 
from array import *
from django.core.exceptions import ObjectDoesNotExist
import json
from django.http import HttpRequest
import requests
# Create your views here.
@api_view(['GET',])
def api_get_form_viewById(request,id):
    try:
        form = Forms.objects.get(id=id)
    except Forms.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if(request.method == "GET"):
        serializer = serializers.FormsSerializer(form)
        return Response(serializer.data)

@api_view(['POST'])
def api_create_file_view(request):

    if(request.method)=="POST":
        serializer= serializers.FileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        #return Response("HALO")

@api_view(['POST'])
def api_create_processing_view(request):
    idForm=request.data['formId']
    images=request.data['files']
    form=request.data['form']
    containerAux=[]
    # JsonQuestion=requests.get('http://127.0.0.1:8000/api/form/'+str(idForm))
    # json_body = JsonQuestion.json()
    json_body = form
    indexQuestion = 0
    for i,cell in enumerate(images):
        for y,value in enumerate(scanner(indexQuestion, cell,json_body)):
            if(isinstance(value,list)):
                #Respuestas de seleccion multiple
                containerMultiple = []
                for z,valuemultiple in enumerate(value):
                    if json_body['questions'][y + indexQuestion]['answers'][valuemultiple]["id"]==valuemultiple:
                        containerMultiple.append(json_body['questions'][y + indexQuestion]['answers'][valuemultiple]['name'])
                containerAux.append(containerMultiple)
            elif(isinstance(value,str)):
                #Respuestas de desarrollo
                containerAux.append(value)
            else:
                #Respuestas de seleccion simple / escala
                if json_body['questions'][y + indexQuestion]['answers'][value]["id"]==value:
                    containerAux.append(json_body['questions'][y + indexQuestion]['answers'][value]['name'])
        indexQuestion = len(containerAux)
                
    # r = requests.post('http://127.0.0.1:8000/api/insert/responseForm', json={
    #                 "response":containerAux,
    #                 "createdAt":"2020-02-08T16:31:23.043000Z",
    #                 "updatedAt":"2020-02-08T16:31:23.043000Z",
    #                 "formId":idForm
    #             })
    return Response(containerAux)

@api_view(['GET',])
def getResponses(request,id):
    try:
        answers = Response_Form.objects.get(id=id)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if(request.method == "GET"):
        serializer = serializers.Response_FormSerializer(answers)
        return Response(serializer.data)

@api_view(['POST'])
def postRespones(request):

    if(request.method)=="POST":
        serializer= serializers.Response_FormSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        #return Response("HALO")


#def getResponses(id):
#    try:
#        answers = Response_Form.objects.get(id=id)
#   except ObjectDoesNotExist:
#        return Response(status=status.HTTP_404_NOT_FOUND)
#   serializer = serializers.Response_FormSerializer(answers)
#   return jsonify(serializer.data)
    
    #serializer = serializers.Re)sponse_FormSerializer(answers)
    #return "hello"