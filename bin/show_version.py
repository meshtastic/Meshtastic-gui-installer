#!/usr/bin/env python
"""Show the version number"""

version_filename = "meshtastic_flasher/version.py"

lines = None

with open(version_filename, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for line in lines:
    if line.startswith("__version__"):
        # get rid of quotes around the version
        line2 = line.replace("'", "")
        # split on whitespace
        words = line2.split(" ")
        # Note: This format is for github actions
        print(f'::set-output name=version::{words[2].strip()}')
