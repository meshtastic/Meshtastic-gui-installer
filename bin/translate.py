#!/usr/bin/env python
"""Use the deepl.com service to translate some text"""
import os
import sys
import deepl

# Create a Translator object providing your DeepL API authentication key.
# To avoid writing your key in source code, you can set it in an environment
# variable DEEPL_AUTH_KEY, then read the variable in your Python code:
translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))

# simple arg check
if len(sys.argv) < 3:
    print(f"usage: {sys.argv[0]} lang text")
    print("  example: FR 'hello world'")
    sys.exit(3)

# Translate text into a target language, in this case, French
result = translator.translate_text(sys.argv[2], target_lang=sys.argv[1])
print(result)
