FROM node:latest as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install -g @quasar/cli
RUN npm install
COPY . .
RUN quasar build

FROM nginx:stable as production-stage
COPY ./static /srv/www/pmdragon/static
COPY ./ssl /srv/www/pmdragon/ssl
COPY --from=build-stage /app/dist/spa /srv/www/pmdragon/web

CMD ["nginx", "-g", "daemon off;"]
