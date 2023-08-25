from src import user_message, Column
from src import NumOutlier, IsNA, IsIncorrectDataType, MissingData, WrongCategory, HasTypo, EmailChecker
import numpy as np

def test_messages():
    cell_str = 'hello'
    col = Column(np.array(['string1', '2', '3.0', '1.0']), 0)
    assert user_message(cell_str, col, IsNA()) == IsNA().message(cell_str, col)
    assert user_message(cell_str, col, IsIncorrectDataType()) == IsIncorrectDataType().message(cell_str, col)
    assert user_message(cell_str, col, MissingData()) == MissingData().message(cell_str, col)
    num_col = Column(np.array(['1', '-1', '0']), 0)
    assert user_message('10', num_col, NumOutlier()) == NumOutlier().message('10', num_col)
    assert user_message(cell_str, col, WrongCategory()) == WrongCategory().message(cell_str, col)
    assert user_message('hllo', col, HasTypo()) == HasTypo().message('hllo', col)
    assert user_message(cell_str, col, EmailChecker()) == EmailChecker().message(cell_str, col)
    