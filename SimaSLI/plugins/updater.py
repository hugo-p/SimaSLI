from sima import core, config, logger
from appJar import gui
import base64
import requests
import importlib
import sys
import os


class Updater:
    """Updater plugin"""
    def __init__(self):
        self.update = False
        self.local = config.__version__
        self.current = 0.0

        self.url = 'https://raw.githubusercontent.com/hugo-p/SimaSLI/master/SimaSLI/data/version'
    
    def CheckUpdate(self):
        req = requests.get(self.url)
        if req.status_code == requests.codes.ok:
            self.current = float(req.text)
            if self.current > self.local:
                self.update = True
            else:
                self.update = False
        else:
            return("Content was not found.")


def OnInit():
    logger.log(0, "updater.py --> OnInit()")
    my_config = config.Config()
    errorCheck(my_config.setconfig())
    
    if my_config.update_check:
        updater = Updater()
        error = updater.CheckUpdate() #no error test, if no connection
        
        if updater.update:
            logger.log(0, "updater.py --> Local version: {lv} | Current version: {cv}".format(lv=updater.local, cv=updater.current))
            logger.log(2, "A new version is available")
            logger.log(2, "SimaSLI | v{ver}".format(ver=updater.current))

            if my_config.update_auto:
                if os.path.exists("downloader.py"):
                    logger.log(0, "downloader.py --> initialize a downloader")
                    os.system("downloader.py http://hugo.pointcheval.fr/projets/sima/projects/simasli/sima.zip sima.py")

                elif os.path.exists("downloader.exe"):
                    logger.log(0, "downloader.exe --> initialize a downloader")
                    os.system("downloader.exe http://hugo.pointcheval.fr/projets/sima/projects/simasli/sima.zip sima.py")
            else:
                logger.log(2, "Enable auto-update or go through GUI to download it.")

        else:
            logger.log(0, "updater.py --> Local version: {lv} | Current version: {cv}".format(lv=updater.local, cv=updater.current))
            logger.log(1, "You have latest version")
            logger.log(1, "SimaSLI | v{ver}".format(ver=updater.local))
    else:
            logger.log(0, "updater.py --> Local version: {lv} | Current version: {cv}".format(lv=config.__version__, cv="Not checked."))
            logger.log(2, "Current version not checked. [EnableUpdateCheck=False]")
            logger.log(1, "SimaSLI | v{ver}".format(ver=config.__version__))        

def OnCliLoad():
    pass

def OnGuiLoad(app):
    pass

def OnUpdate(app):
    logger.log(0, "updater.py --> OnUpdate()")
    
    updater = Updater()
    error = updater.CheckUpdate() #no error test, if no connection
    
    if updater.update:
        rep = app.yesNoBox("Update checker", "An update is available!\nYour version: v{lv}\nActual version: v{cv}\nProceed to update?".format(lv=updater.local, cv=updater.current))
        if rep:
            if os.path.exists("downloader.py"):
                logger.log(0, "downloader.py --> initialize a downloader")
                os.system("downloader.py http://hugo.pointcheval.fr/projets/sima/projects/simasli/sima.zip sima.py")

            elif os.path.exists("downloader.exe"):
                logger.log(0, "downloader.exe --> initialize a downloader")
                os.system("downloader.exe http://hugo.pointcheval.fr/projets/sima/projects/simasli/sima.zip sima.py")
    else:
        app.okBox("Update checker", "No update found!\nYou have the latest version.")

def OnInterpreter(word):
    pass

def OnGuiClose(app):
    pass

def errorCheck(error):
    if type(error) is str:
        logger.log(3, error)
        sys.exit(1)