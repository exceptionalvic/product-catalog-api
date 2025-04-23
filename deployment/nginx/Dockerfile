FROM nginx:1.19.8

COPY nginx.conf /etc/nginx/nginx.conf

RUN rm /etc/nginx/conf.d/default.conf
COPY server.conf /etc/nginx/conf.d/server.conf