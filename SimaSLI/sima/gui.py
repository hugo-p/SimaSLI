import sys
import serial
import os
import time
from appJar import gui
from sima import core, config, logger, plugin
import plugins.PluginLoader as pl

import random

global status
status = 0

fontDefault = ("Comic Sans", "15", "normal")
fontInterLabel = ("Sans Serif", "35", "bold")

my_config = config.Config()

if type(my_config.setconfig()) is str:
    logger.log(3, error)
    sys.exit(1)

my_board = core.Arduino(my_config.port, my_config.baud, my_config.serial_timeout, my_config.refresh)
my_board.initialize()

def btnFunc(button):
    global status
    if button == "Reload":
        refreshConfig(app)
    elif button == "Apply":
        applyConfig(app)
    elif button == "plgquit":
        app.hideSubWindow("subPluginManager")
        status = 0
    elif button == "applyLearn":
        if status == 2:
            #in learning mode
            if my_board.state:
                code = my_board.lastline
                word_fr = app.getEntry("French word")
                word_en = app.getEntry("English word")
                my_db.AddDB(code, word_fr, word_en, my_config.db_path)
                logger.log(0, "New entry added to database: {code};{word_fr};{word_en}".format(code=code,word_fr=word_fr,word_en=word_en))
            else:
                logger.log(2, "Can't learn new words in no-glove mode.")


def tbFunc(button):
    global status
    if button == "HOME":
        homeScreen()
        status = 0
    elif button == "INTERPRETATION":
        interScreen()
        status = 1
    elif button == "LEARNING":
        learnScreen()
        launch("subLearn")
        status = 2
    elif button == "REFRESH GLOVE":
        refreshGlove(app)
    elif button == "REFRESH DATABASE":
        refreshDB(app)
    elif button == "OPEN DATABASE":
        openDB(app)
    elif button == "SETTINGS":
        launch("subSettings")
        status = 4
    elif button == "UPDATER":
        pl.OnUpdate(app)
    elif button == "PLUGIN MANAGER":
        launch("subPluginManager")
        status = 3
    elif button == "ABOUT":
        simaAbout(app)
    elif button == "FULLSCREEN":
        fullscreen(app)
    elif button == "CONSOLE":
        app.stop()
        logger.log(0, "Console mode...")
        from sima import cli
    elif button == "EXIT":
        app.stop()

def fullscreen(self):
    app.setToolbarButtonDisabled("FULLSCREEN")
    app.setGeometry("fullscreen")

def launch(win):
    app.showSubWindow(win)

def openDB(self):
    path = app.openBox(title="Open database", dirName="data/", fileTypes=[('database', '*.db'), ('database', '*.xml'), ('plain text', '*.txt')], asFile=True)
    if path is None:
        logger.log(0, "Opening aborded")
    else:
        logger.log(0, ("Opened: " + os.path.relpath(path.name))) #get relative path
        config.saveconfig('SIMA', 'DatabasePath', os.path.relpath(path.name))
        refreshConfig(app)
        refreshDB(app)

def refreshDB(self):
    logger.log(0, "Refresh database.")
    global my_db
    my_db = core.Database()
    my_db.LoadDB(my_config.db_path)
    app.setStatusbar("Words loaded: {}".format(len(my_db.wordlist)), 0)

def refreshGlove(self):
    logger.log(0, "Reset glove connection.")
    my_board.stop()
    my_board.initialize()

def refreshStatusbar():
    if status == 0:
        #idle
        app.setStatusbar("Status: {}".format("idle"), 1)
    elif status == 1:
        #interpretation
        app.setStatusbar("Status: {}".format("interpretation"), 1)
    elif status == 2:
        #interpretation
        app.setStatusbar("Status: {}".format("learning"), 1)
    elif status == 3:
        #interpretation
        app.setStatusbar("Status: {}".format("plugin manager"), 1)
    elif status == 4:
        #interpretation
        app.setStatusbar("Status: {}".format("settings"), 1)

def checkStop():
    pl.OnGuiClose(app)
    return True

def simaAbout(self):
    app.infoBox("About SimaSLI", 
                        "---\n" + 
                        "Application wrote by hugo-p." + "\n" +
                        "---\n" +
                        "This software is the host for Sima Glove that actually interprets sign language.\nSimaSLI is licensed under the Apache License 2.0\nProject by Benoit, hugo-p, Loris and Le Bao.\n" +
                        "---\n\t" +
                        app.SHOW_VERSION().replace("\n", "\n\t") + "\n" +
                        "---")
def simaHelp(self):
    app.infoBox("SimaSLI", "For help, visit " + "http://hugo.pointcheval.fr")

def addIconMenu(self):
        if app.platform == app.MAC:
            logger.log(0, "Detected platform: MAC")
            app.addMenuItem("MAC_APP", "About SimaSLI", simaAbout)
            app.addMenuWindow()
            app.addMenuHelp(app.appJarHelp)
        elif app.platform == app.WINDOWS:
            logger.log(0, "Detected platform: WINDOWS")
            app.addMenuSeparator('WIN_SYS')
            app.addMenuItem("WIN_SYS", "About SimaSLI", simaAbout)
            app.addMenuItem("WIN_SYS", "SimaSLI Help", simaHelp)

def refreshConfig(self):
    global my_config
    my_config = config.Config()
    error = my_config.setconfig()

    if type(error) is str:
        logger.log(3, error)
        sys.exit(1)
    
    app.setEntry("entryPort", my_config.port)
    app.setSpinBox("spinBaud", my_config.baud, callFunction=False)
    app.setSpinBox("spinRefresh", my_config.refresh, callFunction=False)
    app.setSpinBox("spinSerTimeout", my_config.serial_timeout, callFunction=False)

    app.setEntry("entryDbPath", my_config.db_path)
    app.setCheckBox("EnableDebugMode", ticked=my_config.debug_mode, callFunction=False)
    app.setSpinBox("spinDbgCode", my_config.default_code, callFunction=False)

    app.setSpinBox("spinSynthLang", my_config.synth_lang, callFunction=False)
    app.setCheckBox("SynthEnablePersistance", ticked=my_config.synth_persistant, callFunction=False)
    app.setCheckBox("EnableUpdateCheck", ticked=my_config.update_check, callFunction=False)
    app.setCheckBox("EnableAutoUpdate", ticked=my_config.update_auto, callFunction=False)

def applyConfig(self):
    config.saveconfig('ARDUINO', 'Port', app.getEntry("entryPort"))
    config.saveconfig('ARDUINO', 'BaudRate', app.getSpinBox("spinBaud"))
    config.saveconfig('ARDUINO', 'RefreshRate', app.getSpinBox("spinRefresh"))
    config.saveconfig('ARDUINO', 'SerialTimeout', app.getSpinBox("spinSerTimeout"))

    config.saveconfig('SIMA', 'DatabasePath', app.getEntry("entryDbPath"))
    config.saveconfig('SIMA', 'EnableDebugMode', app.getCheckBox("EnableDebugMode"))
    config.saveconfig('SIMA', 'DefaultCode', app.getSpinBox("spinDbgCode"))

    config.saveconfig('PLUGINS', 'SynthLang', app.getSpinBox("spinSynthLang"))
    config.saveconfig('PLUGINS', 'SynthEnablePersistance', app.getCheckBox("SynthEnablePersistance"))
    config.saveconfig('PLUGINS', 'EnableUpdateCheck', app.getCheckBox("EnableUpdateCheck"))
    config.saveconfig('PLUGINS', 'EnableAutoUpdate', app.getCheckBox("EnableAutoUpdate"))
    
# create a GUI variable called app
app = gui("Sima: Sign Language Interpreter | Version {}".format(config.__version__), "1280x720")
app.setIcon("res/sima.gif")
app.setResizable(canResize=False)
app.setGuiPadding(5, 5)
app.setBg("white")
app.setFont(15, fontDefault)
app.bindKey("r", refreshDB)
app.bindKey("o", openDB)
app.bindKey("g", refreshGlove)
pl.OnGuiLoad(app)

# Main components
tools = ["HOME", "INTERPRETATION", "LEARNING", "REFRESH GLOVE", "REFRESH DATABASE", "OPEN DATABASE", "SETTINGS", "UPDATER", "PLUGIN MANAGER" ,"ABOUT", "FULLSCREEN", "CONSOLE",  "EXIT"]
app.addToolbar(tools, tbFunc, findIcon=False)
app.setToolbarImage("HOME", "res/home.gif")
app.setToolbarImage("INTERPRETATION", "res/interpretation.gif")
app.setToolbarImage("LEARNING", "res/learning.gif")
app.setToolbarImage("REFRESH GLOVE", "res/reload_hand.gif")
app.setToolbarImage("REFRESH DATABASE", "res/database_refresh.gif")
app.setToolbarImage("OPEN DATABASE", "res/database_open.gif")
app.setToolbarImage("SETTINGS", "res/settings.gif")
app.setToolbarImage("UPDATER", "res/update_checker.gif")
app.setToolbarImage("PLUGIN MANAGER", "res/plugin_manager.gif")
app.setToolbarImage("ABOUT", "res/about.gif")
app.setToolbarImage("FULLSCREEN", "res/fullscreen.gif")
app.setToolbarImage("CONSOLE", "res/console.gif")
app.setToolbarImage("EXIT", "res/exit.gif")

app.addStatusbar(fields=2)

my_db = core.Database()
my_db.LoadDB(my_config.db_path)
app.setStatusbar("Words loaded: {}".format(len(my_db.wordlist)), 0)

addIconMenu(app)

# Main screen
app.addLabel("help", "Welcome in SimaSLI v{} ! Choose a mode in the toolbar.".format(config.__version__))
app.getLabelWidget("help").config(font=fontDefault)

app.addLabel("words", "Signe non reconnu\nUnknown sign")
app.getLabelWidget("words").config(font=fontInterLabel)

app.setLabel("words", "FR: {fr}\nEN: {en}".format(fr="Non reconnu", en="Unknown sign"))
app.setLabelFg("words", "red")

app.setLabelHeight("help", 27)
app.hideLabel("words")
app.setToolbarButtonDisabled("HOME")

# Interpretation screen
def interScreen():
    app.setLabelHeight("help", 0)
    app.setLabelHeight("words", 20)
    app.hideLabel("help")
    app.setToolbarButtonEnabled("HOME")
    app.setToolbarButtonEnabled("LEARNING")
    app.setToolbarButtonDisabled("INTERPRETATION")
    app.showLabel("words")

# Home screen
def homeScreen():
    app.setLabelHeight("help", 27)
    app.setLabelHeight("words", 0)
    app.hideLabel("words")
    app.setToolbarButtonEnabled("INTERPRETATION")
    app.setToolbarButtonEnabled("LEARNING")
    app.setToolbarButtonDisabled("HOME")
    app.showLabel("help")

def learnScreen():
    app.setLabelHeight("help", 0)
    app.setLabelHeight("words", 20)
    app.hideLabel("help")
    app.setToolbarButtonEnabled("HOME")
    app.setToolbarButtonEnabled("INTERPRETATION")
    app.setToolbarButtonDisabled("LEARNING")
    app.showLabel("words")

## Subwindows
# Settings window
app.startSubWindow("subSettings", title="SimaSLI Settings", modal=True, transient=False, blocking=False)
app.setResizable(canResize=False)

app.startLabelFrame("Arduino", 0,0,2)
app.addLabel("lblPort", "Port", 0, 0)
app.addEntry("entryPort", 0, 1)
app.setEntry("entryPort", my_config.port)
app.addLabel("lblBaud", "BaudRate", 1, 0)
app.addSpinBoxRange("spinBaud", 300, 115200, 1, 1)
app.setSpinBox("spinBaud", my_config.baud, callFunction=False)
app.addLabel("lblRefresh", "RefreshRate", 2, 0)
app.addSpinBoxRange("spinRefresh", 20, 1000, 2, 1)
app.setSpinBox("spinRefresh", my_config.refresh, callFunction=False)
app.addLabel("lblSerTimeout", "SerialTimeout\t\t\t", 3, 0) #tabulation for the right width
app.addSpinBoxRange("spinSerTimeout", 1, 30, 3, 1)
app.setSpinBox("spinSerTimeout", my_config.serial_timeout, callFunction=False)
app.stopLabelFrame()

app.startLabelFrame("Sima", 1,0,2)
app.addLabel("lblDbPath", "DatabasePath", 0, 0)
app.addEntry("entryDbPath", 0, 1)
app.setEntry("entryDbPath", my_config.db_path)
app.addCheckBox("EnableDebugMode", 1, 0)
app.setCheckBox("EnableDebugMode", ticked=my_config.debug_mode, callFunction=False)
app.addLabel("lblDbgCode", "DefaultCode\t\t\t", 2, 0) #tabulation for the right width
app.addSpinBoxRange("spinDbgCode", 0, 66666, 2, 1)
app.setSpinBox("spinDbgCode", my_config.default_code, callFunction=False)
app.stopLabelFrame()

app.startLabelFrame("Plugins", 2,0,2)
app.addLabel("lblSynthLang", "SynthLang\t\t\t", 0, 0) #tabulation for the right width
app.addSpinBox("spinSynthLang", ["english", "french"], 0, 1)
app.setSpinBox("spinSynthLang", my_config.synth_lang, callFunction=False)
app.addCheckBox("SynthEnablePersistance", 1, 0)
app.setCheckBox("SynthEnablePersistance", ticked=my_config.synth_persistant, callFunction=False)
app.addCheckBox("EnableUpdateCheck", 2, 0)
app.setCheckBox("EnableUpdateCheck", ticked=my_config.update_check, callFunction=False)
app.addCheckBox("EnableAutoUpdate", 3, 0)
app.setCheckBox("EnableAutoUpdate", ticked=my_config.update_auto, callFunction=False)
app.stopLabelFrame()

app.addButton("Reload", btnFunc, 3,0)
app.addButton("Apply", btnFunc, 3,1)
app.setButtonImage("Reload", "res/reload.gif")
app.setButtonImage("Apply", "res/accept.gif")
app.stopSubWindow()

# Plugin manager window
app.startSubWindow("subPluginManager", title="SimaSLI Plugin Manager", modal=True, transient=False, blocking=False)
app.setResizable(canResize=False)
app.setGeometry(700, 300)
app.hideTitleBar()
plugins = plugin.LoadPlugins()
n = []
d = []
v = []
e = []
for p in plugins:
    n.append(p.name)
    d.append(p.desc)
    v.append(p.version)
    e.append(p.state)
app.addListBox("plglist", n, 0,0)
app.addTextArea("plgdesc", 0,1)
app.setTextAreaWidth("plgdesc", 30)
app.addNamedButton("Quit", "plgquit", btnFunc, 1,0)
app.setButtonImage("plgquit", "res/exit.gif")
app.addGrip(1,1)
app.stopSubWindow()

# Learning window
app.startSubWindow("subLearn", title="SimaSLI Learning", modal=False, transient=False, blocking=False)
app.setResizable(canResize=False)
app.setGeometry(530, 130)
#app.addLabel("helpLearn", "Write the words that you want to learn.\nThey will be add to the database.")
app.addLabelEntry("English word",0,0)
app.addLabelEntry("French word",1,0)
app.setEntryWidth("English word", 35)
app.setEntryWidth("French word", 35)
app.addNamedButton("Apply", "applyLearn", btnFunc, 2,0)
app.setButtonImage("applyLearn", "res/edit.gif")
app.stopSubWindow()


#background event
def background():
    global status
    if status==0:
        homeScreen()
    elif status==1:
        #interpretation
        if my_board.state:
            time.sleep((my_config.refresh/1000) - 0.1)
            error = my_board.read()
            if type(error) is str:
                logger.log(3, error)
                status = 0
                my_board.state = False
            else:
                code = my_board.lastline
                for w in my_db.wordlist:
                    if code == w.code:
                        app.setLabel("words", "FR: {fr}\nEN: {en}".format(fr=w.word_fr, en=w.word_en))
                        app.setLabelFg("words", "green")
                        pl.OnInterpreter(w)
                        logger.log(0, w.code)
        else:
            for w in my_db.wordlist:
                if str(my_config.default_code) == w.code:
                    app.setLabel("words", "FR: {fr}\nEN: {en}".format(fr=w.word_fr, en=w.word_en))
                    app.setLabelFg("words", "orange")
    elif status==2:
        #learning
        if my_board.state:
            time.sleep((my_config.refresh/1000) - 0.1)
            error = my_board.read()
            if type(error) is str:
                logger.log(3, error)
                status = 0
                my_board.state = False
            else:
                code = my_board.lastline
                app.setLabel("words", "CODE: {c}".format(c=code))
                app.setLabelFg("words", "blue")
        else:
            app.setLabel("words", "CODE: null")
            app.setLabelFg("words", "orange")
    elif status==3:
        #plugin manager
        plgselected = app.getListItems("plglist")
        if plgselected != []:
            idx = n.index(plgselected[0])
            desc = d[idx]
            ver = v[idx]
            ena = e[idx]
            text = ("{d}\n\nVersion: {v}\n\nEnabled: {e}".format(d=desc,v=ver,e=ena))
            app.clearTextArea("plgdesc", callFunction=False)
            app.setTextArea("plgdesc", text, callFunction=False)
    if status != 2:
        app.hideSubWindow("subLearn")
    refreshStatusbar()

# register the background function
app.registerEvent(background)
# call background function each x milliseconds
app.setPollTime(100)

# global call on close
app.setStopFunction(checkStop)

# start the GUI
app.go()