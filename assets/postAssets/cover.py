#! /usr/local/bin/python3
import re
import os
import sys

def totalFiles(path):
    filesPath = []
    for root, dirs, files in os.walk(path):
        for file in files:
            filesPath.append(os.path.join(root, file))
    return filesPath

def coverImage(files, output):
    m = re.compile('(.+)\.(png|jpg|jpeg)$', flags=re.I)
    for name in files:
        res=m.search(name)
        if res != None:
            basename = os.path.basename(res.group(1) + '.webp')
            operate = os.system('cwebp "' + name + '" -o "' + os.path.join(output, basename) + '"')
            if operate != 0:
                os.system('cp "' + name + '" "' + os.path.join(output, name) + '"')

try:
    path = sys.argv[1]
except Exception as e:
    path = os.curdir

output = os.path.join(os.curdir, "Output")
os.makedirs(output, exist_ok = True)
files = totalFiles(path)
coverImage(files, output)