import sys
import os

def get_file_loc(term):
    paths = sys.path
    best_path = None
    for path in paths:
        if term in path:
            best_path = path
            break
    splited = best_path.split('\\')
    return '\\'.join(splited[:splited.index(term)+1])

path = get_file_loc('Epq-sailing-rating')
run_path = path + '\\main.py'
inp_path = path + '\\tests\\in.input'
os.system(f'cd {path}')
os.system('dir')
os.system(f'{run_path} test t {inp_path}')
