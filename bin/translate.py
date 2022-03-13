#!/usr/bin/env python
"""Use the deepl.com service to translate some text"""
import os
import sys
import deepl

translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))

# simple arg check
if len(sys.argv) < 3:
    print(f"usage: {sys.argv[0]} lang text")
    print("  example: FR 'hello world'")
    sys.exit(3)

# translate text into a target language
result = translator.translate_text(sys.argv[2], target_lang=sys.argv[1])
print(result)
