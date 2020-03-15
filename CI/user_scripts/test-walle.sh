#!/bin/bash
set -x

export COMPOSE_PROJECT_NAME="tester"


docker rm "${COMPOSE_PROJECT_NAME}"_test
docker image rm "${COMPOSE_PROJECT_NAME}"_wall_e_test
docker build -t ${COMPOSE_PROJECT_NAME}_wall_e_test -f CI/Dockerfile.test --build-arg CONTAINER_HOME_DIR=/usr/src/app --build-arg UNIT_TEST_RESULTS=/usr/src/app/tests --build-arg TEST_RESULT_FILE_NAME=all-unit-tests.xml .
docker run -d --name ${COMPOSE_PROJECT_NAME}_test ${COMPOSE_PROJECT_NAME}_wall_e_test

while [ "$(docker inspect -f '{{.State.Running}}' ${COMPOSE_PROJECT_NAME}_test)"  = "true" ]
do
	echo "waiting for testing to complete"
	sleep 1
done

docker logs ${COMPOSE_PROJECT_NAME}_test
