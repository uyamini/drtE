import numpy as np

def can_be_float(s):
    """Returns whether s can be cast as a float without exception.
    
    Args:
        s (str) : a string to check
        
    Returns:
        is_float (bool) : whether the string can be cast as a float
    """
    try:
        float(s)
        return True
    except ValueError:
        return False

def is_float_char(c):
    """Returns whether the given character could be in a valid float string
    
    Args:
        c (str) : a single character
    
    Returns:
        could_be (bool) : whether the character could be in a valid float
    """
    return c.isnumeric() or c == '.' or c == '-'

def can_be_int(s):
    """Returns whether s can be cast as a int without exception.
    
    Args:
        s (str) : a string to check
        
    Returns:
        is_int (bool) : whether the string can be cast as a int
    """
    try:
        int(s)
        return True
    except ValueError:
        return False

def float_is_int(f):
    """Returns whether f is a close enough to the nearest integer.
    
    Args:
        f (float) : the float to look at 

    Returns:
        is_int (bool) : whether the float is basically an integer
    """
    return np.isclose(f, round(f))

def arr_to_set(arr):
    """Turns an array into a set.
    
    Args:
        arr (np.array) : the 2D array to convert

    Returns:
        s (set) : a set of tuples with the same elements as arr.
    """
    return set(map(tuple, arr))

def excel_inds(inds):
    """Converts integer indices to an Excel cell.
    
    Args:
        inds (np.array) : a [y, x] pair
    
    Returns:
        letter_inds (str) : a string that can be used to reference an .xslx cell
    """
    row = inds[0] + 1
    col_chars = []
    col_n = inds[1] + 1
    while col_n > 0:
        col_n, remainder = divmod(col_n - 1, 26)
        col_chars.append(chr(65 + remainder))
    col = ''.join(reversed(col_chars))
    return col + str(row)

def excel_range(inds):
    """Returns a range as used in Excel from one cell to the same cell."""
    cell_str = excel_inds(inds)
    return f'{cell_str}:{cell_str}'
