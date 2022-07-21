"""
Library to read 2D scans
"""
import os
import decimal
import numpy as np
import xarray as xr
from datetime import datetime
from farpy._farprt import Farprt
from farpy._paths import Path

path = Path()

class Scan2D():
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
        self.parentFolder = parentFolder
        self.farprt = None  # It will be file with the farprt objects
        self.growthRateBlock = None  # It will be filled with the growthrate
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

    def readGrowthRateBlock(self):
        """
        Read the glowth rate and mode frequency from the scan

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
        for i1, var1 in enumerate(self.vars[0].values):
            for i2, var2 in enumerate(self.vars[1].values):
                tmp1 = self.vars[0].attrs['decimals']
                tmp2 = self.vars[1].attrs['decimals']
                fmt1 = f'_%.{tmp1}f'
                fmt2 = f'_%.{tmp2}f'
                name = os.path.join(self.parentFolder, 
                                    self.vars[0].attrs['long_name'] + fmt1%var1,
                                    self.vars[1].attrs['long_name'] + fmt2%var2,
                                    'farprt'
                )
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
        self.growthRateBlock['omega'] = \
            xr.DataArray(OMEGA, dims=(self.vars[0].attrs['long_name'],
                                      self.vars[1].attrs['long_name']),
                         coords=coords)
        self.growthRateBlock['gamma'] = \
            xr.DataArray(GAMMA, dims=(self.vars[0].attrs['long_name'], 
                                      self.vars[1].attrs['long_name']))
    
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