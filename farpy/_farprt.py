"""
Contain the object to read the farprt output file.

Jose Rueda-Rueda: jrrueda@us.es
"""
from statistics import median
import numpy as np
import xarray as xr
import os
import pandas as pd
import matplotlib.pyplot as plt
from copy import deepcopy
from farpy._namelist import readNamelist
import logging
logger = logging.getLogger('farpy.Farprt')


class Farprt:
    """
    Main class to read and interact with the farprt file

    List of public methods:
    - read_energy_block(): read the energy blocks (energies and grow rates)
    """

    def __init__(self, file: str):
        """
        Init the object

        For the moment, it does nothing, just save the filename
        """
        self.file = file
        self.namelist = None
        self.energyData = None

    def readNamelistBlock(self):
        """
        Read the namelist block

        Jose Rueda: jrrueda@us.es
        """
        self.namelist = readNamelist(self.file, header=11)

    def readEnergyBlock(self):
        """
        Read the energy block

        This is not efficient, but I do not know any other way of reading such a
        file
        """
        # Check the namelist options of this simulation
        if self.namelist is None:
            print('Namelist was not loaded, loading it')
            self.readNamelistBlock()
            print('Namelist read')
        if self.namelist['alpha_on'] == 1:
            two_FI_specie = True
        else:
            two_FI_specie = False

        data = {
            'l': int(),
            'm': int(),
            'n': int(),
            'ke': float(),
            'me': float(),
            'vprlf': float(),
            'gamke': float(),
            'gamme': float(),
            'gamvpr': float(),
            'numrun': int(),
            'numruno': int(),
            'nstep': int(),
            'time': float(),
            'dt': float(),
        }
        if two_FI_specie:
            raise Exception('Sorry still not done')
            data['cosa_extra1'] = []
            data['cosa_extra2'] = []
        # self.data = pd.DataFrame(columns=('l', 'm',
        #                                   'n', 'ke', 'me', 'vprlf', 'gamke', 'gamme', 'gamvpr', 'numrun',
        #                                   'numruno', 'nstep', 'time', 'dt',))
        self.energyData = pd.DataFrame(data, index=[])
        print('Reading energy block')
        with open(self.file) as f:
            for line in f:
                if line.startswith('energy:numrun'):  # we found the firs line
                    # Separate the coment line in the 5 blocks
                    dum_num, dum_runo, dum_nstep, dum_time, dum_dt = \
                        line.split(',')
                    # from each bloc, read the number
                    numrun = dum_num.split('=')[-1].strip()
                    numruno = dum_runo.split('=')[-1].strip()
                    nstep = int(dum_nstep.split('=')[-1])
                    time = float(dum_time.split('=')[-1])
                    dt = float(dum_dt.split('=')[-1])
                    # read the dummy white line
                    dummy = f.readline()
                    # read the dummy line with the headers
                    dummy = f.readline()
                    # now read all the lines with the mode information
                    # we will do a filthy trick, if the line has less of 200
                    # characters will be the empty line between the blocks
                    numbers = f.readline()
                    len_of_line = len(numbers)
                    while len_of_line > 60:
                        array_of_numbers = numbers.split()
                        # if the number is ridully low, is bad printed, for
                        # example instead of 4e-280, far3d write  4-280, which
                        # makes the reading imposible, so take zero
                        try:
                            ke = float(array_of_numbers[3])
                        except ValueError:
                            ke = 0.0
                        try:
                            me = float(array_of_numbers[4])
                        except ValueError:
                            me = 0.0
                        try:
                            vprlf = float(array_of_numbers[5])
                        except ValueError:
                            vprlf = 0.0

                        row_to_add = {
                            'l': int(array_of_numbers[0]),
                            'm': int(array_of_numbers[1]),
                            'n': int(array_of_numbers[2]),
                            'ke': ke,
                            'me': me,
                            'vprlf': vprlf,
                            'gamke': float(array_of_numbers[6]),
                            'gamme': float(array_of_numbers[7]),
                            'gamvpr': float(array_of_numbers[8]),
                            'numrun': numrun,
                            'numruno': numruno,
                            'nstep': nstep,
                            'time': time,
                            'dt': dt,
                        }
                        self.energyData = self.energyData.append(
                            row_to_add.copy(), ignore_index=True)
                        numbers = f.readline()
                        len_of_line = len(numbers)
        # Ensure datatypes
        self.energyData.l = self.energyData.l.astype(int)
        self.energyData.m = self.energyData.m.astype(int)
        self.energyData.n = self.energyData.n.astype(int)
        self.energyData.nstep = self.energyData.nstep.astype(int)
        # Get the total energy
        # @@Todo check the normalization of this
        self.energyData['te'] = self.energyData.ke + self.energyData.me

    def plotEnergy(self, n=1, var='ke', m=None, ax=None):
        """
        Plot the mode energy
        """
        # --- Check the inputs
        if not isinstance(n, (np.ndarray, list)):
            n = np.array([n])
        if not isinstance(m, (np.ndarray, list)) and m is not None:
            m = np.array([m])
        else:
            m = np.unique(self.energyData.m)
        try:
            dum = self.energyData[var]
        except KeyError:
            print('Variable not found. Possible variables:')
            print(self.energyData.keys())
            raise Exception('Not available variable')

        # --- Proceed to plot
        unique_steps = np.unique(self.energyData.time)
        if ax is None:
            fig, ax = plt.subplots()
            created = True
        else:
            created = False
        for inn, nn in enumerate(n):
            indexn = self.energyData.n == nn
            unique_m = np.unique(self.energyData.m[indexn])
            for im, mm in enumerate(unique_m):
                if mm in m:
                    dummy = self.energyData[var][indexn][
                        self.energyData.m[indexn] == mm]
                    ax.plot(unique_steps, dummy,
                            label='n: %i, m: %i' % (nn, mm))
        ax.legend()
        if created:
            ax.set_ylabel(var)
            ax.set_xlabel('Time [$\\tau_R$]')

    def readGrowthRate(self, convergency_level = 0.1):
        """
        Read the Growth Rate and mode frequency

        @param convergency_level: level to consider if there is convergency or
            not. If the std/mean of the growthrate is larger than this number,
            it will be considered that no convergency is reached.

        Up to now, no method is assumed, in this non-converged case, the code
        will still consider the mean

        This can be easily changed uppon request
        """
        m = []
        n = []
        gamma = []
        omega = []
        var = []
        starting = (' psi   :', ' phi   :', ' pr    :', ' nfast :', ' vfast :',
                    ' vth   :')
        logger.info('Reading Growth Rate block')
        with open(self.file) as f:
            for line in f:
                if line.startswith(starting):  # we found a line
                    things = line.split()
                    var.append(things[0])
                    m.append(int(things[3]))
                    n.append(int(things[5]))
                    gamma.append(float(things[7]))
                    omega.append(float(things[9]))
        logger.info('Ordering the data')
        # Now that the data was read, is time to play with it
        # --- Move to npumpy arrays
        m = np.array(m)
        n = np.array(n)
        n_unique = np.unique(n)
        m_unique = np.unique(m)
        gamma = np.array(gamma)
        omega = np.array(omega)
        # --- Check the convergence
        for kn in n_unique:
            flags = n == kn
            std_gamma = gamma[flags].std()
            mean_gamma = gamma[flags].mean()
            test = std_gamma/mean_gamma
            if test > convergency_level:
                text = 'No convergence: n=%i mean_gamma/std_gamma = %f' % (kn,test)
                logger.warning('10: %s', text)
        # --- Save the stuff in place
        OMEGA = np.empty(shape=(m_unique.size, n_unique.size, 6))
        OMEGA.fill(np.nan)
        GAMMA = np.empty(shape=(m_unique.size, n_unique.size, 6))
        GAMMA.fill(np.nan)
        # TODO: This is not an optimum way of doing it, need a better way
        vars = np.array(['psi', 'phi', 'pr', 'nfast', 'vfast', 'vth'])
        for i in range(m.size):
            # See where we need to save the data
            ivar = np.where(vars == var[i])[0]
            imm = np.where(m_unique == m[i])[0]
            inn = np.where(n_unique == n[i])[0]
            # Save the data
            OMEGA[imm, inn, ivar] = omega[i]
            GAMMA[imm, inn, ivar] = gamma[i]
        # Save everything in a array
        self.GrowthRateBlock = xr.Dataset()
        self.GrowthRateBlock['omega'] = \
            xr.DataArray(OMEGA, dims=('m', 'n', 'var'),
                         coords={'var': vars, 'm': m_unique, 'n': n_unique})
        self.GrowthRateBlock['gamma'] = \
            xr.DataArray(GAMMA, dims=('m', 'n', 'var'))
        self.GrowthRateBlock['avg_omega_n'] = \
            xr.DataArray(np.nanmean(OMEGA, axis=(0, 2)), dims='n')
        self.GrowthRateBlock['avg_gamma_n'] = \
            xr.DataArray(np.nanmean(GAMMA, axis=(0, 2)), dims='n')
        self.GrowthRateBlock['avg_omega'] = \
            xr.DataArray(np.nanmean(OMEGA)
        self.GrowthRateBlock['avg_gamma'] = \
            xr.DataArray(np.nanmean(GAMMA)
        # A bit of metadata is always welcome
        self.GrowthRateBlock['n'].attrs['long_name'] = 'Toroidal mode number'
        self.GrowthRateBlock['m'].attrs['long_name'] = 'Poloidal mode number'
        self.GrowthRateBlock['var'].attrs['long_name'] = 'Var Short Name'
   
    def st2time(self, step: int):
        print('ToBe Done')
        pass

    def time2st(self, time: float):
        print('ToBe Done')
        pass
