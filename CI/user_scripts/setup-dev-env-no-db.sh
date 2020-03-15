#!/bin/bash

if [ -z "${COMPOSE_PROJECT_NAME}" ]; then
	echo "COMPOSE_PROJECT_NAME needs to be set"
	exit 1
fi

if [ -z "${ORIGIN_IMAGE}" ]; then
	echo "ORIGIN_IMAGE needs to be set"
	exit 1
fi

./scripts/localhostDestroyDevEnv.sh

docker volume create --name="${COMPOSE_PROJECT_NAME}_logs"
export ENVIRONMENT="LOCALHOST"
export DB_ENABLED="0"
docker-compose -f CI/user_scripts/docker-compose-mount-nodb.yml up -d

sleep 20
containerFailed=$(docker ps -a -f name="${COMPOSE_PROJECT_NAME}_wall_e" --format "{{.Status}}" | head -1)
if [[ "${containerFailed}" != *"Up"* ]]; then
    docker logs ${testContainerName}
    exit 1
fi

echo "wall_e succesfully launched!"
