import configparser
import argparse

__version__ = 5.0

class Config:
    """All config attributs"""

    def __init__(self):
        self.port = ""
        self.baud = 9600
        self.refresh = 100
        self.serial_timeout = 10

        self.db_path = "data/database.xml"
        self.debug_mode = False
        self.default_code = 14111
        
        self.synth_lang = "english"
        self.synth_persistant = True
        self.update_check = True
        self.update_auto = False
   
    def setconfig(self):
        self.config = configparser.ConfigParser()
        self.configfile = "data/settings.ini"

        if not self.config.read(self.configfile, encoding='utf-8'):
            return ("Config file not found.")

        self.config = configparser.ConfigParser(interpolation=None)
        self.config.read(self.configfile, encoding='utf-8')

        self.confsections = {"ARDUINO", "SIMA", "PLUGINS"}.difference(self.config.sections())
        if self.confsections:
            return ("Config section missing: {}".format(', '.join(['[%s]' % s for s in self.confsections])))

        self.port = self.config.get('ARDUINO', 'Port', fallback=None)
        self.baud = self.config.getint('ARDUINO', 'BaudRate', fallback=9600)
        self.refresh = self.config.getint('ARDUINO', 'RefreshRate', fallback=100)
        self.serial_timeout = self.config.getint('ARDUINO', 'SerialTimeout', fallback=10)

        self.db_path = self.config.get('SIMA', 'DatabasePath', fallback="data/database.xml")
        self.debug_mode = self.config.getboolean('SIMA', 'EnableDebugMode', fallback=False)
        self.default_code = self.config.getint('SIMA', 'DefaultCode', fallback=14111)

        self.synth_lang = self.config.get('PLUGINS', 'SynthLang', fallback="english")
        self.synth_persistant = self.config.getboolean('PLUGINS', 'SynthEnablePersistance', fallback=True)
        self.update_check = self.config.getboolean('PLUGINS', 'EnableUpdateCheck', fallback=True)
        self.update_auto = self.config.getboolean('PLUGINS', 'EnableAutoUpdate', fallback=False)

def GetArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--console", help="Legacy mode.", action="store_true")
    parser.add_argument("-n", "--noplugins", help="Disable all plugins.", action="store_true")
    args = parser.parse_args()
    return args

def saveconfig(section, key, value):
    try:
        config = configparser.RawConfigParser()
        config.read('data/settings.ini')
        config.set((section), (key), (value))
        with open('data/settings.ini', 'w+') as cfg:
            config.write(cfg)
            cfg.close()
        with open('data/settings.ini', 'a') as myfile:
            myfile.write('''# Configure the right serial port
# Windows: COM1, COM2, COM3 etc..
# Linux : /dev/ttyUSB0 or /dev/ttys0
# Set the Baud rate
# Set the refresh rate (send code every x milliseconds)
# Set the serial timeout (timer before the port is considered unavailable)

# Set the path of your database file
# Configure the debug mode in console
# Set the default code if the glove is offline.

# Configure the default language for the voice synthesis. ('french' or 'english')
# Enable/Disable persistant mode. (audio files are conserved if enable)
# Enable/Disable Update Checker
# Enable/Disable Auto updater''')
            myfile.close()
    except:
        return ("Error while saving configuration file")