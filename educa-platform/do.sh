#!/bin/bash

COLUMNS="$(tput cols)"
LINES="$(tput lines)"
BOLD=$(tput sgr0)

COMPOSE_FILES="-f docker-compose.yml"
DOCKER_COMPOSE="docker compose ${COMPOSE_FILES}"

_requires() {
    service="$1"
    $DOCKER_COMPOSE ps -q $service &> /dev/null
    if [[ "$?" == 1 ]]; then 
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
    $DOCKER_COMPOSE exec -w /code/educa web_run /bin/bash
}

migrate() {
    _requires web_run
    $DOCKER_COMPOSE exec -w /code/educa web_run python manage.py migrate "$@"
}

makemigrations() {
    _requires web_run
    $DOCKER_COMPOSE exec -w /code/educa web_run python manage.py makemigrations "$@"
}

check() {
    _requires web_run
    $DOCKER_COMPOSE exec -w /code/educa web_run python manage.py check
}

exec_cmd() {
    $DOCKER_COMPOSE exec -e COLUMNS -e LINES "$@"
}

_usage() {
    cat <<USAGE
Convenience wrapper around docker compose.    

Usage: 
    build [<arg>]          Build images
    exec [<arg>]           Execute a command in a container
    compose                Run raw docker compose commands
    migrate [<arg>]        Apply Django migrations
    makemigrations [<arg>] Create new Django migrations
    check                  Validate Django settings
    shell                  Open bash inside web_run container
    start [<arg>]          Start Django server (+ deps)
    stop                   Stop Django server (+ deps)           
USAGE
}

if [ "$1" == "" ]; then 
    _usage
    exit 0
fi

"$@"
