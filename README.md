# API_PYTHON
Python Api to consume services from PosgreSQL data


# librerias necesarias para correr 
 pip install django
 pip install djangorestframewrok
 pip install opencv-python
 pip install psycopg2
 pip install imutils
 pip install numpy
 pip install scipy
 pip install requests

# para hacer la migracion de la BD

python manage.py migrate

 # Para correrlo

 python manage.py runserver

# Request Para servicios

## [POST] http://127.0.0.1:8000/api/formResponse

### lee la imagen (ver imagen example.jpg) del mapa de bits y da como salida las respuestas en un JSON
body:
{
    "formId":idFormFromBdd(table: employeeapi_forms)
    "files":[
        "base64image"
    ]
}

## [GET] http://127.0.0.1:8000/api/form/<IdForm>

### Da como resultado la estructura del formulaion (encuesta) en detalle en un JSON

