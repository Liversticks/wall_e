#!/bin/bash

if [ -z "${COMPOSE_PROJECT_NAME}" ]; then
	echo "COMPOSE_PROJECT_NAME needs to be set"
	exit 1
fi

pushd CI/user_scripts
cp docker-compose-mount.yml docker-compose.yml
docker-compose rm -f -s -v
docker volume rm "${COMPOSE_PROJECT_NAME}_logs"
docker image rm "${COMPOSE_PROJECT_NAME}_wall_e"
docker network rm "${COMPOSE_PROJECT_NAME}_default"
rm docker-compose.yml
popd
