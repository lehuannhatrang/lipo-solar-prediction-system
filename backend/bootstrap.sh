#!/bin/sh
set -e

# Define usage for clarity
usage() {
    echo "Usage: bootstrap.sh [worker|beat|flask]"
    exit 1
}

# Check the first argument and execute the corresponding service
if [ "$1" = "worker" ]; then
    echo "Starting Celery worker..."
    cd src
    celery -A celery_init worker --loglevel=info -P eventlet
elif [ "$1" = "beat" ]; then
    echo "Starting Celery beat..."
    cd src
    celery -A celery_init beat --loglevel=info
elif [ "$1" = "flask" ]; then
    echo "Starting Flask app..."
    export FLASK_APP=./src/app.py
    export FLASK_RUN_HOST=0.0.0.0
    flask run
else
    echo "Unknown command: $1"
    usage
fi
