#!/usr/bin/env pwsh

cd "$PSScriptRoot/.."
# TODO: detect if git or hg
$RUST_FILES=$($(hg status -man 2>/dev/null || git diff --name-only --staged) | Select-String -Pattern ".rs$")
if ($RUST_FILES) {
	echo "Formatting rust files with rustfmt: $RUST_FILES"
	rustfmt $RUST_FILES
} else {
	echo "Skipping rustfmt"
}
