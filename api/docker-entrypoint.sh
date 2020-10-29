#!/usr/bin/env bash

echo -e "\e[94m Collecting static...\e[0m"
python manage.py collectstatic --clear --noinput

echo -e "\e[94m Making migrations...\e[0m"
python manage.py makemigrations
python manage.py migrate

echo -e "\e[94m Loading predefined data...\e[0m"
python manage.py loaddata data.json

echo -e "\e[92m Starting service...\e[0m"
uvicorn conf.asgi:application --uds /run/uvicorn/pmdragon_api.sock