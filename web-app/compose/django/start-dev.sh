#!/bin/sh
python manage.py makemigrations datasets
python manage.py makemigrations linking
python manage.py migrate
#Could alternatively be started from here
python manage.py runserver_plus 0.0.0.0:8000

