import farpy
import matplotlib.pyplot as plt
# ----
# %% Settings
# ----
prefix = '41091_n1_'
p1 = False  # Plot the input profiles for the simulation
p2 = True
# ---
# %% Load the scan data
# --
Scan = farpy.scan.Scan1D(prefix=prefix)
Scan.readNamelist()
Scan.readProfiles()
Scan.readEigensolver()
Scan.renormFrequencyEigenSolver()
# ---
# %%  Plot input profiles
# ---
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
# ---------------
# %% Plot the mode frequencies and growth rate
# ---------------
if p2:
    Scan.plotFrequenciesEigensolver(vmin=-1e-10, vmax=1e-10)
