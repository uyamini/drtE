from src import KNearestNeighbors, csvToMatrix
import numpy as np

_ENABLED = False

def test_knn():
    if _ENABLED:
        mat = csvToMatrix('test_sheets/test_sheet_1.csv')[1:]
        for col in range(mat.shape[1] - 1):
            m = KNearestNeighbors(5, col)
            m.fit(mat)
            for preds in [m.predict(mat, set(), nprocs = 1), m.predict(mat, set(), nprocs = 8)]:
                assert preds.shape == (mat.shape[0],)
                assert preds.dtype == mat.dtype
