#!/bin/bash

# if any of the commands in your code fails for any reason, the entire script fails
set -o errexit
# fail exit if one of your pipe command fails
set -o pipefail
# exits if any of your variables is not set
set -o nounset

postgres_ready() {
python << END
import sys

import psycopg2

try:
    psycopg2.connect(
        dbname="${SQL_DATABASE}",
        user="${SQL_USER}",
        password="${SQL_PASSWORD}",
        host="${SQL_HOST}",
        port="${SQL_PORT}",
    )
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)

END
}
until postgres_ready; do
  >&2 echo ' ### Waiting for PostgreSQL to become available... ###'
  sleep 3
done
>&2 echo '### PostgreSQL is available ###'

echo
echo "##########################################"
echo "#### Welcome To Leonardo Cloud Docker ####"
echo "##########################################"
echo

rabbitmq_ready() {
    echo "### Waiting for rabbitmq ###"

    while ! nc -z rabbitmq 5672; do
      sleep 1
    done

    echo "### Rabbitmq started ###"
}

rabbitmq_ready

echo "### Running migrations ###"
python manage.py migrate
echo "### Migrations running completed ###"
python manage.py collectstatic --no-input
ls
ls staticfiles
exec "$@"
