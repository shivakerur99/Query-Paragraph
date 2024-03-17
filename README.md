# CodeMonk-assesment
first make create virtualenv in django app 
creation command [virtualenv monk]
then activate the env
using command [authenv\Scripts\activate]

then install this packages in virtualenv
check pip freeze
and select which needs be installed
asgiref==3.7.2
Django>=3.0,<4.0
django-cors-headers==4.0.0
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.0
psycopg2==2.9.9
PyJWT==2.8.0
pytz==2024.1
sqlparse==0.4.4
tzdata==2023.4

next check database connection 

create new database 

make database connection 
DATABASES = {
    'default': {
        "ENGINE":"django.db.backends.postgresql",
        "NAME": "monkdb" ,
        "USER" : "postgres",
        "PASSWORD": "Shivanand99805257!",
        "HOST": "127.0.0.1",
        "PORT": "5432",
     }
 }

this is for postgresql database

find view.py and study what i written how i should convert input and pass into for API and achieved that


run cmd python manage.py makemigrations
run cmd python manage.py migrate
run cmd python manage.py runserver
finally it runs on port and acess it and run all apis in it
