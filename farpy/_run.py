"""
Module to run FAR3D simulations
"""
import os
from farpy._paths import Path
paths = Path()


def runFAR3d(model_name: str, cluster: bool = False):
    """
    Run the FAR3D code

    Note: simple an iterative run is used,
    @TODO: Add cluster submission
    """
    # Check if the far3D model exist
    path = os.path.join(os.path.expanduser('~'), 'FAR3d',
                        'Models', model_name)
    if not os.path.isdir(path):
        raise Exception('Model forlder not found')
    # launch the code
    os.system('cd %s' % path + '; ./xfar3d')

def runEigensolver(model_name: str, number1, number2, cluster: bool = False):
    """
    Run the eigensolver
    :param model_name:
    :param cluster:
    :return:
    """
    # Check if the far3D model exist
    path = os.path.join(os.path.expanduser('~'), 'FAR3d',
                        'Models', model_name)
    if not os.path.isdir(path):
        raise Exception('Model forlder not found')
    # launch the code
    pat = os.path.join(os.path.expanduser('~'), 'FAR3d','Addon',
                       'Eigensolver', 'xEigen')
    os.system('cd %s' % path + '; ' + pat + ' %f %f' % (number1, number2))
