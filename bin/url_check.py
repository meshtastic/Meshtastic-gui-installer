#!/usr/bin/env python
"""Validate all doc_url entries. Return 1 if any are non valid."""

import sys
import requests
from meshtastic_flasher.util import load_fields

def url_checker(url):
    retval = False
    if url != '':
        try:
            get = requests.get(url)
            if get.status_code == 200:
                retval = True
        except:
            pass
    return retval


all_valid = True
fields = load_fields()
for f in fields:
    if 'doc_url' in fields[f]:
        doc_url = fields[f]['doc_url']
        if not url_checker(doc_url):
            print(f'Invalid doc_url:{doc_url}')
            all_valid = False
if not all_valid:
    sys.exit(1)
