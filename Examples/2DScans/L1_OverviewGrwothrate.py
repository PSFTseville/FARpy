"""
Example of how to read and plot the growthrate/Omega of the scan

Lines marked with # -# at the end need to be adjusted to your paths/computer

Please do not modify this file, copy it to your 'MyRoutines' folder and change
things there

Created for version 0.0.1 of farpy. Since then, things could have change so
is possible some minor errors appear or some faster workaround was implemented.
If you need it, open an issue in GitHub asking for an update
"""
import farpy 
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec

# ------------------------------------------------------------------------------
# --- Settings
# ------------------------------------------------------------------------------
rootScanFolder = '/home/joserueda/Downloads/beta_cvfp_swept_n_1_m_1-6'  # -#
cmap = farpy.plt.Gamma_II()




# ------------------------------------------------------------------------------
# --- Reading the scan
# ------------------------------------------------------------------------------
Scan = farpy.scan.Scan2D(rootScanFolder)  # Initialise the scan object
Scan.readNamelist()     # Read the namelist of the simulations
Scan.readGrowthRateBlock()  # Read the growth rate and Omega
Scan.readProfiles()     # Read the input profile information
Scan.readModes()        # Read the mode profile
Scan.renormFrequency()  # Change frequency to kHz
Scan.renormCVFP()       # Use Tfast as coordinate

# ------------------------------------------------------------------------------
# --- Plot
# ------------------------------------------------------------------------------
fig = plt.figure()
gs1 = gridspec.GridSpec(2, 2)
ax1 = plt.subplot(gs1[0,0])
ax2 = plt.subplot(gs1[0,1])
ax3 = plt.subplot(gs1[1,0:2])

# Now make the 2 fisrt axis to share the axes, in order the zoom to work in
# in common

ax2.sharex(ax1)
ax2.sharey(ax1)

# Now plot the modes of the first point
Scan.modes[0,0].plotRho(var_name='phi', ax=ax3, n=None, m=None, R_I='R')
Scan.modes[0,0].plotRho(var_name='phi', ax=ax3, n=None, m=None, R_I='I', 
                        line_params={'linestyle':'--'})
text = ax3.text(0.05, 0.05, 'Temp',
         horizontalalignment='left',
         color='k', verticalalignment='bottom',
         transform=ax3.transAxes)

# Now plot the Omega and gamma
Scan.plotGrowthRateBlock('omega', ax=ax1, cmap=cmap)
Scan.plotGrowthRateBlock('gamma', ax=ax2, cmap=cmap)

# Small function to update the plot
def onclick(event, ax0=ax2, ax=ax3, Scan=Scan, text=text):
    if event.button == 1:
        # ask for a new point
        plt.sca(ax0)
        point, = plt.ginput(1)
        # Clean the axis
        for i in range(len(ax.lines)):
            ax.lines[-1].remove()
        # Plot the new stuff
        i2 = np.argmin(np.abs(Scan.growthRateBlock['Tf'].values-point[0]))
        i1 = np.argmin(np.abs(Scan.growthRateBlock['beta'].values-point[1]))
        Scan.modes[i1,i2].plotRho(var_name='phi', ax=ax, n=None, m=None, R_I='R')
        Scan.modes[i1,i2].plotRho(var_name='phi', ax=ax, n=None, m=None, R_I='I', 
                                  line_params={'linestyle': '--'})
        ax.set_title('beta=%.2f, Tf=%.0f' % (Scan.growthRateBlock['beta'][i1], 
                                             Scan.growthRateBlock['Tf'][i2]))
        #ax.legend(loc='lower left', ncol=6)
        kind = np.unravel_index(Scan.modes[i1,i2].data['phi'].argmax(), 
                                Scan.modes[i1,i2].data['phi'].shape)
        n = Scan.modes[i1,i2].data['n'][kind[1]]
        m = Scan.modes[i1,i2].data['m'][kind[2]]
        text.remove()
        text = ax3.text(0.05, 0.05, 'n=%i, m=%i' % (n, m),
                        horizontalalignment='left',
                        color='k', verticalalignment='bottom',
                        transform=ax3.transAxes)
        plt.draw()
fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()
plt.draw()  # Not needed for old matplotlib versions
# Set the layout to tight to avoid collisions
plt.tight_layout()