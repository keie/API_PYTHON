from django.db import models


class FileApi(models.Model):
    file2 = models.CharField(max_length=5000 , default="true")

    #Create / Insert / Add POST
    #Retrieve / Fetch - GET
    #Update / Edit - PUT
    #Delete/ Remove - DELETE
