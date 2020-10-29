#!/usr/bin/env bash
su -m rabbituu -c "celery -A conf.celery worker --loglevel=INFO"