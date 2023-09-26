FROM python:3.8.11-slim

RUN useradd -mU stoobly 
USER stoobly
WORKDIR /home/stoobly

COPY --chown=stoobly:stoobly . ./
RUN pip install . && rm -rf * && mkdir .mitmproxy .stoobly 

ENTRYPOINT [".local/bin/stoobly-agent", "run"]
EXPOSE 8080
EXPOSE 4200
VOLUME /home/stoobly/.stoobly
VOLUME /home/stoobly/.mitmproxy
