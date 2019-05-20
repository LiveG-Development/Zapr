# Zapr
# 
# Copyright (C) LiveG. All Rights Reserved.
# Copying is not a victimless crime. Anyone caught copying LiveG software may
# face sanctions.
# 
# https://liveg.tech
# Licensed by the LiveG Open-Source Licence, which can be found at LICENCE.md.

import os
import json

import libs.output as output
import libs.lang as lang

import libs.strings.en_GB

_ = lang._

def scan(content):
    contentLines = content.split("\n")
    generatedDocs = {}

    targetName = ""
    targetParams = []
    targetReturn = {}
    targetShortDescription = ""
    targetLongDescription = ""

    while len(contentLines) > 0:
        contentLines[0] = contentLines[0].strip()
        contentBody = contentLines[0].split(" ")

        if len(contentBody) > 0:
            if contentBody[0] == "@name":
                if len(contentBody) > 1:
                    if targetName != "":
                        generatedDocs[targetName] = {
                            "params": targetParams,
                            "return": targetReturn,
                            "shortDescription": targetShortDescription,
                            "longDescription": targetLongDescription
                        }

                        targetName = ""
                        targetParams = []
                        targetReturn = {}
                        targetShortDescription = ""
                        targetLongDescription = ""

                    targetName = " ".join(contentBody[1:])
                else:
                    output.warning(_("genDocsIllegal", [contentLines[0]]))
            elif contentBody[0] == "@param":
                if len(contentBody) >= 4:
                    if targetName != "":
                        targetParams.append({
                            "name": contentBody[1],
                            "type": contentBody[2],
                            "description": " ".join(contentBody[3:])
                        })
                    else:
                        output.warning(_("genDocsUnspecified", [contentLines[0]]))
                else:
                    output.warning(_("genDocsIllegal", [contentLines[0]]))
            elif contentBody[0] == "@return":
                if len(contentBody) >= 3:
                    if targetName != "":
                        targetReturn = {
                            "type": contentBody[1],
                            "description": " ".join(contentBody[2:])
                        }
                    else:
                        output.warning(_("genDocsUnspecified", [contentLines[0]]))
                else:
                    output.warning(_("genDocsIllegal", [contentLines[0]]))
            elif contentBody[0] == "@shortDescription":
                if len(contentBody) > 1:
                    if targetName != "":
                        targetShortDescription = " ".join(contentBody[1:])
                    else:
                        output.warning(_("genDocsUnspecified", [contentLines[0]]))
                else:
                    output.warning(_("genDocsIllegal", [contentLines[0]]))
            elif contentBody[0] == "@longDescription":
                if len(contentBody) > 1:
                    if targetName != "":
                        if targetLongDescription == "":
                            targetLongDescription = " ".join(contentBody[1:])
                        else:
                            targetLongDescription += "\n" + " ".join(contentBody[1:])
                    else:
                        output.warning(_("genDocsUnspecified", [contentLines[0]]))
                else:
                    output.warning(_("genDocsIllegal", [contentLines[0]]))

        contentLines.pop(0)
    
    if targetName != "":
        generatedDocs[targetName] = {
            "params": targetParams,
            "return": targetReturn,
            "shortDescription": targetShortDescription,
            "longDescription": targetLongDescription
        }
    
    return generatedDocs

def generate():
    for root, subdirs, files in os.walk(os.getcwd()):
        importedLibs = []

        neededPath = os.path.join("docs", os.path.relpath(root))

        if not os.path.exists(neededPath):
            os.makedirs(neededPath)

        for i in range(0, len(files)):
            if os.path.isfile(os.path.join(root, files[i])):
                infile = open(os.path.join(root, files[i]), "rb")
                infileData = infile.read()

                infile.close()

                outfile = open(os.path.join(neededPath, ".".join(files[i].split(".")[:-1])) + ".json", "w")
                
                if files[i].endswith(".js"):
                    output.action(_("genDocs", [files[i]]))

                    json.dump(scan(infileData.decode("utf-8")), outfile)

                outfile.close()
    
    output.returns(_("genDocsSuccessful"))