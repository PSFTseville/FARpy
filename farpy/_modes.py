"""
Read the mode amplitudes

Jose Rueda: jrrueda@us.es

This module try to kinda mimic the struture of the harmonics object created by
Pablo Oyola for his library to analyse MEGA output
"""

import os
import logging
import numpy as np
import xarray as xr
import farpy._Plotting as libplt
import matplotlib.pyplot as plt
from farpy._paths import Path
__all__ = ['Modes']
# Initialise some classes
paths = Path()
logger = logging.getLogger('farpy.Models')


# ------------------------------------------------------------------------------
# --- Auxiliar function
# ------------------------------------------------------------------------------
def _getFileList(path: str = '.', start: str = 'vth', extension: str = ''):
    """
    Produces a sorted file name list with all the harmonics files found
    in the input path and matching with the extension.

    Pablo Oyola - pablo.oyola@ipp.mpg.de
    ft.
    Jose Rueda - jrrueda@us.es

    @param path: path to look for the files.
    @param start: first characters of the target files
    @param extension: extension of the target files.
    """

    # --- Making the list of the files in the path.
    filenames = list()
    for file in os.listdir(path):
        if file.startswith(start) and file.endswith(extension):
            filenames.append(file)

    filenames = sorted(filenames)
    if len(filenames) == 0:
        raise Exception('No files with matching extension')

    return filenames


# ------------------------------------------------------------------------------
# --- Modes class
# ------------------------------------------------------------------------------
class Modes:
    """
    Read and handle mode amplitude information.

    Jose Rueda: jrrueda@us.es
    """
    def __init__(self, model_name: str = None, path: str = None):
        """
        Initialise the class and read the files

        @param model_name: Name of the model to load, it is assumed to be inside
            the model folder, which is assumed to be inside the FAR3d folder
        @param path: if present, this folder will be assumed to contain all the
            results, and the model_name input will be ignored
        """
        if path is None:
            path = os.path.join(os.getenv('HOME'), 'FAR3d',
                                'Models', model_name)
            if not os.path.isdir(path):
                raise Exception('FAR3d not in home dir? Give me the right path')
        self.model_name = model_name
        self.path = path
        self._read_files()

    def _read_files(self, names: list = None):
        """
        Read the files

        @param names: prefix of the files to be read, if none, all simulation
            files will be read
        """
        if names is None:
            names = ['vthprlf', 'vth', 'vr', 'vprlf', 'uzt', 'psi', 'pr',
                     'phi', 'nf']            
        # see how many runs there are:
        files_of_vth = _getFileList(self.path, start='psi')
        nruns = len(files_of_vth)
        logger.info('Found %i runs', nruns)
        runs = []
        for file in files_of_vth:
            runs.append(file.split('_')[1])
        # Read a header, to allocate the variables size:
        filename = os.path.join(self.path, files_of_vth[0])
        nr, two_nmodes_plus_1 = np.loadtxt(filename, skiprows=1).shape
        fid = open(filename)
        line = fid.readline()
        fid.close()
        n = []
        m = []
        try:  # New far3D format, with R, I
            found_I = False
            for s in line.split():
                if s == 'I':  # n/m repeat, so stop
                    found_I = True
                    break
                if len(s.split('/')) == 2:
                    m.append(int(s.split('/')[0]))
                # the m comes with /, so the only other numbers in the line are n
                try:
                    n.append(int(s))
                except ValueError:  # we have an R
                    pass
            if not found_I:
                raise Exception()
        except:
            n = []
            m = []
            for s in line.split():
                if len(s.split('/')) == 2:
                    dummy_m = int(s.split('/')[0])
                    if dummy_m < 0:  # n/m repeat, so stop
                        break
                    m.append(dummy_m)
                # the m comes with /, so the only other numbers in the line are n
                try:
                    n.append(int(s))
                except ValueError:  # we have an R
                    pass
        n = np.array(n)
        unique_n = np.unique(n)
        indeces_n = np.zeros(n.size, dtype=int)
        for iin, nn in enumerate(n):
            indeces_n[iin] = np.where(unique_n == nn)[0]
        m = np.array(m)
        unique_m = np.unique(m)
        indeces_m = np.zeros(m.size, dtype=int)
        for iim, mm in enumerate(m):
            indeces_m[iim] = np.where(unique_m == mm)[0]

        if (2*len(n)+1) != two_nmodes_plus_1:
            print('n:', n)
            print('m:', m)
            print('n shape:', n.shape)
            print('m shape:', m.shape)
            raise Exception('Something went wrong reading the header')

        # preallocate the macro matrix
        # data = np.empty(
        #     (nruns, unique_n.size, unique_m.size, 2, len(names), nr))
        # read all the files:
        data = xr.Dataset()
        for file in names:
            logger.info('Reading %s', file)
            dum = np.empty(
                (nruns, unique_n.size, unique_m.size, 2, nr))
            for iis, s in enumerate(runs):
                filename = os.path.join(self.path, file + '_' + s)
                dummy = np.loadtxt(filename, skiprows=1)
                # put each colum in place
                for icolum in range(1, int((two_nmodes_plus_1+1)/2)):
                    # amplitude
                    dum[iis, indeces_n[icolum-1], indeces_m[icolum-1], 0, :] =\
                        dummy[:, icolum]
                    dum[iis, indeces_n[icolum-1], indeces_m[icolum-1], 1, :] =\
                        dummy[:, icolum + n.size]
            data[file] = xr.DataArray(
                dum.copy(), dims=('run', 'n', 'm', 'R_I', 'r'),
                coords={'run': runs, 'n': unique_n, 'm': unique_m, 
                        'R_I': ['R', 'I'], 'r': dummy[:, 0]})
        self.data = data

    def plotRho(self, run: str = '0000', n: int = 1, m: int = 1, R_I: str = 'R',
                var_name='pr', ax=None, ax_params: dict = {}, 
                line_params: dict = {}):
        """
        Plot the radial profile of the mode

        @param run: string identifying the runs to plot. It can be a list of
             strings, in that case, several runs will be plotted
        @param n: number of the mode to plot. can be an integer or an array 
            (or list) of integers
        @param m: number of the mode to plot. can be an integer or an array 
            (or list) of integers
        @param R_I: 'R' to plot the real part, 'I' to plot the imaginary
        @param var_name: variable to be plotted. See self.data for a list
        @param ax: axes where to plot, is none, new one will be created
        @param ax_params: axis parameters for the function axis_beauty. Notice
            that they will not be applyed if ax is not None
        @param line_params: line parameters for the function matplotlib plot 
            function. Notice that no label can't be set, as it is set
            automatically in the routine with the m/n value
        """
        # Initialise plotting options
        ax_options = {
            'xlabel': 'r',
            'grid': 'both',
        }
        ax_options.update(ax_params)
        # check that everything is a list as it should:
        if not isinstance(run, (list, np.ndarray)):
            run = np.array([run])
        if n is not None:
            if not isinstance(n, (np.ndarray,)):
                if not isinstance(n, (list,)):
                    n = np.array([n])
                else:
                    n = np.array(n)
        else:
            n = self.data.n.values
        if m is not None:
            if not isinstance(m, (np.ndarray,)):
                if not isinstance(m, (list,)):
                    m = np.array([m])
                else:
                    m = np.array(m)
        else:
            m = self.data.m.values
        if not isinstance(R_I, (list, np.ndarray)):
            R_I = np.array([R_I])
        if not isinstance(var_name, (list, np.ndarray)):
            var_name = np.array([var_name])
        # Check that we have that variable
        for s in var_name:
            if s not in self.data.keys():
                print('Variable not found: %s', s)
                print('Possible variables: ', self.data.keys())
                raise Exception('Not available variable')
        # --- Now the loop
        if ax is None:
            fig, ax = plt.subplots()
            created = True
        else:
            created = False
        for irun, r in enumerate(run):
            for jRI, RI in enumerate(R_I):
                for jn, nn in enumerate(n):
                    for jm, mm in enumerate(m):
                        for ivar, vvar in enumerate(var_name):

                            name = '%s: %s %s n=%s m=%s' % (r, vvar, RI, nn, mm)
                            logging.info('Plotting %s', name)
                            # Select the data
                            ax.plot(self.data.r,
                                     self.data[vvar].sel(run=r, n=nn,
                                                         m=mm, R_I=RI).values,
                                     label='%s: n=%i - m=%i'%(RI, nn, mm),
                                     **line_params)
        if created:
            libplt.axis_beauty(ax, ax_options)
        return ax
