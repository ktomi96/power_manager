#!/bin/bash
docker run --rm -v $(pwd)/env:/app/env -v $(pwd)/logs:/app/logs -v $(pwd)/database:/app/database --name webserver webserver