#!/bin/bash

branch_name="${1}"
token="${2}"

deleted_discord_branch_channels () {
	branch_name="${1}"
	token="${2}"

	url="https://discordapp.com/api/users/@me/guilds"
	curl -H "Authorization: Bot ${token}"  "${url}" > output.json
	guild_id=$(cat output.json | jq -r .[].id)

	url="https://discordapp.com/api/guilds/${guild_id}/channels"
	curl -H "Authorization: Bot ${token}"  "${url}" > output.json
	mapfile -t list_of_channel_ids < <( cat output.json | jq -r .[].id )
	mapfile -t list_of_channel_names < <( cat output.json | jq -r .[].name )
	rm output.json

	for (( i=0; i<${#list_of_channel_ids[@]}; i++ ))
	do
		if [ "${list_of_channel_names[$i]}" = "${branch_name}" ]; then
			branch_id="${list_of_channel_ids[$i]}"
		fi

		if [ "${list_of_channel_names[$i]}" = "${branch_name}_logs" ]; then
			log_channel_id="${list_of_channel_ids[$i]}"
		fi

		if [ "${list_of_channel_names[$i]}" = "${branch_name}_reminders" ]; then
			reminder_channel_id="${list_of_channel_ids[$i]}"
		fi
	done
	if [ -z "${branch_id}" ]; then
		echo "branch_id was not detected"
	else
		url="https://discordapp.com/api/channels/${branch_id}"
		curl -X DELETE -H "Authorization: Bot ${token}"  "${url}"
	fi

	if [ -z "${log_channel_id}" ]; then
		echo "log_channel_id was not detected"
	else
		url="https://discordapp.com/api/channels/${log_channel_id}"
		curl -X DELETE -H "Authorization: Bot ${token}"  "${url}"
	fi

	if [ -z "${reminder_channel_id}" ]; then
		echo "reminder_channel_id was not detected"
	else
		url="https://discordapp.com/api/channels/${reminder_channel_id}"
		curl -X DELETE -H "Authorization: Bot ${token}"  "${url}"
	fi

}

destroy_docker_resources () {
	export COMPOSE_PROJECT_NAME="TEST_${1}"
	./CI/destroy-dev-env.sh

}

deleted_discord_branch_channels "${branch_name}" "${token}"

destroy_docker_resources "${branch_name}"
