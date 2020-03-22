#!/bin/bash


## PURPOSE: intended to be used by jenkins whenever it needs to re-create the base docker image for a test branch
set -e -o xtrace
# https://stackoverflow.com/a/5750463/7734535

export test_base_image_name_lower_case=$(echo "${COMPOSE_PROJECT_NAME}"_wall_e_base | awk '{print tolower($0)}')
export test_wall_e_image_name_lower_case=$(echo "${COMPOSE_PROJECT_NAME}"_wall_e | awk '{print tolower($0)}')
export test_wall_e_container="${COMPOSE_PROJECT_NAME}"_wall_e
export dockerfile="CI/server_scripts/Dockerfile.base"
export commit_folder="wall_e_commits"
export requirements_file_location="wall_e/src/requirements.txt"
export current_commit=$(git log -1 --pretty=format:"%H")



re_create_image () {
    docker stop "${test_wall_e_container}" || true
    docker rm "${test_wall_e_container}" || true
    docker image rm -f "${test_base_image_name_lower_case}" "${test_wall_e_image_name_lower_case}" || true
    docker build --no-cache -t ${test_base_image_name_lower_case} -f "${dockerfile}" --build-arg CONTAINER_HOME_DIR="${CONTAINER_HOME_DIR}" .
    mkdir -p "${JENKINS_HOME}"/"${commit_folder}"
    echo "${current_commit}" > "${JENKINS_HOME}"/"${commit_folder}"/"${COMPOSE_PROJECT_NAME}"
    exit 0
}

if [ ! -f "${JENKINS_HOME}"/"${commit_folder}"/"${COMPOSE_PROJECT_NAME}" ]; then
    # either this is the first time created a docker image for this wall-e copy or the previous file that contains
    # what commit was last worked on is lost. either way we need to destory the docker image so the docker-compose will
    # re-create it and save the current commit to a file in preparation for the next commit
    echo "No previous commits detected. Will [re-]create ${test_base_image_name_lower_case} docker image "
    re_create_image
else
    echo "previus commit detected. Will now test to se if re-creation is needed"
    # the file that contains the commit exists and we will check all changes done to see if any of them touched
    # the 2 files that mandate destroying the docker image
    previous_commit=$(cat "${JENKINS_HOME}"/"${commit_folder}"/"${COMPOSE_PROJECT_NAME}")
    files_changed=($(git diff --name-only "${current_commit}" "${previous_commit}"))
    for file_changed in "${files_changed[@]}"
    do
        if [[ "${file_changed}" == "${requirements_file_location}" || "${file_changed}" == "${dockerfile}" ]]; then
            echo "will need to re-create docker image ${test_base_image_name_lower_case}"
            re_create_image
        fi
    done
fi

echo "No modifications were needed to base image"
echo "${current_commit}" > "${JENKINS_HOME}"/"${commit_folder}"/"${COMPOSE_PROJECT_NAME}"
exit 0