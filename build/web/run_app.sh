#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
venv/bin/python manage.py migrate

# Collect static files
echo "Collect static files"
venv/bin/python manage.py collectstatic --noinput

# if PORTFOLIO_BLOG_DEBUG is set to True, run the development server
if [ "$PORTFOLIO_BLOG_DEBUG" = "True" ]; then
    echo "Running development server"
    venv/bin/python manage.py runserver 0.0.0.0:8000
else
    # Start Gunicorn processes
    echo "Starting Gunicorn."
    exec venv/bin/python -m gunicorn --bind 0.0.0.0:8000 victorngeno.wsgi
fi
