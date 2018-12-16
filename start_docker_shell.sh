#!/bin/bash

echo "running JSShell 2.0 CLI ..."

if [[ $(docker-compose ps | grep "jsshell-20_db") ]]; then
    echo "db exists, skipping creation..."
else
    echo "db not exists, creating it..."
    docker-compose up --build --detach db
fi

if [[ $(docker-compose ps | grep "jsshell-20_web") ]]; then
    echo "web API exists, skipping creation..."
else
    echo "web API not exists, creating it..."
    docker-compose up --build --detach web
fi

docker-compose run --rm shell
