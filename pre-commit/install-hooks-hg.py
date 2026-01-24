#!/usr/bin/env python3
import os, sys, platform, re
from pathlib import Path

def err(*args, **wkargs):
	print(*args, **wkargs, file=sys.stderr)

# first check that this is a mercurial repo
hg_dir = Path(__file__).parents[1] / ".hg"
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
hook_matches = list(re.finditer(r'^\w*\[\w*hooks\w*\]', hgrc_file))
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
	prefix = "bash "

err("WIP")
exit(1)

