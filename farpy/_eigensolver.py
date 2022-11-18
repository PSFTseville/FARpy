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

        :param folder:
        :param ID:
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

    def _read_egn_mode_asci(self):
        """

        :return:
        """
        # Get the name of the file to be read
        file = os.path.join(self.path, 'egn_mode_asci.dat')
        # Open the file and read the data
        with open(file, 'r') as fid:
            numberOfModes = int(fid.readline())
            numberOfPoloidalModes = int(fid.readline())
            numberOfRadialPoints = int(fid.readline())
            nn = np.zeros(numberOfPoloidalModes, int)
            mm = np.zeros(numberOfPoloidalModes, int)
            for i in range(numberOfPoloidalModes):
                mm[i] = int(fid.readline())
                nn[i] = int(fid.readline())
            self.header = {
                'numberOfModes': numberOfModes,
                'numberOfPoloidalModes': numberOfPoloidalModes,
                'numberOfRadialPoints': numberOfRadialPoints,
                'n': nn,
                'm': mm,
            }
            # To short a bit the naming:
            ns = numberOfRadialPoints
            nmat = numberOfModes
            mn_col = numberOfPoloidalModes
            # Now read the core stuff
            # --- Allocate the vectors
            rho = np.zeros(self.header['numberOfRadialPoints'])
            im_col = self.header['m']
            in_col = self.header['n']
            dm = np.zeros(self.header['numberOfModes'])
            dm_rd = np.zeros(self.header['numberOfModes'])
            iacept = np.zeros(self.header['numberOfModes'], int)
            i_orig = np.zeros(self.header['numberOfModes'], int)
            egn_vectors0 = np.zeros((mn_col, ns))
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
                                    self.header['numberOfPoloidalModes'],
                                    self.header['numberOfRadialPoints']))
            logger.info('Reading modes')
            for j in range(nmat):
                for m in range(ns):
                    for i in range(mn_col):
                        egn_vectors0[i, m] = float(fid.readline())
                if iacept[j] != -1:
                    egn_vectors[iacept[j], :, :] = egn_vectors0.copy()
            self.extraLines = fid.readlines()
        self.egn_vectors = egn_vectors
        self.rho = rho


    def _read_egn_values(self):

        # Get the name of the file to be read
        file = os.path.join(self.path, 'egn_values.dat')
        # Open the file and read the data
        self.egn_values = np.loadtxt(file)

    def _read_egn_vector(self):
        """
        Mimic the effect of the colum.f90 script
        :return:
        """


