"""Paths to the different folders and codes"""
import os
from farpy._aux import update_case_insensitive
import f90nml


class Path:
    """
    Paths of the different codes and folders

    It will try to look for the paths in the file Data/MyData/Paths.txt

    Please do not change this class to avoid merge conflics
    """

    def __init__(self, machine='PC'):
        """Initialise the class"""
        home = os.path.expanduser('~')
        self.farpy = os.path.join(home, 'FARpy')
        self.far3d = os.path.join(home, 'FAR3d')
        self.Results = os.path.join(self.farpy, 'Results')
        # Generic case, assume you have linux :-)
        if os.path.isdir('/usr/share/fonts/truetype'):
            self.fonts = [
                '/usr/share/fonts/truetype',
                '/usr/share/fonts/opentype',
            ]
        else:  # You have windows and I have no idea whe the fonts are
            self.fonts = ['']
        # Load the custom paths
        file = os.path.join(self.farpy, 'Data', 'MyData', 'Paths.txt')
        nml = f90nml.read(file)
        update_case_insensitive(self.__dict__, nml['paths'])
