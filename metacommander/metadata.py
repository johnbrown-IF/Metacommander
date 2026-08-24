# Copyright (c) 2024 Alexey Galkin
# SPDX-License-Identifier: MIT

import json

class Metadata:

    DEFAULT_FILENAME = 'metadata.json'
    def DEFAULT_DICTIONARY():
        return {
            'prompt': '> ',
            'separator': '. ',
            'wait': 0.3,
            'cut': [0, 0],
            'logging': True,
            'aliases': {},
            'synonyms': {},
            'replaces': {},
            'notes': {},
            'bookmarks': {},
            'log': [],
            'auto-transcript': '',
        }

    def __init__(self, filename=None):
        self.filename = filename
        if self.filename:
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    self.dictionary = json.loads(f.read())
                    return
            except:
                # Check in the Load metacommand
                if hasattr(self, 'dictionary'):
                    self.filename = None
                    return
                # Create the file later if it does not exist
                pass
        self.dictionary = Metadata.DEFAULT_DICTIONARY()
        self.filename = self.filename or Metadata.DEFAULT_FILENAME

    def save(self, name=None):
        try:
            with open(name or self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.dictionary, f, ensure_ascii=False)
                return True
        except:
            print('An error occurred while saving the metadata.')

    def __del__(self):
        self.save()