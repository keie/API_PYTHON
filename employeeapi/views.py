from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from . import models
from .models import Forms
from .models import Response_Form
from . import serializers
from fileapi.views import (
    test,
    scanner
    ) 
from array import *
from django.core.exceptions import ObjectDoesNotExist
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
    container=[]
    JsonQuestion=getResponses(request.data['formId'])
    for i,cell in enumerate(images):
        container.append(scanner(cell))
    return Response(JsonQuestion)

#@api_view(['GET',])
#def getResponses(request,id):
#    try:
#        answers = Response_Form.objects.get(id=id)
#    except ObjectDoesNotExist:
#        return Response(status=status.HTTP_404_NOT_FOUND)
#    if(request.method == "GET"):
#        serializer = serializers.Response_FormSerializer(answers)
#        return Response(serializer.data)


def getResponses(id):
    try:
        answers = Response_Form.objects.get(id=id)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = serializers.Response_FormSerializer(answers)
    return Response(serializer.data)