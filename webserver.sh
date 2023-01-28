#!/bin/bash
docker run -v $(pwd)/env:/app/env -v $(pwd)/logs:/app/logs -v $(pwd)/database:/app/database webserver