#!/bin/bash
docker build -f Dockerfile.webserver -t webserver --build-arg ENABLE_FRONTEND=true .
