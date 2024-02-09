#!/bin/bash

set -e

cd "$(dirname "$0")"

python3.10 -m uvicorn knockem.app:app
