"""
This module read (and in the future writes) the input namelist

jose Rueda: jrrueda@us.es
"""
import farpy._aux as faraux
__all__ = ['readNamelist']


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
        'bet0_f': None,
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
        out['bet0_f'] = float(fid.readline())
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
