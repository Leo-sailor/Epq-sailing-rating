import csv
import LocalDependencies.Framework.base_func as base
from sys import path
from time import time
from pickle import dumps as _dumps, loads as _loads
from LocalDependencies.Framework.logger import log

log = log()


class csv_base:
    def __init__(self, file_location, protected_rows: list[int] = None, protected_cols: list[int] = None, *,
                 new_open=None):
        log.queue(0, 'opening file with:', (protected_cols, protected_rows, file_location))
        if new_open is None:
            new_open = open
        if protected_cols is None:
            protected_cols = []
        if protected_rows is None:
            protected_rows = []
        self.file_location = file_location
        self.protected_row = protected_rows
        self.protected_col = protected_cols
        try:
            with new_open(file_location, newline='') as csvfile:
                log.queue(2, 'opening file with', file_location)
                spam_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                x = 0
                rows = []

                for line in spam_reader:
                    try:  # for each line in the csv
                        rows.append(line[0])
                    except IndexError:
                        continue  # append the raw string of the line to the output
                    rows[x] = rows[x].split(',')  # takes the raw string and splits into an array
                    x += 1
        except FileNotFoundError:
            log.queue(3, 'file not found, so new file being created', file_location)
            with open(file_location, 'x', newline=''):
                rows = [[]]

        column = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
        for x in range(0, len(rows)):
            for y in range(0, len(rows[0])):
                column[y].append(rows[x][y])
        for bad_loc, col in enumerate(reversed(column)):
            loc = 20 - bad_loc
            if len(col) == 0:
                column.pop(loc)
        self.column_first = column
        self.row_first = rows
        self.open = new_open

    def get_row(self, row: int, miss: list[int] | int = None) -> list:
        log.queue(0, 'retriving row', (row, miss))
        if miss is None:
            return self.row_first[row]
        elif isinstance(miss, int):
            temp = self.row_first[row][:]
            temp.pop(miss)
            return temp
        elif isinstance(miss, list):
            miss.sort(reverse=True)
            temp = self.row_first[row][:]
            for index in miss:
                temp.pop(index)
            return temp
        else:
            log.queue(5, 'the type of miss is not: int,list, None', miss)
            raise TypeError

    def get_cell(self, row: int, column: int):
        return self.row_first[row][column]

    def protect_rows(self, rows: int | list[int]):
        if isinstance(rows, list):
            self.protected_row += rows
        elif isinstance(rows, int):
            self.protected_row.append(rows)
        else:
            log.queue(5, 'the type of rows is not: int,list', rows)
            raise TypeError
        log.queue(0, 'new rows protected', rows)

    def protect_cols(self, columns: int | list[int]):
        if isinstance(columns, list):
            self.protected_col += columns
        elif isinstance(columns, int):
            self.protected_col.append(columns)
        else:
            log.queue(5, 'the type of columns is not: int,list', columns)
            raise TypeError
        log.queue(0, 'new columns protected', columns)

    def get_column(self, column, excluded_rows: int | list[int] = None):
        if excluded_rows is None:
            return self.column_first[column][:]
        elif isinstance(excluded_rows, int):
            excluded_rows = [excluded_rows]
        excluded_rows.sort(reverse=True)
        to_print = self.column_first[column][:]
        for index in excluded_rows:
            to_print.pop(index)
        return to_print

    def save(self):
        log.queue(2, 'saving file')
        with self.open(self.file_location, 'w', newline='') as csvfile:
            spam_writer = csv.writer(csvfile, delimiter=',',
                                     quotechar=',', quoting=csv.QUOTE_MINIMAL)
            for row in self.row_first:
                spam_writer.writerow(row)

    def __del__(self):
        self.save()

    def custom_iter(self, row_from: int = None, row_to: int = None):
        if row_from is None and row_to is None:
            return iter(self.row_first)
        elif row_from is None:
            return iter(self.row_first[:row_to])
        elif row_to is None:
            return iter(self.row_first[row_from:])
        else:
            return iter(self.row_first[row_from:row_to])

    def index(self, val, col=0):
        """
        indexes the first column of the table unless otherwise specified
        """
        return self.column_first[col].index(val)

    def print_column(self, column, separate_line: bool, excluded_rows: int | list[int] = None) -> str:
        if type(excluded_rows) == int or excluded_rows is None:
            excluded_rows = [excluded_rows]
        if separate_line:
            to_print = []
            for x in range(0, len(self.column_first[column])):
                if x not in excluded_rows:
                    to_print.append(self.column_first[column][x])
            return '\n'.join(to_print)
        else:
            excluded_rows.sort()
            to_print = self.column_first[column][:]
            for index in reversed(excluded_rows):
                if index is not None:
                    to_print.pop(index)
            return ', '.join(to_print)

    def get_row_num(self, term: str, col: int):
        return self.column_first[col].index(term)

    def num_columns(self):
        return len(self.column_first)

    def num_rows(self):
        return len(self.row_first)

    def add_row(self, array: list):
        log.queue(0, 'row added to table', array)
        for val, item in enumerate(array):
            array[val] = base.findandreplace(str(item), ' ', '-', True)
        for x in range(len(array)):
            try:
                self.column_first[x].append(array[x])
            except IndexError:
                self.column_first.append([])
                self.column_first[x].append(array[x])
        self.row_first.append(array)

    def add_col(self, array: list):
        log.queue(0, 'row added to table', array)
        for val, item in enumerate(array):
            array[val] = base.findandreplace(item, ' ', '-', True)
        for x in range(len(array)):
            self.row_first[x].append(str(array[x]))
        self.column_first.append(array)

    def remove_row(self, row_num: int):
        log.queue(0, 'row removed from table', row_num)
        self.row_first.pop(row_num)
        for col in self.column_first:
            try:
                col.pop(row_num)
            except Exception as e:
                breakpoint()
                raise e

    def update_value(self, term, row: int | str, column: int, col_search: int = None, bypass: bool = False):
        # col search says what column to search in , only in the case row is a string and needs indexing
        term = str(term)
        if col_search is None:
            col_search = 0
        if type(row) == str:
            row = self.column_first[col_search].index(row)
        if (row not in self.protected_row and column not in self.protected_col) or bypass:
            log.queue(0, f'row: {row}, col: {column} value: {self.row_first[row][column]} changes to {term}')
            self.row_first[row][column] = term
            self.column_first[column][row] = term
        else:
            raise PermissionError("You do not have permissions to change this cell")


def set_session():
    return int(time())


class csv_new(csv_base):
    def __init__(self, file_location, protected_rows: list[int] = None, protected_cols: list[int] = None,
                 universe=None):
        super(csv_new, self).__init__(file_location, protected_rows, protected_cols)
        self.session_start = set_session()
        self.open = open
        if universe is not None:
            log.queue(1, 'openning a universe file')
            folder = path[0]
            self.host_file_loc = ''.join((folder, '\\universes\\', universe, '\\host-', universe, '.csv'))
            self.host_file_obj = csv_base(self.host_file_loc)
            self.prev_version_num = int(self.host_file_obj.get_cell(1, 0))
            self.universe = universe
            self.update_count = 0

    def update_value_single(self, term, row: int, column: bool, bypass: bool = False):
        self.update_value(term, row, column, 0, bypass)
        self.auto_save_file()

    def similar_names(self, similar_names_func: callable, *, col: int | list[int] = None, row: int | list[int] = None):
        if col is not None:
            if isinstance(col,int):
                col = [col]
            for column in col:
                to_change = similar_names_func(self.get_column(column))
                self.column_first[column] = to_change
                [self.row_first[loc].__setitem__(column, item) for loc, item in enumerate(to_change)]
        if row is not None:
            if isinstance(row,int):
                col = [row]
            for row in col:
                to_change = similar_names_func(self.get_row(row))
                self.row_first[row] = to_change
                [self.column_first[loc].__setitem__(row, item) for loc, item in enumerate(to_change)]

    def set_session(self):
        self.session_start = set_session()

    def sort_on_col(self, column: int, ret: bool = False, reverse: bool = False, target_col: int = None,
                    exclude_rows: int | list[int] = None, greater_than: list[int, float] = None):
        def get_element(lists: list):
            return base.force_int(lists[column])

        valid = _loads(_dumps(self.row_first))
        new = []
        new_new = []
        if exclude_rows is not None:
            if isinstance(exclude_rows, int):
                exclude_rows = [exclude_rows]
            exclude_rows.sort(reverse=True)
            for row in exclude_rows:
                valid.pop(row)
        if greater_than is not None:
            original_len = len(valid)
            for bad_loc, val in enumerate(reversed(_loads(_dumps(valid)))):
                loc = original_len - 1 - bad_loc
                if int(val[greater_than[0]]) < greater_than[1]:
                    valid.pop(loc)

        if target_col is not None:
            valid.sort(reverse=reverse, key=get_element)
            for x in range(0, len(valid)):
                self.update_value((x + 1), valid[x][0], target_col, bypass=True)
        if ret:
            valid.sort(reverse=reverse, key=lambda y: y[column])
            for x in range((len(new) - 1), -1, -1):
                new_new.append(new[x])
            new_new.append(valid)
            return new_new

    def add_row(self, array: list):
        super(csv_new, self).add_row(array)
        self.auto_save_file()

    def add_col(self, array: list):
        super(csv_new, self).add_col(array)
        self.auto_save_file()

    def update_value(self, term, row: int | str, column: int, col_search: int = None, bypass: bool = False):
        super(csv_new, self).update_value(term, row, column, col_search)
        if not bypass:
            self.auto_save_file()

    def remove_row(self, row_num: int):
        super(csv_new, self).remove_row(row_num)
        self.auto_save_file()

    def __del__(self):
        self.auto_save_file(force=True)

    def auto_save_file(self, *, force: bool = False):
        self.update_count += 1
        if self.update_count % 100 != 1 and not force:
            return None
        self.set_session()
        log.queue(0, 'file auto save starting')
        filename = ''.join((self.universe, '-', str(self.session_start), '.csv'))
        folder = ''.join((path[0], '\\universes\\', self.universe, '\\'))
        cfile = ''.join((folder, filename))

        with self.open(cfile, 'w', newline='') as csvfile:  # saves the file
            spam_writer = csv.writer(csvfile, delimiter=',',
                                     quotechar=',', quoting=csv.QUOTE_MINIMAL)

            for x in range(0, len(self.column_first[0])):  # number of rows # assembles the row
                spam_writer.writerow(self.row_first[x])
        log.queue(0, 'main csv written')  # writes the row  # clears the row for the next one
        with self.open(self.host_file_loc, 'w', newline='') as csvfile:  # first auto save
            spam_writer = csv.writer(csvfile, delimiter=',',
                                     quotechar=',', quoting=csv.QUOTE_MINIMAL)
            spam_writer.writerow(self.host_file_obj.get_row(0))
            spam_writer.writerow(
                [self.prev_version_num + 1, self.session_start, filename, base.hashfile(cfile, new_open=self.open)])
            for x in range(1, len(self.host_file_obj.row_first)):
                spam_writer.writerow(self.host_file_obj.get_row(x))
        self.prev_version_num += 1
        self.host_file_obj = csv_base(self.host_file_loc, new_open=self.open)
