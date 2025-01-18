#!/bin/bash
set -e

cli=stoobly-agent
user=stoobly

if [[ "${1#-}" != "$1" ]]; then
    # If first arg is `-some-option` or `--some-option` or empty, pass it to $cli run
	set -- $cli run "$@"
fi

# If the current current user UID == 0
if [ "$(id -u)" = '0' ]; then
    # If the first argument is $cli OR bin/*
    if [ "$1" = $cli ] || [[ "$1" == bin/* ]]; then
        # changes any file that is not already $user to be owned by $user
        find . \! -user $user -exec chown $user '{}' +

        # gosu is used to run commands as a different user, switches to $user without creating a new process
        # "$0" refers to the name of the script itself, which will be executed again
        # "$@" passes all arguments that were originally passed to the script
        exec gosu $user "$0" "$@"
    fi
fi

exec "$@"
