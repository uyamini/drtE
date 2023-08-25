from src import Driver

if __name__ == '__main__':
    driver = Driver('test_sheets/test_sheet_1.csv', dupes = [False, False, False])
    driver.find_dirty_cells()
    for i in range(driver.dirty_inds.shape[0]):
        print(f'Dirty cell found in cell {driver.inds_with_head[i, 1] + 1} of row \n{driver.old_mat[driver.dirty_inds[i, 0]]}\n' +
              driver.user_message(i) +
              f'\nSuggested: {driver._clean_cell(driver.dirty_inds[i], driver.reasons[i])}\n')
