from rest_framework import serializers
from .models import Employee
from .models import File
from .models import Forms
from .models import Response_Form

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'

class FormsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forms
        fields = '__all__'

class Response_FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response_Form
        fields = '__all__'

#api <-> mobile app/ web app/ etc. json/xml