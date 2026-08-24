# Copyright (c) 2024 Alexey Galkin
# SPDX-License-Identifier: MIT

import re

import metacommander.metacommands as mc

class Preparser:

    def __init__(self, metadata):
        self.metadata = metadata
        self.metacommands = mc.Metacommands()
        mc.Synonym.update_synonyms(self, metadata)

    def send(self, user_input):
        parsed = self.metacommands.parse(user_input, self.metadata)
        if not parsed[0]:
            # Checking for aliases
            for command, substitute in self.metadata.dictionary['aliases'].items():
                if user_input.split()[0] == command or user_input == command:
                    return self.metacommands.parse(user_input.replace(command, substitute), self.metadata)
        return parsed

    def receive(self, block):
        # Checking for replaces
        for text, substitute in self.metadata.dictionary['replaces'].items():
            block = re.sub(text, substitute, block, flags=re.IGNORECASE)
        return block