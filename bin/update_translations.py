#!/usr/bin/env python
"""Update the fields.json file from an updated file that was created using show_entries_for_lang.py and edited"""

import sys

from meshtastic_flasher.util import load_fields, write_fields

# simple arg check
if len(sys.argv) < 2:
    print(f"usage: {sys.argv[0]} input_file")
    print("  example: foo.txt")
    sys.exit(3)

filename = sys.argv[1].lower()
print(f'filename:{filename}')


field = None
key = None
en_entry = None
tr_entry = None

fields = load_fields()

with open(filename, encoding='utf-8') as input_file:
    lines = input_file.readlines()

    lang = None
    if lines[0].startswith('lang:'):
        tmp = lines[0]
        lang = tmp[5:].strip()
    print(f'lang:{lang}:')

    for line in lines:
        if line.startswith('** field:'):
            # update the last entry processed (Note: need to deal with the last entry.)
            if en_entry is not None and tr_entry is not None:
                # remove the trailing new lines (which separate the entries)
                # pylint: disable=unsubscriptable-object
                tmp = tr_entry[:-4]
                # if there still is a trailing new line, remove it
                if tmp[-1:] == '\n':
                    tmp = tmp[:-1]
                fields[field][key][lang] = tmp
                print(f'tr_entry:{tr_entry}')
            tmp = line.split(' ')
            tmp2 = tmp[1].split(':')
            tmp3 = tmp[2].split(':')
            field = tmp2[1]
            key = tmp3[1].strip()
            #print(f'field:{field} key:{key}')
            en_entry = None
            tr_entry = None
        elif line.startswith('en:'):
            en_entry = line[3:]
        elif line.startswith(f'{lang}:'):
            tr_entry = line[3:].strip()
        else:
            if en_entry is not None:
                if tr_entry is not None:
                    tr_entry = tr_entry + '\n' + line

write_fields(fields)
