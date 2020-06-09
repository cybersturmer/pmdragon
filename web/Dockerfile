FROM node:latest as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:stable as production-stage
COPY ./static /srv/www/pmdragon/static
COPY ./ssl /srv/www/pmdragon/ssl
COPY --from=build-stage /app/dist /srv/www/pmdragon/web


CMD ["nginx", "-g", "daemon off;"]
