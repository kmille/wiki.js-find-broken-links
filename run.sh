#!/bin/sh
set -eu
poetry run python wikijs_find_broken_links/__init__.py 2>&1 | tee wiki.log
