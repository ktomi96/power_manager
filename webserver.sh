#!/bin/bash
docker run --rm -v $(pwd)/env:/app/env -v $(pwd)/logs:/app/logs -v $(pwd)/database:/app/database -p 5000:5000 --name webserver webserver