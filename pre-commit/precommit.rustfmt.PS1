#!/usr/bin/env pwsh

#cd "$PSScriptRoot/.."
pwd
if (Test-Path -Path ".hg") {
	$RUST_FILES=$(hg status -man | Select-String -Pattern ".rs$")
} elseif (Test-Path -Path ".git") {
	$RUST_FILES=$(git diff --name-only --staged | Select-String -Pattern ".rs$")
} else {
	echo "not a mercurial or git repo. Aborting."
	exit 1
}

if ($RUST_FILES) {
	echo "Formatting rust files with rustfmt: $RUST_FILES"
	rustfmt --check $RUST_FILES
	$EXIT_CODE=$?
	if (-not $EXIT_CODE) {
		rustfmt $RUST_FILES
		echo "Reformatting changes applied. Re-commit to keep changes."
		exit 1
	}
} else {
	echo "Skipping rustfmt"
}
