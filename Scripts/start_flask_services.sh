#!/bin/bash

# Start Nginx
systemctl start nginx

# Change to directory of flask app
cd /home/jenkins/workspace/flask_website/Application

# Install requirements
# python3 -m pip install Flask
# python3 -m pip install flask_socketio
# python3 -m pip install gunicorn==20.1.0 eventlet==0.30.2
pip uninstall gunicorn
pip uninstall flask-socketio
pip uninstall eventlet
pip install -r /home/jenkins/workspace/flask_website/requirements.txt


# Start Gunicorn
echo "Starting Gunicorn..."
gunicorn --worker-class eventlet -w 1 wsgi:app --access-logfile /home/jenkins/workspace/flask_website/logs/gunicorn_access.log --error-logfile /home/jenkins/workspace/flask_website/logs/gunicorn_error.log --log-level info -b 0.0.0.0:8000 --daemon

# Wait for Gunicorn to start
sleep 5
 
# Check if Gunicorn is running
GUNICORN_PID=$(pgrep -f "gunicorn")

if [ -n "$GUNICORN_PID" ]; then
    echo "Gunicorn is running (PID: $GUNICORN_PID)"
else
    echo "Gunicorn failed to start. Aborting script."
    echo "(PID: $GUNICORN_PID)"
    exit 1
fi
