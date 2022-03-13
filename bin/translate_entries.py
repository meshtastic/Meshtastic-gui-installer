#!/usr/bin/env python
"""Translate entries"""

import os
import sys
import deepl

from meshtastic_flasher.util import load_fields, write_fields


# simple arg check
if len(sys.argv) < 2:
    print(f"usage: {sys.argv[0]} lang")
    print("  example: DE")
    sys.exit(3)


translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))

lang = sys.argv[1].lower()
print(f'lang:{lang}')

fields = load_fields()
print(f'There are {len(fields)} fields.')

new_fields = fields

i = 0
for field in fields:
    if 'text' in field:
        print(f'field:{field}')
        tmp = fields[field]['text']
        print(f'tmp:{tmp}')
        # translate text into a target language
        result = translator.translate_text(tmp, target_lang=sys.argv[1])
        if isinstance(tmp, str):
            # there were no tranlsations, so add english, and new lang
            new_entry = { "en": tmp, lang: f'{result}'}
            print(f'new_entry:{new_entry}')
            del new_fields[field]['text']
            new_fields[field]['text'] = new_entry
        break
    if i > 1:
        break

print('before write_fields')
write_fields(new_fields)
