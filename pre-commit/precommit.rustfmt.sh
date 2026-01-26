#!/bin/bash
# NOTE: runs in repo root

set -eo pipefail

RUST_FILES="$(echo $(hg status -man 2>/dev/null || git diff --name-only --staged) | egrep "\.rs$")"
if [ -z $RUST_FILES ]; then
	echo "Skipping rustfmt"
else
	echo "Formatting rust files with rustfmt: $RUST_FILES"
	rustfmt $RUST_FILES
fi
