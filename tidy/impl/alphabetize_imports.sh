#!/bin/bash
set -e

python3 -m pip install "isort==5.12.0" > /dev/null

# enforce use of GNU version of coreutils
. ./tidy/util/enforce_gnu_utils.sh

python3 -m isort .

echo
