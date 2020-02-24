from rest_framework import serializers
from .models import FileApi

class FileApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileApi
        fields = ['file2',]