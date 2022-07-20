from farpy._farprt import Farprt
from farpy._modes import Modes
from farpy._namelist import readNamelist
import farpy._Plotting as plt
import farpy._Profiles as profiles
import farpy._Scan as scan

try:
    plt.plotSettings()
except:
    print('It was not possible to initialise the plotting settings')
