import logging
from sima import config
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')

my_config = config.Config()
error = my_config.setconfig()

if type(error) is str:
    log(3, error)
    sys.exit(1)

if not my_config.debug_mode:
	logging.getLogger("requests").setLevel(logging.WARNING)
	logging.getLogger("urllib3").setLevel(logging.WARNING)

GREEN = ('\033[92m')  #green
YELLOW = ('\033[93m') #yellow
RED = ('\033[91m')    #red
END = ('\033[0m')     #reset

def log(code, msg):
	msg = str(msg)
	if code == 0 and my_config.debug_mode:
		logging.debug(msg)
	if code == 1:
		logging.info(GREEN + msg + END)
	if code == 2:
		logging.warning(YELLOW + msg + END)
	if code == 3:
		logging.error(RED + msg + END)