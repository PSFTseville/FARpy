"""
Example of how to run a fast-particle beta scan
"""
import os
import farpy
import numpy as np
import matplotlib.pyplot as plt
from farpy._paths import Path
paths = Path()
# ----------------------------------------------------------------------------
# %% Settings
# ----------------------------------------------------------------------------
referenceSIM = 'ASDEX'
profileFileName = 'ASDEX_41091.txt'
equilibiumName = 'Eq_ASDEX'
basic_scan_name = '41091_n_1_bet0_f'
betaValues = np.logspace(-3, -1, 25)

# ----------------------------------------
# %% Load the reference simulation
# ---------------------------------------
referenceFolder = \
    os.path.join(os.path.expanduser('~'), 'FAR3d',
                 'Models', referenceSIM)
namelistFile = os.path.join(referenceFolder, 'Input_Model')
executableFile = os.path.join(referenceFolder, 'xfar3d')
equilibriumFile = os.path.join(referenceFolder, equilibiumName)
profileFile = os.path.join(referenceFolder, profileFileName)
namelist = farpy.readNamelist(namelistFile)

# ----------------------------------------------------
# Proceed with the scan
# ----------------------------------------------------
far3D = \
    os.path.join(os.path.expanduser('~'), 'FAR3d',
                 'Models')
for i in range(betaValues.size):
    # Create the folder for the new model
    nameModel = basic_scan_name + '_%8.6f' % betaValues[i]
    modelPath = os.path.join(far3D, nameModel)
    os.makedirs(modelPath, exist_ok=True)
    # Copy the executable there
    os.system('cp %s %s' % (executableFile, modelPath))
    # Copy the input profiles and equilibrium
    os.system('cp %s %s' % (equilibriumFile, modelPath))
    os.system('cp %s %s' % (profileFile, modelPath))
    # Change the beta value in the namelist
    namelist2 = namelist.copy()
    namelist2['bet0_f'] = betaValues[i]
    # Write the namelist
    farpy.writeNamelist(os.path.join(modelPath, 'Input_Model'), namelist2)
    # Execute the code
    farpy.run.runFAR3d(nameModel)
    # Execute the eigensolver
    farpy.run.runEigensolver(nameModel, 0.1, 0.5)
