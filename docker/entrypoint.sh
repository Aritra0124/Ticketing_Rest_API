#!/bin/sh

set -e

echo "Waiting for database..."
echo DB_NAME: ${MYSQL_DATABASE}
echo DB_HOST: ${MYSQL_HOST}
echo DB_PORT: ${MYSQL_PORT}
while ! nc -z ${MYSQL_HOST} ${MYSQL_PORT}; do sleep 1; done
echo "Connected to database."

# Apply database migrations
python manage.py makemigrations

python manage.py migrate

# Collect static files (if applicable)
python manage.py collectstatic --noinput

# Start the Django development server
python manage.py runserver 0.0.0.0:8000
