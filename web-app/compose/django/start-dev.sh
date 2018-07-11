#!/bin/sh
echo "Make migrations..."
python manage.py makemigrations
echo "Migrating"
python manage.py migrate
#Could alternatively be started from here

export DJANGO_SETTINGS_MODULE='config.settings.local'

echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('baseuser', 'myemail@example.com', 'Pass12345678')" | python manage.py shell --plain

echo "Starting server"
python manage.py runserver_plus 0.0.0.0:8000

