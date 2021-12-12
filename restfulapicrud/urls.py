"""restfulapicrud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
#from .router import router
from employeeapi.views import (
    api_create_file_view,
    api_get_form_viewById,
    api_create_processing_view,
    getResponses,
    postRespones
)

app_name = 'file'

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('api/',include(router.urls)),
    # path('api/fileapi/',include('fileapi.urls','file_api')),
    #path('api/',include(router.urls)),
    path('api/create',api_create_file_view,name="create"),
    path('api/form/<id>',api_get_form_viewById,name="form"),
    path('api/formResponse',api_create_processing_view,name="formResponse"),
    path('api/answers/<id>',getResponses,name="answer"),
    path('api/insert/responseForm',postRespones,name="create")
]
