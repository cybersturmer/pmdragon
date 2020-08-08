FROM node:latest as build-stage
LABEL maintainer="cybersturmer@ya.ru" \
      application="PMDRAGON_FRONT" \
      deployment="STATIC" \
      version="2.0"

WORKDIR /app
COPY ./client/package*.json ./
RUN npm install -g @quasar/cli
RUN npm install
COPY ./client .
RUN quasar build

FROM nginx:stable as production-stage
COPY ./api/static /srv/www/pmdragon/static
COPY ./client/ssl /srv/www/pmdragon/ssl
COPY --from=build-stage /app/dist/spa /srv/www/pmdragon/web

CMD ["nginx", "-g", "daemon off;"]
