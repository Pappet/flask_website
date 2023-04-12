#!/bin/bash

# Start Nginx
systemctl start nginx

# Change to directory of flask app
<<<<<<< HEAD
cd /home/jenkins/workspace/flask_website
=======
cd /home/jenkins/workspace
>>>>>>> 494506a (Changes)

# Start venv
source venv/bin/activate

# Start Gunicorn and Flask App
gunicorn app:app --access-logfile /home/flask_app/logs/gunicorn_access.log --error-logfile /home/flask_app/logs/gunicorn_error.log --log-level info -b 0.0.0.0:8000 --daemon

 