#!/bin/bash
docker run --network=host -v $(pwd)/env:/app/env -v $(pwd)/logs:/app/logs logger