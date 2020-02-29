from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.
class Employee(models.Model):
    fullname = models.CharField(max_length=100)
    emp_code = models.CharField(max_length=3)
    mobile = models.CharField(max_length=15)

class File(models.Model):
    fullname = models.CharField(max_length=5000)

class Forms(models.Model):
    id= models.IntegerField(primary_key=True)
    name=models.CharField(max_length=5000)
    questions=JSONField()
    description=models.CharField(max_length=5000)
    closeDate=models.DateTimeField(auto_now=True)
    closed=models.BooleanField()
    rememberPeriod=models.IntegerField(default=0)
    createdat=models.DateTimeField(auto_now=True)
    updatedat=models.DateTimeField(auto_now=True)
    projectId=models.IntegerField(default=0)

class Response_Form(models.Model):
    response=JSONField()
    createdAt=models.DateTimeField(auto_now=True)
    updatedAt=models.DateTimeField(auto_now=True)
    formId=models.IntegerField(default=0)


    #Create / Insert / Add POST
    #Retrieve / Fetch - GET
    #Update / Edit - PUT
