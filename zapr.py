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
import shutil
import subprocess
import json

import libs.colours as colours
import libs.storage as storage
import libs.output as output
import libs.lang as lang
import libs.serve as serve

import libs.strings.en_GB

_ = lang._

VERSION = "V0.1.0"

args = sys.argv

requiredInstalls = False

if (len(args) > 1 and (args[1] == "--hide" or args[1] == "-h")):
    args.pop(1)
elif storage.read("hide") != "true":
    print(_("welcome", [colours.get("lyellow"), colours.get("white"), VERSION]))
    print(_("copyright"))
    print("")

    if storage.read("locale") == None:
        output.warning(_("setLocaleWarning", [lang.getLocale()]))
        print("")

# Install libraries for when they don't exist
def installLib(name, description):
    global requiredInstalls

    requiredInstalls = True

    output.action(_("installRequiredLibs", [description]))

    returns = subprocess.call([sys.executable, "-m", "pip", "install", name], stdout = subprocess.PIPE, stderr = subprocess.PIPE)

    if returns != 0:
        output.error(_("installRequiredLibsError"))

        sys.exit(1)

# Try importing the libraries, if not install them
try:
    import jsmin
except:
    installLib("jsmin", "JavaScript minifier")

try:
    import htmlmin
except:
    installLib("htmlmin", "HTML minifier")

try:
    import cssmin
except:
    installLib("cssmin", "CSS minifier")

if requiredInstalls: print("")

# Finally, import any local libraries that require the external libraries
import libs.minify as minify

# CLI section
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
        if len(args) > 2:
            if args[2] == "app":
                output.action(_("buildDir", [os.getcwd()]))

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
            elif args[2] == "static":
                output.action(_("cleanUpBuildDir"))

                try:
                    shutil.rmtree("build")
                except:
                    pass

                output.action(_("buildDir", [os.getcwd()]))

                manifest = {}
                manifestLoads = {}

                try:
                    manifestFile = open(os.path.join(os.getcwd(), "manifest.json"), "r")
                    manifest = json.load(manifestFile)
                except:
                    output.error(_("invalidManifest"))
                    sys.exit(1)

                try:
                    manifestLoads["urlFormat"] = manifest["urlFormat"]
                    manifestLoads["defaultLocale"] = manifest["defaultLocale"]
                    manifestLoads["staticFiles"] = manifest["staticFiles"]
                    manifestLoads["localeFiles"] = manifest["localeFiles"]
                    manifestLoads["rootFiles"] = manifest["rootFiles"]
                except:
                    output.error(_("invalidManifest"))
                    sys.exit(1)

                try:
                    directory = os.path.join(os.getcwd(), "build")

                    if not os.path.exists(directory):
                        os.mkdir(directory)

                    urlFormat = manifestLoads["urlFormat"]
                    defaultLocale = manifestLoads["defaultLocale"]

                    staticPath = manifestLoads["staticFiles"].split("/")
                    staticFiles = os.path.join(*staticPath)

                    localePath = manifestLoads["localeFiles"].split("/")
                    localeFiles = os.path.join(*localePath)

                    rootPath = manifestLoads["rootFiles"].split("/")
                    rootFiles = os.path.join(*rootPath)

                    minify.static(urlFormat, defaultLocale, staticFiles, localeFiles, rootFiles, os.getcwd(), manifestLoads)

                    output.returns(_("buildSuccessful"))
                except:
                    output.error(_("buildError"))
                    sys.exit(1)
            else:
                output.error(_("invalidCommandStructure"))
                sys.exit(1)
        else:
            output.error(_("invalidCommandStructure"))
            sys.exit(1)
    elif args[1] == "serve":
        try:
            serve.serve()
        except:
            output.error(_("serveError"))
            sys.exit(1)
    else:
        output.error(_("invalidCommand"))
        sys.exit(1)

sys.exit(0)
