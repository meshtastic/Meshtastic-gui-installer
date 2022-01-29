#!/usr/bin/env python3
"""Zip the standalone executable files."""

import sys
import zipfile

if len(sys.argv) != 3:
    print(f"usage: {sys.argv[0]} file_to_zip zip_filename")
    sys.exit()

file_to_zip=sys.argv[1]
zip_filename=sys.argv[2]

with zipfile.ZipFile(zip_filename, "w") as zf:
    zf.write(file_to_zip)
    zf.close()
