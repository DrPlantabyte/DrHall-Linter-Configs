#!/bin/bash

set -eo pipefail

cd "$(dirname "$0")/.."
RUST_FILES="$($(hg status -man 2>/dev/null || git diff --name-only --staged) | egrep "\.rs$")"
if [ -z $RUST_FILES ]; then
	echo "Skipping rustfmt"
else
	echo "Formatting rust files with rustfmt: $(echo $RUST_FILES)"
	rustfmt $RUST_FILES
fi
