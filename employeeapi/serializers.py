from rest_framework import serializers
from .models import Employee
from .models import File

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'

#api <-> mobile app/ web app/ etc. json/xml