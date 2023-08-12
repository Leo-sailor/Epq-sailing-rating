import sys
import os


def get_file_loc(term):
    paths = sys.path
    best_path = None
    for small_path in paths:
        if term in small_path:
            best_path = small_path
            break
    split = best_path.split('\\')
    return '\\'.join(split[:split.index(term) + 1])


path = get_file_loc('Epq-sailing-rating')
run_path = path + '\\main.py'
inp_path = path + '\\tests\\1.inp.pickle'
out_path = path + '\\tests\\1.out.pickle'
os.system(f'cd {path}')
os.system('dir')
main_line = f'{run_path} record text {inp_path} {out_path}'
os.system(main_line)
os.system('cd tests')
os.system(f'un-pickler.py {inp_path} {out_path}')
