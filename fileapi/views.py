from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import FileApi
from fileapi.serializers import FileApiSerializer

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
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)