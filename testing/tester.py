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

test_name = input('eneter the test name: ')
if ' ' in test_name:
    raise NameError('cannot inclue spaces')
path = get_file_loc('Epq-sailing-rating')
run_path = path + '\\main.py'
inp_path = path + f'\\tests\\{test_name}.inp.pickle'
out_path = path + f'\\tests\\{test_name}.out.pickle'
cmd = os.system
cmd('echo off')
cmd(f'cd {path}')
cmd('dir')
cmd('echo on')
main_line = f'{run_path} test text {inp_path} {out_path}'
cmd(main_line)
print(main_line)
