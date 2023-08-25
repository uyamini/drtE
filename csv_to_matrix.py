import pandas as pd
import numpy as np
from .utilities import can_be_float
import csv

def csvToMatrix(csv_name):
    """Takes the name of the csv file and returns the 2D matrix version of the file.

    Args:
        csv_name (str) : the name of the csv file
        
    Returns:
        result_mat (2d array) : Matrix version of the csv file
    """
    with open(csv_name, 'r') as sheet:
        delimiter = csv.Sniffer().sniff(sheet.read()).delimiter
    df = pd.read_csv(csv_name, dtype = str, delimiter = delimiter, na_filter = False)
    res = np.empty((df.shape[0] + 1, df.shape[1]), dtype = 'U128')
    res[0] = df.columns
    res[1:] = df.to_numpy(dtype = 'U128')
    return res

def has_header(mat):
    """Determines whether the spreadsheet has a header.
    
    Args:
        mat (np.array) : a 2D array of strings

    Returns:
        header (int) : how many rows to skip initially
    """
    all_strs = lambda i: not any(map(can_be_float, mat[i]))
    return int(all_strs(0) and 
               not all(map(all_strs, range(1, mat.shape[0]))))
