from src import can_be_float, can_be_int, excel_inds
import numpy as np

def test_can_be_float():
    assert can_be_float('0')
    assert can_be_float('0.0')
    assert can_be_float('-1.0')
    assert can_be_float('-1')
    assert not can_be_float('')
    assert not can_be_float('not a float')

def test_can_be_int():
    assert can_be_int('0')
    assert can_be_int('-1')
    assert not can_be_int('s')

def test_excel_inds():
    assert excel_inds(np.array([0, 0])) == 'A1'
    assert excel_inds(np.array([3, 3])) == 'D4'
    assert excel_inds(np.array([25, 27])) == 'AB26'
    assert excel_inds(np.array([2, 26 ** 3])) == 'YZA3'
    assert excel_inds(np.array([4, 25])) == 'Z5'
    assert excel_inds(np.array([10, 26 ** 3 - 1])) == 'YYZ11'
