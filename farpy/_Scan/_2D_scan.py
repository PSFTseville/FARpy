"""
Library to read 2D scans
"""
import os
import sys
import numpy as np
import xarray as xr
import decimal
from farpy._farprt import Farprt

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

        """
        self.parentFolder = parentFolder

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
                name = os.path.join(parentFolder, 
                                    var1Name + fmt1%var1,
                                    var2Name + fmt2%var2,
                                    'farprt'
                )
                fars[i1, i2] = Farprt(name)
                fars[i1, i2].readGrowthRate()
                OMEGA[i1, i2] = fars[i1, i2].GrowthRateBlock['avg_omega'].values[0]
                GAMMA[i1, i2] = fars[i1, i2].GrowthRateBlock['avg_gamma'].values[0]
        self.farprt = fars
        self.GrowthRateBlock = xr.Dataset()
        coords = {}
        coords[var1Name] = self.vars[0].values
        coords[var2Name] = self.vars[1].values
        self.GrowthRateBlock['omega'] = \
            xr.DataArray(OMEGA, dims=(var1Name, var2Name),
                         coords=coords)
        self.GrowthRateBlock['gamma'] = \
            xr.DataArray(GAMMA, dims=(var1Name, var2Name),
                         coords=coords)
