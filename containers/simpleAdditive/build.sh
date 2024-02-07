#!/bin/bash

set -e

cd "$(dirname "$0")"

# adapted from https://stackoverflow.com/a/62915644/17332200
tar -ch . | docker build -

exit 0