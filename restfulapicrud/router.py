from employeeapi.viewsets import EmployeeViewset
from employeeapi.models import File
from rest_framework import routers
from django.contrib import admin

#router = routers.DefaultRouter()
#router.register('employee',EmployeeViewset)
admin.site.register(File)


# localhost:p/api/employee/5
# GET,POST,UPDATE,DELETE
# list,retrieve