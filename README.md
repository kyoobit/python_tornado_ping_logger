# Python Tornado Ping Logger

An API widget which logs data




# Building and Running 

## Building and running using a container
These instructions are written for Podman. Replace `podman` with `docker` as needed:

Building an image:

    podman build --tag tornado-ping-logger:${TAG:=v1} .

View available application options:

    podman run --rm --name tornado-ping-logger-help tornado-ping-logger:${TAG:=v1} --help

Run a container instance:

    podman run --rm --detach --publish 8888:8888/tcp \
    --name tornado-ping-logger tornado-ping-logger:v1 --verbose
