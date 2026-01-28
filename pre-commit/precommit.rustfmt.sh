#!/bin/bash
# NOTE: runs in repo root

set -eo pipefail
cd "$(dirname "$0")/.."

RUST_FILES="$(echo $(hg status -man 2>/dev/null || git diff --name-only --staged) | egrep "\.rs$")"
if [ -z $RUST_FILES ]; then
	echo "Skipping rustfmt"
else
	echo "Formatting rust files with rustfmt: $RUST_FILES"
	set +e
	rustfmt --check $RUST_FILES
	EXIT_CODE=$?
	set -e
	if [ $EXIT_CODE -ne 0 ]; then
		rustfmt $RUST_FILES
		echo "Reformatting changes applied. Re-commit to keep changes."
		exit 1
	fi
fi
