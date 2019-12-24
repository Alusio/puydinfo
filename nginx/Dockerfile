FROM nginx:1.17.2-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
COPY nginx.crt /etc/ssl/
COPY nginx.key /etc/ssl