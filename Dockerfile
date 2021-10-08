FROM python:3.8.11-slim

RUN mkdir -p /app
WORKDIR /app
COPY . /app
RUN pip install .

EXPOSE 8080
EXPOSE 4200

ENTRYPOINT ["stoobly-agent", "run"]
