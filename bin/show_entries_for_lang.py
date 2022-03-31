#!/usr/bin/env python
"""Show entries for language"""

import sys

from meshtastic_flasher.util import load_fields

# simple arg check
if len(sys.argv) < 2:
    print(f"usage: {sys.argv[0]} lang")
    print("  example: de")
    sys.exit(3)

lang = sys.argv[1].lower()
print(f'lang:{lang}')

fields = load_fields()
print(f'There are {len(fields)} fields.')

for field in fields:
    for key in ['text', 'tooltip', 'description', 'label']:
        if key in fields[field]:
            tmp = fields[field][key]
            if not isinstance(tmp, str):
                en_entry = fields[field][key]['en']
                if lang in fields[field][key]:
                    lang_entry = fields[field][key][lang]
                    print(f'** field:{field} key:{key} \nen:{en_entry}\n{lang}:{lang_entry}\n\n')
