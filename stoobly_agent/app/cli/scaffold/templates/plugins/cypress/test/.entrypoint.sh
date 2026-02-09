#!/bin/sh
set -e

# Copy ca certificate and update trust store
if [ -f "/home/stoobly/.stoobly/ca_certs/mitmproxy-ca-cert.cer" ]; then
  cp /home/stoobly/.stoobly/ca_certs/mitmproxy-ca-cert.cer /usr/local/share/ca-certificates/mitmproxy-ca-cert.crt || true
  update-ca-certificates
fi

# Execute the CMD from Dockerfile or passed command
exec gosu stoobly "$@"