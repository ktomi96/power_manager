#!/bin/bash
docker run --rm --network=host -v $(pwd)/env:/app/env -v $(pwd)/database:/app/database --name logger logger