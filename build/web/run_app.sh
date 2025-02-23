#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# if PORTFOLIO_BLOG_DEBUG is set to True, run the development server
if [ "$PORTFOLIO_BLOG_DEBUG" = "True" ]; then
    echo "Running development server"
    python manage.py runserver 0.0.0.0:8000
else
    # Start Gunicorn processes
    echo "Starting Gunicorn."
    exec gunicorn --bind 0.0.0.0:8000 victorngeno.wsgi
fi
