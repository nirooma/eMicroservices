FROM nginx:1.21.3
RUN rm /etc/nginx/conf.d/default.conf
RUN rm /etc/nginx/nginx.conf

COPY nginx.conf /etc/nginx/
COPY eMicroservices.conf /etc/nginx/conf.d