"""
Library to read 2D scans
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
from mpl_toolkits.axes_grid1 import make_axes_locatable
from farpy._farprt import Farprt
from farpy._namelist import readNamelist
from farpy._paths import Path
from farpy._Profiles.profiles import ProfilesInput
from farpy._modes import Modes
from farpy._Scan._General_scan_class import Scan

path = Path()
logger = logging.getLogger('farpy.Scans')


class Scan2D(Scan):
    """
    Read and handle 2D variable scan of FAR3D simulations

    Jose Rueda: jrrueda@us.es

    It is assumed that the scan is like follows:
    <ParentFolder>
        <varName1>_<var1Value>
            <varName2>_<var2Value>
    It is assumed that all the <varName1> folders contains the subfolders 
    <varName2> for the same cases. Actually, the values will be extracted from
    the first folder <varName1>, so if another one have more, those will not
    be read

    All values of var 1 and var2 are supposed to have the same number of 
    decimals!!!

    """
    def __init__(self, parentFolder: str = None):
        """
        Initialise the scan

        This will explore the folder structure and see the variables which where
        used for the scan

        Jose Rueda: jrrueda@us.es

        @param parentFolder: root folder which contain the scan data
        """
        # --- Pre allocate a bit of attributes:
        Scan.__init__(self)
        # --- See what it is inside
        var1Values = []
        var2Values = []
        read_subfolder = True
        for coso in os.listdir(parentFolder):
            d = os.path.join(parentFolder, coso)
            if os.path.isdir(d):
                # If it is a folder, get the values
                var1Name, dummy = coso.split('_')
                var1Values.append(dummy)
                # If it is a folder, do the same with the subfolder
                if read_subfolder:
                    for coso2 in os.listdir(d):
                        d2 = os.path.join(d, coso2)
                        if os.path.isdir(d2):
                            var2Name, dummy2 = coso2.split('_')
                            var2Values.append(dummy2)
                    read_subfolder = False
        # --- Now we have the variables and the values of the scan, so let's
        # - Save the variables stuff
        self.vars = [
            xr.DataArray(np.unique(np.array(var1Values)).astype(float)),
            xr.DataArray(np.unique(np.array(var2Values)).astype(float))
        ]
        self.vars[0].attrs['long_name'] = var1Name
        d = decimal.Decimal(var1Values[0])
        self.vars[0].attrs['decimals'] = abs(d.as_tuple().exponent)

        self.vars[1].attrs['long_name'] = var2Name
        d = decimal.Decimal(var2Values[0])
        self.vars[1].attrs['decimals'] = abs(d.as_tuple().exponent)

    # --------------------------------------------------------------------------
    # --- Growth rate and frequency
    # --------------------------------------------------------------------------
    def readGrowthRateBlock(self):
        """
        Read the growth rate and mode frequency from the scan

        #TODO: handle the case whith different n
        """
        # - Load the data
        # Allocate the space for latter
        n1 = self.vars[0].size
        n2 = self.vars[1].size
        fars = np.full((n1, n2), None, dtype=np.ndarray)
        OMEGA = np.empty(shape=(n1, n2))
        OMEGA.fill(np.nan)
        GAMMA = np.empty(shape=(n1, n2))
        GAMMA.fill(np.nan)
        # Format for the files
        tmp1 = self.vars[0].attrs['decimals']
        tmp2 = self.vars[1].attrs['decimals']
        fmt1 = f'_%.{tmp1}f'
        fmt2 = f'_%.{tmp2}f'
        logger.info('Reading growthrate and omega')
        for i1, var1 in enumerate(self.vars[0].values):
            for i2, var2 in enumerate(self.vars[1].values):
                name = os.path.join(self.parentFolder, 
                                    self.vars[0].attrs['long_name'] + fmt1%var1,
                                    self.vars[1].attrs['long_name'] + fmt2%var2,
                                    'farprt'
                )
                if os.path.isfile(name):
                    fars[i1, i2] = Farprt(name)
                    fars[i1, i2].readGrowthRate()
                    OMEGA[i1, i2] = \
                        fars[i1, i2].growthRateBlock['avg_omega'].values
                    GAMMA[i1, i2] = \
                        fars[i1, i2].growthRateBlock['avg_gamma'].values
        self.farprt = fars
        self.growthRateBlock = xr.Dataset()
        coords = {}
        coords[self.vars[0].attrs['long_name']] = self.vars[0].values
        coords[self.vars[1].attrs['long_name']] = self.vars[1].values
        self.growthRateBlock['om_r'] = \
            xr.DataArray(OMEGA, dims=(self.vars[0].attrs['long_name'],
                                      self.vars[1].attrs['long_name']),
                         coords=coords)
        self.growthRateBlock['om_r'].attrs['units'] = ''
        self.growthRateBlock['om_r'].attrs['long_name'] = 'Mode Frequency'

        self.growthRateBlock['gamma'] = \
            xr.DataArray(GAMMA, dims=(self.vars[0].attrs['long_name'], 
                                      self.vars[1].attrs['long_name']))
        self.growthRateBlock['gamma'].attrs['units'] = ''
        self.growthRateBlock['gamma'].attrs['long_name'] = 'Growth rate'
    
    def exportGrowthRateBlock(self, filename: str = None):
        """
        Export the readed growthRateBlock into a file

        @filename: Filename to save the results, if present, the format variable
            will be ignored. And the format will be deduced from the file 
            extension
        """
        if filename is None:
            now = datetime.now()
            string = now.strftime("%Y_%m_%d_%H_%M_%S")
            filename = \
                os.path.join(path.Results, 'S2D_growthRateBlock' + string 
                             + '.nc')
        self.growthRateBlock.to_netcdf(filename)
    
    def plotGrowthRateBlock(self, var: str = 'omega', ax=None, **kargs):
        """
        2D plot of the growth rate variables
        """
        if ax is None:
            fig, ax = plt.subplots()
        # Plot the stuff
        img = self.growthRateBlock[var].plot.pcolormesh(ax=ax,
                                                        add_colorbar=False,
                                                        **kargs)
        ax.set_box_aspect(1)
        
        # Create the axis for the colobar
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="10%", pad=0.05)
        label = '%s [%s]' % (self.growthRateBlock[var].attrs['long_name'],
                             self.growthRateBlock[var].attrs['units'])
        plt.colorbar(img, label=label, cax=cax)
        return ax
        
    # --------------------------------------------------------------------------
    # --- Namelist and profiles
    # --------------------------------------------------------------------------
    def readNamelist(self, complete: bool = False):
        """
        Read the namelist files

        @param complete: if True, all namefiles will be read, if False, just the
            first one
        """
        # -- Allocate the space
        n1 = self.vars[0].size
        n2 = self.vars[1].size
        namelist = np.full((n1, n2), None, dtype=np.ndarray)
        # -- Format to read
        tmp1 = self.vars[0].attrs['decimals']
        tmp2 = self.vars[1].attrs['decimals']
        fmt1 = f'_%.{tmp1}f'
        fmt2 = f'_%.{tmp2}f'
        if complete:
            x1 = self.vars[0].values
            x2 = self.vars[1].values
        else:
            x1 = self.vars[0].values[0:1]
            x2 = self.vars[1].values[0:1]
        logger.info('Reading input namelist')
        # -- Read the files
        for i1, var1 in enumerate(x1):
            for i2, var2 in enumerate(x2):

                name = os.path.join(self.parentFolder, 
                                    self.vars[0].attrs['long_name'] + fmt1%var1,
                                    self.vars[1].attrs['long_name'] + fmt2%var2,
                                    'Input_Model'
                )
                namelist[i1, i2] = readNamelist(name)
        self.namelist = namelist

    def readProfiles(self, complete: bool = False):
        """
        Read the input profile file

        @param complete if True, all namefiles will be read, if False, just the
        first one
        """
        if self.namelist is None:
            logger.warning('11: reading namelist')
            self.readNamelist()
        # -- Allocate the space
        n1 = self.vars[0].size
        n2 = self.vars[1].size
        profiles = np.full((n1, n2), None, dtype=np.ndarray)
        # -- Format to read
        tmp1 = self.vars[0].attrs['decimals']
        tmp2 = self.vars[1].attrs['decimals']
        fmt1 = f'_%.{tmp1}f'
        fmt2 = f'_%.{tmp2}f'
        if complete:
            x1 = self.vars[0].values
            x2 = self.vars[1].values
        else:
            x1 = self.vars[0].values[0:1]
            x2 = self.vars[1].values[0:1]
        logger.info('Reading input profiles')
        # -- Read the files
        for i1, var1 in enumerate(x1):
            for i2, var2 in enumerate(x2):
                profileName = self.namelist[i1,i2]['ext_prof_name']
                name = os.path.join(self.parentFolder, 
                                    self.vars[0].attrs['long_name'] + fmt1%var1,
                                    self.vars[1].attrs['long_name'] + fmt2%var2,
                                    profileName
                )
                profiles[i1, i2] = ProfilesInput(name)
        self.profiles = profiles

    # --------------------------------------------------------------------------
    # --- Modes
    # --------------------------------------------------------------------------
    def readModes(self):
        """
        Read the mode profiles
        """
        # -- Allocate the space
        n1 = self.vars[0].size
        n2 = self.vars[1].size
        modes = np.full((n1, n2), None, dtype=np.ndarray)
        # -- Format to read
        tmp1 = self.vars[0].attrs['decimals']
        tmp2 = self.vars[1].attrs['decimals']
        fmt1 = f'_%.{tmp1}f'
        fmt2 = f'_%.{tmp2}f'
        # -- Read the files
        logger.info('Reading modes')
        for i1, var1 in enumerate(tqdm(self.vars[0].values)):
            for i2, var2 in enumerate(self.vars[1].values):

                name = os.path.join(self.parentFolder, 
                                    self.vars[0].attrs['long_name'] + fmt1%var1,
                                    self.vars[1].attrs['long_name'] + fmt2%var2)
                modes[i1, i2] = Modes(name)
        self.modes = modes

    # --------------------------------------------------------------------------
    # --- Re-normalization
    # --------------------------------------------------------------------------
    def renormFrequency(self, complete: bool = False):
        """
        Transform from code units to real kHz

        @param complete: if true, for each simulation, its own profile file will
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
            B = self.profiles[0,0]['bt0'].values
            R0 = self.profiles[0,0]['rmajr'].values
            mi_mp = self.profiles[0,0]['mi_mp'].values
            ni0 = self.profiles[0,0]['ni'].sel(rho=0.0).values
            F = B / 2.0 / cnt.pi / R0 \
                / np.sqrt(cnt.mu_0 * cnt.m_p * mi_mp * ni0 * 1.0e20) / 1000.0
        
        # Apply factor
        self.growthRateBlock['omega'] = self.growthRateBlock['om_r'] * F
        self.growthRateBlock['omega'].attrs['units'] = 'kHz'
        self.growthRateBlock['omega'].attrs['long_name'] = 'Mode Frequency'

    def renormCVFP(self, complete: bool = False):
        """
        Translate from CVFP to Tfast
        
        @param complete: if true, for each simulation, its own profile file will
            be used, if false, it will be considered that they share the
            plasma parameters
    
        Note that this will only work if one of your coordinates of the scan is
        the cvft parameter
        """
        if 'cvfp' not in self.growthRateBlock.coords.keys():
            raise Exception('Sorry, cvfp not foun as coordinate')
        if complete:
            raise Exception('Sorry, still not implemented')
        # --- Check that we have the information
        if self.profiles is None:
            raise Exception('Read first the profiles')
        
        # --- precalculate the factor
        if not complete:
            B = self.profiles[0,0]['bt0'].values
            mi_mp = self.profiles[0,0]['mi_mp'].values
            ni0 = self.profiles[0,0]['ni'].sel(rho=0.0).values
            Va0 = B \
                / np.sqrt(cnt.mu_0 * cnt.m_p * mi_mp * ni0 * 1.0e20)
        # Get the 'Temperature' in Jules
        Tf = (self.growthRateBlock['cvfp'].values*Va0)**2 * cnt.m_p * mi_mp
        # Get the 'Temperature' in keV
        Tf /= cnt.e*1000.0

        # Save the temperature
        self.growthRateBlock['Tf'] = xr.DataArray(Tf, dims='cvfp')
        self.growthRateBlock['Tf'].attrs['units'] = 'keV'
        self.growthRateBlock['Tf'].attrs['long_name'] = 'Tf'

        # Exchange the axis to this temperature
        self._swap_cvfp_tf()

    def _swap_cvfp_tf(self):
        """
        Exchange cvfp axis with TF axis
        """
        self.growthRateBlock = self.growthRateBlock.swap_dims({"cvfp": "Tf"})

    def _swap_tf_cvsp(self):
        """
        Exchange cvfp axis with TF axis
        """
        self.growthRateBlock = self.growthRateBlock.swap_dims({"cvfp": "Tf"}) 
    # --------------------------------------------------------------------------