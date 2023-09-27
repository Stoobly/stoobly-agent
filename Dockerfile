FROM python:3.8.11-slim

COPY . /tmp/stoobly-agent
RUN cd /tmp/stoobly-agent && pip install . && rm -rf /tmp/stoobly-agent
RUN useradd -mU stoobly

USER stoobly
WORKDIR /home/stoobly
RUN mkdir .mitmproxy .stoobly  

ENTRYPOINT ["stoobly-agent", "run"]
EXPOSE 8080
EXPOSE 4200
VOLUME /home/stoobly/.stoobly
VOLUME /home/stoobly/.mitmproxy
