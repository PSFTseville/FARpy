"""
Auxiliary routines
"""
import numpy as np

__all__ = ['parse_bool', 'give_me_n_numbers', 'update_case_insensitive']

# ------------------------------------------------------------------------------
# --- Reading
# ------------------------------------------------------------------------------
def parse_bool(string):
    """
    parse fortran booleans ('.false.', '.true.')
    """
    if string.lower() == '.false.':
        b = False
    else:
        b = True
    return b

def parse_bool_Python_to_Fortran(boolean):
    """
    parse python to fortran booleans ('.false.', '.true.')
    """
    if boolean:
        b = '.true.'
    else:
        b = '.false.'
    return b


def give_me_n_numbers(fid, n, dtype=int):
    """
    Optain n numbers from an open file, evein if they are in different lines

    :param fid: pointer to an open file
    :param n: number of numbers to be read
    :param dtype: dtype to apply
    """
    numbers = np.zeros(n, dtype=dtype)
    got_numbers = 0
    while got_numbers != n:
        line = fid.readline()
        splits = line.split(',')
        for s in splits:
            if '*' not in s:
                try:
                    numbers[got_numbers] = dtype(s)
                    got_numbers += 1
                except ValueError:
                    pass
            else:
                second_split = s.split('*')
                nnumbers = int(second_split[0])
                numbers[got_numbers:(got_numbers+nnumbers)] =\
                    dtype(second_split[1]) * np.ones(nnumbers, dtype=dtype)
                got_numbers += nnumbers
    return numbers


# -----------------------------------------------------------------------------
# --- Dictionaries
# -----------------------------------------------------------------------------
def update_case_insensitive(a, b):
    """
    Update a dictionary avoiding problems due to case sensitivity

    Jose Rueda Rueda: jrrueda@us.es

    Note: This is a non-perfectly efficient workaround. Please do not use it
    routinely inside heavy loops. It will only change in a the fields contained
    in b, it will not create new fields in a

    Please, Pablo, do not kill me for this extremelly uneficient way of doing
    this

    :params a: Main dictionary
    :params b: Dictionary with the extra information to include in a
    """
    keys_a_lower = [key.lower() for key in a.keys()]
    keys_a = [key for key in a.keys()]
    keys_b_lower = [key.lower() for key in b.keys()]
    keys_b = [key for key in b.keys()]

    for k in keys_b_lower:
        if k in keys_a_lower:
            for i in range(len(keys_a_lower)):
                if keys_a_lower[i] == k:
                    keya = keys_a[i]
            for i in range(len(keys_b_lower)):
                if keys_b_lower[i] == k:
                    keyb = keys_b[i]
            a[keya] = b[keyb]


