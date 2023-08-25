import numpy as np
from pyparsing import col
from .csv_to_matrix import csvToMatrix, has_header
import multiprocessing as mp
from itertools import starmap
from .rules import NumOutlier, IsNA, IsIncorrectDataType, MissingData, WrongCategory
from .rules import HasTypo, EmailChecker, duplicate_row, duplicate_columns, user_message, redundant_columns
from .column import Column
from .utilities import arr_to_set, excel_range
import pandas as pd
import xlwings as xw
import warnings
from .path_utils import get_extension, ALLOWED_EXTENSIONS
from matplotlib.figure import Figure

_ALL_PREDS = [MissingData, IsNA, EmailChecker, IsIncorrectDataType, NumOutlier, HasTypo, WrongCategory]
_ESCAPE_CHARS = {',', '\n', '"', '\t'}

class Driver:
    """The class responsible for finding dirty cells and cleaning them.
    
    Args:
        sheet_path (str) : a path to the matrix to read
        preds (list | None) : a list of predicates to use. If None (the default), it will use all of them
        dupes (list) : a list of Booleans, with the first corresponding to whether to remove duplicate
            rows, the second for duplicate columns, the third for redundant columns. The default is True for 
            first two and False for the last.

    Fields:
        progress (int) : how much progress (out of 100) this has made
        old_mat (np.array) : the user's uploaded spreadsheet, WITHOUT the header if one is present.
            After the header and duplicates are removed, this is read-only
        header (int) : how many rows to skip at the top of the spreadsheet. Typically either 0 or 1
        clean_mat (np.array) : the cleaned version of the user's spreadsheet, WITH the header if one
            is present. Make sure to call clean_all_cells() before using this
        cols (list) : a list of Column objects, one for each column in the user's spreadsheet
        all_preds (list) : a list of objects derived from RuleBase which indicate what to use when finding
            dirty cells
        dirty_inds (np.array) : an array of [y, x] pairs to be used to index into old_mat. As such, they will
            not include the header
        s_inds (set) : a set of tuples with the same indices as dirty_inds
        inds_with_head (np.array) : an array of [y, x] pairs to be used to index into clean_mat. They do include
            the header
        reasons (np.array) : an array of objects derived from RuleBase. reasons[i] is the reason why the cell at
            dirty_inds[i] is dirty
    """
    def __init__(self, path, preds = None, dupes = [True, True, False]):
        self.progress = 0
        self.old_mat = csvToMatrix(path)
        self.progress = 10
        self.header = has_header(self.old_mat)
        self.duplicates = [0,0,0]
        self.missing = 0
        self._del_dupes(dupes[0], dupes[1], dupes[2])
        self.clean_mat = self.old_mat.copy()
        self.old_mat = self.old_mat[self.header:]
        self.cols = None
        self._col_list()

        if preds is None:
            self.all_preds = _ALL_PREDS
        else:
            self.all_preds = preds
        self.all_preds = [ p() for p in self.all_preds ]

        self.dirty_inds = None
        self.s_inds = None
        self.inds_with_head = None
        self.reasons = None
        self.progress = 20
        

    def _del_dupes(self, del_rows, del_cols, red_cols):
        """Deletes duplicate rows if del_rows and duplicate columns if del_cols. Saves res to self.old_mat."""
        # duplicate rows 
        if(del_rows):
            dupes = duplicate_row(self.old_mat)
            self.duplicates[0] = len(dupes)
            self.old_mat = np.delete(self.old_mat, dupes, 0)
        # duplicate columns
        if(del_cols):
            dupes = duplicate_columns(self.old_mat)
            self.duplicates[1] = len(dupes)
            self.old_mat = np.delete(self.old_mat, dupes, 1)
        
        # redundant columns
        if(red_cols):
            red_pairs = redundant_columns(self.old_mat)
            red = [a[1] for a in red_pairs]
            self.duplicates[2] = len(red)
            self.old_mat = np.delete(self.old_mat, red, 1)

    def _col_list(self, nprocs = 8):
        """Analyzes each column into Column objects and sets self.cols."""
        mat_t = self.old_mat.T
        args = [ (mat_t[i], i) for i in range(mat_t.shape[0]) ]
        nprocs = min(nprocs, mat_t.shape[0])
        if nprocs > 1:
            with mp.Pool(nprocs) as pool:
                self.cols = pool.starmap(Column, args, chunksize = mat_t.shape[0] // nprocs)
        else:
            self.cols = list(starmap(Column, args))

    def _dirty_row(self, row):
        """Worker function for all_dirty_cells"""
        new_row = [None] * len(row)
        for col in range(len(row)):
            for pred in range(len(self.all_preds)):
                if self.all_preds[pred].is_dirty(row[col], self.cols[col]):
                    new_row[col] = self.all_preds[pred]
                    break
        return new_row

    def find_dirty_cells(self, nprocs = 8):
        """Finds the indices and reasons for every dirty cell and sets self.inds and self.reasons.
        
        Args:
            nprocs (int) : how many processes to use. Default is 8. If 1, it will not create any
                new processes.

        Returns:
            None
        """
        nprocs = min(nprocs, self.old_mat.shape[0])

        if nprocs > 1:
            with mp.Pool(nprocs) as pool:
                is_dirty = np.array(pool.map(self._dirty_row, self.old_mat), dtype = object)
        else:
            is_dirty = np.array(list(map(self._dirty_row, self.old_mat)), dtype = object)

        not_none = is_dirty != None
        self.dirty_inds = np.argwhere(not_none)
        self.reasons = is_dirty[not_none]

        self.inds_with_head = self.dirty_inds.copy()
        for i in range(self.dirty_inds.shape[0]):
            self.inds_with_head[i, 0] += self.header
        self.s_inds = arr_to_set(self.dirty_inds)
        self.progress = 50

    def _clean_cell(self, inds, reason):
        """Returns the suggested change to the cell in self.old_mat at inds based on reason."""
        return reason.clean(inds, self.old_mat, self.cols[inds[1]], self.s_inds)

    def _get_suggs(self, nprocs = 1, num_dots = 20):
        """Returns the suggested changes to old_mat."""
        nprocs = min(nprocs, self.dirty_inds.shape[0])
        args = []
        for i in range(self.dirty_inds.shape[0]):
            args.append((self.dirty_inds[i], self.reasons[i]))

        if nprocs > 1:
            with mp.Pool(nprocs) as pool:
                return np.array(pool.starmap(self._clean_cell, 
                                             args, 
                                             chunksize = self.dirty_inds.shape[0] // nprocs), 
                                dtype = 'U128')

        res = np.empty(len(args), dtype = 'U128')
        per_dot = len(args) // num_dots if num_dots else 0
        dot_str = f'|{" " * num_dots}|'
        dot_count = 0
        per_prog = max(1, 10 * len(args) // (100 - self.progress))
        for i in range(len(args)):
            if per_dot and i % per_dot == 0:
                print(dot_str, end = '\r')
                dot_count += 1
                dot_str = f'|{"." * dot_count}{" " * (num_dots - dot_count)}|'
            if (i + 1) % per_prog == 0:
                self.progress += 10
                
            res[i] = self._clean_cell(*args[i])
        if per_dot: print()
        return res

    def clean_all_cells(self, nprocs = 8, num_dots = 20):
        """Cleans all the cells and saves the changes to self.clean_mat.
        
        Args:
            nprocs (int) : how many processes to use. If 1 , it will not create any
                new processes. Default is 8
            num_dots (int) : how many dots to print to the terminal. Default is 20. Set to 0 to silence
                all printing

        Returns:
            None
        """
        suggs = self._get_suggs(nprocs = nprocs, num_dots = num_dots)
        for i in range(suggs.shape[0]):
            self.clean_mat[tuple(self.inds_with_head[i])] = suggs[i]
 
    def user_message(self, inds_ind):
        """Returns a user-readable message for the dirty cell at self.old_mat[self.dirty_inds[inds_ind]].
        
        Args:
            inds_ind (int) : the index within self.dirty_inds where the indices of the dirty cell can be found

        Returns:
            message (str) : the user-readable message
        """
        return user_message(self.old_mat[tuple(self.dirty_inds[inds_ind])],
                            self.cols[self.dirty_inds[inds_ind, 1]],
                            self.reasons[inds_ind])

    def save_clean(self, new_pth):
        """Saves self.clean_mat to new_pth. Use save_excel to save excel sheets.
        
        Args:
            new_pth (str) : the path to save the csv to 

        Returns:
            None
        """
        for y in range(self.clean_mat.shape[0]):
            for x in range(self.clean_mat.shape[1]):
                for char in self.clean_mat[y, x]:
                    if char in _ESCAPE_CHARS:
                        self.clean_mat[y, x] = f'"{self.clean_mat[y, x]}"'
                        break

        np.savetxt(new_pth, 
                   self.clean_mat, 
                   fmt = '%s', 
                   delimiter = ',', 
                   encoding = 'utf-8')

    def save_excel(self, pth):
        """Saves clean_mat to an excel file at pth.
        Args:
            pth (str) : the path to save the file to

        Returns:
            None
        """
        for y in range(self.clean_mat.shape[0]):
            for x in range(self.clean_mat.shape[1]):
                if (len(self.clean_mat[y, x]) > 1 and
                    self.clean_mat[y, x][0] == '"' and
                    self.clean_mat[y, x][-1] == '"'):
                    self.clean_mat[y, x] = self.clean_mat[y, x][1:-1]

        df = pd.DataFrame(self.clean_mat)
        with pd.ExcelWriter(pth, engine = 'xlsxwriter', engine_kwargs = {'options' : {'strings_to_numbers' : True}}) as writer:
            df.to_excel(writer, index_label = None, header = False, index = False)

    def highlight_excel(self, pth):
        """Highlights the cells of the excel sheet at pth.
        
        Args:
            pth (str) : where to find the Excel sheet
 
        Returns:
            None
        """
        try:
            app = xw.App(visible=False)
            wb = xw.Book(pth)
        except ValueError:
            warnings.warn('WARNING: could not highlight spreadsheet because user still has old "cleaned.xlsx" file open.')
            return

        #Name of sheet hardcoded 
        xl_sheet = wb.sheets['Sheet1']
        for i in range(len(self.reasons)):
            xl_sheet.range(excel_range(self.inds_with_head[i])).color = self.reasons[i].color
        wb.save()
        wb.close()
        app.quit()
        self.progress = 150

    def reason_counts(self):
        """Returns a mapping from each predicate type to how many cells are dirty based on that predicate."""
        mapping = { p : 0 for p in self.all_preds }
        for r in self.reasons:
            mapping[r] += 1
        return mapping

    def save_pie_chart(self, path):
        """Saves a pie chart to path based on reason_counts."""
        counts = self.reason_counts()
        fig = Figure()
        ax = fig.subplots()
        sizes = [ counts[p] for p in self.all_preds if counts[p] ] # order matters so shouldn't use counts.values
        # sizes.append(self.missing)
        labels = [ p.name for p in self.all_preds if counts[p] ]
        # labels.append("Missing")
        colors = [ (p.color[0] / 255, p.color[1] / 255, p.color[2] / 255) for p in self.all_preds if counts[p] ]
        # colors.append(((255/255, 154/255, 162/255)))
        ax.pie(sizes, labels = labels, colors = colors)
        fig.savefig(path)
    
    def summary_stats(self):
        """Returns the reason_counts for reporting."""
        counts = self.reason_counts()
        sizes = [ counts[p] for p in self.all_preds ] # order matters so shouldn't use counts.values
        labels = [ p.name for p in self.all_preds ]
        missing = 0
        if MissingData() not in self.all_preds:
            m = MissingData()
            for row in self.clean_mat:
                for j in row :
                    if m.is_dirty(j, None):
                        missing += 1
        dupes = self.duplicates
        return sizes, labels, dupes, missing

def clean_and_save(dirty_path, clean_path, preds = None, dupes = [True, True, False]):
    """Cleans the sheet at dirty_path and saves the cleaned version to clean_path.
    
    Args:
        dirty_path (str) : the path to the dirty spreadsheet
        clean_path (str) : the path to save the cleaned sheet to
        preds (list) : a list of types derived from RuleBase. If None (the default),
            it will use all the predicates.
        dupes (list) : a list of Booleans, with the first corresponding to whether to remove duplicate
            rows, the second for duplicate columns, the third for redundant columns. The default is True for 
            first two and False for the last.

    Returns:
        driver (Driver) : the driver that did all the processing, in case the client
            wants it to do a bit more
    """
    dirty_extns = ALLOWED_EXTENSIONS
    clean_extns = dirty_extns | {'xlsx'}
    clean_extn = get_extension(clean_path)
    if get_extension(dirty_path) not in dirty_extns:
        raise ValueError(f'Invalid file type to read: {dirty_path}')
    if clean_extn not in clean_extns:
        raise ValueError(f'Invalid file type to write to: {clean_path}')

    driver = Driver(dirty_path, preds = preds, dupes = dupes)
    driver.find_dirty_cells()
    driver.clean_all_cells(num_dots = 0)

    if clean_extn in dirty_extns:
        driver.save_clean(clean_path)
    else:
        driver.save_excel(clean_path)
    return driver
