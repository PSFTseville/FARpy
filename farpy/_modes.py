"""
Read the mode amplitudes

Jose Rueda: jrrueda@us.es

This module try to kinda mimic the struture of the harmonics object created by
Pablo Oyola for his library to analyse MEGA output
"""

import os
import sys
import numpy as np
import xarray as xr
import farpy._Plotting as libplt
import matplotlib.pyplot as plt

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


class Modes:
    def __init__(self, model_name: str, path: str = None):
        if path is None:
            path = os.path.join(os.getenv('HOME'), 'FAR3d',
                                'Models', model_name)
            if not os.path.isdir(path):
                raise Exception('FAR3d not in home dir? Give me the right path')
        self.model_name = model_name
        self.path = path
        self._read_files()

    def _read_files(self):
        names = [
            'vthprlf',
            'vth',
            'vr',
            'vprlf',
            'uzt',
            'psi',
            'pr',
            'phi',
            'nf',
        ]
        # see how many runs there are:
        files_of_vth = _getFileList(self.path, start='psi')
        nruns = len(files_of_vth)
        print('Found %i runs' % nruns)
        runs = []
        for file in files_of_vth:
            runs.append(file.split('_')[1])
            print('run %s found' % runs[-1])
        # Read a header, to allocate the variables size:
        filename = os.path.join(self.path, files_of_vth[0])
        nr, two_nmodes_plus_1 = np.loadtxt(filename, skiprows=1).shape
        fid = open(filename)
        line = fid.readline()
        fid.close()
        n = []
        m = []
        for s in line.split():
            if s == 'I':  # n/m repeat, so stop
                break
            if len(s.split('/')) == 2:
                m.append(int(s.split('/')[0]))
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
            raise Exception('Something went wrong reading the header')
        # preallocate the macro matrix
        data = np.empty(
            (nruns, unique_n.size, unique_m.size, 2, len(names), nr))
        # read all the files:
        for iis, s in enumerate(runs):
            for ifile, file in enumerate(names):
                print('Reading %s' % file)
                filename = os.path.join(self.path, file + '_' + s)
                dummy = np.loadtxt(filename, skiprows=1)
                # put each colum in place
                for icolum in range(1, int((two_nmodes_plus_1-1)/2)):
                    # amplitude
                    data[iis, indeces_n[icolum-1], indeces_m[icolum-1], 0, ifile, :] =\
                        dummy[:, icolum]
                    
                    data[iis, indeces_n[icolum-1], indeces_m[icolum-1], 1, ifile, :] =\
                        dummy[:, icolum + n.size]
        # Now create the magic of the array:
        self.data = xr.DataArray(
            data,
            dims=('run', 'n', 'm', 'R_I', 'var_name', 'r'),
            coords={'run': runs, 'n': unique_n.astype(str), 'm': unique_m.astype(str), 'R_I': ['R', 'I'],
                    'var_name': names, 'r': dummy[:, 0]}
        )

    def plotRho(self, run = '0000', n = '1', m = '1', R_I = 'R', var_name='pr',
                ax=None, ax_params: dict = {}):
        """
        Plot the radial profile of the mode

        @param run: string identifying the runs to plot. It can be a list of
             strings, in that case, several runs will be plotted
        @param n: number of the mode to plot. Can be a string, an array of
            strings, a number or array of numbers
        @param m: m number of the mode to plot. Can be a string, an array of
            strings, a number or array of numbers
        @param R_I: 'R' to plot the real part, 'I' to plot the imaginary
        @param var_name: variable to be plotted. See self.data.var for a list
        @param ax: axes where to plot, is none, new one will be created
        @param ax_params: axis parameters for the function axis_beuty. Notice
            that they will not be applyed if ax is not None
        """
        # Initialise plotting options
        ax_options = {
            'xlabel': 'r',
            'grid': 'both',
        }
        # check that everything is a list as it should:
        if not isinstance(run, (list, np.ndarray)):
            run = np.array([run])
        if not isinstance(n, (np.ndarray,)):
            if not isinstance(n, (list,)):
                n = np.array([n])
            else:
                n = np.array(n)
        n = n.astype(str)
        if not isinstance(m, (np.ndarray,)):
            if not isinstance(m, (list,)):
                m = np.array([m])
            else:
                m = np.array(m)
        m = m.astype(str)
        if not isinstance(R_I, (list, np.ndarray)):
            R_I = np.array([R_I])
        if not isinstance(var_name, (list, np.ndarray)):
            var_name = np.array([var_name])
        # Check that we have that variable
        for s in var_name:
            if s not in self.data.var_name:
                print('Variable not found: %s', s)
                print('Possible variables: ', self.data.var_name)
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
                            print(name)
                            plt.plot(self.data.r,
                                     self.data.sel(run=r, var_name=vvar, n=nn,
                                                   m=mm, R_I=RI))
        if created:
            libplt.axis_beauty(ax, ax_params)
