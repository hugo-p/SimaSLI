from sima import core, config, logger
from gtts import gTTS
from playsound import playsound
import os
import shutil
import hashlib
import sys

class Voice:
    """Voice synthesis plugin"""
    
    def __init__(self):
        self.lang = "en-uk"
        self.path = "data/voice/"

    def speak(self, word):
        my_config = config.Config()
        errorCheck(my_config.setconfig())

        if my_config.synth_lang == "french":
            self.lang = "fr"
            name = hashlib.md5((word.word_fr).encode('utf-8')).hexdigest()
            if os.path.exists(self.path + name + ".mp3"):
                logger.log(0, "voice.py --> File is already present.")
                playsound(self.path + name + ".mp3")
            else:
                logger.log(0, "voice.py --> File must be downloaded.")
                tts = gTTS(text=word.word_fr, lang=self.lang, slow=False)
                tts.save(self.path + name + ".mp3")
                playsound(self.path + name + ".mp3")
        else:
            self.lang = "en-uk"
            name = hashlib.md5((word.word_fr).encode('utf-8')).hexdigest()
            if os.path.exists(self.path + name + ".mp3"):
                logger.log(0, "voice.py --> File is already present.")
                playsound(self.path + name + ".mp3")
            else:
                logger.log(0, "voice.py --> File must be downloaded.")
                tts = gTTS(text=word.word_en, lang=self.lang, slow=False)
                tts.save(self.path + name + ".mp3")
                playsound(self.path + name + ".mp3")

    def cleanDb(self):
        my_config = config.Config()
        errorCheck(my_config.setconfig())
        if not my_config.synth_persistant:
            if os.path.isdir(self.path):
                logger.log(0, "voice.py --> Cleaning {d} ...".format(d=self.path))
                try:
                    for mp3 in os.listdir(self.path):
                        file_path = os.path.join(self.path, mp3)
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                except Exception as e:
                    return("Error while cleaning local file. Please delete manually " + self.path + " or restart Sima. Exception: " + e)
    
    def createDir(self):
        if not os.path.isdir(self.path):
            logger.log(0, "voice.py --> Voice database created.")
            os.makedirs(self.path)

def OnInit():
    Voice.createDir(Voice())

def OnCliLoad():
    pass

def OnGuiLoad(app):
    pass

def OnUpdate(app):
    pass

def OnInterpreter(word):
    Voice.speak(Voice(), word)

def OnGuiClose(app):
    errorCheck(Voice.cleanDb(Voice()))

def errorCheck(error):
    if type(error) is str:
        logger.log(3, error)
        sys.exit(1)