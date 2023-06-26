import matplotlib.pyplot as plt
from time import time as _time
from LocalDependencies.Csv_custom import csvBase
import LocalDependencies.General as Base
from sys import path as _path
if __name__ == '__main__':
    x1 = [1, 2, 3]
    y1 = [2, 4, 1]
    # plotting the line 1 points
    plt.plot(x1, y1, label="line 1")

    # line 2 points
    x2 = [1, 2, 3]
    y2 = [4, 1, 3]
    # plotting the line 2 points
    plt.plot(x2, y2, label="line 2")

    # naming the x axis
    plt.xlabel('x - axis')
    # naming the y axis
    plt.ylabel('y - axis')
    # giving a title to my graph
    plt.title('Two lines on same graph!')

    plt.show()


def plot_sailors(start_date: int, sailorids: str | list[str], field_num: int, universe: str, end_date: int = int(_time())):
    if isinstance(field_num, str):
        column_correlation = {'c': 1, 's': 2, 'l': 7, 'm': 8,
                              'h': 9, 'i': 0, 'o': 10, 'r': 11,
                              'e': 12, 'z': 5, 't': 6}
        field_num = column_correlation[field_num]
    if isinstance(sailorids, str):
        sailorids = [sailorids]
    to_graph = []
    universe_loc = ''.join((_path[0], '\\universes\\', universe, '\\'))
    host_file = csvBase(universe_loc + 'host-' + universe + '.csv')
    for num,sailor in enumerate(sailorids):
        to_graph.append([])
        for row in host_file.custom_iter(1):
            file = csvBase(universe_loc + row[2])
            loc = file.index(sailor)
            date = file.getcell(loc,13)
            if start_date <= date <= end_date:
                datapoint = [file.getcell(loc, field_num), date]
                to_graph[num].append(datapoint)
        to_graph[num] = Base.sort_on_element(to_graph[num], 1, False, False)
        plt.plot([to_graph[num][x][1] for x in range(len(to_graph[num]))],
                 [to_graph[num][x][0] for x in range(len(to_graph[num]))])
    plt.show()


