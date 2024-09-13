#!/bin/bash
set -e

start_gunicorn() {
    extra_files=$(find /app/templates -name "*.html" -printf "--reload-extra-file %p ")
    echo "Starting Gunicorn..."
    gunicorn --reload --reload-engine=poll $extra_files dasha.wsgi
}

start_gunicorn
