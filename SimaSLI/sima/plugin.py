from lxml import etree
import glob

class Plugin:
    """Class that defines a plugin with :
    - his name
    - his description
    - his version
    - his state..."""

    def __init__(self, file, name, desc, version, state):
        self.file = file
        self.name = name
        self.desc = desc
        self.version = version
        self.state = state

def CreatePlugin(p, xml):
    """Function that loads the plugin."""

    tree = etree.parse(xml)
    root = tree.getroot()

    file = p
    name = root[0].text
    desc = root[1].text
    version = root[2].text
    state = str2bool(root[3].text)
    
    plugin = Plugin(file, name, desc, version, state)
    return plugin

def LoadPlugins():
    """Function that loads the plugin directory and create plugin objects."""
    plugs = glob.glob("plugins/*.py")
    plugins = []
    for p in plugs:
        p = p.replace(".py","")
        p = p.replace("plugins\\","")
        if p == "__init__":
            pass
        if p == "PluginLoader":
            pass
        else:
            xml = "plugins/{p}.xml".format(p=p)
            try:
                plg = CreatePlugin(p, xml)
                plugins.append(plg)
            except:
                pass
    return plugins

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1", "oui", "vrai", "activé", "active", "on", "enable", "enabled")