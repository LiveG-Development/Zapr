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
import base64
import json
import jsmin
import htmlmin
import cssmin

import libs.output as output
import libs.lang as lang
import libs.cache as cache

import libs.strings.en_GB

_ = lang._

importedLibs = []
importedAssets = []

def js(content):
    initialContentLines = content.split("\n")
    finalContentLines = []

    finalContentLines.append("var _assets = {};")

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
                            siteData = cache.get(library)

                            if siteData != False:
                                finalContentLines.append(js(siteData.decode("utf-8")))
                            else:
                                output.warning(_("unknownImport", [initialContentLines[0][3:]]))
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
                        siteData = cache.get(library)

                        if siteData != False:
                            finalContentLines.append(js(siteData.decode("utf-8")))
                        else:
                            output.warning(_("unknownImport", [initialContentLines[0][3:]]))
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
        elif initialContentLines[0].startswith("// @asset"):
            try:
                asset = initialContentLines[0][10:]
                assetName = ""

                if not (asset in importedAssets):
                    importedLibs.append(asset)

                    if asset.startswith("http://") or asset.startswith("https://"):
                        assetName = asset.split("/")[-1]

                        output.action(_("importAsset", [assetName, asset]))

                        try:
                            siteData = cache.get(asset)

                            if siteData != False:
                                finalContentLines.append("_assets[\"" + assetName.replace("\"", "-") + "\"] = \"" + base64.b64encode(siteData).decode("utf-8") + "\";")
                            else:
                                output.warning(_("unknownAsset", [initialContentLines[0][3:]]))
                        except:
                            output.warning(_("unknownAsset", [initialContentLines[0][3:]]))
                    else:
                        assetName = asset.split("/")[-1]

                        output.action(_("importAsset", [assetName, asset]))

                        try:
                            file = open(os.path.join(*asset.split("/")), "rb")
                            fileData = file.read()

                            file.close()

                            finalContentLines.append("_assets[\"" + assetName.replace("\"", "-") + "\"] = \"" + base64.b64encode(fileData).decode("utf-8") + "\";")
                        except:
                            output.warning(_("unknownAsset"), [initialContentLines[0][3:]])
            except:
                output.warning(_("illegalAsset", [initialContentLines[0][3:]]))
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
                siteData = cache.get(library)

                if siteData != False:
                    minified = minified.replace(importStatement, html(siteData.decode("utf-8")))
                else:
                    output.warning(_("unknownImport", [initialContentLines[0][3:]]))
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
            infile = open(os.path.join(root, files[i]), "rb")
            infileData = infile.read()

            infile.close()

            outfile = open(os.path.join(neededPath, files[i]), "wb")
            
            if files[i].endswith(".js"):
                outfile.write(js(infileData.decode("utf-8")).encode("utf-8"))
            elif files[i].endswith(".html"):
                outfile.write(html(infileData.decode("utf-8")).encode("utf-8"))
            elif files[i].endswith(".css"):
                outfile.write(css(infileData.decode("utf-8")).encode("utf-8"))
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
                infile = open(os.path.join(root, files[j]), "rb")
                infileData = infile.read()

                infile.close()

                outfile = open(os.path.join(neededPath, files[j]), "wb")
                
                if files[j].endswith(".js"):
                    outfile.write(js(infileData.decode("utf-8")).encode("utf-8"))
                elif files[j].endswith(".html"):
                    outfile.write(translate(html(infileData.decode("utf-8")), openLocaleFileData, supportedLocales[i]).encode("utf-8"))
                elif files[j].endswith(".css"):
                    outfile.write(css(infileData.decode("utf-8")).encode("utf-8"))
                else:
                    outfile.write(infileData)

                outfile.close()