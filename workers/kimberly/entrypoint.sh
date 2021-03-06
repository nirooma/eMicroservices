#!/bin/bash

# if any of the commands in your code fails for any reason, the entire script fails
set -o errexit
# fail exit if one of your pipe command fails
set -o pipefail
# exits if any of your variables is not set
set -o nounset

echo
echo "##########################################"
echo "#### Welcome To Kimberly Cloud Docker ####"
echo "##########################################"
echo

rabbitmq_ready() {
    echo "### Waiting for rabbitmq ###"

    while ! nc -z rabbitmq 5672; do
      sleep 3
    done

    echo "### Rabbitmq started ###"
}
rabbitmq_ready


exec "$@"


