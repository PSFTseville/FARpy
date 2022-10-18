"""
Read the mode amplitudes and energy

Done for farpy version: 0.0.2
"""
import farpy
import matplotlib.pyplot as plt

## -----------------------------------------------------------------------------
# --- Settings
# ------------------------------------------------------------------------------
folder = '/home/joserueda/Downloads/QPS_non_linear'

## -----------------------------------------------------------------------------
# --- Load modes
# ------------------------------------------------------------------------------
modes = farpy.Modes(path=folder)
## -----------------------------------------------------------------------------
# --- Plot the energy
# ------------------------------------------------------------------------------
# Plot the energy
fig, ax = plt.subplots(2)
modes.data.eke.sel(n=0).plot.line(x='run', ax=ax[0])
modes.data.ekenc.sel(n=0).plot.line(x='run', ax=ax[1])
ax[0].set_yscale('log')
ax[1].set_yscale('log')
## -----------------------------------------------------------------------------
# --- Use time
# ------------------------------------------------------------------------------
# Swap run id and time
modes._change_runID_with_time()
fig2, ax2 = plt.subplots(2)
modes.data.eke.sel(n=0).plot.line(x='time', ax=ax2[0])
modes.data.ekenc.sel(n=0).plot.line(x='time', ax=ax2[1])
ax2[0].set_yscale('log')
ax2[1].set_yscale('log')