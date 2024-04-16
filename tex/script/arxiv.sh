#!/bin/bash

set -e
shopt -s globstar

find binder -type f ! \( -name "*.pdf" -o -name "*.tex" -o -name "*.bib" \) -exec rm -f {} +


find . -type d -name dishtiny -exec rm -rf {} +
find . -type d -name hstrat -exec rm -rf {} +
find . -type d -name conduit -exec rm -rf {} +
find . -type d -name docs -exec rm -rf {} +
find . -type d -empty -delete
find . -type l -delete

find . -type f | grep -P '[^a-zA-Z0-9_+.,=/-]+' | xargs rm -rf
find . -name '.*' -not -name '.' -not -name '..' -exec rm {} \;

rm -f arxiv.tar.gz
make cleaner
make
make clean
cp bu1.bbl main.bbl
cp bu1.blg main.blg
tar -czvf arxiv.tar.gz *
