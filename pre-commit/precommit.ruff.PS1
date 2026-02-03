#!/usr/bin/env pwsh

cd "$PSScriptRoot/.."
if (Test-Path -Path ".hg") {
	$PYTHON_FILES=$(hg status -man | Select-String -Pattern ".py$")
} elseif (Test-Path -Path ".git") {
	$PYTHON_FILES=$(git diff --name-only --staged | Select-String -Pattern ".py$")
} else {
	echo "Not a Mercurial nor Git repo. Aborting."
	exit 1
}

if ($PYTHON_FILES) {
	echo "Formatting and linting python files with ruff: $PYTHON_FILES"
	echo "ruff format..."
	uv tool run ruff format --exit-non-zero-on-format $PYTHON_FILES
	$EXIT_CODE1=$?
	echo "ruff check..."
	uv tool run ruff check --exit-non-zero-on-fix $PYTHON_FILES
	$EXIT_CODE2=$?
	if (-not $EXIT_CODE1 -or -not $EXIT_CODE2) {
		echo "Reformatting changes applied. Re-commit to keep changes."
		exit 1
	}
} else {
	echo "Skipping ruff"
}
