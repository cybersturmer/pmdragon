FROM node:latest as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:stable as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY ./static /srv/www/pmdragon/static
COPY ./ssl /srv/www/pmdragon/ssl
COPY nginx-conf/sitename.conf /etc/nginx/nginx.conf

CMD ["nginx", "-g", "daemon off;"]
