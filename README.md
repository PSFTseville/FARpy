# FARpy
Read and Plot FAR3D results.

Support to prepare FAR3D inputs is still not given nor planned, but could be added in the future uppon user request

More information of the FAR3D code can be found in the following refereces: INCLUDE HERE THE ARTICLES

## Installation and documentation
### Prerequisites. Python 3.7 or higher
Needed packages. Only listed 'non-standard' packages. See below, there is a script to install them.

#### Essentials
The module will not work without them:
- f90nml: To read FORTRAN namelist in an easy way `pip install f90nml`. This is the suite standard to read and write namelists!!!
- xarray: This will provide the basic format to save the data

#### Optional
Still none

### Cloning the library and installing
In order to clone the library just open a terminal in your home directory and type:
```bash
 git clone https://github.com/JoseRuedaRueda/FARpy.git FARpy
```
To install all non-standard (not machine dependent) packages, you can give a try the script: `first_run.py`. It will work in personal computers and *standard installations* although things can go wrong if your system has some particular rights limitations and you are not allowed to change them using =pip install= (for example if you are in some cluster). In these cases, you should use a virtual environment:

1. Install virtualenv: `pip install virtualenv`
2. Create your virtual environment (let us call it farpy): `virtualenv -p python3 --system-site-packages farpy`
3. Activate your virtual environment (remember to do this everytime you are using the library or add it to your login script): `source farpy/bin/activate`
4. Force install the compatible versions using `pip install modulename==X.X.X`. A list of compatible versions is listed here:
```python
scipy==1.7.0
scikit-image==0.16.2
pyfftw==0.12.0
pandas==1.3.1
```
### Getting started
**Importing the suite**

*Short story*: Go to the root directory of FARpy, in your python terminal, run: `import farpy`

*Long story*: In order to import the Library as `import farpy as MyAwesomeName`, you need to set in your environment the different paths to the sub-modules. To do this, you just need to run the `file paths.py`. For example, just type in a python terminal `run paths_suite` (being on the main FARpy directory). After running it, you should be able to import the suite from everywhere in your computer. However, if your working directory is the root directory of the Suite, there is no need of running this line, you can just execute directly `import farpy as MyAwesomeName` and enjoy (as the function `paths.py` is called in the Sutie `__init__.py`)

**Using it**

Please see the examples in the Examples folder of the Suite, it contains the basic lines to execute the suite for each of they main capabilities. Please note than the examples does not contain all possibles ways of doing things iside the code, you will need to dig arround a bit if you need something too specific.

### Paths
There are three files containing the paths and routes for the suite:
- `paths.py`: Located in the main directory of the suite. This one just contain the routes pointing to the python packages/files needed by the suite. It says to python where to find what it needs. If you need to add something due to the peculiarities of your system, please do it locally in your bash file or open a issue in gitlab, do not modify this file.
- `_Paths.py`: Located inside the Lib folder, there they are all the paths pointing towards the different codes (FILDSIM, INPASIM etc) and the results/strike maps directories. Again do not modify this file just to put your custom paths, please.
- `MyData/Paths.txt`: It could happen that you have FAR3D or whatever installed in a route which is not *the official*. Inside this file, you can set all these paths. The file should be created when you run the script `first_run.py`; although you can always copy it from the `Data/MyDataTemplates folder`.

**Important:** The suite must be installed in your home directory. The reason for this is that I found no other way for the Suite to localise this custom directory. Please, if you find a woraround for this, send me an email and we will be happy to implement it.

### Documentation
- All objects and methods are documented such that the user can understand what is going on
- As everything has doc-strings, you can always write in the python terminal <fname>? and you will get all the description of the <fname> method or object
- The routines in the Example folder are intended to illustrate the use of the different tools in the suite. Please, if you want to play with them, make your own copy on 'MyRoutines', modifying the examples can cause merge conflicts in the future
- If you have installed Doxygen you can generate the documentation in html and LaTex format just opening a terminal in the Suite root directory and typing  `doxygen Doxyfile`. Once the documentation is generated, you can open the index with the following command `xdg-open doc/index.html`. For a (old and outdated) Doxygen generated documentation, see: <https://hdvirtual.us.es/discovirt/index.php/s/FBjZ9FPfjjwMDS2> download the content and open the index.html file, inside the html folder.

## Data export
All data exported and saved by this tool is done with netCDF. Platform independendent and binary format. There is no plans to add aditional formats such as ASCII text.

If the user is *alergic* to the use of programing languages in order to read the netCDF, this NASA program could be usefull: https://www.giss.nasa.gov/tools/panoply/download/ It allows you to open and plot the variables in the netCDF file

## Active Development
### Version control
Each release will be denoted by 3 numbers: a.b.c meaning:
- c: bug fixed and improved comments and documentation. Some new capabilities could be added (see changelog). The higher the number, the better.
- b: Significant changes, versions a.b1.c1 and a.b2.c2, should run perfectly with the same inputs.  But some internal routines may have changed, so if you have your own scripts using them 'outside the main loop' something can go wrong for you. The higher b, the more extra capabilities you have
- a: indicate major changes in the code, versions with different 'a' may be not compatible, not recommended update to a higher 'a' version close to a conference

### Branches
- master: Stable branch, things should work, may be a delay including new features
- dev-branch: developers branch, may have some small bugs or not fully developed features. Include the latest features, not recommended for general public
- 'tmp'-branch: linked to specific commits to include new features. Do not use these branches except you are the developer in charge of the new feature. Unicorns can appear

### Note for developers
- Before changing anything in a module open a issue in GitLab to start a discussion
- Indentation must be done via 4 spaces!
- PEP 8 guide is recommended, if some piece of code want to be merged without this standard, the maintainers could modify your code to adapt it to this standard (or completely deny your merge request)
  + maximum 80 character-long lines
  + space separation between operators, i.e., =a + b=
  + no blanks at the end of the lines
  + PEP8 in atom: <https://atom.io/packages/linter-python-pep8>
  + PEP8 in spyder: Tools > Preferences > Completion and linting > Code style and activating the option called #Enable code style linting#

### Issues and new implementations
If you are going to report a bug (or issue) please follow the template in <https://gitlab.mpcdf.mpg.de/ruejo/scintsuite/-/issues/71>

If a new implementation is required, open the appropriate issue in the GIT and link it to the milestone it corresponds (if possible). The following tags are available:

- Documentation: improve the documentation of a given section.
- Feature request: request to implement a new feature in the code.
- Minor mod.: request to implement minor modifications in the code.
- Enhancement: modify the implementation of a given feature to improve the efficiency or make easier some processing.
- Discussion: a forum to discuss ideas of implementation.
- Bug: minor error found in the code. To be corrected at the earliest convenience.
- Major error: an important error has to be solved in the code as soon as possible.
- Minor priority: Label for maintainer, indicates that the request has low priority in the ToDo list
