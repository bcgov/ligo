#!/bin/sh
echo "Make migrations..."
python manage.py makemigrations
echo "Migrating"
python manage.py migrate
#Could alternatively be started from here
echo "Starting server"
python manage.py runserver_plus 0.0.0.0:8000

