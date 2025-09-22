#!/bin/bash

COLUMNS=$(tput cols)
LINES=$(tput lines)
BOLD=$(tput bold)
NORMAL=$(tput sgr0)

COMPOSE_FILES="-f docker-compose.yml"
DOCKER_COMPOSE="docker compose ${COMPOSE_FILES}"

_requires() {
    service="$1"
    $DOCKER_COMPOSE ps -q $service &> /dev/null
    if [[ $? -ne 0 ]]; then
        echo "'$service' service is not running. Please run \`start\` first." 
        exit 1
    fi 
}

build() {
    $DOCKER_COMPOSE build --force-rm "${@:3}"
}

compose() {
    $DOCKER_COMPOSE "$@"
}

start() {
    $DOCKER_COMPOSE up "$@"
}

stop() {
    $DOCKER_COMPOSE down "$@"
}

shell() {
    _requires web_run
    $DOCKER_COMPOSE exec -w /code/myshop web_run /bin/bash
}

migrate() {
    _requires web_run
    $DOCKER_COMPOSE exec -w /code/myshop web_run ./manage.py migrate "$@"
}

makemigrations() {
    _requires web_run
    $DOCKER_COMPOSE exec -w /code/myshop web_run python manage.py makemigrations "$@"
}

check() {
    _requires web_run
    $DOCKER_COMPOSE exec -w /code/myshop web_run ./manage.py check
}

_usage() {
    cat <<USAGE
Convenience wrapper around docker compose.

Usage: 
    ${BOLD}build${NORMAL} [<arg>]
        Builds all the images (or the ones specified).

    ${BOLD}compose${NORMAL} [<arg>]
        Minimal wrapper around docker-compose, ensures the correct config files are loaded.

    ${BOLD}migrate${NORMAL} [<arg>]
        Apply any unapplied Django migrations.

    ${BOLD}makemigrations${NORMAL} [<arg>]
        Creates a new Django migration.

    ${BOLD}check${NORMAL}
        Validates Django settings.

    ${BOLD}shell${NORMAL}
        Opens a bash terminal in web_run.

    ${BOLD}start${NORMAL} [<arg>]
        Start the Django server (and dependent services). Pass `-d` for detached mode.

    ${BOLD}stop${NORMAL} [<arg>]
        Stop the Django server (and dependent services).

USAGE
}

if [ "$1" == "" ]; then 
    _usage
    exit 0
fi 

"$@"
