#!/bin/sh
set -e

# Copy certs and update trust store
if [ -d "/home/stoobly/.stoobly/certs" ]; then
  cp /home/stoobly/.stoobly/certs/*.crt /usr/local/share/ca-certificates/ || true
  update-ca-certificates
fi

# Execute the CMD from Dockerfile or passed command
exec gosu stoobly "$@"