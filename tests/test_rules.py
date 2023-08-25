from src import NumOutlier, Column, IsNA, IsIncorrectDataType, MissingData, WrongCategory, HasTypo, EmailChecker
import numpy as np

ENABLED_STR_OUTLIER = False

def _def_col():
    return Column(np.array(['0', '1', '-1']), 0)

def test_outliers():
    c = _def_col()
    rule = NumOutlier()
    assert rule.is_dirty('10', c)
    assert rule.is_dirty('10.0', c)
    assert not rule.is_dirty('aa', c)
    assert not rule.is_dirty('0', c)
    assert not rule.is_dirty('0.0', c)
    assert rule.is_dirty('-10', c)
    assert not rule.is_dirty('-1', c)

    c = Column(np.array(['202500',
                         '357286',
                         '500000',
                         '400000',
                         'na',
                         '',
                         '400000',
                         '5']), 
               0)
    assert rule.is_dirty('5', c), c._quants

def test_na():
    c = _def_col()
    rule = IsNA()
    assert rule.is_dirty('na', c)
    assert rule.is_dirty('Na', c)
    assert rule.is_dirty('N/A', c)
    assert rule.is_dirty('n/a', c)
    assert rule.is_dirty('not applicable', c)
    assert not rule.is_dirty('real text', c)
    assert rule.is_dirty('nan', c)
    assert not rule.is_dirty('1', c)
    assert not rule.is_dirty('0.0', c)

def test_correct_dtype():
    c = _def_col()
    rule = IsIncorrectDataType()
    assert c.column_type == 'int'
    assert rule.is_dirty('string', c)
    assert rule.is_dirty('1.0', Column(np.array(['string']), 0))
    assert not rule.is_dirty('s', Column(np.array(['string']), 0))
    assert not rule.is_dirty('1', c)
    assert rule.is_dirty('1.0', c)
    assert rule.is_dirty('-1.0', c)
    assert not rule.is_dirty('1.0', Column(np.array(['0.0', '1.0']), 0))

def test_missing():
    c = _def_col()
    rule = MissingData()
    assert rule.is_dirty('', c)
    assert rule.is_dirty(' ', c)
    assert rule.is_dirty('\t', c)
    assert not rule.is_dirty('hello', c)
    assert not rule.is_dirty('0', c)

def test_is_email():
    cols = [Column(np.array(['simran@gmail.com', 'yamini@u.northwestern.edu', 'simg@u.northwestern.edu']), 0),
            Column(np.array(['email1@gmail.com', 'not an email', 'def not an email']), 0)]
    for col in range(len(cols)):
        rule = EmailChecker()
        assert col == rule.is_dirty('abc@gmail.com', cols[col])
        assert col != rule.is_dirty('123', cols[col])
        assert col != rule.is_dirty('random_string', cols[col])
        assert col == rule.is_dirty('s@nu.northwestern.edu', cols[col])
        assert col != rule.is_dirty('27.5', cols[col])
        assert col != rule.is_dirty('hello@xx', cols[col])

def test_whitesp():
    #this is terribly written code, sorry 🙈
    from src.strip_whitespaces import clean_whitespaces
    col = Column(np.array(['   string', 'hello', '    what da dog doin   ']), 0)
    x = np.array(['   string', 'hello', '    what da dog doin   '])
    y = np.array(['123', '  twentytwo', 'hi my name is  Bob'])
    l = []
    m = []
    for i in x:
        l.append(clean_whitespaces(i, col))
    l = np.array(l)

    for j in y:
        m.append(clean_whitespaces(j,col))
    m = np.array(m)

    assert np.array_equal(l,np.array(['string', 'hello', 'what da dog doin']))
    assert np.array_equal(m, np.array(['123', 'twentytwo', 'hi my name is Bob']))

def test_wrong_cat():
    col = Column(np.array(['yes', 'no', 'yes', 'yes', 'no', 'no', 'n', 'y', 'yes', 'no']), 0)
    rule = WrongCategory()
    assert rule.is_dirty('y', col)
    assert rule.is_dirty('n', col)
    assert not rule.is_dirty('yes', col)
    assert not rule.is_dirty('no', col)

def test_has_typo():
    rule = HasTypo()
    assert rule.is_dirty('cmptr', None)
    assert rule.is_dirty('my cmptr', None)
    assert not rule.is_dirty('computer', None)
    assert not rule.is_dirty('my computer is great', None)
