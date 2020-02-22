from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from . import models
from . import serializers
# Create your views here.

@api_view(['POST'])
def api_create_file_view(request):

    if(request.method)=="POST":
        serializer= serializers.FileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        #return Response("HALO")