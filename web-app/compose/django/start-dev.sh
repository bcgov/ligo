#!/bin/sh
echo "Make migrations datasets"
python manage.py makemigrations datasets
echo "Make migrations linking"
python manage.py makemigrations linking
echo "Migrating"
python manage.py migrate
#Could alternatively be started from here
echo "Starting server"
python manage.py runserver_plus 0.0.0.0:8000

