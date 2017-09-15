__author__ = "hugo-p"
__copyright__ = "Copyright 2017, The Sima Project"
__version__ = "1.0.0"
__contact__ = "hugo.pointcheval.fr"

import argparse
import shutil
from distutils import dir_util
import zipfile
import sys
import wget
import os
import subprocess
import importlib

class Downloader:
    """An update downloader"""

    def __init__(self):
        self.url = GetArguments().url
        self.script = GetArguments().script
        self.clean = GetArguments().clean

        self.dlDir = "updater_packages/"
        self.pkgName = "sima.zip" #here the filename (It must be the same as on server)

    def DlUpdate(self):
        try:
            file_name = wget.download(self.url)
        except:
            return("Error while downloading update.")
        try:
            zip_ref = zipfile.ZipFile(file_name, 'r')
            zip_ref.extractall(self.dlDir)
            zip_ref.close()
        except:
            return("\nError while extracting update.")

    def ApplyUpdate(self):
        try:
            dir_util.copy_tree(self.dlDir, "./")
        except:
            return("Error while copying files.")

def GetArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="the update package url")
    parser.add_argument("script", help="the script that will be executed after the update")
    parser.add_argument("-c", "--clean", help="clean folders", action="store_true")
    args = parser.parse_args()
    return args

def clean(dl):
    if os.path.isdir(dl.dlDir):
        print("Cleaning {d} ...".format(d=dl.dlDir))
        try:
            shutil.rmtree(dl.dlDir, ignore_errors=False, onerror=None)
        except:
            return("Error while cleaning local file. Please delete manually " + dl.dlDir)
    
    if os.path.exists(dl.pkgName):
        print("Cleaning {f} ...".format(f=dl.pkgName))
        try:
            os.remove(dl.pkgName)
        except:
            return("Error while cleaning local file. Please delete manually " + dl.pkgName)

def testError(error):
    if type(error) is str:
        print(error)
        sys.exit(1)

if __name__ == "__main__":
    dl = Downloader()

    error = clean(dl)
    testError(error)
    
    if dl.clean:
        print("Cleaning finished.")
        sys.exit(1)

    error = dl.DlUpdate()
    testError(error)
    
    error = dl.ApplyUpdate()
    testError(error)

    print("\nUpdated finished.")
    print("\nRestart your program.")