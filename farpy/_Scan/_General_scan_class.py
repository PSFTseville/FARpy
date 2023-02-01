"""
Just a dummy skeleton of a scan class, to share the same names
"""


class Scan():
    """
    Just a basic scan object to define common attributes

    It should not be called or initialised directly, this is
    just supposed to be called by the child class
    """
    def __init__(self):
        """
        Just initialise the attributes
        """
        self.parentFolder = None  # Root folder of the scan
        self.prefix = None  # prefix name for the simulations
        self.farprt = None  # It will be file with the farprt objects
        self.growthRateBlock = None  # It will be filled with the growthrate
        self.namelist = None  # It will be filled with the namelists
        self.profiles = None  # It will be filled with the profiles
        self.vars = None      # It will be filled with the variables used in the scan
        self.eigen = None     # To be filled with eigen solver results