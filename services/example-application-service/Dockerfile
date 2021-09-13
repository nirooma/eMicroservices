FROM python:3.9.6-slim-buster



# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV WORK_DIR=/opt/donatello

# set working directory
WORKDIR $WORK_DIR

# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc postgresql curl \
  && apt-get clean

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false
# Copy poetry.lock* in case it doesn't exist in the repo

COPY ./pyproject.toml ./poetry.lock* ./

RUN poetry install --no-root --no-dev

COPY . $WORK_DIR
