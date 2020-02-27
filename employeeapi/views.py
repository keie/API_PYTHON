from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from . import models
from .models import Forms
from . import serializers
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