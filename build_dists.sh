#!/usr/bin/env bash

set -euo pipefail

BUILD_DIR=dist/$(now)/

SOURCE_DATE_EPOCH=$(git log -n 1 --format=%at HEAD)
export SOURCE_DATE_EPOCH
time python -m build --outdir "$BUILD_DIR"
TEMP_DIR=$(mktemp --directory)
tar xzvf "$BUILD_DIR"/scienceworld-1.1.3.tar.gz -C "$TEMP_DIR"
pushd "$TEMP_DIR"

# Based on https://reproducible-builds.org/docs/archives/#full-example
# Requires GNU Tar 1.28+ (i.e., newer than 2014)
tar --format=ustar \
    --sort=name \
    --mtime="@${SOURCE_DATE_EPOCH}" \
    --owner=0 --group=0 --numeric-owner \
    -czf scienceworld-1.1.3.tar.gz scienceworld-1.1.3/

popd
mv "$TEMP_DIR"/scienceworld-1.1.3.tar.gz "$BUILD_DIR"
rm -r "$TEMP_DIR"
