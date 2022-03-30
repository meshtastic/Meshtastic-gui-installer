#!/usr/bin/env python
"""Translate entries"""

import os
import deepl

from meshtastic_flasher.util import load_fields, write_fields


translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))

fields = load_fields()
print(f'There are {len(fields)} fields.')

new_fields = fields

# If you add a new language, add it here and form.py populate_languages()
for lang in ["de", "es", "et", "fr", "it", "pl", "zh", "ru", "ja", "ro"]:
    for field in fields:
        for key in ['text', 'tooltip', 'description', 'label']:
            if key in fields[field]:
                #print(f'field:{field}')
                tmp = fields[field][key]
                # translate text into a target language
                if isinstance(tmp, str):
                    # there were no tranlsations, so add english, and new lang
                    result = translator.translate_text(tmp, target_lang=lang)
                    new_entry = { "en": tmp, lang: f'{result}'}
                    print(f'new_entry:{new_entry}')
                    del new_fields[field][key]
                    new_fields[field][key] = new_entry
                else:
                    if lang not in fields[field][key]:
                        # no translation for this field
                        tmp2 = fields[field][key]['en']
                        result = translator.translate_text(tmp2, target_lang=lang)
                        print(f'field:{field} result:{result}')
                        new_fields[field][key][lang] = f'{result}'

print('before write_fields')
write_fields(new_fields)
