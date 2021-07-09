FROM python:3.8.11-slim

RUN pip install stoobly

EXPOSE 8080
EXPOSE 4200

ENTRYPOINT ["stoobly", "run"]
