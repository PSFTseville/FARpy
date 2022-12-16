"""
This module read (and in the future writes) the input namelist

jose Rueda: jrrueda@us.es
"""
import os
import farpy._aux as faraux
__all__ = ['readNamelist', 'writeNamelist']


def readNamelist(file, header: int = 0):
    """
    Read the namelist

    @param file: name of the file to be read
    @param header: number of header lines to skip, (for the farprt file)

    @return out: dictionary containing all the namelist parameters
    """
    # Preallocate the dictionary:
    out = {
        'nstres': None,
        'numrun': None,
        'numruno': None,
        'numvac': None,
        'nonlin': None,
        'ngeneq': None,
        'eq_name': None,
        'maxstp': None,
        'dt0': None,
        'ldim': None,
        'leqdim': None,
        'jdim': None,
        'ext_prof': None,
        'ext_prof_name': None,
        'ext_prof_len': None,
        'iflr_on': None,
        'epflr_on': None,
        'ieldamp_on': None,
        'twofl_on': None,
        'alpha_on': None,
        'Trapped_on': None,
        'matrix_out': None,
        'm0dy': None,
        'mm': None,
        'nn': None,
        'mmeq': None,
        'nneq': None,
        'ipert': None,
        'widthi': None,
        'Auto_grid_on': None,
        'ni': None,
        'nis': None,
        'ne': None,
        'delta': None,
        'rc': None,
        'Edge_on': None,
        'edge_p': None,
        'gamma': None,
        's': None,
        'betath_factor': None,
        'ietaeq': None,
        'spe1': None,
        'bet0_f': None,
        'spe2': None,
        'bet0_falp': None,
        'omcy': None,
        'omcyb': None,
        'rbound': None,
        'omcyalp': None,
        'itime': None,
        'dpres': None,
        'stdifp': None,
        'stdifu': None,
        'stdifv': None,
        'stdifnf': None,
        'stdifvf': None,
        'stdifnfalp': None,
        'stdifvfalp': None,
        'LcA0': None,
        'LcA1': None,
        'LcA2': None,
        'LcA3': None,
        'LcA0alp': None,
        'LcA1alp': None,
        'LcA2alp': None,
        'LcA3alp': None,
        'omegar': None,
        'iflr': None,
        'r_epflr': None,
        'r_epflralp': None,
        'lplots': None,
        'nprint': None,
        'ndump': None,
        'DIIID_u': None,
        'EP_dens_on': None,
        'Adens': None,
        'Bdens': None,
        'Alpha_dens_on': None,
        'Adensalp': None,
        'Bdensalp': None,
        'EP_vel_on': None,
        'Alpha_vel_on': None,
        'q_prof_on': None,
        'Eq_vel_on': None,
        'Eq_velp_on': None,
        'Eq_Presseq_on': None,
        'Eq_Presstot_on': None,
        'deltaq': None,
        'deltaiota': None,
        'etascl': None,
        'eta0': None,
        'reta': None,
        'etalmb': None,
        'cnep': None,
        'ctep': None,
        'cnfp': None,
        'cvep': None,
        'cvfp': None,
        'cnfpalp': None,
        'cvfpalp': None,
        'eqvt': None,
        'eqvp': None
    }
    with open(file, 'r') as fid:
        for i in range(header):
            fid.readline()
        fid.readline()
        fid.readline()
        out['nstres'] = int(fid.readline())
        fid.readline()
        # Don't go to integer because 0 matters
        out['numrun'] = fid.readline().split('\n')[0].strip()
        fid.readline()
        out['numruno'] = fid.readline().split('\n')[0].strip()
        fid.readline()
        out['numvac'] = int(fid.readline())
        fid.readline()
        out['nonlin'] = int(fid.readline())
        fid.readline()
        out['ngeneq'] = int(fid.readline())
        fid.readline()
        out['eq_name'] = fid.readline().split('\n')[0].strip()
        fid.readline()
        out['maxstp'] = int(fid.readline())
        fid.readline()
        out['dt0'] = float(fid.readline())  # @Todo, float or int?
        fid.readline()
        out['ldim'] = int(fid.readline())
        fid.readline()
        out['leqdim'] = int(fid.readline())
        fid.readline()
        out['jdim'] = int(fid.readline())
        fid.readline()
        out['ext_prof'] = int(fid.readline())
        fid.readline()
        out['ext_prof_name'] = fid.readline().split('\n')[0].strip()
        fid.readline()
        out['ext_prof_len'] = int(fid.readline())
        fid.readline()
        out['iflr_on'] = int(fid.readline())
        fid.readline()
        out['epflr_on'] = int(fid.readline())
        fid.readline()
        out['ieldamp_on'] = int(fid.readline())
        fid.readline()
        out['twofl_on'] = int(fid.readline())
        fid.readline()
        out['alpha_on'] = int(fid.readline())
        fid.readline()
        out['Trapped_on'] = int(fid.readline())
        fid.readline()
        out['matrix_out'] = faraux.parse_bool(fid.readline())
        fid.readline()
        out['m0dy'] = int(fid.readline())
        fid.readline()
        fid.readline()
        fid.readline()
        fid.readline()
        out['mm'] = faraux.give_me_n_numbers(fid, out['ldim'], dtype=int)
        fid.readline()
        out['nn'] = faraux.give_me_n_numbers(fid, out['ldim'], dtype=int)
        fid.readline()
        out['mmeq'] = faraux.give_me_n_numbers(fid, out['leqdim'], dtype=int)
        fid.readline()
        out['nneq'] = faraux.give_me_n_numbers(fid, out['leqdim'], dtype=int)
        fid.readline()
        fid.readline()
        out['ipert'] = int(fid.readline())
        fid.readline()
        out['widthi'] = float(fid.readline())
        fid.readline()
        out['Auto_grid_on'] = int(fid.readline())
        fid.readline()
        out['ni'] = int(fid.readline())
        fid.readline()
        out['nis'] = int(fid.readline())
        fid.readline()
        out['ne'] = int(fid.readline())
        fid.readline()
        out['delta'] = float(fid.readline())
        fid.readline()
        out['rc'] = float(fid.readline())
        fid.readline()
        out['Edge_on'] = int(fid.readline())
        fid.readline()
        out['edge_p'] = int(fid.readline())
        fid.readline()
        fid.readline()
        out['gamma'] = int(fid.readline())
        fid.readline()
        out['s'] = float(fid.readline())
        fid.readline()
        out['betath_factor'] = int(fid.readline())
        fid.readline()
        out['ietaeq'] = int(fid.readline())
        fid.readline()
        out['spe1'] = int(fid.readline())
        fid.readline()
        out['bet0_f'] = float(fid.readline())
        fid.readline()
        out['spe2'] = int(fid.readline())
        fid.readline()
        out['bet0_falp'] = float(fid.readline())
        fid.readline()
        out['omcy'] = float(fid.readline())
        fid.readline()
        out['omcyb'] = float(fid.readline())
        fid.readline()
        out['rbound'] = float(fid.readline())
        fid.readline()
        out['omcyalp'] = float(fid.readline())
        fid.readline()
        out['itime'] = int(fid.readline())
        fid.readline()
        out['dpres'] = float(fid.readline())
        #  ---------------------------   Diffusivity block
        fid.readline()
        fid.readline()
        out['stdifp'] = int(fid.readline())
        fid.readline()
        out['stdifu'] = int(fid.readline())
        fid.readline()
        out['stdifv'] = int(fid.readline())
        fid.readline()
        out['stdifnf'] = int(fid.readline())
        fid.readline()
        out['stdifvf'] = int(fid.readline())
        fid.readline()
        out['stdifnfalp'] = int(fid.readline())
        fid.readline()
        out['stdifvfalp'] = int(fid.readline())
        #  ---------------------------   Landau block
        fid.readline()
        fid.readline()
        out['LcA0'] = float(fid.readline())
        fid.readline()
        out['LcA1'] = float(fid.readline())
        fid.readline()
        out['LcA2'] = float(fid.readline())
        fid.readline()
        out['LcA3'] = float(fid.readline())
        fid.readline()
        out['LcA0alp'] = float(fid.readline())
        fid.readline()
        out['LcA1alp'] = float(fid.readline())
        fid.readline()
        out['LcA2alp'] = float(fid.readline())
        fid.readline()
        out['LcA3alp'] = float(fid.readline())
        #  ---------------------------   Damping block
        fid.readline()
        fid.readline()
        out['omegar'] = float(fid.readline())
        fid.readline()
        out['iflr'] = float(fid.readline())
        fid.readline()
        out['r_epflr'] = float(fid.readline())
        fid.readline()
        out['r_epflralp'] = float(fid.readline())
        fid.readline()
        fid.readline()
        out['lplots'] = int(fid.readline())
        fid.readline()
        out['nprint'] = int(fid.readline())
        fid.readline()
        out['ndump'] = int(fid.readline())
        fid.readline()
        fid.readline()
        out['DIIID_u'] = int(fid.readline())
        fid.readline()
        fid.readline()
        fid.readline()
        out['EP_dens_on'] = int(fid.readline())
        fid.readline()
        out['Adens'] = int(fid.readline())
        fid.readline()
        out['Bdens'] = float(fid.readline())
        fid.readline()
        out['Alpha_dens_on'] = int(fid.readline())
        fid.readline()
        out['Adensalp'] = int(fid.readline())
        fid.readline()
        out['Bdensalp'] = float(fid.readline())
        fid.readline()
        out['EP_vel_on'] = int(fid.readline())
        fid.readline()
        out['Alpha_vel_on'] = int(fid.readline())
        fid.readline()
        out['q_prof_on'] = int(fid.readline())
        fid.readline()
        out['Eq_vel_on'] = int(fid.readline())
        fid.readline()
        out['Eq_velp_on'] = int(fid.readline())
        fid.readline()
        out['Eq_Presseq_on'] = int(fid.readline())
        fid.readline()
        out['Eq_Presstot_on'] = int(fid.readline())
        fid.readline()
        out['deltaq'] = int(fid.readline())
        fid.readline()
        out['deltaiota'] = int(fid.readline())
        fid.readline()
        out['etascl'] = int(fid.readline())
        fid.readline()
        out['eta0'] = int(fid.readline())
        fid.readline()
        out['reta'] = float(fid.readline())
        fid.readline()
        out['etalmb'] = float(fid.readline())
        fid.readline()
        out['cnep'] = faraux.give_me_n_numbers(fid, 11, float)
        fid.readline()
        out['ctep'] = faraux.give_me_n_numbers(fid, 11, float)
        fid.readline()
        out['cnfp'] = faraux.give_me_n_numbers(fid, 11, float)
        fid.readline()
        out['cvep'] = faraux.give_me_n_numbers(fid, 11, float)
        fid.readline()
        out['cvfp'] = faraux.give_me_n_numbers(fid, 11, float)
        fid.readline()
        out['cnfpalp'] = faraux.give_me_n_numbers(fid, 11, float)
        fid.readline()
        out['cvfpalp'] = faraux.give_me_n_numbers(fid, 11, float)
        fid.readline()
        out['eqvt'] = faraux.give_me_n_numbers(fid, 11, float)
        fid.readline()
        out['eqvp'] = faraux.give_me_n_numbers(fid, 11, float)
    return out



def writeNamelist(filename, namelist, overwrite: bool = True):
    """
    Write the namelist

    :param file: path to the namelist file to be written
    :param namelist: dictionary containing all namelist fields
    :param overwrite: boolena flag to decide wether to overwrite
        the current namelist or not

    :return: Nothing
    """
    if os.path.isfile(filename) and not overwrite:
        raise Exception('Namelist file exist')
    with open(filename, 'w') as fid:
        fid.writelines('------MAIN INPUT VALIABLES. Created with FARpy------\n')
        fid.writelines('!!!!!!!!!!! nstres: if 0 new run, if 1 the run is a continuation\n')
        fid.writelines('%i \n' % namelist['nstres'])
        fid.writelines('!!!!!!!!!!! numrun: run number\n')
        fid.writelines('%s \n' % namelist['numrun'])
        fid.writelines('!!!!!!!!!!! numruno: name of the previous run output\n')
        fid.writelines('%s \n' % namelist['numruno'])
        fid.writelines('!!!!!!!!!!! numvac: run number index\n')
        fid.writelines('%i \n' % namelist['numvac'])
        fid.writelines('!!!!!!!!!!! nonlin: linear run if 0, non linear run if 1 (no available yet)\n')
        fid.writelines('%i \n' % namelist['nonlin'])
        fid.writelines('!!!!!!!!!!! ngeneq: equilibrium input (only VMEC available now)\n')
        fid.writelines('%i \n' % namelist['ngeneq'])
        fid.writelines('!!!!!!!!!!! eq_name: equilibrium name\n')
        fid.writelines('%s \n' % namelist['eq_name'])
        fid.writelines('!!!!!!!!!!! maxstp: simulation time steps\n')
        fid.writelines('%i \n' % namelist['maxstp'])
        fid.writelines('!!!!!!!!!!! dt0: simulation time step\n')
        fid.writelines('%i \n' % namelist['dt0'])
        fid.writelines('!!!!!!!!!!! ldim: total number of poloidal modes (equilibrium + dynamic)\n')
        fid.writelines('%i \n' % namelist['ldim'])
        fid.writelines('!!!!!!!!!!! leqdim: equilibrium poloidal modes\n')
        fid.writelines('%i \n' % namelist['leqdim'])
        fid.writelines('!!!!!!!!!!! jdim: number of radial points\n')
        fid.writelines('%i \n' % namelist['jdim'])
        fid.writelines('!!!!!!!!!!! ext_prof: include external profiles if 1\n')
        fid.writelines('%i \n' % namelist['ext_prof'])
        fid.writelines('!!!!!!!!!!! ext_prof_name: external profile file name\n')
        fid.writelines('%s \n' % namelist['ext_prof_name'])
        fid.writelines('!!!!!!!!!!! ext_prof_len: number of lines in the external profile\n')
        fid.writelines('%i \n' % namelist['ext_prof_len'])
        fid.writelines('!!!!!!!!!!! iflr_on: activate thermal ion FLR damping effects if 1\n')
        fid.writelines('%i \n' % namelist['iflr_on'])
        fid.writelines('!!!!!!!!!!! epflr_on: activate fast particle FLR damping effects if 1\n')
        fid.writelines('%i \n' % namelist['epflr_on'])
        fid.writelines('!!!!!!!!!!! ieldamp_on: activate electron-ion Landau damping effect if 1\n')
        fid.writelines('%i \n' % namelist['ieldamp_on'])
        fid.writelines('!!!!!!!!!!! twofl_on: activate two fluid effects if 1\n')
        fid.writelines('%i \n' % namelist['twofl_on'])
        fid.writelines('!!!!!!!!!!! alpha_on: activate a 2nd fast particle species if 1\n')
        fid.writelines('%i \n' % namelist['alpha_on'])
        fid.writelines('!!!!!!!!!!! Trapped_on: activate correction for trapped 1st fast particle species if 1\n')
        fid.writelines('%i \n' % namelist['Trapped_on'])
        fid.writelines('!!!!!!!!!!! matrix_out: activate eigensolver output\n')
        fid.writelines('%s \n' % faraux.parse_bool_Python_to_Fortran(namelist['matrix_out']))
        fid.writelines('!!!!!!!!!!! m0dy: equilibrium modes as dynamic\n')
        fid.writelines('%i \n' % namelist['m0dy'])
        fid.writelines('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')
        fid.writelines('==================================/ MODEL PARAMETERS \===================================\n')
        fid.writelines('!!!!!!!!!!!!!!!!!!!!!!!!!!!!! MODES INCLUDED IN THE MODEL !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')
        fid.writelines('!!!!!!!!!!! mm: poloidal dynamic and equilibrium modes\n')
        s = ''
        for n in namelist['mm']:
            s += str(n) + ','
        fid.writelines('%s \n' % s)
        fid.writelines('!!!!!!!!!!! nn: toroidal dynamic and equilibrium modes\n')
        s = ''
        for n in namelist['nn']:
            s += str(n) + ','
        fid.writelines('%s \n' % s)
        fid.writelines('!!!!!!!!!!! mmeq: poloidal equilibrium modes\n')
        s = ''
        for n in namelist['mmeq']:
            s += str(n) + ','
        fid.writelines('%s \n' % s)
        fid.writelines('!!!!!!!!!!! nneq: toroidal equilibrium modes\n')
        s = ''
        for n in namelist['nneq']:
            s += str(n) + ','
        fid.writelines('%s \n' % s)
        fid.writelines('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! PERTURBATION !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')
        fid.writelines('!!!!!!!!!!! ipert: different options to drive a perturbation in the equilibria\n')
        fid.writelines('%i \n' % namelist['ipert'])
        fid.writelines('!!!!!!!!!!! widthi: size of the perturbation\n')
        fid.writelines('%e \n' % namelist['widthi'])
        fid.writelines('!!!!!!!!!!! Auto_grid_on: auto grid spacing option\n')
        fid.writelines('%i \n' % namelist['Auto_grid_on'])
        fid.writelines('!!!!!!!!!!! ni: number of points interior to the island\n')
        fid.writelines('%i \n' % namelist['ni'])
        fid.writelines('!!!!!!!!!!! nis: number of points in the island\n')
        fid.writelines('%i \n' % namelist['nis'])
        fid.writelines('!!!!!!!!!!! ne: number of points exterior to the island\n')
        fid.writelines('%i \n' % namelist['ne'])
        fid.writelines('!!!!!!!!!!! delta: normalized width of the uniform fine grid (island)\n')
        fid.writelines('%f \n' % namelist['delta'])
        fid.writelines('!!!!!!!!!!! rc: center of the fine grid (island) along the normalized minor radius\n')
        fid.writelines('%f \n' % namelist['rc'])
        fid.writelines('!!!!!!!!!!! Edge_on: activates the VMEC data extrapolation\n')
        fid.writelines('%i \n' % namelist['Edge_on'])
        fid.writelines('!!!!!!!!!!! edge_p: grid point from where the VMEC data is extrapolated\n')
        fid.writelines('%i \n' % namelist['edge_p'])
        fid.writelines('!!!!!!!!!!!!!!!!!!!!!!!!!!!!! PLASMA PARAMETERS !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')
        fid.writelines('!!!!!!!!!!! gamma: adiabatic index\n')
        fid.writelines('%i \n' % namelist['gamma'])
        fid.writelines('!!!!!!!!!!! s: magnetic Lundquist number\n')
        fid.writelines('%e \n' % namelist['s'])
        fid.writelines('!!!!!!!!!!! betath_factor: thermal beta factor\n')
        fid.writelines('%i \n' % namelist['betath_factor'])
        fid.writelines('!!!!!!!!!!! ietaeq: resistivity profile type (if 1 the electron temperature is used)\n')
        fid.writelines('%i \n' % namelist['ietaeq'])
        fid.writelines('!!!!!!!!!!! spe1: species first EP population\n')
        fid.writelines('%i \n' % namelist['spe1'])
        fid.writelines('!!!!!!!!!!! bet0_f: fast particle beta\n')
        fid.writelines('%f \n' % namelist['bet0_f'])
        fid.writelines('!!!!!!!!!!! spe2: species second EP population\n')
        fid.writelines('%i \n' % namelist['spe2'])
        fid.writelines('!!!!!!!!!!! bet0_falp: 2nd species fast particle beta\n')
        fid.writelines('%i \n' % namelist['bet0_falp'])
        fid.writelines('!!!!!!!!!!! omcy: normalized fast particle cyclotron frequency\n')
        fid.writelines('%f \n' % namelist['omcy'])
        fid.writelines('!!!!!!!!!!! omcyb: normalized fast particle cyclotron frequency\n')
        fid.writelines('%f \n' % namelist['omcyb'])
        fid.writelines('!!!!!!!!!!! rbound: normalized helicaly trapped bound length\n')
        fid.writelines('%f \n' % namelist['rbound'])
        fid.writelines('!!!!!!!!!!! omcyalp: normalized 2nd species fast particle cyclotron frequency\n')
        fid.writelines('%f \n' % namelist['omcyalp'])
        fid.writelines('!!!!!!!!!!! itime: time normalization option\n')
        fid.writelines('%i \n' % namelist['itime'])
        fid.writelines('!!!!!!!!!!! dpres: electron pressure normalized to the total pressure (two fluid effects)\n')
        fid.writelines('%f \n' % namelist['dpres'])
        fid.writelines('!!!!!!!!!!!!!!!!!!!!!!!!!!!!! DIFFUSIVITIES !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')
        fid.writelines('!!!!!!!!!!! stdifp: thermal pressure eq. diffusivity\n')
        fid.writelines('%i \n' % namelist['stdifp'])
        fid.writelines('!!!!!!!!!!! stdifu: vorticity eq. diffusivity\n')
        fid.writelines('%i \n' % namelist['stdifu'])
        fid.writelines('!!!!!!!!!!! stdifv: thermal particle parallel velocity eq. diffusivity\n')
        fid.writelines('%i \n' % namelist['stdifv'])
        fid.writelines('!!!!!!!!!!! stdifnf: fast particle density eq. diffusivity\n')
        fid.writelines('%i \n' % namelist['stdifnf'])
        fid.writelines('!!!!!!!!!!! stdifvf: fast particle parallel velocity eq. diffusivity\n')
        fid.writelines('%i \n' % namelist['stdifvf'])
        fid.writelines('!!!!!!!!!!! stdifnfalp: fast particle parallel velocity eq. diffusivity\n')
        fid.writelines('%i \n' % namelist['stdifnfalp'])
        fid.writelines('!!!!!!!!!!! stdifvfalp: fast particle parallel velocity eq. diffusivity\n')
        fid.writelines('%i \n' % namelist['stdifvfalp'])
        fid.writelines('!!!!!!!!!!!!!!!!!!!!!!!!!!!!! LANDAU CLOSURE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')
        fid.writelines('!!!!!!!!!!! LcA0: Landau closure 1\n')
        fid.writelines('%f \n' % namelist['LcA0'])
        fid.writelines('!!!!!!!!!!! LcA1: Landau closure 2\n')
        fid.writelines('%f \n' % namelist['LcA1'])
        fid.writelines('!!!!!!!!!!! LcA2: correction to the fast particle beta\n')
        fid.writelines('%f \n' % namelist['LcA2'])
        fid.writelines('!!!!!!!!!!! LcA3: correction to the ratio between fast particle thermal velocity and Alfven velocity\n')
        fid.writelines('%f \n' % namelist['LcA3'])
        fid.writelines('!!!!!!!!!!! LcA0alp: Landau closure 1 2nd species\n')
        fid.writelines('%f \n' % namelist['LcA0alp'])
        fid.writelines('!!!!!!!!!!! LcA1alp: Landau closure 2 2nd species\n')
        fid.writelines('%f \n' % namelist['LcA1alp'])
        fid.writelines('!!!!!!!!!!! LcA2alp: correction to the 2nd species fast particle beta\n')
        fid.writelines('%f \n' % namelist['LcA2alp'])
        fid.writelines('!!!!!!!!!!! LcA3alp: correction to the ratio between fast particle thermal velocity and Alfven velocity 2nd species\n')
        fid.writelines('%f \n' % namelist['LcA3alp'])
        fid.writelines('!!!!!!!!!!!!!!!!!!!!!!!!!!!!! DAMPINGS !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')
        fid.writelines('!!!!!!!!!!! omegar: eigenmode frequency without damping effects\n')
        fid.writelines('%f \n' % namelist['omegar'])
        fid.writelines('!!!!!!!!!!! iflr: thermal ions larmor radius normalized to the minor radius\n')
        fid.writelines('%f \n' % namelist['iflr'])
        fid.writelines('!!!!!!!!!!! r_epflr: energetic particle larmor radius normalized to the minor radius\n')
        fid.writelines('%f \n' % namelist['r_epflr'])
        fid.writelines('!!!!!!!!!!! r_epflralp: 2nd species energetic particle larmor radius normalized to the minor radius\n')
        fid.writelines('%f \n' % namelist['r_epflralp'])
        fid.writelines('!!!!!!!!!!!!!!!!!!!!!!!!!!!!! OUTPUT !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')
        fid.writelines('!!!!!!!!!!! lplots: number of eigenfunction modes in the output files\n')
        fid.writelines('%i \n' % namelist['lplots'])
        fid.writelines('!!!!!!!!!!! nprint: number of step for an output in farprt file\n')
        fid.writelines('%i \n' % namelist['nprint'])
        fid.writelines('!!!!!!!!!!! ndump: number of step for an output\n')
        fid.writelines('%i \n' % namelist['ndump'])
        fid.writelines('!!!!!!!!!!!!!!!!!!!!!!!!!!!!! OTHER PARAMETERS !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')
        fid.writelines('!!!!!!!!!!! DIIID_u: turn on to use the same units than TRANSP output in the external profiles (cm not m)\n')
        fid.writelines('%i \n' % namelist['DIIID_u'])
        fid.writelines('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')
        fid.writelines('================================/ SELF PROFILES PARAMETERS \============================\n')
        fid.writelines('!!!!!!!!!!! EP_dens_on: user defined fast particle density profile (if 1)\n')
        fid.writelines('%i \n' % namelist['EP_dens_on'])
        fid.writelines('!!!!!!!!!!! Adens: fast particle density profile flatness\n')
        fid.writelines('%i \n' % namelist['Adens'])
        fid.writelines('!!!!!!!!!!! Bdens: location of the fast particle density profile gradient\n')
        fid.writelines('%f \n' % namelist['Bdens'])
        fid.writelines('!!!!!!!!!!! Alpha_dens_on: user defined 2nd species fast particle density profile (if 1)\n')
        fid.writelines('%i \n' % namelist['Alpha_dens_on'])
        fid.writelines('!!!!!!!!!!! Adensalp: 2nd species fast particle density profile flatness\n')
        fid.writelines('%i \n' % namelist['Adensalp'])
        fid.writelines('!!!!!!!!!!! Bdensalp: location of the 2nd species fast particle density profile gradient\n')
        fid.writelines('%f \n' % namelist['Bdensalp'])
        fid.writelines('!!!!!!!!!!! EP_vel_on: user defined fast particle vth/vA0 profile (if 1)\n')
        fid.writelines('%i \n' % namelist['EP_vel_on'])
        fid.writelines('!!!!!!!!!!! Alpha_vel_on: user defined 2nd species fast particle vth/vA0 profile (if 1)\n')
        fid.writelines('%i \n' % namelist['Alpha_vel_on'])
        fid.writelines('!!!!!!!!!!! q_prof_on: the safety factor profile of the external profile is used (is 1)\n')
        fid.writelines('%i \n' % namelist['q_prof_on'])
        fid.writelines('!!!!!!!!!!! Eq_vel_on: the safety factor profile of the external profile is used (is 1)\n')
        fid.writelines('%i \n' % namelist['Eq_vel_on'])
        fid.writelines('!!!!!!!!!!! Eq_velp_on: the safety factor profile of the external profile is used (is 1)\n')
        fid.writelines('%i \n' % namelist['Eq_velp_on'])
        fid.writelines('!!!!!!!!!!! Eq_Presseq_on: the safety factor profile of the external profile is used (is 1)\n')
        fid.writelines('%i \n' % namelist['Eq_Presseq_on'])
        fid.writelines('!!!!!!!!!!! Eq_Presstot_on: the equilibrium + fast particle pressure profiles of the external profile is used (is 1)\n')
        fid.writelines('%i \n' % namelist['Eq_Presstot_on'])
        fid.writelines('!!!!!!!!!!! deltaq: safety factor displacement (only tokamak eq.)\n')
        fid.writelines('%i \n' % namelist['deltaq'])
        fid.writelines('!!!!!!!!!!! deltaiota: iota displacement (only stellarator eq.)\n')
        fid.writelines('%i \n' % namelist['deltaiota'])
        fid.writelines('!!!!!!!!!!! etascl: user defined constant resistivity (if ietaeq=2)\n')
        fid.writelines('%i \n' % namelist['etascl'])
        fid.writelines('!!!!!!!!!!! eta0: user defined resistivity profile (if ietaeq=3)\n')
        fid.writelines('%i \n' % namelist['eta0'])
        fid.writelines('!!!!!!!!!!! reta: user defined resistivity profile (if ietaeq=3)\n')
        fid.writelines('%f \n' % namelist['reta'])
        fid.writelines('!!!!!!!!!!! etalmb: user defined resistivity profile (if ietaeq=3)\n')
        fid.writelines('%f \n' % namelist['etalmb'])
        fid.writelines('!!!!!!!!!!! cnep: user defined thermal plasma density profile\n')
        s = ''
        for n in namelist['cnep']:
            s += str(n) + ','
        fid.writelines('%s \n' % s)
        fid.writelines('!!!!!!!!!!! ctep: user defined thermal electron plasma temperature profile\n')
        s = ''
        for n in namelist['ctep']:
            s += str(n) + ','
        fid.writelines('%s \n' % s)
        fid.writelines('!!!!!!!!!!! cnfp: user defined energetic particles density profile\n')
        s = ''
        for n in namelist['cnfp']:
            s += str(n) + ','
        fid.writelines('%s \n' % s)
        fid.writelines('!!!!!!!!!!! cvep: user defined thermal ions parallel velocity profile (only for thermal ion FLR effects)\n')
        s = ''
        for n in namelist['cvep']:
            s += str(n) + ','
        fid.writelines('%s \n' % s)
        fid.writelines('!!!!!!!!!!! cvfp: user defined energetic particles parallel velocity profile\n')
        s = ''
        for n in namelist['cvfp']:
            s += str(n) + ','
        fid.writelines('%s \n' % s)
        fid.writelines('!!!!!!!!!!! cnfpalp: user defined 2nd species energetic particles density profile\n')
        s = ''
        for n in namelist['cnfpalp']:
            s += str(n) + ','
        fid.writelines('%s \n' % s)
        fid.writelines('!!!!!!!!!!! cvfpalp: user defined 2nd species energetic particles parallel velocity profile\n')
        s = ''
        for n in namelist['cvfpalp']:
            s += str(n) + ','
        fid.writelines('%s \n' % s)
        fid.writelines('!!!!!!!!!!! eqvt: user defined equilibrium thermal toroidal velocity profile\n')
        s = ''
        for n in namelist['eqvt']:
            s += str(n) + ','
        fid.writelines('%s \n' % s)
        fid.writelines('!!!!!!!!!!! eqvp: user defined equilibrium thermal poloidal velocity profile\n')
        s = ''
        for n in namelist['eqvp']:
            s += str(n) + ','
        fid.writelines('%s \n' % s)
        fid.writelines('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    return


def plotNamelistProfile(namelist, name, ax=None):
    """
    Plot a profile using the parameters in the namelist
    :param namelist:
    :param name:
    :param ax:
    :return:
    """
