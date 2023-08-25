import numpy as np
from src import Driver

def test_cleaner():
    driver = Driver('test_sheets/test_sheet_1.csv')
    assert driver.header == 1
    driver.find_dirty_cells()
    driver.clean_all_cells(num_dots = 0)
    for i in range(driver.dirty_inds.shape[0]):
        sugg = driver._clean_cell(driver.dirty_inds[i],
                                  driver.reasons[i])
        assert type(sugg) == str
        assert not driver.reasons[i].is_dirty(sugg, driver.cols[driver.dirty_inds[i, 1]])
        assert sugg == driver.clean_mat[tuple(driver.inds_with_head[i])]
    

