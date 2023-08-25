
# eg : sample = ' 1234    Q-24 2010-11-29         563   abc  a6G47er15        '


def clean_whitespaces(cell_str,col):
    if col.column_type == 'alpha':

        clean_str = ' '.join(cell_str.strip().split())
        return clean_str
    return -1




