import shutil
import requests
import json
import sys
import os
import errno
import argparse

parser = argparse.ArgumentParser(description="Downloads Images from Open Image database.")
parser.add_argument('-d','--dest', help='output folder name')
parser.add_argument('-j','--json', help='json database file name or location')
args = parser.parse_args()

def makeDir(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

outputFolder = args.dest 
jsonFile = args.json 

urls = []
makeDir(outputFolder)

for line in open(jsonFile, 'r'):
    urls.append(json.loads(line))

for u in urls:
    url = u['original_url']
    filename = os.path.basename(url) 
    fileToSave = outputFolder + '/' + filename
    with open(fileToSave, 'wb') as f:
        print url
        try:
            response = requests.get(url, stream=True, timeout=0.5, allow_redirects=False)
            if response.status_code == 200:
                for block in response.iter_content(1024):
                    if not block:
                        break
                    f.write(block)
        except requests.exceptions.RequestException as e:
            print e
