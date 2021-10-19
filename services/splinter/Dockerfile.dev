# client/Dockerfile

# pull official base image
FROM node:16-alpine

ENV WORK_DIR=/opt/splinter

# set working directory
WORKDIR $WORK_DIR

# add `/usr/src/app/node_modules/.bin` to $PATH
ENV PATH $WORK_DIR/node_modules/.bin:$PATH

# install app dependencies
COPY package.json .
COPY package-lock.json .
RUN npm ci
RUN npm install react-scripts@4.0.3 --silent

# copy project
COPY . .