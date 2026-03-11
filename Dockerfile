# Stage 1 (build only): compile gosu from source
# This stage is discarded after the build — Golang does NOT appear in the final image.
# Building from source lets us control the Go version and avoid CVEs
# in the pre-compiled release binaries. https://github.com/tianon/gosu
FROM golang:1.24.13-alpine AS gosu-builder
ENV GOSU_VERSION=1.19
WORKDIR /go/src/github.com/tianon
RUN apk add --no-cache git
RUN git clone https://github.com/tianon/gosu.git --branch $GOSU_VERSION
WORKDIR /go/src/github.com/tianon/gosu
RUN go mod download
RUN go build

# Stage 2 (final image): Python runtime only
# Only the compiled gosu binary is copied from Stage 1 — no Go toolchain included.
FROM python:3.14.3-slim

RUN useradd -mU stoobly

COPY --from=gosu-builder /go/src/github.com/tianon/gosu/gosu /usr/local/bin/gosu
RUN chmod +x /usr/local/bin/gosu; \
# Verify that the binary works
	gosu --version; \
	gosu nobody true

# Install dependencies
COPY . /tmp/stoobly-agent
RUN cd /tmp/stoobly-agent && pip install . && rm -rf /tmp/stoobly-agent

WORKDIR /home/stoobly

COPY stoobly_agent/app/cli/scaffold/templates/build /usr/local/bin/
COPY docker-entrypoint.sh /usr/local/bin/
ENTRYPOINT ["docker-entrypoint.sh"]

# Proxy port
EXPOSE 8080

# UI $port
EXPOSE 4200

CMD ["stoobly-agent", "run"]

