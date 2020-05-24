FROM python:3.8
LABEL maintainer="cybersturmer@ya.ru" \
      application="PMDRAGON" \
      deployment="STATIC" \
      version="2.0"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV ENVIRONMENT development
ENV CONTAINER_PATH /srv/www/pmdragon

RUN echo "Installing Python dependencies..."
COPY ./conf/common/requirements.txt ${CONTAINER_PATH}/conf/common/requirements.txt
COPY ./conf/${ENVIRONMENT}/requirements.txt ${CONTAINER_PATH}/conf/${ENVIRONMENT}/requirements.txt

RUN apt-get install apt && \\
pip install --upgrade pip && \\
pip install -r ${CONTAINER_PATH}/conf/${ENVIRONMENT}/requirements.txt
RUN echo "Installation was successfull."

RUN echo "Copying application files..."
COPY ./ ${CONTAINER_PATH}
