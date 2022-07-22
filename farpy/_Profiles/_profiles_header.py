"""
Just the header with the name, colum index and units of all profiles.

Inside the dictionary, the first number means the option DIII_u, while the
second one the option alpha_on.

So in a case where the DIIID_u is not activated (=0, profiles not in TRANSP
units) and the second fast particle species is included (alpha_on=1) the header
will be:
header = profilesOrder[0][1]

Up to now, only the 'basic' option 0,0 is implemented
"""

profilesOrderInputs = {
    0: {
        0: {
            'rho': {
                'i': 0,  # Column index in the file
                'units': '',  # Units
                'longName': 'Normalized square value of the toroidal flux',
                'shortName': '$\\rho_t$',
            },
            'q': {
                'i': 1,  # Column index in the file
                'units': '',  # Units
                'longName': 'Safety factor',
                'shortName': '$q$',
            },
            'nnbi': {
                'i': 2,  # Column index in the file
                'units': '$10^{20}$m${}^{-3}$',  # Units
                'longName': 'Density of energetic particles',
                'shortName': '$n_{nbi}$'
            },
            'ni': {
                'i': 3,  # Column index in the file
                'units': '$10^{20}$m${}^{-3}$',  # Units
                'longName': 'Thermal ion density',
                'shortName': '$n_{i}$'
            },
            'ne': {
                'i': 4,  # Column index in the file
                'units': '$10^{20}$m${}^{-3}$',  # Units
                'longName': 'Thermal electron density',
                'shortName': '$n_{e}$'
            },
            'nimp': {
                'i': 5,  # Column index in the file
                'units': '$10^{20}$m${}^{-3}$',  # Units
                'longName': 'Impurity density',
                'shortName': '$n_{imp}$'
            },
            'tnbi': {
                'i': 6,  # Column index in the file
                'units': 'keV',  # Units
                'longName': 'Temperature of the energetic particles',
                'shortName': '$T_{nbi}$',
            },
            'ti': {
                'i': 7,  # Column index in the file
                'units': 'keV',  # Units
                'longName': 'Temperature thermal ions',
                'shortName': '$T_{i}$',
            },
            'te': {
                'i': 8,  # Column index in the file
                'units': 'keV',  # Units
                'longName': 'Temperature thermal electrons',
                'shortName': '$T_{e}$',
            },
            'pnbi': {
                'i': 9,  # Column index in the file
                'units': 'kPa',  # Units
                'longName': 'Presure of the energetic particles',
                'shortName': '$p_{nbi}$',
            },
            'p': {
                'i': 10,  # Column index in the file
                'units': 'kPa',  # Units
                'longName': 'Presure of the thermal particles',
                'shortName': '$p$',
            },
            'pequil': {
                'i': 11,  # Column index in the file
                'units': 'kPa',  # Units
                'longName': 'Equilibrium pressure',
                'shortName': '$\\phi_i$',
            },
            'vtor': {
                'i': 12,  # Column index in the file
                'units': 'km/s',  # Units
                'longName': 'Plasma toroidal rotation',
                'shortName': '$v_{tor}$',
            },
            'vpol': {
                'i': 13,  # Column index in the file
                'units': 'km/s',  # Units
                'longName': 'Plasma poloidal rotation',
                'shortName': '$v_{pol}$',
            },
        }
    }
}


profilesOrderDat = {   # Order of the file profiles.dat
    0: {
        0: {
            'rho': {
                'i': 0,  # Column index in the file
                'units': '',  # Units
                'longName': 'Normalized radius',
                'shortName': '$r$',
            },
            'np': {
                'i': 1,  # Column index in the file
                'units': '',  # Units
                'longName': 'Thermal plasma density',
                'shortName': '$n_{p}$',
            },
            'te': {
                'i': 2,  # Column index in the file
                'units': '',  # Units
                'longName': 'thermal electron temperature',
                'shortName': '$t_{e}$'
            },
            'nnbi': {
                'i': 3,  # Column index in the file
                'units': '',  # Units
                'longName': 'Density of energetic particles',
                'shortName': '$n_{nbi}$'
            },
            'dnnbidr': {
                'i': 4,  # Column index in the file
                'units': '',  # Units
                'longName': 'Radial derivative of the energetic particle density',
                'shortName': '$dn_{nbi}/dr$'  # @ToDo: change this acordinly
            },
            'vfova': {
                'i': 5,  # Column index in the file
                'units': '',  # Units
                'longName': 'Energetic particle thermal velocity normalised to the'
                + 'Alfven valocity in the magntic axis',
                'shortName': '$v^{th}_{nbi}$'
            },
            'cureq': {
                'i': 6,  # Column index in the file
                'units': '',  # Units
                'longName': 'Electric current',
                'shortName': '$I$'
            },
            'feq': {
                'i': 7,  # Column index in the file
                'units': '',  # Units
                'longName': 'Current density',
                'shortName': '$j$',
            },
            'p': {
                'i': 8,  # Column index in the file
                'units': '',  # Units
                'longName': 'Presure of the thermal particles',
                'shortName': '$p$',
            },
            'iota': {
                'i': 9,  # Column index in the file
                'units': '',  # Units
                'longName': 'Iota profile (no normalization)',
                'shortName': '$\\iota$',
            },
            '1/D': {
                'i': 10,  # Column index in the file
                'units': '',  # Units
                'longName': 'Inverse of the Jacobian matrix for n=0, '
                + 'no normalization',
                'shortName': '$1/D$',
            },
            'curvature': {
                'i': 11,  # Column index in the file
                'units': '',  # Units
                'longName': 'Radial derivative of the metric Jacobian for n=0, '
                + 'no normalization',
                'shortName': '$c$',
            },
            'shear': {
                'i': 12,  # Column index in the file
                'units': '',  # Units
                'longName': 'Magnetic shear, no normalization',
                'shortName': '$s_m$',
            },
            'eta': {
                'i': 13,  # Column index in the file
                'units': '',  # Units
                'longName': 'Plasma resistivity',
                'shortName': '$\\eta$',
            },
        },
        1: {}
    },
    1: {
        0: {
            'rho': {
                'i': 0,  # Column index in the file
                'units': '',  # Units
                'longName': 'Normalized radius',
                'shortName': '$r$',
            },
            'nnbi': {
                'i': 1,  # Column index in the file
                'units': '',  # Units
                'longName': 'Density of energetic particles',
                'shortName': '$n_{nbi}$'
            },
            'ne': {
                'i': 2,  # Column index in the file
                'units': '',  # Units
                'longName': 'Thermal plasma electron density',
                'shortName': '$n_{p}$',
            },
            'ni': {
                'i': 3,  # Column index in the file
                'units': '',  # Units
                'longName': 'Thermal plasma ion density',
                'shortName': '$n_{p}$',
            },
            'tnbi': {
                'i': 4,  # Column index in the file
                'units': '',  # Units
                'longName': 'Energetic particle temperature',
                'shortName': '$t_{nbi}$'
            },
            'ti': {
                'i': 5,  # Column index in the file
                'units': '',  # Units
                'longName': 'Thermal ion temperature',
                'shortName': '$t_{i}$'
            },
            'te': {
                'i': 6,  # Column index in the file
                'units': '',  # Units
                'longName': 'Thermal electron temperature',
                'shortName': '$t_{e}$'
            },
            'vfova': {
                'i': 7,  # Column index in the file
                'units': '',  # Units
                'longName': 'Energetic particle thermal velocity normalised to'
                + 'the Alfven valocity in the magntic axis',
                'shortName': '$v^{th}_{nbi}$'
            },
            'cureq': {
                'i': 8,  # Column index in the file
                'units': '',  # Units
                'longName': 'Electric current',
                'shortName': '$I$'
            },
            'feq': {
                'i': 9,  # Column index in the file
                'units': '',  # Units
                'longName': 'Current density',
                'shortName': '$j$',
            },
            'p': {
                'i': 10,  # Column index in the file
                'units': '',  # Units
                'longName': 'Presure of the thermal particles',
                'shortName': '$p$',
            },
            'iota': {
                'i': 11,  # Column index in the file
                'units': '',  # Units
                'longName': 'Iota profile (no normalization)',
                'shortName': '$\\iota$',
            },
            'q': {
                'i': 12,  # Column index in the file
                'units': '',  # Units
                'longName': 'q profile (no normalization)',
                'shortName': '$q$',
            },
            '1/D': {
                'i': 13,  # Column index in the file
                'units': '',  # Units
                'longName': 'Inverse of the Jacobian matrix for n=0, '
                + 'no normalization',
                'shortName': '$1/D$',
            },
            'curvature': {
                'i': 14,  # Column index in the file
                'units': '',  # Units
                'longName': 'Radial derivative of the metric Jacobian for n=0, '
                + 'no normalization',
                'shortName': '$c$',
            },
            'shear': {
                'i': 15,  # Column index in the file
                'units': '',  # Units
                'longName': 'Magnetic shear, no normalization',
                'shortName': '$s_m$',
            },
            'eta': {
                'i': 16,  # Column index in the file
                'units': '',  # Units
                'longName': 'Plasma resistivity',
                'shortName': '$\\eta$',
            },
        },
        1: {
            'rho': {
                'i': 0,  # Column index in the file
                'units': '',  # Units
                'longName': 'Normalized radius',
                'shortName': '$r$',
            },
            'nnbi': {
                'i': 1,  # Column index in the file
                'units': '',  # Units
                'longName': 'Density of energetic particles',
                'shortName': '$n_{nbi}$'
            },
            'ne': {
                'i': 2,  # Column index in the file
                'units': '',  # Units
                'longName': 'Thermal plasma electron density',
                'shortName': '$n_{p}$',
            },
            'ni': {
                'i': 3,  # Column index in the file
                'units': '',  # Units
                'longName': 'Thermal plasma ion density',
                'shortName': '$n_{p}$',
            },
            'nnbi2': {
                'i': 4,  # Column index in the file
                'units': '',  # Units
                'longName': 'Density of energetic particles, second specie',
                'shortName': '$n_{nbi2}$'
            },
            'tnbi': {
                'i': 5,  # Column index in the file
                'units': '',  # Units
                'longName': 'Energetic particle temperature',
                'shortName': '$t_{nbi}$'
            },
            'ti': {
                'i': 6,  # Column index in the file
                'units': '',  # Units
                'longName': 'Thermal ion temperature',
                'shortName': '$t_{i}$'
            },
            'te': {
                'i': 7,  # Column index in the file
                'units': '',  # Units
                'longName': 'Thermal electron temperature',
                'shortName': '$t_{e}$'
            },
            'tnbi2': {
                'i': 8,  # Column index in the file
                'units': '',  # Units
                'longName': 'Energetic particle temperature, second specie',
                'shortName': '$t_{nbi2}$'
            },
            'vfova': {
                'i': 9,  # Column index in the file
                'units': '',  # Units
                'longName': 'Energetic particle thermal velocity normalised to the'
                + 'Alfven valocity in the magntic axis',
                'shortName': '$v^{th}_{nbi}$'
            },
            'cureq': {
                'i': 10,  # Column index in the file
                'units': '',  # Units
                'longName': 'Electric current',
                'shortName': '$I$'
            },
            'feq': {
                'i': 11,  # Column index in the file
                'units': '',  # Units
                'longName': 'Current density',
                'shortName': '$j$',
            },
            'p': {
                'i': 12,  # Column index in the file
                'units': '',  # Units
                'longName': 'Presure of the thermal particles',
                'shortName': '$p$',
            },
            'iota': {
                'i': 13,  # Column index in the file
                'units': '',  # Units
                'longName': 'Iota profile (no normalization)',
                'shortName': '$\\iota$',
            },
            'q': {
                'i': 14,  # Column index in the file
                'units': '',  # Units
                'longName': 'q profile (no normalization)',
                'shortName': '$q$',
            },
            '1/D': {
                'i': 15,  # Column index in the file
                'units': '',  # Units
                'longName': 'Inverse of the Jacobian matrix for n=0, '
                + 'no normalization',
                'shortName': '$1/D$',
            },
            'curvature': {
                'i': 16,  # Column index in the file
                'units': '',  # Units
                'longName': 'Radial derivative of the metric Jacobian for n=0, '
                + 'no normalization',
                'shortName': '$c$',
            },
            'shear': {
                'i': 17,  # Column index in the file
                'units': '',  # Units
                'longName': 'Magnetic shear, no normalization',
                'shortName': '$s_m$',
            },
            'eta': {
                'i': 18,  # Column index in the file
                'units': '',  # Units
                'longName': 'Plasma resistivity',
                'shortName': '$\\eta$',
            },
        },
    }
}

profilesOrderDat[0][1] = profilesOrderDat[0][0]

profilesOrderExDat = {   # Order of the file profiles.dat
    0: {
        'rho': {
            'i': 0,  # Column index in the file
            'units': '',  # Units
            'longName': 'Normalized minor radius',
            'shortName': '$r$',
        },
        'nnbi': {
            'i': 1,  # Column index in the file
            'units': '',  # Units
            'longName': 'Density of energetic particles',
            'shortName': '$n_{nbi}$'
        },
        'ne': {
            'i': 2,  # Column index in the file
            'units': '',  # Units
            'longName': 'Thermal plasma electron density',
            'shortName': '$n_{e}$',
        },
        'ni': {
            'i': 3,  # Column index in the file
            'units': '',  # Units
            'longName': 'Thermal plasma ion density',
            'shortName': '$n_{i}$',
        },
        'tnbi': {
            'i': 4,  # Column index in the file
            'units': 'keV',  # Units
            'longName': 'Temperature of the energetic particles',
            'shortName': '$T_{nbi}$',
        },
        'ti': {
            'i': 5,  # Column index in the file
            'units': 'keV',  # Units
            'longName': 'Temperature thermal ions',
            'shortName': '$T_{i}$',
        },
        'te': {
            'i': 6,  # Column index in the file
            'units': 'keV',  # Units
            'longName': 'Temperature thermal electrons',
            'shortName': '$T_{e}$',
        },
        'vztor': {
            'i': 7,  # Column index in the file
            'units': 'm/s',  # Units
            'longName': 'Plasma toroidal rotation',
            'shortName': '$v_{tor}$',
        },
        'vtor': {
            'i': 8,  # Column index in the file
            'units': 'm/s',  # Units
            'longName': 'Plasma toroidal rotation',
            'shortName': '$v_{tor}$',
        },
        'vtor': {
            'i': 9,  # Column index in the file
            'units': 'm/s',  # Units
            'longName': 'Thermal ion velocity',
            'shortName': '$v_{tor}$',
        },
        'eta': {
            'i': 10,  # Column index in the file
            'units': '',  # Units
            'longName': 'Plasma resistivity',
            'shortName': '$\\eta$'
        },
    },
    1: {
        'rho': {
            'i': 0,  # Column index in the file
            'units': '',  # Units
            'longName': 'Normalized minor radius',
            'shortName': '$r$',
        },
        'nnbi': {
            'i': 1,  # Column index in the file
            'units': '',  # Units
            'longName': 'Density of energetic particles',
            'shortName': '$n_{nbi}$'
        },
        'ne': {
            'i': 2,  # Column index in the file
            'units': '',  # Units
            'longName': 'Thermal plasma electron density',
            'shortName': '$n_{e}$',
        },
        'ni': {
            'i': 3,  # Column index in the file
            'units': '',  # Units
            'longName': 'Thermal plasma ion density',
            'shortName': '$n_{i}$',
        },
        'nnbi2': {
            'i': 4,  # Column index in the file
            'units': '',  # Units
            'longName': 'Density of energetic particles, second specie',
            'shortName': '$n_{nbi2}$'
        },
        'tnbi': {
            'i': 5,  # Column index in the file
            'units': 'keV',  # Units
            'longName': 'Temperature of the energetic particles',
            'shortName': '$T_{nbi}$',
        },
        'ti': {
            'i': 6,  # Column index in the file
            'units': 'keV',  # Units
            'longName': 'Temperature thermal ions',
            'shortName': '$T_{i}$',
        },
        'te': {
            'i': 7,  # Column index in the file
            'units': 'keV',  # Units
            'longName': 'Temperature thermal electrons',
            'shortName': '$T_{e}$',
        },
        'tnbi2': {
            'i': 8,  # Column index in the file
            'units': 'keV',  # Units
            'longName': 'Temperature of the energetic particles, second specie',
            'shortName': '$T_{nbi2}$',
        },
        'vztor': {
            'i': 9,  # Column index in the file
            'units': 'm/s',  # Units
            'longName': 'Plasma toroidal rotation',
            'shortName': '$v_{tor}$',
        },
        'vtor': {
            'i': 10,  # Column index in the file
            'units': 'm/s',  # Units
            'longName': 'Plasma toroidal rotation',
            'shortName': '$v_{tor}$',
        },
        'vtor': {
            'i': 11,  # Column index in the file
            'units': 'm/s',  # Units
            'longName': 'Thermal ion velocity',
            'shortName': '$v_{tor}$',
        },
        'eta': {
            'i': 12,  # Column index in the file
            'units': '',  # Units
            'longName': 'Plasma resistivity',
            'shortName': '$\\eta$'
        },
    }
}
