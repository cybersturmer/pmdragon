FROM python:3.8
LABEL maintainer="cybersturmer@ya.ru" \
      application="PMDRAGON" \
      deployment="STATIC" \
      version="2.0"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir -p /srv/www/pmdragon
WORKDIR /srv/www/pmdragon

COPY Pipfile* ./
COPY docker-entrypoint.sh /usr/local/bin/

RUN set -ex; \
    pip install --upgrade pip; \
    pip install pipenv; \
    pipenv install --deploy --system; \
    ln -s usr/local/bin/docker-entrypoint.sh; \
    chmod +x /usr/local/bin/docker-entrypoint.sh; \
    adduser --disabled-password --gecos '' rabbituu

COPY . .
