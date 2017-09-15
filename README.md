# SímaSLI
Our website: [here](http://hugo.pointcheval.fr)

Our GitHub Page: [here](https://hugo-p.github.io/SimaSLI/)

Our GitHub Project: [here](https://github.com/hugo-p/SimaSLI)

***

1. [Documentation](#documentation)
2. [SimaArduino](#simaarduino)
	* [Features](#features)
	* [Usage](#usage)
3. [SimaSLI v5.0](#simasli)
	* [Features](features-1)
	* [Requirements](#requirements)
	* [Usage](#usage-1)
	* [Screenshots](#screenshots)
4. [Plugins](#plugins)
	* [SimaVoice](#simavoice)
	* [SimaDirect](#simadirect)
5. [Deprecated](#deprecated)
	1. [SimaSLI v4.0](#simasli-v40)
	2. [SimaSLI v3.0](#simasli-v30)
	3. [SimaSLI v2.0](#simasli-v20)

***

## Documentation

French presentations: [here](http://hugo.pointcheval.fr/projets/sima/presentation.html)

Documentation is available on our website: [here](http://hugo.pointcheval.fr/projets/sima/index.html)


## SimaArduino
#### Features
* Lists for fast processing/more readable
* Flex sensors support
* Microswitch support
* 1 finger = 6 states
* Serial communication
* Sends code every 150ms

It acquires the value of flex sensors and "remaps" to make a multiple of 3.
Then it tests in wich state is the finger.
A code is sent to the host. (eg. 14111 represents "hello" in sign language)

#### Usage
Simply adjust the pins and it's ready to be upload on your board.


## SimaSLI

The major update **v5.0** brings a lot of changes, and new features.

The CLI version is now "**legacy mode**" or "**console mode**".

The GUI version is now the **default version**.

#### Features
* Completely rewrote for Python 3.6
* New GUI framework. *Bye PyGame, hello Tcl-Tk (wich is more cross-platform).*
* XML Database file. *No more txt file, fastest parsing.*
* Sima.core module. *With all important python objects for words, database, arduino board.*
* New configuration system. *Works with config object, wich can be modified during execution.*
* New interface. *Hold your breath and take a look at the screenshots*
* Plugin loader. *Yes! now we have a plugin system!*
* Fullscreen support. *BYE DECORATIONS & TASK BAR!*

#### Requirements
* Python 3

Run setup.py and all dependences will be download.

* Modules:
	* pyserial
	* appjar
	* lxml

* OS: Windows, Mac or Linux.

#### Usage
Download latest version: **v5.0 beta**.

Run **sima.py**.

Then juste follow the instructions... (for example if there is an update, all is automatic. It just depends of your configuration!)

* Launch arguments:
	
	`-c` or `--console` for leagacy mode.
	
	`-n` or `--noplugins` disable all plugins.

	`-h` or `--help` show help message.

#### Screenshots
Home screen
![SimaSLI HomeScreen](http://hugo.pointcheval.fr/projets/sima/img/github/sima1.png)
Configuration
![SimaSLI Config](http://hugo.pointcheval.fr/projets/sima/img/github/sima2.png)
Database
![SimaSLI Db](http://hugo.pointcheval.fr/projets/sima/img/github/sima3.png)
Plugin Manager
![SimaSLI Plugins](http://hugo.pointcheval.fr/projets/sima/img/github/sima4.png)
Learning mode
![SimaSLI Learn](http://hugo.pointcheval.fr/projets/sima/img/github/sima5.png)

## Plugins
In SimaSLI v5.0 a plugin loader has been implemented.
You can easely add and even create plugins.

It works with our _**global calls system**_.

For example:

```python
def OnInit():
	logger.log(0, "myplugin.py --> OnInit()")
```

It will result with a nice message text in the console when Sima starts.

All functions are registred in the **TestPlugin.py** file (don't delete it).

When you create a plugin you must provide a XML file with the exact same name. And it must contain the plugin's informations.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<plugin>
    <name>What a wonderful plugin</name>
    <description>it's my wonderful plugin</description>
    <version>0.1</version>
    <state>enabled</state>
</plugin>
```

Take a look of our plugins to understand the _**global calls system**_.

### SimaVoice 
Allows **Voice Synthesis** in SimaSLI v5.0

It's a new version of our old SimaVoice.

- New audio engine: **playsound**. *Bye PyGame mixer!*
- Voice Python Object.
- It's a plugin. *It means you can disable it or even delete the file and Sima will continue to works.*

It uses 2 calls of _**global calls system**_:

```python
OnInit()

OnInterpreter(word)

OnGuiClose(app)
```
### SimaDirect
It's an update-checker and auto-updater.

Basically it's an integration of my **downloader.py** app wich is available in [gist](https://gist.github.com/hugo-p/9d228d8781dee1b34096d5f851ef58ac).

This plugin creates a new object **Updater** on initialization of Sima. Then if an update is available it launch the **downloader.py** with the right arguments.

It uses 2 calls of _**global calls system**_:

```python
OnInit()

OnUpdate()
```

***

## Deprecated

### SimaSLI v4.0

/!\ Deprecated! Now please use [Latest SimaSLI](#simasli)!

It's the final version of our interpreter!
Basically it's a mix of the 2 sub-versions (CLI & GUI).
The code as been revamped, and cleaned.

#### Features
* SimaCore - One module: all the core features.
* Config file
	* Arduino: port, baudrate, serial timeout.
	* Sima: database file's name, debug mode, debug code and test timeout
* Launch arguments: CLI or GUI
* Pretty logger

#### Requirements
* Python 2.7~
* Modules
	* pyserial
	* colorama
	* pygame

`pip install pyserial`

`pip install colorama`

`pip install pygame`

Dear Macintosh users, because of a problem related to the use of Pygame you can't use SimaSLI. Use SimaCLI instead.

#### Usage

##### Sources

* Download the latest release (SimaSLI is the V4.X) [here](https://github.com/hugo-p/SimaSLI/releases).
* Extract it
* Open a console in the root folder of SimaSLI
* And launch it with

`python main.py`

Note that you can use some args:

`python main.py -n` or `python main.py --nogui` Disable the GUI

`python main.py -n -v` or `python main.py --nogui --voice` Enable the Voice Synthesis

`python main.py --help` Display help

Windows french users: do not use accents in the database ! (or if you really want to use them you have to configure your cmd):
`chcp 1252`

##### Windows Application

* Download the latest release (SimaSLI is the V4.X) [here](https://github.com/hugo-p/SimaSLI/releases).
* Extract it
* Launch "main.exe"

Note that you can use some args:

`main.exe -n` or `main.exe --nogui` Disable the GUI

`main.exe -n -v` or `main.exe --nogui --voice` Enable the Voice Synthesis

Do not use accents in the database ! (or if you really want to use them you have to configure your cmd):
`chcp 1252`

#### Screenshots
Main window/console
![SLI Main](http://hugo.pointcheval.fr/projets/sima/img/SLI_main.png)
Nogui argument
![SLI Nogui](http://hugo.pointcheval.fr/projets/sima/img/SLI_nogui.png)
Interpretation mode
![SLI Interpretation](http://hugo.pointcheval.fr/projets/sima/img/SLI_inter.png)


### SimaSLI v3.0

/!\ Deprecated! Now please use [Latest SimaSLI](#simasli)!

It's the GUI version of our interpreter. And the latest release is available (SimaGUI is the V3.X) [here](https://github.com/hugo-p/SimaSLI/releases).

#### Features
* Graphical User Interface (SDL/Pygame)
* Custom database file
* Custom debug code
* Timeout customizable
* 3 modes (interpreter, learning, test)

#### Usage
Configure the tool with the config file. And launch it!

#### Screenshots
Main window

![GUI Main](http://hugo.pointcheval.fr/projets/sima/img/GUI_main.png)

Interpretation mode

![GUI Interpretation](http://hugo.pointcheval.fr/projets/sima/img/GUI_inter.png)

Learning mode

![GUI Learning](http://hugo.pointcheval.fr/projets/sima/img/GUI_learn.png)

Test mode

![GUI Test](http://hugo.pointcheval.fr/projets/sima/img/GUI_test1.png)
![GUI Test](http://hugo.pointcheval.fr/projets/sima/img/GUI_test2.png)


### SimaSLI v2.0

/!\ Deprecated! Now please use [Latest SimaSLI](#simasli)!

It's the first prototype. And the latest release is available (SimaCLI is the V2.X) [here](https://github.com/hugo-p/SimaSLI/releases).

#### Features
* Config file
* 3 modes (interpreter, learning, test)
* Works without serial communication

#### Usage
Configure Sima with the config file. Make sure you have a database file named db.txt and let's go!
You can easely set new words with the learning mode: it will add the sign to the database.
The database file can be edited too.

#### Screenshots
Main window
![CLI Main](http://hugo.pointcheval.fr/projets/sima/img/CLI_main.png)
Interpretation mode
![CLI Interpretation](http://hugo.pointcheval.fr/projets/sima/img/CLI_inter.png)
Learning mode
![CLI Learning](http://hugo.pointcheval.fr/projets/sima/img/CLI_learn.png)
Test mode
![CLI Test](http://hugo.pointcheval.fr/projets/sima/img/CLI_test.png)

