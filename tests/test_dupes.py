from src import duplicate_row, duplicate_columns, csvToMatrix, redundant_columns

_SHEET = csvToMatrix('test_sheets/test_sheet_1.csv')

def test_dupe_rows():
    dupes = duplicate_row(_SHEET)
    assert dupes == [7]

def test_dupe_cols():
    dupes = duplicate_columns(_SHEET)
    assert dupes == [7]

def test_red_cols():
    mat = csvToMatrix('test_sheets/test_sheet_1_redundant.csv')
    reds = redundant_columns(mat)
    real_reds = [(0, 1),
                 (0, 3),
                 (0, 4),
                 (0, 6),
                 (2, 7),
                 (8, 9)]
    assert reds == real_reds
