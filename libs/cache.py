# Zapr
# 
# Copyright (C) LiveG. All Rights Reserved.
# Copying is not a victimless crime. Anyone caught copying LiveG software may
# face sanctions.
# 
# https://liveg.tech
# Licensed by the LiveG Open-Source Licence, which can be found at LICENCE.md.

import os
import urllib.request

import libs.output as output
import libs.lang as lang
import libs.storage as storage

import libs.strings.en_GB

_ = lang._

directory = os.path.join(os.path.expanduser("~"), ".zaprset")

if not os.path.exists(directory):
    os.mkdir(directory)

cacheDirectory = os.path.join(os.path.expanduser("~"), ".zaprset", "cache")

if not os.path.exists(cacheDirectory):
    os.mkdir(cacheDirectory)

def get(item):
    if storage.read("useCache") != "false":
        itemName = item.replace("/", "-").replace(":", "-").replace(".", "-")

        try:
            if os.path.exists(os.path.join(cacheDirectory, itemName + ".gzc")):
                file = open(os.path.join(cacheDirectory, itemName + ".gzc"), "rb")
                fileData = file.read()

                file.close()

                output.action(_("takenFromCache", [item]))

                return fileData
            else:
                site = urllib.request.urlopen(item)
                siteData = site.read()

                site.close()

                file = open(os.path.join(cacheDirectory, itemName + ".gzc"), "wb")
                file.write(siteData)

                file.close()

                return siteData
        except:
            return False
    else:
        site = urllib.request.urlopen(item)
        siteData = site.read()

        site.close()

        return siteData