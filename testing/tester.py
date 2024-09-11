import sys
import os
import shutil


def copy_folder(source_folder, dest_folder):
    if not os.path.exists(dest_folder):
        os.mkdir(dest_folder)
    if source_folder[-1] != '\\':
        source_folder += '\\'
    if dest_folder[-1] != '\\':
        dest_folder += '\\'
    # fetch all files
    for file_name in os.listdir(source_folder):
        # construct full file path
        source = source_folder + file_name
        destination = dest_folder + file_name
        # copy only files
        if os.path.isfile(source):
            shutil.copy(source, destination)
        else:
            copy_folder(source_folder + file_name, dest_folder + file_name)


def delete_folder(folder_name):
    if folder_name[-1] != '\\':
        folder_name += '\\'
    for file in os.listdir(folder_name):
        if os.path.isfile(folder_name + file):
            os.remove(folder_name + file)
        else:
            delete_folder(folder_name + file)
    os.rmdir(folder_name)


def get_file_loc(term):
    paths = sys.path
    best_path = None
    for small_path in paths:
        if term in small_path:
            best_path = small_path
            break
    split = best_path.split('\\')
    return '\\'.join(split[:split.index(term) + 1])


def all():
    files = os.listdir(path + '\\testing\\tests')
    for val,item in enumerate(files):
        files[val] = item.split('.')[0]
    names = set(files)
    for file in names:
        excute_test(file,True)


def excute_test(test_name, reset):
    if reset:
        os.mkdir(path + '\\testing\\temp')
        copy_folder(path + '\\universes', path + '\\testing\\temp\\universes')
    run_path = path + '\\main.py'
    inp_path = path + f'\\testing\\tests\\{test_name}.inp.pickle'
    out_path = path + f' \\testing\\tests\\{test_name}.out.pickle'
    if not os.path.exists(out_path):
        out_path = ''
    cmd = os.system
    cmd(f'cd {path}')
    main_line = f'{run_path} test text {inp_path}{out_path}'
    cmd(main_line)
    if reset:
        delete_folder(path + '\\universes')
        copy_folder(path + '\\testing\\temp\\universes', path + '\\universes')
        delete_folder(path + '\\testing\\temp')
    print(main_line)


args = sys.argv[1:]
args += [0, 0, 0, 0, 0]
if args[0] not in [0, 'pass']:
    test_name = args[0]
elif args[0] == 'all':
    test_name = ''
else:
    test_name = input('enter the test name (press enter for all): ')
if ' ' in test_name:
    raise NameError('the test name cannot inclue spaces')
path = get_file_loc('Epq-sailing-rating')
if args[1] in ['yes', '1', 'y'] or test_name == '':
    reset_files = True
elif args[1] in ['no', '0', 'n']:
    reset_files = False
else:
    reset_files = input('would you like to reset files after this test - 1 for yes, 0 for no')
    reset_files = reset_files == '1'

if test_name == '':
    all()
else:
    excute_test(test_name, reset_files)
