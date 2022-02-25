#!/usr/bin/env python
"""Bump the version number"""

version_filename = "meshtastic_flasher/version.py"

lines = None

with open(version_filename, 'r', encoding='utf-8') as f:
    lines = f.readlines()

with open(version_filename, 'w', encoding='utf-8') as f:
    for line in lines:
        if line.startswith("__version__"):
            # get rid of quotes around the version
            line2 = line.replace("'", "")
            # split on whitespace
            words = line2.split(" ")
            # split the version into parts (by period)
            v = words[2].split(".")
            ver = f'{v[0]}.{v[1]}.{int(v[2]) + 1}'
            f.write('"""File to hold the version"""\n')
            f.write('\n')
            f.write(f"__version__ = '{ver}'\n")
