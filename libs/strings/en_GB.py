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
    "installRequiredLibs": "Installing required libraries for Zapr ({0})...",
    "installRequiredLibsError": "Couldn't install required libraries. Try running Zapr by itself with administrator/superuser privileges.",
    "help": """usage: zapr [--hide | -h] <command> [<args>]

List of commands used in Zapr:
    help        Display this help screen.
    var         Read, set or delete variables.
                <name>              Read data contained in variable.
                <name> <data>       Write data to variable.
                <name> --delete     Delete variable.
    build       Build files in directory and output them to the `build` subdirectory.
                app                 Build files as final app.
                static              Build files as final static site.
    docgen      Generate documentation for Zapr JavaScript libraries to the `docs` subdirectory.
    """,
    "invalidCommand": "Command is invalid.",
    "invalidCommandStructure": "Command structure is invalid.",
    "setLocaleWarning": "Don't forget to set your locale! We've determined locale to be {0}, but to be sure that this is your locale, type:\n    zapr var locale {0}",
    "varNoMatch": "No matches found for {0}.",
    "varReturn": "{0}: {1}",
    "varDeleteSuccess": "Deleted {0}.",
    "varDeleteFail": "Could not delete {0}. {0} may not exist or may have special permissions.",
    "varWriteReturn": "Set {0} to {1}.\n{0}: {1}",
    "buildDir": "Building for directory {0}...",
    "buildRootFiles": "Building root files...",
    "cleanUpBuildDir": "Cleaning up `build` directory...",
    "invalidManifest": "Could not read manifest.json. It may be invalid, may not exist or may have special permissions.",
    "buildError": "An error occurred when building the app file.",
    "buildSuccessful": "File built successfully.",
    "importLibrary": "Importing library {0} from {1}...",
    "importAsset": "Importing asset {0} from {1}...",
    "circularImport": "Ignored circular import of library {0}.",
    "illegalImport": "Illegal or malformed import statement: {0}",
    "unknownImport": "Unknown source for import statement: {0}",
    "circularAsset": "Ignored circular import of asset {0}.",
    "illegalAsset": "Illegal or malformed asset statement: {0}",
    "unknownAsset": "Unknown source for asset statement: {0}",
    "takenFromCache": "Taken {0} from cache.",
    "buildLocale": "Building for locale {0}...",
    "doubleLanguageFile": "Double language file ignored: {0}",
    "servePort": "Serving port: {0}",
    "serveError": "Could not serve. The `build` directoy may not exist or may have special permissions, or an internal error may have occurred.",
    "genDocs": "Generating documentation for {0}...",
    "genDocsSuccessful": "Documentation generated successfully.",
    "genDocsIllegal": "Illegal or malformed documentation statement ignored: {0}",
    "genDocsUnspecified": "Unspecified mandatory information for documentation statement, statement ignored: {0}",
    "cleanUpDocsDir": "Cleaning up `docs` directory..."
}