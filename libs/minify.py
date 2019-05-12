# Zapr
# 
# Copyright (C) LiveG. All Rights Reserved.
# Copying is not a victimless crime. Anyone caught copying LiveG software may
# face sanctions.
# 
# https://liveg.tech
# Licensed by the LiveG Open-Source Licence, which can be found at LICENCE.md.

import os
import re
import json
import jsmin
import htmlmin
import cssmin
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
        elif initialContentLines[0].startswith("// @import!"):
            try:
                library = initialContentLines[0][12:]
                libraryName = ""

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
            except:
                output.warning(_("illegalImport", [initialContentLines[0][3:]]))
        else:
            finalContentLines.append(initialContentLines[0])
        
        initialContentLines.pop(0)

    return jsmin.jsmin("\n".join(finalContentLines))

def html(content):
    minified = htmlmin.minify(content)
    imports = re.findall(r"\{\{ @import (.*?) \}\}", minified)

    for i in range(0, len(imports)):
        importStatement = "{{ @import " + imports[i] + " }}"

        library = imports[i]
        libraryName = ""

        if library.startswith("http://") or library.startswith("https://"):
            libraryName = library.split("/")[-1].split(".")[0]

            output.action(_("importLibrary", [libraryName, library]))

            try:
                site = urllib.request.urlopen(library)
                siteData = site.read().decode("utf-8")

                site.close()

                minified = minified.replace(importStatement, html(siteData))
            except:
                output.warning(_("unknownImport", [imports[i]]))
        else:
            libraryName = library.split("/")[-1]

            output.action(_("importLibrary", [libraryName, library + ".html"]))

            try:
                libPath = library.split("/")
                
                libPath[-1] += ".html"

                file = open(os.path.join(*libPath), "r")
                fileData = file.read()

                file.close()

                minified = minified.replace(importStatement, html(fileData))
            except:
                output.warning(_("unknownImport", [imports[i]]))

    return minified

def css(content):
    return cssmin.cssmin(content)

def translate(content, localeFile, locale):
    currentContent = content

    currentContent = currentContent.replace("{{ @locale }}", locale)
    currentContent = currentContent.replace("{{ @localeFriendlyName }}", localeFile["friendlyName"])
    currentContent = currentContent.replace("{{ @localeFriendlyNameShort }}", localeFile["friendlyNameShort"])
    currentContent = currentContent.replace("{{ @localeDirection }}", localeFile["direction"])

    ilReFinder = r"\{\{ @if locale: (.*?)" + re.escape(locale) + r"(.*?) \}\}(.*?)\{\{ @endIf \}\}"

    while len(re.findall(ilReFinder, currentContent)) > 0:
        currentContent = re.sub(ilReFinder, re.findall(ilReFinder, currentContent)[0][2], currentContent, count = 1)

    stringKeys = list(localeFile["strings"].keys())

    for i in range(0, len(stringKeys)):
        currentContent = currentContent.replace("{{ " + stringKeys[i] + " }}", localeFile["strings"][stringKeys[i]])

    return currentContent

def static(urlFormat, defaultLocale, staticFiles, localeFiles, rootFiles, workingDir, manifest):
    global importedLibs

    locales = {}

    output.action("Building root files...")

    for root, subdirs, files in os.walk(rootFiles):
        importedLibs = []

        neededPath = os.path.join("build", os.path.relpath(root, manifest["rootFiles"]))

        if not os.path.exists(neededPath):
            os.makedirs(neededPath)

        for i in range(0, len(files)):
            infile = open(os.path.join(root, files[i]), "r")
            infileData = infile.read()

            infile.close()

            outfile = open(os.path.join(neededPath, files[i]), "w")
            
            if files[i].endswith(".js"):
                outfile.write(js(infileData))
            elif files[i].endswith(".html"):
                outfile.write(html(infileData))
            elif files[i].endswith(".css"):
                outfile.write(css(infileData))
            else:
                outfile.write(infileData)

            outfile.close()
    
    for root, subdirs, files in os.walk(localeFiles):
        for i in range(0, len(files)):
            if not (files[i] in locales.keys()):
                locales[files[i].split(".")[0]] = os.path.join(root, files[i])
            else:
                output.warning(_("doubleLanguageFile", [root.replace("\\", "/") + files[i]]))

    supportedLocales = list(locales.keys())

    for i in range(0, len(supportedLocales)):
        output.action(_("buildLocale", [supportedLocales[i]]))

        openLocaleFile = open(locales[supportedLocales[i]], "r")
        openLocaleFileData = json.load(openLocaleFile)

        openLocaleFile.close()

        for root, subdirs, files in os.walk(staticFiles):
            importedLibs = []

            splittablePath = ("build/" + manifest["urlFormat"].replace("<locale>", supportedLocales[i]).replace("<path>", os.path.relpath(root, manifest["staticFiles"]))).split("/")
            neededPath = os.path.join(*splittablePath)

            if not os.path.exists(neededPath):
                os.makedirs(neededPath)

            for j in range(0, len(files)):
                infile = open(os.path.join(root, files[j]), "r")
                infileData = infile.read()

                infile.close()

                outfile = open(os.path.join(neededPath, files[j]), "w")
                
                if files[j].endswith(".js"):
                    outfile.write(js(infileData))
                elif files[j].endswith(".html"):
                    outfile.write(translate(html(infileData), openLocaleFileData, supportedLocales[i]))
                elif files[j].endswith(".css"):
                    outfile.write(css(infileData))
                else:
                    outfile.write(infileData)

                outfile.close()