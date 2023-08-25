from os import listdir
from os.path import exists
from time import sleep

ALLOWED_EXTENSIONS = {'txt', 'csv'}
ROOT_PATH = 'src/ui/Flask'
CLEAN_NAME = 'cleaned.csv'
CLEAN_XL = 'cleaned.xlsx'
PIE_NAME = 'pie_chart.png'
DATA_PATH = ROOT_PATH + '/temp_files'
CLEAN_PATH = DATA_PATH + '/' + CLEAN_NAME
CLEAN_XL_PATH  = DATA_PATH + '/' + CLEAN_XL
PIE_PATH = DATA_PATH + '/' + PIE_NAME
DEF_CONFIG_NAME = 'def_config.txt'
CUSTOM_CONFIG_NAME = 'custom_config.txt'

def get_extension(filename):
    """Returns the extension of the file (e.g. txt or csv)."""
    if '.' not in filename: return ''
    return filename.rsplit('.', 1)[1].lower()

def allowed_file(filename):
    return get_extension(filename) in ALLOWED_EXTENSIONS

def data_file_path():
    """Returns the path to the user's file or an empty string if it has not been uploaded."""
    root_path = DATA_PATH
    files = listdir(root_path)
    config_files = [DEF_CONFIG_NAME,
                    CUSTOM_CONFIG_NAME]
    for f in files:
        if (allowed_file(f) and 
            f not in config_files):
            return root_path + '/' + f
    return ''

def config_file_path():
    """Returns the path to the user's file. 
    
    If the user has not selected any files, it will return the default configs.

    Args:
        None

    Returns:
        pth (str) : the path to the config files
    """
    root_path = DATA_PATH
    custom = root_path + '/' + CUSTOM_CONFIG_NAME
    if exists(custom):
        return custom
    return root_path + '/' + DEF_CONFIG_NAME

def wait_for_data():
    """Waits for data to be placed in the data folder by Flask."""
    print('Starting to wait')
    while not data_file_path():
        sleep(1) # tell the OS to context switch away so we're not wasting time
    print('Found file')
