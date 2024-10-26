FROM python:3.12.3-slim

RUN useradd -mU stoobly

# Install gosu for easy step-down from root: https://github.com/tianon/gosu/releases
# See: https://github.com/tianon/gosu/blob/master/INSTALL.md
ENV GOSU_VERSION 1.17
RUN set -eux; \
# Save list of currently installed packages for later so we can clean up
	savedAptMark="$(apt-mark showmanual)"; \
	apt-get update; \
	apt-get install -y --no-install-recommends ca-certificates gnupg wget; \
	rm -rf /var/lib/apt/lists/*; \
	\
	dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')"; \
	wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch"; \
	wget -O /usr/local/bin/gosu.asc "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch.asc"; \
	\
# Verify the signature
	export GNUPGHOME="$(mktemp -d)"; \
	gpg --batch --keyserver hkps://keys.openpgp.org --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4; \
	gpg --batch --verify /usr/local/bin/gosu.asc /usr/local/bin/gosu; \
	gpgconf --kill all; \
	rm -rf "$GNUPGHOME" /usr/local/bin/gosu.asc; \
	\
# Clean up fetch dependencies
	apt-mark auto '.*' > /dev/null; \
	[ -z "$savedAptMark" ] || apt-mark manual $savedAptMark; \
	apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false; \
	\
	chmod +x /usr/local/bin/gosu; \
# Verify that the binary works
	gosu --version; \
	gosu nobody true

# Install dependencies
COPY . /tmp/stoobly-agent
RUN cd /tmp/stoobly-agent && pip install . && rm -rf /tmp/stoobly-agent

WORKDIR /home/stoobly
RUN mkdir .mitmproxy .stoobly && chown stoobly:stoobly .mitmproxy .stoobly

VOLUME /home/stoobly/.stoobly
VOLUME /home/stoobly/.mitmproxy

COPY docker-entrypoint.sh /usr/local/bin/
ENTRYPOINT ["docker-entrypoint.sh"]

# Proxy port
EXPOSE 8080

# UI $port
EXPOSE 4200

CMD ["stoobly-agent"]
