#!/bin/bash
set -e

cli=stoobly-agent
data_dir=.stoobly
user=stoobly
user_home=/home/stoobly

if [[ "${1#-}" != "$1" ]]; then
    # If first arg is `-some-option` or `--some-option` or empty, pass it to $cli run
	set -- $cli run "$@"
fi

# If the current current user UID == 0
if [ "$(id -u)" = '0' ]; then
    # If the first argument is $cli OR bin/*
    if [ "$1" = $cli ] || [[ "$1" == bin/* ]] || [[ "$1" == .stoobly/* ]]; then
        # changes any file that is not already $user to be owned by $user

        if [ -d "$data_dir" ]; then
            find "$data_dir" -maxdepth 1 \! -user $user -exec chown $user:$user '{}' +
        fi

        if [ -d "$user_home/$data_dir" ]; then
            find "$user_home/$data_dir" -maxdepth 1 \! -user $user -exec chown $user:$user '{}' +
        fi

        # gosu is used to run commands as a different user, switches to $user without creating a new process
        # "$0" refers to the name of the script itself, which will be executed again
        # "$@" passes all arguments that were originally passed to the script
        exec gosu $user "$0" "$@"
    fi
fi

exec "$@"
