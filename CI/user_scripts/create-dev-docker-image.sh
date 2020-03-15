#!/bin/bash


# PURPOSE: TO BE USED BY THE USER WHEN THEY HAVE MADE CHANGES TO EITHER THE DOCKERFILE.BASE OR REQUIREMENTS FILE
# WHICH MEANS THEY CAN NO LONGE RELY ON THE REPO STORED AT SFUCSSSORG/WALL_E FOR THEIR LOCAL DEV AND NEED TO CREATE THEIR OWN
## DOCKER WALL_E BASE IMAGE TO WORK OFF OF

set -e -o xtrace
# https://stackoverflow.com/a/5750463/7734535

if [ -z "${COMPOSE_PROJECT_NAME}" ]; then
	echo "COMPOSE_PROJECT_NAME needs to be set"
	exit 1
fi

export testBaseImageName_lowerCase=$(echo "${COMPOSE_PROJECT_NAME}"_wall_e_base | awk '{print tolower($0)}')
export DOCKERFILE="CI/server_scripts/Dockerfile.base"
export CONTAINER_HOME_DIR="/usr/src/app"

./scripts/localhostDestroyDevEnv.sh

docker image rm -f "${testBaseImageName_lowerCase}" || true
docker build --no-cache -t ${testBaseImageName_lowerCase} -f "${DOCKERFILE}" --build-arg CONTAINER_HOME_DIR="${CONTAINER_HOME_DIR}" .
