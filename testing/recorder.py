import sys
import os
import time

def cmd(*args):
    print('\n')
    print(*args)
    os.system(*args)
    time.sleep(1)


def get_file_loc(term):
    paths = sys.path
    best_path = None
    for small_path in paths:
        if term in small_path:
            best_path = small_path
            break
    split = best_path.split('\\')
    return '\\'.join(split[:split.index(term) + 1])


def main():
    test_name = input('eneter the test name: ')
    if ' ' in test_name:
        raise NameError('cannot inclue spaces')
    path = get_file_loc('Epq-sailing-rating')
    print(f' path used is {path}')
    run_path = path + '\\main.py'
    inp_path = path + f'\\testing\\tests\\{test_name}.inp.pickle'
    out_path = path + f' \\testing\\tests\\{test_name}.out.pickle'
    if os.path.exists(inp_path):
        print('this test name already exists')
        choice = int(input('Press (0) to quit\nPress (1) to overwrite that test\nPress (2) to eneter a new test name'))
        if choice == 0:
            exit(0)
        elif choice != 1:
            main()
            exit(0)
    inp = input('Press (0) to record an output file\n'
                'Press (1) to not record an expected output file(useful if likely to change: ')
    if int(inp) == 1:
        out_path= ''
    cmd(f'cd "{path}"')
    main_line = f'main.py record text "{inp_path}" "{out_path}"'
    cmd(main_line)
    cmd('cd testing')

    cmd(f'un-pickler.py "{inp_path}" "{out_path}"')


if __name__ == '__main__':
    main()
