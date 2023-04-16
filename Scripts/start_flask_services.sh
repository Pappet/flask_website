#!/bin/bash

# Start Nginx
systemctl start nginx

# Change to directory of flask app
cd /home/jenkins/workspace/flask_website/Application

# Install requirements
pip install -r /home/jenkins/workspace/flask_website/requirements.txt

export FLASK_APP=app.py  # On Linux or macOS

# flask db init
# flask db migrate -m "Initial migration"
# flask db upgrade

# Start Gunicorn
echo "Starting Gunicorn..."
# gunicorn --worker-class eventlet -w 1 wsgi:app --access-logfile /home/jenkins/workspace/flask_website/logs/gunicorn_access.log --error-logfile /home/jenkins/workspace/flask_website/logs/gunicorn_error.log --log-level info -b 0.0.0.0:8000 --daemon
nohup gunicorn --worker-class eventlet -w 1 wsgi:app --access-logfile /home/jenkins/workspace/flask_website/logs/gunicorn_access.log --error-logfile /home/jenkins/workspace/flask_website/logs/gunicorn_error.log --log-level info -b 0.0.0.0:8000 &

# Wait for Gunicorn to start
# sleep 5
 
# Check if Gunicorn is running
# GUNICORN_PID=$(pgrep -f "gunicorn")

# if [ -n "$GUNICORN_PID" ]; then
#     echo "Gunicorn is running (PID: $GUNICORN_PID)"
# else
#     echo "Gunicorn failed to start. Aborting script."
#     echo "(PID: $GUNICORN_PID)"
#     exit 1
# fi
