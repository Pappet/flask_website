#!/bin/bash

# Start Nginx
systemctl start nginx

# Change to directory of flask app
cd /home/flask_website/workspace/flask_website/Application

# Start venv
echo "Activating venv..."
python3 -m venv venv
. /home/flask_website/workspace/flask_website/Application/venv/bin/activate
pip install -r /home/flask_website/workspace/flask_website/requirements.txt


# Start Gunicorn
echo "Starting Gunicorn..."
gunicorn app:app --access-logfile /home/flask_website/workspace/flask_website/logs/gunicorn_access.log --error-logfile /home/flask_website/workspace/flask_website/logs/gunicorn_error.log --log-level info -b 0.0.0.0:8000 --daemon

# Wait for Gunicorn to start
sleep 5
 
# Check if Gunicorn is running
GUNICORN_PID=$(pgrep -f "gunicorn app:app")

if [ -n "$GUNICORN_PID" ]; then
    echo "Gunicorn is running (PID: $GUNICORN_PID)"
else
    echo "Gunicorn failed to start"
fi
