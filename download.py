import shutil
import requests
import json
import sys
import os
import errno
import argparse
from multiprocessing import Pool
from progress.bar import Bar

def makeDir(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def job(url):
    filename = os.path.basename(url) 
    fileToSave = args.dest + '/' + filename
    with open(fileToSave, 'wb') as f:
        try:
            response = requests.get(url, stream=True, timeout=0.5, allow_redirects=False)
            if response.status_code == 200:
                for block in response.iter_content(1024):
                    if not block:
                        break
                    f.write(block)
        except requests.exceptions.RequestException as e:
            print e

def main():
    makeDir(args.dest)
    
    urls = [json.loads(line)['original_url'] for line in open(args.json, 'r')]

    pool = Pool()
    bar = Bar('Downloading...', max=len(urls))
    for i in pool.imap(job, urls):
        bar.next()
    bar.finish()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Downloads Images from Open Image database.")
    parser.add_argument('-d','--dest', help='output folder name')
    parser.add_argument('-j','--json', help='json database file name or location')
    args = parser.parse_args()

    main()
