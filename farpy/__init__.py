from farpy._farprt import Farprt
from farpy._modes import Modes
from farpy._namelist import readNamelist
import farpy._Plotting as plt
import farpy._Profiles as profiles
import farpy._Scan as scan
from farpy._logger import _CustomFormatter
import logging

# ------------------------------------------------------------------------------
# --- Initialise the level of the logging
# ------------------------------------------------------------------------------
logging.basicConfig()
logger = logging.getLogger('farpy')
logger.setLevel(logging.INFO)
if len(logger.handlers) == 0:
    hnd = logging.StreamHandler()
    hnd.setFormatter(_CustomFormatter())
    logger.addHandler(hnd)
logger.setLevel(logging.DEBUG)
logger.propagate = False

try:
    plt.plotSettings()
except:
    print('It was not possible to initialise the plotting settings')
