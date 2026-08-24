METACOMMANDER v1.2 (by Alexey Galkin, 2024)

Metacommander is a Python wrapper (preparser) for terminal-based Interactive Fiction interpreters and text adventures. It gives the player additional control options and adds many new features to existing programs. The program was created with special attention to screen reader users.

Potentially, any interpreter or game that can work entirely through input and output streams should run in Metacommander. The author successfully ran it with Dumb Frotz, Glulxe (CheapGlk), instead-cli, IntFicPy, and dgdebug (Dialog). However, it is possible that some functions (including those of the programs themselves) may not work or may not work properly (see the Troubleshooting below).


CHANGELOG

  Version 1.2 (7.11.2024)

    > Added the "Transcript" metacommand.
    > Added the "Auto-transcript" metacommand.
    > Added synonyms for setting Boolean values in the settings: yes/no, y/n, on/off, enable/disable.
    > When a parameter is reset to the default, its value is shown.
    > Updated the "Search" metacommand. Each search result is preceded by its log number that can be used to navigate through the log.
    > Updated in-game manual and the "README".

  Version 1.1 (14.06.2024)

    > Added the "Bookmark" metacommand.
    > Added the "Bookmarks" metacommand.
    > Updated in-game manual and the "README".


QUICK START

Metacommander can be run without installation:

    $ python -m metacommander.mc [<program> [<metadata>]] [-h|--help] [-v|--version]

The program (interpreter or game) can be run with its own options. You can specify them in the help of the corresponding program. For example:

    $ python -m metacommander.mc "glulxe -u game.ulx"

See below for metadata information.


OPTIONS

    -h, --help      show the help message and exit
    -v, --version   show program's version, license, and exit


INSTALLATION

To install the program, run the following command:

    $ python -m pip install metacommander.zip

After installing, the executable will be created, which you can run directly from anywhere on the system:

    $ mc [<program> [<metadata>]] [-h|--help] [-v|--version]

To update the program, run the following command:

    $ python -m pip install --upgrade metacommander.zip


METACOMMANDS

A key feature of Metacommander is the built-in metacommands, which are commands interpreted by a wrapper itself instead of the game. They are as follows, and are case insensitive:

Alias

    Synonyms: !alias, !a

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


Auto-transcript

    Synonyms: !auto-transcript, !aut

    Synopsis: !auto-transcript [<file name>]

    Enables or disables auto-transcript. If logging is enabled and the file name is specified, it saves the transcript every turn.

    Enable auto-transcript
        !auto-transcript <file name>

    Disable auto-transcript
        !auto-transcript


Bookmark

    Synonyms: !bookmark, !b

    Synopsis: !bookmark [<name>]

    Creates a bookmark for the last log entry or prints the log entry referenced by the bookmark. If no name is specified, a bookmark is created with the name of the index value of the last log entry.
    See also the "bookmarks" metacommand.


Bookmarks

    Synonyms = !bookmarks, !bs

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


Clear

    Synonyms: !clear, !c

    Synopsis: !clear

    Clears the log. To delete all metadata, use the "!load" metacommand. To stop logging type "!logging false".


Cut

    Synonyms: !cut

    Synopsis: !cut [<start> <end>]

    Sets the cut settings or resets to the default value if no argument is specified.
    This command allows you to remove any leading and trailing characters (and everything in between) from the game output. Almost similar to Python's "slice" function except for the absence of the "step" parameter.


Help

    Synonyms: !help, !h

    Synopsis: !help [<metacommand>]

    Displays a list of all metacommands or a description of specified metacommand.


Load

    Synonyms: !load, !l

    Synopsis: !load [<metadata file>]

    Loads metadata from the file or resets to default metadata if no file is specified.


Logging

    Synonyms: !logging, !log

    Synopsis: !logging [true|false]

    Enables or disables game logging. Or resets to the default value if no argument is specified. With logging disabled, some metacommands will not work.

    Enable logging
        !logging true

    Disable logging
        !logging false


Macro

    Synonyms: !record, !rec

    Synopsis: !record {start|stop}

    Recordes the macro and saves it in the "aliases". Only works with games that support chained commands.

    Start recording
        !rec start

    Stop recording
        !rec stop

    Metacommander will ask you under what name to save the macro. The macro will be saved in the "aliases" under the name you specified. To play a macro, enter its name.


Note

    Synonyms: !note, !n

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


Prompt

    Synonyms: !prompt, !p

    Synopsis: !prompt [<prompt>]

    Sets the prompt or resets to the default value if no argument is specified.


Quit

    Synonyms: !quit, !q

    Synopsis: !quit

    Immediately quits the game and Metacommander. The metadata file will be saved automatically. The game data may not be saved. It is recommended to use in-game commands to quit.


Repeat

    Synonyms: !repeat, !r

    Synopsis: !repeat [<log entry index>]

    Redisplays previous (last, if no index is given) log entries. For example:

        0 - first entry (start of the game)
        1 - second entry
        ...
        -2 - penultimate entry
        -1 - last entry


Replace

    Synonyms: !replace, !rep

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


Save

    Synonyms: !save, !s

    Synopsis: !save [<metadata file>]

    Saves (overwrites if no file is specified) metadata to the file. The metadata is saved automatically after quitting the game. Game saves don't end up in the metadata. Use in-game commands to save the game.


Search

    Synonyms: !search, !sea

    Synopsis: !search <term>

    Returns a list of matches from the log. Regular expressions are supported. Each search result is preceded by its log number that can be used to navigate through the log.


Separator

    Synonyms: !separator, !sep

    Synopsis: !separator [<separator>]

    Sets the command separator for chained commands (if the game supports it) or resets to the default value if no argument is specified.


Synonym

    Synonyms: !synonym, !syn

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


Terminal

    Synonyms: !terminal, !t

    Synopsis: !terminal <command(s)>

    Allows you to run terminal commands. You can assign aliases to terminal commands.


Transcript

    Synonyms: !transcript, !tra

    Synopsis: !transcript <file name>

    Exports all log entries of the current metadata file to the specified file.


Wait

    Synonyms: !wait, !w

    Synopsis: !wait [<seconds>]

    Waiting time for text output by the interpreter or game. Sets the wait time or resets to the default value if no argument is specified. If the text is not output, increase the wait time. Fractional numbers are supported.


METADATA

All settings are saved in the metadata file. It's a regular json file containing game log, aliases, notes, etc. It can be easily edited. It can also be loaded with another game or interpreter. Of course, you can create any number of metadata files for any purpose.
To create an empty metadata template, run Metacommander without arguments.


ADDING NEW METACOMMANDS

One of the key features of Metacommander is its extensibility. All metacommands are placed in classes, so it is quite easy to add a new one using existing metacommands as samples. See examples in the metacommands.py file.


TROUBLESHOOTING

Q: The game text is not displayed.
A: Increase the waiting time (see the "Wait" metacommand).

Q: After entering a command, the game text is output with a delay.
A: Decrease the waiting time (see the "Wait" metacommand).

Q: Metacommander doesn't understand the metacommand I'm entering.
A: Make sure you enter a synonym and not the name of the metacommand. All available metacommands can be viewed with the "!help". For a detailed description of the metacommand use the "!help <metacommand>" or read the "Metacommands" section.

Q: I've created an alias / recorded a macro from several game commands, but it doesn't play.
A: This feature only works with games that support chained commands. See also the "Separator" metacommand.

Q: The program outputs extra prompt characters, blank lines, etc.
A: Use the "Cut" and "Replace" metacommands.
Metacommander is a platform-agnostic tool. It doesn't know anything about the games or interpreters that will run in it. I recommend creating a metadata template file customized for each specific program (interpreter) you run.

Q: My program crashes, some functions don't work.
A: Run the program without the wrapper. Make sure that everything works in the program itself. Try changing the program settings, download the latest version, or run it in a different OS if possible.


LICENSE

Copyright (c) 2024 Alexey Galkin
Released under the MIT license. See the "LICENSE" file.
