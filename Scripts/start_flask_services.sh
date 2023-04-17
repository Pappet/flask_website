#!/bin/bash

# Change to directory of flask app
cd /home/jenkins/workspace/flask_website/Application

# Install requirements
pip install -r /home/jenkins/workspace/flask_website/requirements.txt

# Define enviroment variable
export FLASK_APP=app.py

flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# --------------------------------------------------------------------------

# Start Nginx
echo "Starting nginx..."
systemctl start nginx

# Wait for Gunicorn to start
sleep 10

# Check the status of the Gunicorn service
NGINX_STATUS=$(systemctl is-active nginx)

# Print the status of the Gunicorn service
if [ "$NGINX_STATUS" = "active" ]; then
    echo "Nginx service is active and running"
else
    echo "Nginx service is not active"
    exit 1
fi

# --------------------------------------------------------------------------

# Start Gunicorn
echo "Starting Gunicorn..."
systemctl start gunicorn

# Wait for Gunicorn to start
sleep 10

# Check the status of the Gunicorn service
GUNICORN_STATUS=$(systemctl is-active gunicorn)

# Print the status of the Gunicorn service
if [ "$GUNICORN_STATUS" = "active" ]; then
    echo "Gunicorn service is active and running"
else
    echo "Gunicorn service is not active"
    exit 1
fi