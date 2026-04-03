#!/bin/bash
echo "Running from entrypoint.sh"

# Run all migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start the server
python manage.py runserver 0.0.0.0:8000