# Zapr
# 
# Copyright (C) LiveG. All Rights Reserved.
# Copying is not a victimless crime. Anyone caught copying LiveG software may
# face sanctions.
# 
# https://liveg.tech
# Licensed by the LiveG Open-Source Licence, which can be found at LICENCE.md.

import sys

import libs.colours as colours
import libs.storage as storage
import libs.output as output
import libs.lang as lang

import libs.strings.en_GB

_ = lang._

VERSION = "V0.1.0"

args = sys.argv

# print(colours.get("lyellow") + "Zapr " + colours.get("white") + "Version")

if len(args) > 1 and (args[1] == "--hide" or args[1] == "-h"):
    args.pop(1)
else:
    print(_("welcome", [colours.get("lyellow"), colours.get("white"), VERSION]))
    print(_("copyright"))
    print("")

    if storage.read("locale") == None:
        output.warning(_("setLocaleWarning", [lang.getLocale(), args[0]]))
        print("")

if len(args) == 1:
    print(_("help", [args[0]]))
else:
    if args[1] == "help" or args[1] == "--help" or args[1] == "/?":
        print(_("help", [args[0]]))
    elif args[1] == "var":
        if len(args) > 2:
            name = args[2]

            if len(args) == 3:
                if storage.read(name) == None:
                    output.error(_("varNoMatch", [name]))
                else:
                    output.returns(_("varReturn", [name, storage.read(name)]))
            elif len(args) == 4:
                if args[3] == "--delete":
                    if storage.delete(name):
                        output.returns(_("varDeleteSuccess", [name]))
                    else:
                        output.error(_("varDeleteFail", [name]))
                else:
                    data = args[3]

                    storage.write(name, data)
                    
                    output.returns(_("varWriteReturn", [name, data]))
            else:
                output.error(_("invalidCommandStructure"))
        else:
            output.error(_("invalidCommandStructure"))
    else:
        output.error(_("invalidCommand"))