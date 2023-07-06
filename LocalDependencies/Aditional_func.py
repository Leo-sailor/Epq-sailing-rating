import matplotlib.pyplot as plt
from time import time as _time
from LocalDependencies.Csv_custom import csv_base
import LocalDependencies.General as Base
from sys import path as _path


def plot_sailors(start_date: int, sailorids: str | list[str], field_num: int, universe: str,
                 end_date: int = int(_time())):
    if isinstance(field_num, str):
        column_correlation = {'c': 1, 's': 2, 'l': 7, 'm': 8,
                              'h': 9, 'i': 0, 'o': 10, 'r': 11,
                              'e': 12, 'z': 5, 't': 6}
        field_num = column_correlation[field_num]
    if isinstance(sailorids, str):
        sailorids = [sailorids]
    to_graph = []
    universe_loc = ''.join((_path[0], '\\universes\\', universe, '\\'))
    host_file = csv_base(universe_loc + 'host-' + universe + '.csv')
    for num, sailor in enumerate(sailorids):
        to_graph.append([])
        for row in host_file.custom_iter(1):
            file_obj = csv_base(universe_loc + row[2])
            loc = file_obj.index(sailor)
            date = Base.force_int(file_obj.getcell(loc, 13))
            if start_date <= date <= end_date:
                datapoint = [file_obj.getcell(loc, field_num), date]
                to_graph[num].append(datapoint)
        to_graph[num] = Base.sort_on_element(to_graph[num], 1, False, False)
        plt.plot([to_graph[num][x][1] for x in range(len(to_graph[num]))],
                 [to_graph[num][x][0] for x in range(len(to_graph[num]))])
    plt.xlabel("Number of days since 2000 of rating")
    plt.ylabel()
    plt.show()
