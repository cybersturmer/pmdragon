#!/usr/bin/env bash

echo -e "\e[94m Making migrations...\e[0m"
python manage.py makemigrations
python manage.py migrate

echo -e "\e[94m Loading predefined data...\e[0m"
python manage.py loaddata data.json

echo -e "\e[92m Starting service...\e[0m"
uvicorn --host 0.0.0.0 --reload --port 8000 conf.asgi:application