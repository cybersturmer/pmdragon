#!/usr/bin/env bash

echo "Collecting static files..."
./api/manage.py collectstatic --noinput

echo "Copying to web application..."
cp -R ./api/static/ ./web/static/


echo "Starting service..."
docker-compose -f docker-compose.yml up -d