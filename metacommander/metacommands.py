# Copyright (c) 2024 Alexey Galkin
# SPDX-License-Identifier: MIT

from abc import abstractmethod, ABC
import os
import re
import textwrap

class Metacommands:

    registered_metacommands = {}

    def __init__(self):
        self.register()

    def register(self):
        for cls in Metacommand.__subclasses__():
            self.registered_metacommands.update({cls.__name__.lower(): cls()})

    def parse(self, user_input, metadata):
        tokenized_input = user_input.lstrip().split(' ', 1)
        com = tokenized_input[0]
        args = tokenized_input[1] if len(tokenized_input) > 1 else None
        for metacommand in self.registered_metacommands.values():
            if com.lower() in metacommand.synonyms:
                # Handle metacommand
                metacommand.func(metadata, args)
                return [True]
        # Non-metacommand
        return [False, user_input]

class Metacommand(ABC):

    def wrong_arg_msg(self, message=None):
        print(f'{message or "Wrong metacommand argument."} To get help for the metacommand type: "!help {type(self).__name__.lower()}".')

    @abstractmethod
    def func(self):
        pass

    @property
    @abstractmethod
    def synonyms():
        return []

class Metadata(ABC):

    # The key in the metadata dictionary corresponding to the given metacommand. Defaults to the class name of metacommand.
    @property
    def dictionary_key(self):
        return type(self).__name__.lower()

    # Non-dict keys
    def non_dict(convert):
        def wrapper(self, key, metadata, arg):
            if arg:
                try:
                    metadata.dictionary[key] = convert(self, key, metadata, arg)
                    print('Updated.')
                except:
                    self.wrong_arg_msg()
            else:
                metadata.dictionary[key] = type(metadata).DEFAULT_DICTIONARY()[key]
                print(f'Reset to default value ({metadata.dictionary[key] or "empty"}).')
        return wrapper

    @non_dict
    def float(self, key, metadata, arg):
        return float(arg)

    @non_dict
    def str(self, key, metadata, arg):
        return arg

    @non_dict
    def int_list(self, key, metadata, arg):
        return list(map(int, arg.split()))

    @non_dict
    def bool(self, key, metadata, arg):
        if arg.lower() in ('true', 'on', 'yes', 'y', 'enable'): return True
        if arg.lower() in ('false', 'off', 'no', 'n', 'disable'): return False
        raise ValueError

    # Dict keys
    def dict(self, key, metadata, args):
        if args:
            kv = args.split('=', 1)
            subkey, subvalue = (kv[0].strip(), kv[1].strip() if len(kv) > 1 else None)
            # Reset all keys
            if not subkey:
                metadata.dictionary[key] = type(metadata).DEFAULT_DICTIONARY()[key]
                print(f'Reset to default value ({metadata.dictionary[key] or "empty"}).')
            # Print key's value
            if subvalue is None:
                try:
                    print(metadata.dictionary[key][subkey])
                except KeyError:
                    print('Record not found.')
            else:
                # Update the dict
                metadata.dictionary[key].update({subkey: subvalue})
                # Remove the keys that equal its values
                if subkey == subvalue:
                    del metadata.dictionary[key][subkey]
                print('Updated.')
        else:
            print('\n'.join(' = '.join(_) for _ in metadata.dictionary[key].items()) or 'Records not found.')

    def func(self, metadata, args):
        key = self.dictionary_key
        getattr(self, type(metadata.dictionary[key]).__name__)(key, metadata, args)

class Alias(Metadata, Metacommand):
    '''
    Synopsis: !alias [<shortcut> [=<command(s)>|<shortcut>]] [=]

    Aliases allow you to assign any command to a shortcut abbreviation. You can assign aliases to other metacommands too.

    Define a new alias
        !alias shortcut=command(s)

    Delete an alias
        !alias shortcut=shortcut
        
    Display all of your aliases
        !alias

    Display a particular alias
        !alias shortcut

    Delete all aliases
        !alias =
    '''

    synonyms = ['!alias', '!a']
    dictionary_key = 'aliases'

class Auto_transcript(Metadata, Metacommand):
    '''
    Synopsis: !auto-transcript [<file name>]

    Enables or disables auto-transcript. If logging is enabled and the file name is specified, it saves the transcript every turn.

    Enable auto-transcript
        !auto-transcript <file name>

    Disable auto-transcript
        !auto-transcript
    '''

    dictionary_key = 'auto-transcript'
    synonyms = ['!auto-transcript', '!aut']

class Bookmark(Metacommand):
    '''
    Synopsis: !bookmark [<name>]

    Creates a bookmark for the last log entry or prints the log entry referenced by the bookmark. If no name is specified, a bookmark is created with the name of the index value of the last log entry.
    See also the "bookmarks" metacommand.
    '''

    synonyms = ['!bookmark', '!b']

    def func(self, metadata, name):
        if not metadata.dictionary['logging']:
            print('To add bookmark, enable logging ("!logging true").')
            return
        try:
            Metacommands.registered_metacommands['repeat'].func(metadata, metadata.dictionary['bookmarks'][name])
        except:
            index = str(len(metadata.dictionary['log']) - 1)
            name = name or index
            metadata.dictionary['bookmarks'].update({name: index})
            print(f'Bookmark saved as "{name}".')

class Bookmarks(Metadata, Metacommand):
    '''
    Synopsis: !bookmarks [<name> [=<log entry index>|<name>]] [=]

    This command allows you to work with bookmarks.

    Define a new bookmark
        !bookmarks name=log entry index

    Delete a bookmark
        !bookmarks name=name
        
    Display all of your bookmarks
        !bookmarks

    Display the index of the log entry referenced by the bookmark
        !bookmarks name

    Delete all bookmarks
        !bookmarks =

    See also the "bookmark" metacommand.
    '''

    synonyms = ['!bookmarks', '!bs']

class Clear(Metacommand):
    '''
    Synopsis: !clear

    Clears the log. To delete all metadata, use the "!load" metacommand. To stop logging type "!logging false".
    '''

    synonyms = ['!clear', '!c']

    def func(self, metadata, _):
        metadata.dictionary['log'] = type(metadata).DEFAULT_DICTIONARY()['log']
        print('The log is cleared.')

class Cut(Metadata, Metacommand):
    '''
    Synopsis: !cut [<start> <end>]

    Sets the cut settings or resets to the default value if no argument is specified.
    This command allows you to remove any leading and trailing characters (and everything in between) from the game output. Almost similar to Python's "slice" function except for the absence of the "step" parameter.
    '''

    synonyms = ['!cut']

    def func(self, metadata, arg):
        arg = ' '.join(arg.split()[:2]) if arg else arg
        Metadata.int_list(self, 'cut', metadata, arg)

class Help(Metacommand):
    '''
    Synopsis: !help [<metacommand>]

    Displays a list of all metacommands or a description of specified metacommand.
    '''

    synonyms = ['!help', '!h']

    def func(self, metadata, arg):
        if arg:
            for metacommand in Metacommands.registered_metacommands.values():
                metacommand_name = type(metacommand).__name__.lower()
                if arg.lower() in metacommand.synonyms + [metacommand_name]:
                    help_text = type(metacommand).__name__.capitalize()
                    help_text += f"\n\n{'': >4}Synonyms: {', '.join(metacommand.synonyms)}"
                    help_text += f'\n {metacommand.__doc__}' if metacommand.__doc__ else ''
                    try:
                        if type(metadata.dictionary[metacommand_name]) is not dict:
                            help_text += f"\n{'': >4}Current value: '{metadata.dictionary[metacommand_name]}'"
                            help_text += f"\n{'': >4}Default value: '{type(metadata).DEFAULT_DICTIONARY()[metacommand_name]}'"
                    except:
                        pass
                    for line in help_text.splitlines():
                        print(textwrap.fill(line, subsequent_indent=' ' * 4))
                    return
            print('Metacommand not found. Type "!help" to display a list of available metacommands.')
        else:
            print('Metacommander is a Python wrapper (preparser) for terminal-based Interactive Fiction interpreters and text adventures. It has built-in "metacommands", which are commands interpreted by Metacommander itself instead of the game. They are as follows, and are case unsensitive:\n')
            print('  '.join(sorted(metacommand.synonyms[0] for metacommand in Metacommands.registered_metacommands.values())))
            print('\n\nType "!help [metacommand]" to get a description of the metacommand or read the "README.txt" to find out more.')

class Load(Metacommand):
    '''
    Synopsis: !load [<metadata file>]

    Loads metadata from the file or resets to default metadata if no file is specified.
    '''

    synonyms = ['!load', '!l']

    def func(self, metadata, filename=None):
        old_filename = metadata.filename
        metadata.__init__(filename)
        if metadata.filename:
            print('Metadata restored.')
        else:
            self.wrong_arg_msg('Wrong metadata file.')
            metadata.filename = old_filename

class Logging(Metadata, Metacommand):
    '''
    Synopsis: !logging [true|false]

    Enables or disables game logging. Or resets to the default value if no argument is specified. With logging disabled, some metacommands will not work.

    Enable logging
        !logging true

    Disable logging
        !logging false
    '''

    synonyms = ['!logging', '!log']

class Macro(Metacommand):
    '''
    Synopsis: !record {start|stop}

    Recordes the macro and saves it in the "aliases". Only works with games that support chained commands.

    Start recording
        !rec start

    Stop recording
        !rec stop

    Metacommander will ask you under what name to save the macro. The macro will be saved in the "aliases" under the name you specified. To play a macro, enter its name.
    '''

    synonyms = ['!record', '!rec']

    start = None

    def func(self, metadata, arg):
        arg = arg.lower() if arg else None
        if arg == 'start':
            if not metadata.dictionary['logging']:
                print('To start recording, enable logging ("!logging true").')
                return
            self.start = len(metadata.dictionary['log'])
            print('Start recording.')
        elif arg == 'stop':
            if self.start != None:
                print('Stop recording.')
                record = metadata.dictionary['separator'].join([list(i.keys())[0] for i in metadata.dictionary['log']][self.start:len(metadata.dictionary['log'])])
                print('Enter the macro name.')
                metadata.dictionary['aliases'].update({input(metadata.dictionary['prompt']): record})
                print('Recorded.')
                self.start = None
            else:
                print('There is no recording.')
        else:
            self.wrong_arg_msg()

class Note(Metadata, Metacommand):
    '''
    Synopsis: !note [<shortcut> [=<note>|<shortcut>]] [=]

    This command allows you to take notes.

    Create a new note
        !note shortcut=note

    Delete a note
        !note shortcut=shortcut

    Display all of your notes
        !note

    Display a particular note
        !note note

    Delete all notes
        !note =
    '''

    synonyms = ['!note', '!n']
    dictionary_key = 'notes'

class Prompt(Metadata, Metacommand):
    '''
    Synopsis: !prompt [<prompt>]

    Sets the prompt or resets to the default value if no argument is specified.
    '''

    synonyms = ['!prompt', '!p']

class Quit(Metacommand):
    '''
    Synopsis: !quit

    Immediately quits the game and Metacommander. The metadata file will be saved automatically. The game data may not be saved. It is recommended to use in-game commands to quit.
    '''

    synonyms = ['!quit', '!q']

    def func(*_):
        raise SystemExit

class Repeat(Metacommand):
    '''
    Synopsis: !repeat [<log entry index>]

    Redisplays previous (last, if no index is given) log entries. For example:

        0 - first entry (start of the game)
        1 - second entry
        ...
        -2 - penultimate entry
        -1 - last entry
    '''

    synonyms = ['!repeat', '!r']

    def func(self, metadata, index):
        try:
            print(''.join(metadata.dictionary['log'][int(index or -1)].values()))
        except:
            self.wrong_arg_msg('Wrong log entry index or empty log.')

class Replace(Metadata, Metacommand):
    '''
    Synopsis: !replace [<old value> [=<new value>|<old value>]] [=]

    Replaces a specified text in output with another specified text. Regular expressions are supported.

    Create a replacement
        !replace old value=new value

    Delete a replacement
        !replace old value=old value

    Display all of your replacements
        !replace

    Display a particular replacement
        !replace old value

    Delete all replacements
        !replace =
    '''

    synonyms = ['!replace', '!rep']
    dictionary_key = 'replaces'

class Save(Metacommand):
    '''
    Synopsis: !save [<metadata file>]

    Saves (overwrites if no file is specified) metadata to the file. The metadata is saved automatically after quitting the game. Game saves don't end up in the metadata. Use in-game commands to save the game.
    '''

    synonyms = ['!save', '!s']

    def func(self, metadata, filename):
        if metadata.save(filename):
            metadata.filename = filename
            print('Metadata saved.')

class Search(Metacommand):
    '''
    Synopsis: !search <term>

    Returns a list of matches from the log. Regular expressions are supported. Each search result is preceded by its log number that can be used to navigate through the log.
    '''

    synonyms = ['!search', '!sea']

    def func(self, metadata, term):
        if not term:
            self.wrong_arg_msg('A search term is required.')
        else:
           log = dict.fromkeys(list(f'# {i}\n{list(v.values())[0]}' for i, v in enumerate(metadata.dictionary['log'])))
           r = re.compile(term, re.IGNORECASE)
           results = list(filter(r.search, log))
           if results:
               print(f'{len(results)} match(es) found(s):\n')
               for result in results:
                   print(result)
           else:
               print(f'No matches for "{term}".')

class Separator(Metadata, Metacommand):
    '''
    Synopsis: !separator [<separator>]

    Sets the command separator for chained commands (if the game supports it) or resets to the default value if no argument is specified.
    '''

    synonyms = ['!separator', '!sep']

class Synonym(Metadata, Metacommand):
    '''
    Synopsis: !synonym [<synonym> [=<metacommand name>|<synonym>]] [=]

    Synonyms allow you to replace built-in metacommand synonyms with custom synonyms. The name of the metacommand is displayed in the help header of the corresponding metacommand. This feature can be useful when the metacommand synonym is used in the game itself. You can define as many synonyms as you like for each metacommand. If you just want to add an alias to the metacommand, use the "!alias" instead.
    To return the default synonyms delete the added ones and restart the program.

    Define a new synonym
        !synonym synonym=metacommand name

    Delete a synonym
        !synonym synonym=synonym

    Display all of your synonyms
        !synonym

    Display the metacommand name for the synonym
        !synonym synonym

    Delete all synonyms
        !synonym =
    '''

    synonyms = ['!synonym', '!syn']
    dictionary_key = 'synonyms'

    def update_synonyms(self, metadata):
        synonyms = {}
        {synonyms.update({key: [value]}) if key not in synonyms else synonyms[key].append(value) for value, key in metadata.dictionary['synonyms'].items()}
        for metacommand in synonyms:
            try:
                Metacommands.registered_metacommands[metacommand.lower()].synonyms = synonyms[metacommand]
            except KeyError:
                pass

    def func(self, metadata, arg):
        Metadata.dict(self, 'synonyms', metadata, arg)
        self.update_synonyms(metadata)

class Terminal(Metacommand):
    '''
    Synopsis: !terminal <command(s)>

    Allows you to run terminal commands. You can assign aliases to terminal commands.
    '''

    synonyms = ['!terminal', '!t']

    def func(self, _, command):
        if command:
            os.system(command)
        else:
            self.wrong_arg_msg('A terminal command is required.')

class Transcript(Metacommand):
    '''
    Synopsis: !transcript <file name>

    Exports all log entries of the current metadata file to the specified file.
    '''

    synonyms = ['!transcript', '!tra']

    def func(self, metadata, filename, notify=True):
        if filename:
            if len(metadata.dictionary['log']):
                transcript = '\n'.join([k + '\n' + v for entry in metadata.dictionary['log'] for k, v in entry.items()])
                try:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(transcript)
                    if notify:
                        print('The transcript has been exported.')
                except Exception as e:
                    print(e)
            else:
                print('There are no entries in the log.')
        else:
            self.wrong_arg_msg('A file name is required.')

class Wait(Metadata, Metacommand):
    '''
    Synopsis: !wait [<seconds>]

    Waiting time for text output by the interpreter or game. Sets the wait time or resets to the default value if no argument is specified. If the text is not output, increase the wait time. Fractional numbers are supported.
    '''

    synonyms = ['!wait', '!w']
