from src import IsIncorrectDataType, NumOutlier, IsNA, WrongCategory, HasTypo, MissingData
import numpy as np
from src import Driver, clean_and_save
import os

def test_dirty_cells():
    driver = Driver('test_sheets/test_sheet_1.csv', dupes = [False, False, False])
    driver.find_dirty_cells()
    assert IsNA() != HasTypo()
    assert IsNA() == IsNA()

    right_inds = np.array([[1, 1],
                           [1, 2],
                           [1, 7],
                           [2, 4],
                           [2, 6],
                           [2, 8],
                           [5, 3],
                           [6, 3],
                           [6, 6],
                           [8, 3],
                           [8, 6]])
    right_reasons = [MissingData,
                     NumOutlier,
                     NumOutlier,
                     HasTypo,
                     IsIncorrectDataType,
                     WrongCategory,
                     IsNA,
                     MissingData,
                     NumOutlier,
                     IsNA,
                     NumOutlier]
    right_reasons = [ r() for r in right_reasons ]

    assert right_inds.shape[0] == len(right_reasons)
    assert np.all(driver.inds_with_head == right_inds), (driver.inds_with_head.shape[0], right_inds.shape[0])
    for i in range(len(right_reasons)):
        if driver.reasons[i] != right_reasons[i]:
            print(i, driver.reasons[i], right_reasons[i])
    assert np.all(driver.reasons == right_reasons)
    
def test_clean_and_save():
    old_pth = 'test_sheets/test_sheet_1.csv'
    new_pth = 'test_sheets/cleaned'
    for extn in ['.csv', '.xlsx']:
        clean_and_save(old_pth, new_pth + extn)
        assert os.path.exists(new_pth + extn)
        assert os.path.exists(old_pth)
        os.remove(new_pth + extn)
