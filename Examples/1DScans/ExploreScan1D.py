"""
This script will read a scan done with the egensolver options and plot the
main results

If the folders with resutls are not in the Models folder of FAR3D, please
use also the 'parentFolder' optional input when reading the scan data at line
26.

All lines with !!! at the end must be modified accordingly to your simulations
prior to run the script. Please do not do this in the example itself, to avoid
merge conflict, create a personal copy of the script.
"""

import farpy
import matplotlib.pyplot as plt
# -----------------------------------------------------------------------------
# %% Settings
# -----------------------------------------------------------------------------
prefix = '41091_n1_'   # Prefix of the simulations names  !!!
# Plotting options
p1 = False  # Plot the input profiles for the simulation
p2 = True   # Plot the frequencies and the growth rate
# -----------------------------------------------------------------------------
# %% Load the scan data
# -----------------------------------------------------------------------------
Scan = farpy.scan.Scan1D(prefix=prefix)   # Load the variables and structure
Scan.readNamelist()  # Load a namelist (for future des-normalization)
Scan.readProfiles()  # Load the profiles (for future desnormalization)
Scan.readEigensolver()  # Load the eigensolver data
Scan.renormFrequencyEigenSolver()  # change from code frequency to kHz
# -----------------------------------------------------------------------------
# %%  Plot input profiles
# -----------------------------------------------------------------------------
if p1:
    fig, ax = plt.subplots(3, sharex=True)
    # First suplots, densities
    Scan.profiles[0].plot('ni', ax=ax[0], line_params={'label': 'ni'})
    Scan.profiles[0].plot('ne', ax=ax[0], line_params={'label': 'ne'})
    ax[0].set_ylabel('[$10^{20}$]')
    ax[0].set_xlabel('')
    ax[0].legend()

    Scan.profiles[0].plot('ti', ax=ax[1], line_params={'label': 'Ti'})
    Scan.profiles[0].plot('te', ax=ax[1], line_params={'label': 'Te'})
    ax[1].set_ylabel('[keV]')
    ax[1].set_xlabel('')
    ax[1].legend()
    Scan.profiles[0].plot('nnbi', ax=ax[2], line_params={'label': 'Nfast'})
    ax[2].set_ylabel('[$10^{20}$]')
    ax[2].legend()
# -----------------------------------------------------------------------------
# %% Plot the mode frequencies and growth rate
# -----------------------------------------------------------------------------
if p2:
    Scan.plotFrequenciesEigensolver(vmin=-0.1, vmax=0.1)
