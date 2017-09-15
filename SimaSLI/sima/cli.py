import sys
import serial
from sima import core, config, logger
import plugins.PluginLoader as pl

my_config = config.Config()
error = my_config.setconfig()

if type(error) is str:
    logger.log(3, error)
    sys.exit(1)

pl.OnCliLoad()

logger.log(1, "Database: {path}".format(path=my_config.db_path))
my_db = core.LoadDB(my_config.db_path)
logger.log(1, "{n} words loaded!".format(n=len(my_db)))