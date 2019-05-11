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
    "installRequiredLibs": "Installing required libraries for Zapr...",
    "installRequiredLibsError": "Couldn't install required libraries. Try running Zapr by itself with administrator/superuser privileges.",
    "help": """usage: zapr [--hide | -h] <command> [<args>]

List of commands used in Zapr:
    help        Displays this help screen.
    var         Reads, sets or deletes variables.
                <name>              Read data contained in variable.
                <name> <data>       Write data to variable.
                <name> --delete     Delete variable.
    build       Build files in directory and output them to the `build` subdirectory.
                app                 Build files as final app.
    """,
    "invalidCommand": "Command is invalid.",
    "invalidCommandStructure": "Command structure is invalid.",
    "setLocaleWarning": "Don't forget to set your locale! We've determined locale to be {0}, but to be sure that this is your locale, type:\n    zapr var locale {0}",
    "varNoMatch": "No matches found for {0}.",
    "varReturn": "{0}: {1}",
    "varDeleteSuccess": "Deleted {0}.",
    "varDeleteFail": "Could not delete {0}. {0} may not exist or may have special permissions.",
    "varWriteReturn": "Set {0} to {1}.\n{0}: {1}",
    "buildingDir": "Building for directory {0}...",
    "invalidManifest": "Could not read manifest.json. It may be invalid, may not exist or may have special permissions.",
    "buildError": "An error occurred when building the app file.",
    "buildSuccessful": "File built successfully.",
    "importLibrary": "Importing library {0} from {1}...",
    "illegalImport": "Illegal or malformed import statement: {0}",
    "unknownImport": "Unknown source for import statement: {0}"
}