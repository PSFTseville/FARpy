"""
Read and write profiles

Jose Rueda Rueda: jrrueda@us.es
"""

import numpy as np
import matplotlib.pyplot as plt
from farpy._Profiles._profiles_header import profilesOrderInputs, \
    profilesOrderDat, profilesOrderExDat
from farpy._Plotting._settings import axis_beauty
import xarray as xr


class Profiles:
    """
    Parent class for the profiles, just contains the plot and header
    """

    def __init__(self):
        """
        Just initialise the main attributes
        """
        self.file = None
        self.data = []

    def __getitem__(self, item):
        return self.data[item]

    def plot(self, var='te', ax=None, ax_params={}, line_params={}):
        """
        Plot a given profile

        Jose Rueda: jrrueda@us.es

        @param var: variable to plot
        @param ax: axes where to plot
        @param ax_params: parameters for the axis beauty
        @param line_params: line parameters for the plt.plot function
        """
        # --- Default plotting options
        ax_options = {
            'grid': 'both',
            # 'xlabel': self.header['info']['rho']['shortName'],
            # 'ylabel':  self.header['info'][var]['shortName']
            # + self.header['info'][var]['units'],
        }
        ax_options.update(ax_params)
        # --- Create the axes
        if ax is None:
            fig, ax = plt.subplots()
            created = True
        else:
            created = False
        self.data[var].plot(ax=ax, **line_params)
        ax.set_xlim(self.data.rho[0], self.data.rho[-1])
        # axis beauty:
        if created:
            ax = axis_beauty(ax, ax_options)


class ProfilesInput(Profiles):
    """
    Read and write the input plasma profiles for the Far3D code.

    Jose Rueda: jrrueda@us.es

    @ToDo: The writting part
    """

    def __init__(self, filename=None, DIIID_u=0, alpha_on=0):
        """
        Initialize the object.

        Jose Rueda: jrrueda@us.es

        @param filename: filename for the ASCII file with the profiles, in
            far3D format. If None, the object will be initialised as empty
            ideal if you want to will it with your own profiles and then write
            the file
        @param DIIID_u: namelist variable of the simulation, to decide the units
        @param alpha_on: namelist variable of the simulation, to include a
            second specie
        """
        self.file = filename
        # --- Initilise the profiles
        prof = xr.Dataset()
        # Header
        header = profilesOrderInputs[DIIID_u][alpha_on]

        # --- Read the profiles
        if filename is not None:
            with open(filename) as fid:
                dummy = fid.readline()
                dummy = fid.readline()
                prof['bt0'] = xr.DataArray(float(fid.readline()))
                prof['bt0'].attrs['long_name'] = 'Magnetic field on axis'
                prof['bt0'].attrs['units'] = 'T'
                dummy = fid.readline()
                prof['rmajr'] = xr.DataArray(float(fid.readline()))
                prof['rmajr'].attrs['long_name'] = \
                    'Geometric Center Major radius'
                prof['rmajr'].attrs['units'] = 'm'
                dummy = fid.readline()
                prof['rminr'] = xr.DataArray(float(fid.readline()))
                prof['rminr'].attrs['long_name'] = 'Minor radius'
                prof['rminr'].attrs['units'] = 'm'
                dummy = fid.readline()
                prof['kappa'] = xr.DataArray(float(fid.readline()))
                prof['kappa'].attrs['long_name'] = 'Avg. Elongation'
                prof['kappa'].attrs['units'] = ''
                dummy = fid.readline()
                prof['delta'] = xr.DataArray(float(fid.readline()))
                prof['delta'].attrs['long_name'] = \
                    'Avg. Top/Bottom Triangularity'
                prof['delta'].attrs['units'] = ''
                dummy = fid.readline()
                prof['mainImpurity'] = xr.DataArray(fid.readline())
                prof['mainImpurity'].attrs['long_name'] = \
                    'Main Contaminant Species'
                prof['mainImpurity'].attrs['units'] = ''
                dummy = fid.readline()
                prof['mi_mp'] = xr.DataArray(float(fid.readline()))
                prof['mi_mp'].attrs['long_name'] = \
                    'Main Ion Species mass/proton'
                prof['mi_mp'].attrs['units'] = ''
                macabro = fid.readline()
                elements = macabro.split('=')
                prof['beta0'] = xr.DataArray(float(elements[1].split(',')[0]))
                prof['beta0'].attrs['long_name'] = 'beta(0)'
                prof['beta0'].attrs['units'] = ''
                prof['Rmax'] = xr.DataArray(float(elements[2]))
                prof['beta0'].attrs['long_name'] = 'Rmax'
                prof['beta0'].attrs['units'] = 'm'
                prof['eps'] = xr.DataArray(prof.rminr / prof.rmajr)
                prof['eps'].attrs['long_name'] = 'Aspect ratio'
                prof['eps'].attrs['units'] = ''
                # Finally end of header, uff
            # Now just read and store the profiles
            dummy = np.loadtxt(filename, skiprows=18)
            icolumrho = header['rho']['i']

            for k in header.keys():
                if k == 'rho':
                    continue  # The rho is the axis
                icolum = header[k]['i']
                prof[k] = xr.DataArray(dummy[:, icolum],
                                       dims=('rho'),
                                       coords={'rho': dummy[:, icolumrho]})
                prof[k].attrs['long_name'] = header[k]['longName']
                prof[k].attrs['short_name'] = header[k]['shortName']
                prof[k].attrs['units'] = header[k]['units']
        self.data = prof


class ProfilesOutputDat(Profiles):
    """
    Read and handle the profiles.dat file generated by FAR3d

    Jose Rueda: jrrueda@us.es
    """

    def __init__(self, filename=None, ext_prof: int = 0, alpha_on: int = 0):
        """Initialise the class."""
        self.file = filename
        data = np.loadtxt(filename, skiprows=1)
        nr, nc = data.shape
        if ext_prof == 0 and nc != 14:
            print('Was expecting 14 but I got %i columns' % nc)
            raise Exception('Wrong file?')
        if ext_prof == 1 and alpha_on == 0 and nc != 17:
            print('Was expecting 16 but I got %i columns' % nc)
            raise Exception('Wrong file?')
        if ext_prof == 1 and alpha_on == 1 and nc != 19:
            print('Was expecting 18 but I got %i columns' % nc)
            raise Exception('Wrong file?')
        self.data = data
        self.header = {'info': profilesOrderDat[ext_prof][alpha_on]}


class ProfilesOutputExDat(Profiles):
    """
    Read and handle the profiles_ex.dat file generated by FAR3d

    Jose Rueda: jrrueda@us.es
    """

    def __init__(self, filename=None, alpha_on: int = 0):
        self.file = filename
        data = np.loadtxt(filename, skiprows=1)
        nr, nc = data.shape
        if alpha_on == 0 and nc != 11:
            raise Exception('Wrong file?')
        if alpha_on == 1 and nc != 13:
            raise Exception('Wrong file?')
        self.data = data
        self.header = {'info': profilesOrderExDat[alpha_on]}
