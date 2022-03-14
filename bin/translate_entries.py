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

for field in fields:
    for key in ['text', 'tooltip', 'description', 'label']:
        if key in fields[field]:
            print(f'field:{field}')
            tmp = fields[field][key]
            # translate text into a target language
            if isinstance(tmp, str):
                # there were no tranlsations, so add english, and new lang
                result = translator.translate_text(tmp, target_lang=sys.argv[1])
                new_entry = { "en": tmp, lang: f'{result}'}
                print(f'new_entry:{new_entry}')
                del new_fields[field][key]
                new_fields[field][key] = new_entry
            else:
                # there were tranlsations, so use english
                tmp2 = fields[field][key]['en']
                result = translator.translate_text(tmp2, target_lang=sys.argv[1])
                print(f'result:{result}')
                new_fields[field][key][lang] = f'{result}'

print('before write_fields')
write_fields(new_fields)
