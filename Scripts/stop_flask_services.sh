#!/bin/bash

# Find the Gunicorn master process PID
GUNICORN_MASTER_PID=$(pgrep -f "gunicorn" | sort -n | head -n 1)

# If the process was found, kill it
if [ -n "$GUNICORN_MASTER_PID" ]; then
    echo "Stopping Gunicorn (PID: $GUNICORN_MASTER_PID)..."
    kill "$GUNICORN_MASTER_PID"
    echo "Gunicorn stopped"
else
    echo "Gunicorn not running or not found"
fi
