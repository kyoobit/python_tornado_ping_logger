FROM docker.io/library/alpine:latest

## Add os build dependencies
## podman run --rm --tty --interactive rust:alpine /bin/sh
## apk update; apk info <package>
RUN apk add python3 py3-tornado py3-geoip2

## Copy the source files for the project
COPY app.py /app.py
COPY cli.py /cli.py

## Add a user account
## No need to run as root in the container
RUN addgroup -S appgroup \
    && adduser -S appuser -G appgroup

## Run all future commands as appuser
USER appuser

## Setup the entrypoint
ENTRYPOINT ["python3", "/cli.py"]
## Example usage:
##   podman build --tag tornado-ping-logger:v1 .
##
## View the available program options:
##   podman run --rm --name tornado-ping-logger-help tornado-ping-logger:v1 --help
##
## Run a container instance:
##   podman run --rm --detach --publish 8888:8888/tcp \
##   --name tornado-ping-logger tornado-ping-logger:v1 --verbose