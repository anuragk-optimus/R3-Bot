#!/bin/bash


echo "Starting bot app..."


pip install --no-cache-dir -r requirements.txt

echo "step 1 completed..."


gunicorn --bind 0.0.0.0:8000 --worker-class aiohttp.worker.GunicornWebWorker --timeout 600 app:APP