#!/usr/bin/env python
"""Bump the version number"""
import re

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
            build_num = re.findall(r"\d+", v[2])[0]
            new_build_num = str(int(build_num)+1)
            ver = f'{v[0]}.{v[1]}.{v[2].replace(build_num, new_build_num)}'.replace('\n', '')
            f.write('"""File to hold the version"""\n')
            f.write('\n')
            f.write(f"__version__ = '{ver}'\n")
