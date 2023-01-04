#!/bin/bash
docker run -v $(pwd)/env:/app/env -v $(pwd)/logs:/app/logs webserver