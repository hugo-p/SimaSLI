import sys
import importlib
from sima import core, config, logger, plugin

args = config.GetArguments()

my_config = config.Config()
error = my_config.setconfig()

if type(error) is str:
    logger.log(3, error)
    sys.exit(1)

####################################################
# initialize our "plugins"
OnInitFile = open("plugins/PluginLoader.py", "w+")
OnInitFile.close()

plugins = plugin.LoadPlugins()

if args.noplugins:
    line = "#!/usr/bin/env python3\n"
    line = (line + "\ndef OnInit():\n    pass\n")
    line = (line + "def OnCliLoad():\n    pass\n")
    line = (line + "def OnGuiLoad(app):\n    pass\n")
    line = (line + "def OnUpdate(app):\n    pass\n")
    line = (line + "def OnInterpreter(word):\n    pass\n")
    try:
        OnInitFile = open("plugins/PluginLoader.py", "a")
        OnInitFile.write(line)
        OnInitFile.close()
    except:
        logger.log(3, "Error while loading plugins")
else:

    line = "#!/usr/bin/env python3\n"
    for p in plugins:
        if p.state:
            line = (line + "import plugins.{package} as {package}\n".format(package=p.file))

    line = (line + "\ndef OnInit():\n")

    for p in plugins:
        if p.state:
            line = (line + "    {package}.OnInit()\n".format(package=p.file))

    line = (line + "def OnCliLoad():\n")

    for p in plugins:
        if p.state:
            line = (line + "    {package}.OnCliLoad()\n".format(package=p.file))

    line = (line + "def OnGuiLoad(app):\n")

    for p in plugins:
        if p.state:
            line = (line + "    {package}.OnGuiLoad(app)\n".format(package=p.file))

    line = (line + "def OnUpdate(app):\n")

    for p in plugins:
        if p.state:
            line = (line + "    {package}.OnUpdate(app)\n".format(package=p.file))

    line = (line + "def OnInterpreter(word):\n")

    for p in plugins:
        if p.state:
            line = (line + "    {package}.OnInterpreter(word)\n".format(package=p.file))

    line = (line + "def OnGuiClose(app):\n")

    for p in plugins:
        if p.state:
            line = (line + "    {package}.OnGuiClose(app)\n".format(package=p.file))

    try:
        OnInitFile = open("plugins/PluginLoader.py", "a")
        OnInitFile.write(line)
        OnInitFile.close()
    except:
        logger.log(3, "Error while loading plugins")
#########################################################

import plugins.PluginLoader as pl
pl.OnInit()

if not args.console:
    logger.log(0, "Initializing graphical wrapper...")
    from sima import gui
    sys.exit(1)
elif args.console:
    logger.log(0, "Console mode...")
    from sima import cli
    sys.exit(1)
