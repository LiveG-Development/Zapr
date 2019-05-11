# Zapr
# 
# Copyright (C) LiveG. All Rights Reserved.
# Copying is not a victimless crime. Anyone caught copying LiveG software may
# face sanctions.
# 
# https://liveg.tech
# Licensed by the LiveG Open-Source Licence, which can be found at LICENCE.md.

import os
import jsmin
import urllib.request

import libs.output as output
import libs.lang as lang

import libs.strings.en_GB

_ = lang._

importedLibs = []

def js(content):
    initialContentLines = content.split("\n")
    finalContentLines = []

    while len(initialContentLines) > 0:
        if initialContentLines[0].startswith("// @import"):
            try:
                library = initialContentLines[0][11:]
                libraryName = ""

                if not (library in importedLibs):
                    importedLibs.append(library)

                    if library.startswith("http://") or library.startswith("https://"):
                        libraryName = library.split("/")[-1].split(".")[0]

                        output.action(_("importLibrary", [libraryName, library]))

                        try:
                            site = urllib.request.urlopen(library)
                            siteData = site.read().decode("utf-8")

                            site.close()

                            finalContentLines.append(js(siteData))
                        except:
                            output.warning(_("unknownImport", [initialContentLines[0][3:]]))
                    else:
                        libraryName = library.split("/")[-1]

                        output.action(_("importLibrary", [libraryName, library + ".js"]))

                        try:
                            libPath = library.split("/")
                            
                            libPath[-1] += ".js"

                            file = open(os.path.join(*libPath), "r")
                            fileData = file.read()

                            file.close()

                            finalContentLines.append(js(fileData))
                        except:
                            output.warning(_("unknownImport", [initialContentLines[0][3:]]))
                else:
                    output.action(_("circularImport", [library]))
            except:
                output.warning(_("illegalImport", [initialContentLines[0][3:]]))
        else:
            finalContentLines.append(initialContentLines[0])
        
        initialContentLines.pop(0)

    return jsmin.jsmin("\n".join(finalContentLines))