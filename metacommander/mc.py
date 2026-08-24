#!/usr/bin/env python3
# Copyright (c) 2024 Alexey Galkin
# SPDX-License-Identifier: MIT

import argparse
import os
import subprocess
import tempfile
import time

import metacommander.metadata as md
import metacommander.metacommands as mc
import metacommander.preparser as pre

def main():

    parser = argparse.ArgumentParser(
        description='Metacommander v1.2 (by Alexey Galkin, 2024)\n\nA Python wrapper (preparser) for terminal-based Interactive Fiction interpreters and text adventures.',
        epilog='While running, enter "!help" to display a list of available metacommands. Read the "README.txt" to find out more.',
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument('program', help='an interpreter and (or) a game with or without options', nargs='?')
    parser.add_argument('metadata', help='the metadata file to load', nargs='?')
    parser.add_argument('-v', '--version', help="show program's version, license, and exit", action='version', version='\n'.join(line.lstrip() for line in
        '''
        Metacommander v1.2
        It is distributed under the MIT license (see below).

        MIT License

        Copyright (c) 2024 Alexey Galkin

        Permission is hereby granted, free of charge, to any person obtaining a copy
        of this software and associated documentation files (the "Software"), to deal
        in the Software without restriction, including without limitation the rights
        to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
        copies of the Software, and to permit persons to whom the Software is
        furnished to do so, subject to the following conditions:

        The above copyright notice and this permission notice shall be included in all
        copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
        EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
        MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
        IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
        DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
        OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
        OR OTHER DEALINGS IN THE SOFTWARE.
        '''.splitlines()
    ))

    args = parser.parse_args()

    metadata = md.Metadata(args.metadata)
    
    if not args.program:
        parser.print_help()
        raise SystemExit

    preparser = pre.Preparser(metadata)
    metacommands = mc.Metacommands.registered_metacommands

    # Set up the first key for a log
    # Format: [is metacommand?, output from the game if non-metacommand]
    parsed_input = [False, '']

    with tempfile.TemporaryFile(prefix='metacommander_', suffix='.tmp') as tf:
        try:
            process = subprocess.Popen(args.program.split(), stdin=subprocess.PIPE, stdout=tf)
        except Exception as e:
            print(e)
            raise SystemExit(1)

        #print(tempfile.gettempdir())
        prev_pointer = 0

        while True:
            time.sleep(metadata.dictionary['wait'])
            pointer = os.path.getsize(tf.name)
            tf.seek(-(pointer - prev_pointer), os.SEEK_END)
            prev_pointer = pointer
            output = tf.read().decode('utf-8')

            if output:
                output = preparser.receive(output)[slice(*[n if n != 0 else None for n in metadata.dictionary['cut']], None)]
                print(output)
                if metadata.dictionary['logging']:
                    metadata.dictionary['log'].append({parsed_input[1]: output})
                    if metadata.dictionary['auto-transcript']:
                        metacommands['transcript'].func(metadata, metadata.dictionary['auto-transcript'], False)
                elif metadata.dictionary['auto-transcript']:
                    print('Logging must be enabled to autosave the transcript ("!logging true").')

            # Check if the game quit after the last output
            if process.poll() != None:
                break

            while True:
                usr_input = input(f'\n{metadata.dictionary["prompt"]}')
                parsed_input = preparser.send(usr_input)

            # Non-metacommand
                if not parsed_input[0]:
                    break
            process.stdin.write(bytes(parsed_input[1] + '\n', 'utf-8'))
            process.stdin.flush()

    return process.returncode

if __name__ == '__main__':
    main()