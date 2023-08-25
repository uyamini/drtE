from src import csvToMatrix
import numpy as np

def convert(src_path, dest_path):
    mat = csvToMatrix(src_path)
    np.savetxt(dest_path,
               mat, 
               fmt = '%s',
               delimiter = '\t',
               encoding = 'utf-8')

if __name__ == '__main__':
    convert('test_sheets/covid-data.csv', 'test_sheets/covid-data-txt.txt')