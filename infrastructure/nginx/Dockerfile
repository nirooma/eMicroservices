FROM nginx:1.21.3
RUN rm /etc/nginx/conf.d/default.conf
RUN rm /etc/nginx/nginx.conf

COPY nginx.conf /etc/nginx/
COPY eMicroservices.conf /etc/nginx/conf.d


#RUN rm /etc/nginx/conf.d/default.conf
#COPY nginx.conf /etc/nginx/conf.d
# rm -rf /etc/nginx/sites-enabled/*
# cp $BASE_PATH/perceptoCloud/dockers/cloud/nginx/percepto /etc/nginx/sites-enabled/