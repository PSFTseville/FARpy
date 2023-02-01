"""
Library to read and plot 1D scans
"""
import os
import logging
import decimal
import numpy as np
import xarray as xr
import scipy.constants as cnt
import matplotlib.pyplot as plt
from datetime import datetime
from tqdm import tqdm
from farpy._paths import Path
from farpy._modes import Modes
from adjustText import adjust_text
from farpy._Plotting._settings import axis_beauty
from farpy._eigensolver import EigenSolver
from farpy._farprt import Farprt
from farpy._namelist import readNamelist
from farpy._Scan._General_scan_class import Scan
from farpy._Profiles.profiles import ProfilesInput
from mpl_toolkits.axes_grid1 import make_axes_locatable

path = Path()
logger = logging.getLogger('farpy.Scans')


class Scan1D(Scan):
    """
    Read and handle 1D variable scan of FAR3D simulations

    Jose Rueda: jrrueda@us.es

    It is assumed that the scan is like follows:
    <ParentFolder>
        <varName1>_<var1Value>
    All values of var 1 are supposed to have the same number of
    decimals!!!
    """
    def __init__(self, parentFolder: str = None, prefix: str = None):
        """
        Initialise the scan

        This will explore the folder structure and see the variables which where
        used for the scan

        Jose Rueda: jrrueda@us.es

        :param parentFolder: root folder which contain the scan data, if none,
            the model folder of FAR3D will be used
        :param prefix: Prefix of the simulations name, for example, if we have
            performed a beta scan and named the simulations as
            41091_bet0_f_0.001099, the prefix would be '41091_', everything in
            the folder which does not starts with this, will be ignored
        """
        # Pre-allocate the attributes
        Scan.__init__(self)
        # Define parent folder:
        if parentFolder is None:
            self.parentFolder = os.path.join(path.far3d, 'Models')
        else:
            self.parentFolder = parentFolder

        # Define the prefix:
        self.prefix = prefix

        # get the variable values
        var1Values = []
        for coso in os.listdir(self.parentFolder):
            # See if the object starts with the prefix
            if self.prefix is not None:
                if not coso.startswith(self.prefix):
                    continue
            # If we reached this point, the 'coso' starts with our prefix
            d = os.path.join(self.parentFolder, coso)
            if os.path.isdir(d):  # Make sure it is a folder
                # Eliminate the prefix
                if self.prefix is None:
                    name = coso
                else:
                    _, name = coso.split(self.prefix)
                # Extract the variable value and name
                splits = name.split('_')
                var1Values.append(splits[-1])
                # Yes, I will take the name of the variable each time, this is
                # not extremelly efficient, but will be fine, we will just
                # consume a second or two
                var1Name = name.split('_'+splits[-1])[0]
        # Now we have the variables name and values, so let's save them. Notice
        # that in the 2D and future 3D, the attribute is called vars, so I will
        # keep the name, just for consistency
        self.vars = [
            xr.DataArray(np.unique(np.array(var1Values)).astype(float))
        ]
        self.vars[0].attrs['long_name'] = var1Name
        d = decimal.Decimal(var1Values[0])
        self.vars[0].attrs['decimals'] = abs(d.as_tuple().exponent)

    # -------------------------------------------------------------------------
    # --- Namelist and profiles block
    # -------------------------------------------------------------------------
    def readNamelist(self, complete: bool = False):
        """
        Read the namelist files

        :param complete: if True, all namefiles will be read, if False, just the
            first one
        """
        # -- Allocate the space
        n1 = self.vars[0].size
        namelist = np.full(n1, None, dtype=np.ndarray)
        # -- Format to read
        tmp1 = self.vars[0].attrs['decimals']
        fmt1 = f'_%.{tmp1}f'
        if complete:
            x1 = self.vars[0].values
        else:
            x1 = self.vars[0].values[0:1]
        logger.info('Reading input namelist')
        # -- Read the files
        for i1, var1 in enumerate(x1):
            if self.prefix is None:
                name = os.path.join(self.parentFolder,
                                    self.vars[0].attrs['long_name'] + fmt1 % var1,
                                    'Input_Model'
                                    )
            else:
                name = os.path.join(self.parentFolder, self.prefix +
                                    self.vars[0].attrs['long_name'] + fmt1 % var1,
                                    'Input_Model'
                                    )
            namelist[i1] = readNamelist(name)
        self.namelist = namelist

    def readProfiles(self, complete: bool = False):
        """
        Read the input profile file

        :param complete if True, all namefiles will be read, if False, just the
        first one
        """
        if self.namelist is None:
            logger.warning('11: reading namelist')
            self.readNamelist()
        # -- Allocate the space
        n1 = self.vars[0].size
        profiles = np.full(n1, None, dtype=np.ndarray)
        # -- Format to read
        tmp1 = self.vars[0].attrs['decimals']
        fmt1 = f'_%.{tmp1}f'
        if complete:
            x1 = self.vars[0].values
        else:
            x1 = self.vars[0].values[0:1]
        logger.info('Reading input profiles')
        # -- Read the files
        for i1, var1 in enumerate(x1):
            profileName = self.namelist[i1]['ext_prof_name']
            if self.prefix is None:
                name = os.path.join(self.parentFolder,
                                    self.vars[0].attrs['long_name'] + fmt1%var1,
                                    profileName
                )
            else:
                name = os.path.join(self.parentFolder, self.prefix +
                                    self.vars[0].attrs['long_name'] + fmt1%var1,
                                    profileName
                )
            profiles[i1] = ProfilesInput(name)
        self.profiles = profiles

    # -------------------------------------------------------------------------
    # --- Modes, from standard FAR3D simulation
    # -------------------------------------------------------------------------
    def readModes(self):
        """
        Read the mode profiles
        """
        # -- Allocate the space
        n1 = self.vars[0].size
        modes = np.full(n1, None, dtype=np.ndarray)
        # -- Format to read
        tmp1 = self.vars[0].attrs['decimals']
        fmt1 = f'_%.{tmp1}f'
        # -- Read the files
        logger.info('Reading modes')
        for i1, var1 in enumerate(tqdm(self.vars[0].values)):
            if self.prefix is None:
                name = os.path.join(self.parentFolder,
                                    self.vars[0].attrs['long_name'] + fmt1%var1)
            else:
                name = os.path.join(self.parentFolder, self.prefix +
                                    self.vars[0].attrs['long_name'] + fmt1%var1)

            modes[i1] = Modes(name)
        self.modes = modes

    # --------------------------------------------------------------------------
    # --- Eigensolver data
    # --------------------------------------------------------------------------
    def readEigensolver(self, loadModes: bool = False):
        """
        Read the growth rate and mode frequency from the scan
        """
        # - Load the objects
        n1 = self.vars[0].size
        tmp1 = self.vars[0].attrs['decimals']
        fmt1 = f'_%.{tmp1}f'
        eigen = np.full(n1, None, dtype=np.ndarray)
        # - Load the Eigensolver data
        logger.info('Reading Eigensolver data')
        for i1, var1 in enumerate(self.vars[0].values):
            if self.prefix is not None:
                name = os.path.join(self.parentFolder, self.prefix +
                                    self.vars[0].attrs['long_name'] + fmt1%var1)
            else:
                name = os.path.join(self.parentFolder,
                                    self.vars[0].attrs['long_name'] + fmt1%var1)
            eigen[i1] = EigenSolver(path=name)
            # Read the eigenvalues and modes
            eigen[i1]._read_egn_values()
            eigen[i1]._read_egn_mode_asci_header()
            if loadModes:
                eigen[i1]._read_egn_mode_asci()
        self.eigen = eigen

    # --------------------------------------------------------------------------
    # --- Re-normalization
    # --------------------------------------------------------------------------
    def renormFrequencyEigenSolver(self, complete: bool = False):
        """
        Transform from code units to real kHz

        :param complete: if true, for each simulation, its own profile file will
            be used, if false, it will be considered that they share the
            plasma parameters
        """
        if complete:
            raise Exception('Sorry, still not implemented')
        # --- Check that we have the information
        if self.profiles is None:
            raise Exception('Read first the profiles')

        # --- precalculate the factor
        if not complete:
            B = self.profiles[0]['bt0'].values
            R0 = self.profiles[0]['rmajr'].values
            mi_mp = self.profiles[0]['mi_mp'].values
            ni0 = self.profiles[0]['ni'].sel(rho=0.0).values
            F = B / 2.0 / cnt.pi / R0 \
                / np.sqrt(cnt.mu_0 * cnt.m_p * mi_mp * ni0 * 1.0e20) / 1000.0

        # Apply factor
        for i in range(self.eigen.size):
            self.eigen[i]._data['omega'].values *= F
            self.eigen[i]._data['omega'].attrs['units'] = 'kHz'
            self.eigen[i]._data['omega'].attrs['long_name'] = 'Mode Frequency'

    # -------------------------------------------------------------------------
    # --- Plotting
    # -------------------------------------------------------------------------
    def plotFrequenciesEigensolver(self, ax=None, ax_params: dict = {},
                                   includeColorbar: bool = True,
                                   vmin=-0.1, vmax=0.1):
        """
        Plot the eigen frequency values

        :param ax:
        :return:
        """
        ax_options = {
        }
        ax_options.update(ax_params)
        # create the axes if needed
        if ax is None:
            fig, ax = plt.subplots()
        # Plot the points
        texts = []
        xlist = []
        ylist = []
        for i, eigen in enumerate(self.eigen):
            # Get the values of the scan variable:
            var1 = self.vars[0][i]
            # Get the frequency values
            f = eigen._data['omega']
            # Get the growth rate
            g = eigen._data['gamma']
            # Prepare the x for the scatter
            x = var1.values*np.ones(f.values.size)
            # plot the stuff
            dum = ax.scatter(x,f,c=g,cmap='bwr', vmin=vmin, vmax=vmax)
            # if includeModeLabels:
            #     labels = ['(%i, %i)' % (n, m) for m,n in zip(self.eigen[i]._data.n.values, self.eigen[i]._data.m.values)]
            #     # print(labels)
            #     for i in range(x.size):
            #         texts.append(ax.text(x[i], f.values[i], labels[i]))
        # Include the mode numbers:
        # if includeModeLabels:
        #     adjust_text(texts, only_move={'points': 'y', 'texts': 'y'},
        #                 autoalign='y', ax=ax)
        # Include the colorbar:
        if includeColorbar:
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="4%", pad=0.05)
            plt.colorbar(dum, label='$\gamma [a.u]$', cax=cax)
        # A bit of axis beauty
        ax.set_xlabel(var1.long_name)
        if 'units' in f.attrs.keys():
            label = f.long_name + '[%s]' % f.units
        else:
            label = f.long_name
        ax.set_ylabel(label)
        ax = axis_beauty(ax, ax_options)
        return ax

