# Zapr
# 
# Copyright (C) LiveG. All Rights Reserved.
# Copying is not a victimless crime. Anyone caught copying LiveG software may
# face sanctions.
# 
# https://liveg.tech
# Licensed by the LiveG Open-Source Licence, which can be found at LICENCE.md.

import os
import sys
import subprocess
import json

import libs.colours as colours
import libs.storage as storage
import libs.output as output
import libs.lang as lang
import libs.minify as minify

import libs.strings.en_GB

_ = lang._

VERSION = "V0.1.0"

args = sys.argv

if (len(args) > 1 and (args[1] == "--hide" or args[1] == "-h")):
    args.pop(1)
elif storage.read("hide") != "true":
    print(_("welcome", [colours.get("lyellow"), colours.get("white"), VERSION]))
    print(_("copyright"))
    print("")

    if storage.read("locale") == None:
        output.warning(_("setLocaleWarning", [lang.getLocale()]))
        print("")

try:
    import jsmin
except:
    output.action(_("installRequiredLibs"))

    returns = subprocess.call([sys.executable, "-m", "pip", "install", "jsmin"], stdout = subprocess.PIPE, stderr = subprocess.PIPE)

    if returns != 0:
        output.error(_("installRequiredLibsError"))

        sys.exit(1)

if len(args) == 1:
    print(_("help"))
else:
    if args[1] == "help" or args[1] == "--help" or args[1] == "/?":
        print(_("help"))
    elif args[1] == "var":
        if len(args) > 2:
            name = args[2]

            if len(args) == 3:
                if storage.read(name) == None:
                    output.error(_("varNoMatch", [name]))
                    sys.exit(1)
                else:
                    output.returns(_("varReturn", [name, storage.read(name)]))
            elif len(args) == 4:
                if args[3] == "--delete":
                    if storage.delete(name):
                        output.returns(_("varDeleteSuccess", [name]))
                    else:
                        output.error(_("varDeleteFail", [name]))
                        sys.exit(1)
                else:
                    data = args[3]

                    storage.write(name, data)
                    
                    output.returns(_("varWriteReturn", [name, data]))
            else:
                output.error(_("invalidCommandStructure"))
                sys.exit(1)
        else:
            output.error(_("invalidCommandStructure"))
            sys.exit(1)
    elif args[1] == "build":
        if args[2] == "app":
            output.action(_("buildingDir", [os.getcwd()]))

            manifest = {}
            manifestLoads = {}

            try:
                manifestFile = open(os.path.join(os.getcwd(), "manifest.json"), "r")
                manifest = json.load(manifestFile)
            except:
                output.error(_("invalidManifest"))
                sys.exit(1)

            try:
                manifestLoads["package"] = manifest["package"]
                manifestLoads["version"] = manifest["version"]
                manifestLoads["name"] = manifest["name"]
                manifestLoads["description"] = manifest["description"]
                manifestLoads["defaultLocale"] = manifest["defaultLocale"]
                manifestLoads["mainScript"] = manifest["mainScript"]
            except:
                output.error(_("invalidManifest"))
                sys.exit(1)

            try:
                directory = os.path.join(os.getcwd(), "build")

                if not os.path.exists(directory):
                    os.mkdir(directory)

                infile = open(os.path.join(os.getcwd(), manifestLoads["mainScript"]), "r")
                outfile = open(os.path.join(directory, manifestLoads["package"] + "-" + manifestLoads["version"] + ".html"), "w")
                outtext = "<!DOCTYPE html><html><head><title>" + manifest["name"][manifestLoads["defaultLocale"]].replace("</title>", "<\/title>") + "</title><meta name=\"viewport\" content=\"width=device-width, initial-scale=1, maximum-scale=1, minimum-scale=1, user-scalable=no, minimal-ui\"><script>"
                outtext += minify.js(infile.read()).replace("</script>", "<\/script>")
                outtext += "</script></head><body></body></html>"

                outfile.write(outtext)
                outfile.close()

                output.returns(_("buildSuccessful"))
            except:
                output.error(_("buildError"))
                sys.exit(1)
        else:
            output.error(_("invalidCommandStructure"))
            sys.exit(1)
    else:
        output.error(_("invalidCommand"))
        sys.exit(1)

sys.exit(0)