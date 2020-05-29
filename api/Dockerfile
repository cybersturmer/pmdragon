FROM python:3.8
LABEL maintainer="cybersturmer@ya.ru" \
      application="PMDRAGON" \
      deployment="STATIC" \
      version="2.0"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /srv/www/pmdragon

RUN echo "Installing Python dependencies manager..."
RUN pip install --upgrade pip && \\
pip install pipenv

RUN echo "Copying dependencies files..."
COPY Pipfile ./
COPY Pipfile.lock ./

RUN echo "Installing dependencies..."
RUN set -ex && pipenv install --deploy --system

RUN echo "Copying application files..."
COPY . .

EXPOSE 8000
CMD ["uvicorn --host 0.0.0.0 --port 8000 conf.asgi.application"]
