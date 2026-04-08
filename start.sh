#!/bin/bash

# Kill background processes on exit
trap 'kill $DJANGO_PID 2>/dev/null' EXIT

# Activate virtual environment
source .venv/bin/activate

# Start Django in background
python3 manage.py runserver 0.0.0.0:8000 &
DJANGO_PID=$!

echo "Django started (PID $DJANGO_PID), waiting for it to be ready..."
sleep 2

# Start browser-sync in foreground
/home/swadaddy4life/.nvm/versions/node/v20.19.5/bin/browser-sync start \
  --proxy "localhost:8000" \
  --files "app/templates/**/*.html, static/**/*.css, static/**/*.js, **/*.py" \
  --host 0.0.0.0 \
  --port 3000
