import numpy as np
from src import IsNA, IsIncorrectDataType, MissingData, NumOutlier, WrongCategory, HasTypo, EmailChecker, _ALL_PREDS
from src import config_file_path

def pred_names_to_objs(names):
    """Turns a list of predicate names (as returned by config) into the rules to use.
    
    Args:
        names (list) : a list of string names to use. Technically can be any iterable

    Returns:
        preds (list) : a list of rules to use when finding dirty cells
        dup_lst (list) : a list of booleans, corresponding to whether the user
            wants to delete duplicate rows and columns
    """
    mapping = {IsNA : 'checkNA',
               IsIncorrectDataType : 'IsIncorrectDataType',
               MissingData : 'MissingData',
               NumOutlier : 'NumOutlier',
               WrongCategory : 'WrongCategory',
               HasTypo : 'typo',
               EmailChecker : 'EmailChecker'}
    name_set = set(names)
    res = []
    for pred in _ALL_PREDS:
        if mapping[pred] in name_set:
            res.append(pred)

    dupes = ['DuplicateRows', 'DuplicateColumns', 'RedundantColumns']
    dup_lst = [ el in name_set for el in dupes ]
    return res, dup_lst

def get_preds():
    """Returns the user's selected predicates.
    
    Args:
        None

    Returns:
        preds (list) : a list of rules to use when finding dirty cells
        dup_lst (list) : a list of booleans, corresponding to whether the user
            wants to delete duplicate rows and columns
    """
    with open(config_file_path(), 'r') as config:
        lines = config.readlines()
    for line in range(len(lines)):
        lines[line] = lines[line].replace('\n', '')
    return pred_names_to_objs(lines)
