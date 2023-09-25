import sys
import pickle


def de_pickle(array, display=False):
    coverted = 0
    for item in array:
        if item != '':
            with open(item, 'rb') as f:
                data = pickle.load(f)
            if display:
                if isinstance(data, list):
                    for line in data:
                        print(line)
                else:
                    print(data)
            with open(item + '.txt', 'w') as f:
                f.write('CHANGES WILL NOT AFFECT PICKLE FILE\n')
                if isinstance(data, list):
                    to_print = [str(i) + '\n' for i in data]
                    f.writelines(to_print)
                else:
                    f.write(str(data))
            coverted += 1
    return coverted


if len(sys.argv) > 1:
    de_pickle(sys.argv[1:])
else:
    de_pickle(input("enter files to be de-pickled seperated by commas:").split(','), True)
