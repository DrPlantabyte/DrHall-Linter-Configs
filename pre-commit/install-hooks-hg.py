#!/usr/bin/env python3
import os, sys, platform, re
from pathlib import Path

def err(*args, **wkargs):
	print(*args, **wkargs, file=sys.stderr)

# first check that this is a mercurial repo
this_dir = Path(__file__).parent
root_dir = this_dir.parent
hg_dir = root_dir / ".hg"
if not hg_dir.is_dir():
	err(f"ERROR: Directory '{str(hg_dir)} does not exist'")
	exit(1)

# read the hgrc file, if it exists
hgrc_file = hg_dir / "hgrc"
if hgrc_file.exists():
	hgrc_content = hgrc_file.read_text()
else:
	hgrc_content = ''

# find the [hooks] section, if it exists
hook_matches = list(re.finditer(r'^\w*\[\w*hooks\w*\]', hgrc_content))
if len(hook_matches) > 0:
	insert_index = hook_matches[-1].end(0)
else:
	hgrc_content = hgrc_content + "\n[hooks]"
	insert_index = len(hgrc_content)

# figure out which versions of scripts to use
if platform.system() == "Windows":
	suffix = ".PS1"
	prefix = "powershell.exe -File "
else:
	suffix = ".sh"
	prefix = "sh "

# find pre-commit hook scripts and add them
err(f"Installing pre-commit hook scripts to '{str(hgrc_file)}'...")
for p in this_dir.rglob('*'):
	if p.name.endswith(suffix):
		hook_entry = f'{p.stem} = {prefix}{str(p.relative_to(root_dir))}'
		if hook_entry not in hgrc_content:
			err(f"installing hook '{hook_entry}'")
			hgrc_content = hgrc_content[:insert_index]+'\n'+hook_entry+hgrc_content[insert_index:]
			insert_index += 1+len(hook_entry)
		else:
			err(f"hook '{hook_entry}' already installed")
hgrc_file.write_text(hgrc_content)
err("...Done")
exit(0)

