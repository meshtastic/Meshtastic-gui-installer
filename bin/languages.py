#!/usr/bin/env python
"""Show what languages deepl.com supports"""
import os
import deepl

translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))

print("Target languages:")
for language in translator.get_target_languages():
    if language.supports_formality:
        print(f"{language.code} ({language.name}) supports formality")
    else:
        print(f"{language.code} ({language.name})")
