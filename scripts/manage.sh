#!/usr/bin/env bash

set -o errexit

docker-compose -f docker-compose.yml run --rm django python manage.py $@
