"""
Module to read the eigensolver data

Jose Rueda: jrrueda@us.es

Introduced in version 0.1.0
"""
import os
import logging
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from farpy._Plotting._settings import axis_beauty

# ------------------------------------------------------------------------------
# --- Auxiliary object
# ------------------------------------------------------------------------------
logger = logging.getLogger('farpy.EigenVectors')

# ------------------------------------------------------------------------------
# --- EigenVectors class
# ------------------------------------------------------------------------------
class EigenSolver():
    """
    Class to read and handle the EigenSolver results

    Written by Jose Rueda

    Introduced in version 0.0.5
    """
    def __init__(self, path: str = None, model_name: str = None):
        """
        Read the eigensolver data

        Jose Rueda: jrrueda@us.es

        :param path: path to look for the files. If None, the model will be
            assumed to be located in the FAR3D main folder
        :param model name: model name if none, will be guessed from the path
        """
        if path is None:
            if path is None:
                path = os.path.join(os.path.expanduser('~'), 'FAR3d',
                                    'Models', model_name)
                if not os.path.isdir(path):
                    raise Exception('FAR3d not in home dir? Give me the right path')
        # Save the information in the object
        self.path = path
        if model_name is not None:
            self.model_name = model_name
        else:
            logger.warning('10: Guessing model name from path')
            self.model_name = os.path.split(path)[-1]
        # Allocate the space
        self.header = None
        self.egn_vectors = None
        self.egn_values = None

    def _read_egn_mode_asci_header(self):
        """
        Read the header of the egn_mode_ascii file

        Read the mode number and number of modes in the file
        """
        if self.egn_values is None:
            self._read_egn_values()
        # Get the name of the file to be read
        file = os.path.join(self.path, 'egn_mode_asci.dat')
        self._data.attrs['eigenmodeFile'] = file
        counter = 0
        with open(file, 'r') as fid:
            numberOfModes = int(fid.readline())
            counter += 1
            numberOfPoloidalModes = int(fid.readline())
            counter += 1
            numberOfRadialPoints = int(fid.readline())
            counter += 1
            nn = np.zeros(numberOfPoloidalModes, int)
            mm = np.zeros(numberOfPoloidalModes, int)
            for i in range(numberOfPoloidalModes):
                mm[i] = int(fid.readline())
                nn[i] = int(fid.readline())
                counter += 2
            self.header = {
                'numberOfModes': numberOfModes,
                'numberOfPoloidalModes': numberOfPoloidalModes,
                'numberOfRadialPoints': numberOfRadialPoints,
                'n': np.concatenate((nn, nn), axis=None),
                'm': np.concatenate((mm, -mm[mm.size::-1]), axis=None),
                'headerLines': counter
            }
        self._data['n'] = xr.DataArray(self.header['n'], dims=('mode'))
        self._data['m'] = xr.DataArray(self.header['m'], dims=('mode'))

    def _read_egn_mode_asci(self):
        """
        Read the amplitudes stored in the ascii file
        """
        if self._data is None:
            self._read_egn_values()
        if 'n' not in self._data.keys():
            self._read_egn_mode_asci_header()
        # Open the file and read the data
        with open(self._data.eigenmodeFile, 'r') as fid:
            print(self._data.eigenmodeFile)
            # Skip the header:
            for j in range(self.header['headerLines']):
                fid.readline()

            # To short a bit the naming:
            ns = self.header['numberOfRadialPoints']
            nmat = self.header['numberOfModes']
            mn_col = self.header['numberOfPoloidalModes']
            # Now read the core stuff
            # --- Allocate the vectors
            rho = np.zeros(self.header['numberOfRadialPoints'])
            im_col = self.header['m']
            in_col = self.header['n']
            dm = np.zeros(self.header['numberOfModes'])
            dm_rd = np.zeros(self.header['numberOfModes'])
            iacept = np.zeros(self.header['numberOfModes'], int)
            i_orig = np.zeros(self.header['numberOfModes'], int)
            egn_vectors0 = np.zeros((2*mn_col, ns))
            # Aux quantities
            fscale = 1.0
            freq_max = 1.0e+6
            # Read the frequencies
            ic = 0
            for i in range(self.header['numberOfModes']):
                dm[i] = float(fid.readline())
                dm_test = dm[i]*fscale**2
                if dm_test < freq_max:
                    iacept[i] = ic
                    dm_rd[ic] = dm[i]*fscale**2
                    i_orig[ic] = i
                    ic += 1
                else:
                    iacept[i] = -1
            # Read the radial grid
            logger.info('Reading radial grid')
            for irho in range(self.header['numberOfRadialPoints']):
                rho[irho] = float(fid.readline())
            # Allocate the sapce for the good solutions
            nmat_rd = ic
            egn_vectors = np.zeros((nmat_rd,
                                    2*self.header['numberOfPoloidalModes'],
                                    self.header['numberOfRadialPoints']))
            logger.info('Reading modes')
            for j in range(nmat):
                for m in range(ns):
                    for i in range(mn_col):
                        mneg = 2*mn_col - i - 1
                        egn_vectors0[i, m] = float(fid.readline())
                        egn_vectors0[mneg, m] = float(fid.readline())
                if iacept[j] != -1:
                    egn_vectors[iacept[j], :, :] = egn_vectors0.copy()
            self.extraLines = fid.readlines()
        self._data['amp'] = xr.DataArray(
            egn_vectors, dims=('j', 'mode', 'r'),
            coords={'mode': np.arange(self._data.n.size),
                    'r': rho})

        self.rho = rho

    def _read_egn_values(self):
        """
        Read the eigen values from the 'egn_values.dat' file
        """
        # Get the name of the file to be read
        file = os.path.join(self.path, 'egn_values.dat')
        # Open the file and read the data
        dummy = np.loadtxt(file)
        self._data = xr.Dataset()
        self._data['omega'] = xr.DataArray(
            dummy[:, 0], dims='j',
            coords={'j': np.arange(dummy.shape[0])})
        self._data['gamma'] = xr.DataArray(
            dummy[:, 1], dims='j',
            coords={'j': np.arange(dummy.shape[0])})

    # -------------------------------------------------------------------------
    # %% Print data on terminal
    # -------------------------------------------------------------------------
    def printEigenValues(self):
        """Make a quick and formatted print in the terminal."""
        print('      f      g')
        print('----------------------')
        for i in range(self._data['n'].values.size):
            print('%.3e      %.3e' %
                  (self._data['omega'].values[i],
                   self._data['gamma'].values[i]))

    # -------------------------------------------------------------------------
    # %% Plot modes
    # -------------------------------------------------------------------------
    def plotModeAmplitude(self, omega, ax=None, ax_params: dict = {}):
        """
        Plot the Mode Amplitude profiles

        :param omega: omega of the mode to be plotted (the closest one will be
            chosen)
        :param ax: axes where to plot, if none, new axis will be created
        :param ax_params: dictionary with axis parameters for the function
            axis_beauty
        :return ax: the axes where the lines where drawn
        """
        ax_options = {}
        ax_options.update(ax_params)
        if ax is None:
            fig, ax = plt.subplots()
        # Get the modes closer in frequency
        j = np.argmin(np.abs(self._data.omega.values-omega))
        modes = self._data.amp.isel(j=j)
        for i in range(self._data.n.size):
            label = '(%i, %i)' % (self._data.n.values[i],self._data.m.values[i])
            ax.plot(modes.r, modes.values[i, :], label=label)
        ax.legend()
        ax = axis_beauty(ax, ax_options)
        return ax