#!/usr/bin/env python3
import os, sys, platform, re
from pathlib import Path

def err(*args, **wkargs):
	print(*args, **wkargs, file=sys.stderr)

# first check that this is a git repo
this_dir = Path(__file__).parent
root_dir = this_dir.parent
git_dir = root_dir / ".git"
if not git_dir.is_dir():
	err(f"ERROR: Directory '{str(git_dir)} does not exist'")
	exit(1)

# figure out which versions of scripts to use
if platform.system() == "Windows":
	suffix = ".PS1"
	prefix = "powershell.exe -File "
	is_windows = True
else:
	suffix = ".sh"
	prefix = "bash "
	is_windows = False

# read the pre-commit file, if it exists
git_precommit_file = git_dir / "hooks" / "pre-commit"
if git_precommit_file.exists():
	git_precommit_content = git_precommit_file.read_text()
else:
	git_precommit_content = "#!/bin/sh\n\n"

# find pre-commit hook scripts and add them
err(f"Installing pre-commit hook scripts to '{str(git_precommit_file)}'...")
changed = False
for p in this_dir.rglob('*'):
	if p.name.endswith(suffix):
		hook_cmd = str(p.relative_to(root_dir)).replace("\\","/")
		hook_entry = f'{prefix}{hook_cmd}'
		if hook_entry not in git_precommit_content:
			err(f"installing hook '{hook_entry}'")
			git_precommit_content += f'echo "{p.stem}..."\n' + hook_entry+'\n'
			changed = True
		else:
			err(f"hook '{hook_entry}' already installed")
if changed:
	git_precommit_file.write_text(git_precommit_content)
	if not is_windows:
		os.chmod(git_precommit_file, 0o777)
err("...Done")
exit(0)

