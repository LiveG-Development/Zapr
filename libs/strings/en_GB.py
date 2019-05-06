# Zapr
# 
# Copyright (C) LiveG. All Rights Reserved.
# Copying is not a victimless crime. Anyone caught copying LiveG software may
# face sanctions.
# 
# https://liveg.tech
# Licensed by the LiveG Open-Source Licence, which can be found at LICENCE.md.

import libs.lang as lang

lang.strings["en_GB"] = {
    "welcome": "{0}Zapr{1} {2}",
    "copyright": "Copyright (C) LiveG. All Rights Reserved.",
    "help": """usage: {0} [--hide | -h] <command> [<args>]

List of commands used in Zapr:
    help        Displays this help screen.
    var         Reads, sets or deletes variables.
                [name]              Read data contained in variable.
                [name] [data]       Write data to variable.
                [name] --delete     Delete variable.""",
    "invalidCommand": "Command is invalid.",
    "invalidCommandStructure": "Command structure is invalid.",
    "setLocaleWarning": "Don't forget to set your locale! We've determined locale to be {0}, but to be sure that this is your locale, type:\n    {1} var locale {0}",
    "varNoMatch": "No matches found for {0}.",
    "varReturn": "{0}: {1}",
    "varDeleteSuccess": "Deleted {0}.",
    "varDeleteFail": "Could not delete {0}. {0} may not exist or may have special permissions.",
    "varWriteReturn": "Set {0} to {1}.\n{0}: {1}"
}