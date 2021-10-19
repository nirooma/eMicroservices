
###########
# BUILDER #
###########
ARG PYTHON_VERSION=3.9.6

# pull official base image
FROM python:${PYTHON_VERSION}-slim-buster as builder

# set environment variables
ENV WORK_DIR /tmp

# set work directory
WORKDIR $WORK_DIR

# install system dependencies
RUN apt-get update \
  && apt-get -y install curl \
  && apt-get clean

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* $WORK_DIR/

# Export requirements file
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

#########
# STAGING #
#########

# pull official base image
FROM python:${PYTHON_VERSION}-slim-buster as staging

# create the appropriate directories
ENV HOME /tmp2

# install system dependencies
RUN apt-get update \
  && apt-get -y install gcc \
  && apt-get clean

## install python dependencies
COPY --from=builder tmp/requirements.txt $HOME/requirements.txt
RUN pip wheel --no-cache-dir --no-deps --wheel-dir $HOME/wheels -r $HOME/requirements.txt

#########
# FINAL #
#########
FROM python:${PYTHON_VERSION}-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV ENVIRONMENT production
ENV HOME /opt/donatello

# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat \
  && apt-get clean

# create directory for the app user
WORKDIR $HOME

# create the app user
RUN addgroup --system app && adduser --system --group app

# install dependencies
COPY --from=staging /tmp2/wheels /wheels
COPY --from=staging tmp2/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# copy project
COPY . $HOME

# chown all the files to the app user
RUN chown -R app:app $HOME

# change to the app user
USER app
