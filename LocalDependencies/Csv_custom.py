import csv
import LocalDependencies.General as Base
from sys import path
from time import time
from pickle import dumps as _dumps, loads as _loads


class csvBase:
    def __init__(self, filelocation, protectedrows: list[int] = None, protectedcols: list[int] = None,):
        if protectedcols is None:
            protectedcols = []
        if protectedrows is None:
            protectedrows = []
        self.filelocation = filelocation
        self.protectedrow = protectedrows
        self.protectedcol = protectedcols
        try:
            with open(filelocation, newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                x = 0
                rows = []

                for line in spamreader:  # for each line in the csv
                    rows.append(line[0])  # append the raw string of the line to the output
                    rows[x] = rows[x].split(',')  # takes the raw string and splits itnto an array
                    x += 1
        except FileNotFoundError:
            with open(filelocation, 'x', newline=''):
                rows = [[]]

        column = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
        for x in range(0, len(rows)):
            for y in range(0, len(rows[0])):
                column[y].append(rows[x][y])
        for bad_loc,col in enumerate(reversed(column)):
            loc = 20 - bad_loc
            if len(col) == 0:
                column.pop(loc)
        self.columnfirst = column
        self.rowfirst = rows
    def getrow(self, row: int, miss: list[int] | int = None) -> list:
        if miss is None:
            return self.rowfirst[row]
        elif isinstance(miss, int):
            temp = self.rowfirst[row][:]
            temp.pop(miss)
            return temp
        elif isinstance(miss, list):
            miss.sort(reverse=True)
            temp = self.rowfirst[row][:]
            for index in miss:
                temp.pop(index)
            return temp
        else:
            raise TypeError
    def getcell(self, row: int, column: int):
        return self.rowfirst[row][column]

    def protectrows(self, rows: int | list[int]):
        self.protectedrow.append(rows)

    def protectcols(self, columns: int | list[int]):
        self.protectedcol.append(columns)

    def getcolumn(self, column, excluded_rows: int | list[int] = None):
        if excluded_rows is None:
            return self.columnfirst[column][:]
        elif isinstance(excluded_rows, int):
            excluded_rows = [excluded_rows]
        excluded_rows.sort(reverse=True)
        toprint = self.columnfirst[column][:]
        for index in excluded_rows:
            toprint.pop(index)
        return toprint

    def save(self):
        with open(self.filelocation, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar=',', quoting=csv.QUOTE_MINIMAL)
            for row in self.rowfirst:
                spamwriter.writerow(row)

    def __del__(self):
        self.save()

    def custom_iter(self, row_from:int=None, row_to:int=None):
        if row_from is None and row_to is None:
            return iter(self.rowfirst)
        elif row_from is None:
            return iter(self.rowfirst[:row_to])
        elif row_to is None:
            return iter(self.rowfirst[row_from:])
        else:
            return iter(self.rowfirst[row_from:row_to])

    def index(self,val):
        return self.columnfirst[0].index(val)
    def printcolumn(self, column, sperateline: bool, excudedrows: int | list[int] = None):
        if type(excudedrows) == int:
            excudedrows = [excudedrows]
        if sperateline:
            for x in range(0, len(self.columnfirst[column])):
                if x not in excudedrows:
                    print(self.columnfirst[column][x])
        else:
            excudedrows.sort(reverse=True)
            toprint = self.columnfirst[column][:]
            for index in excudedrows:
                toprint.pop(index)
            print(toprint)

    def getrownum(self, term: str, col: int):
        return self.columnfirst[col].index(term)

    def numcolumns(self):
        return len(self.columnfirst)

    def numrows(self):
        return len(self.rowfirst)

    def addrow(self, array: list):
        for x in range(len(array)):
            self.columnfirst[x].append(str(array[x]))
        for val, item in enumerate(array):
            array[val] = Base.findandreplace(item, ' ', '-', True)
        self.rowfirst.append(array)

    def addcol(self, array: list):
        for x in range(len(array)):
            self.rowfirst[x].append(str(array[x]))
        self.columnfirst.append(array)

    def removerow(self, rownum: int):
        self.rowfirst.pop(rownum)
        for col in self.rowfirst:
            col.pop(rownum)

    def updatevalue(self, term, row: int | str, column: int, colsearch: int = None, bypass: bool = False):
        term = str(term)
        if colsearch is None:
            colsearch = 0
        if type(row) == str:
            row = self.columnfirst[colsearch].index(row)
        if (row not in self.protectedrow and column not in self.protectedcol) or bypass:
            self.rowfirst[row][column] = term
            self.columnfirst[column][row] = term
        else:
            raise PermissionError("You do not have permissions to change this cell")


def set_session():
    return int(time())


class Csvnew(csvBase):
    def __init__(self, filelocation, protectedrows: list[int] = None, protectedcols: list[int] = None, universe=None):
        super(Csvnew, self).__init__(filelocation, protectedrows,protectedcols)
        self.session_start = set_session()
        if universe is not None:
            folder = path[0]
            self.host_file = ''.join((folder, '\\universes\\', universe, '\\host-', universe, '.csv'))
            self.host_file_old = csvBase(self.host_file)
            self.prev_version_num = int(self.host_file_old.getcell(1, 0))
            self.universe = universe

    def updatevaluesingle(self, term, row: int, column: bool, bypass: bool = False):
        self.updatevalue(term, row, column, 0, bypass)
        self.autosavefile()

    def set_session(self):
        self.session_start = set_session()

    def sortoncol(self, column: int, ret: bool = False, reverse: bool = False,
                  targetcol: int = None, excluderows: int | list[int] = None, greaterthan: list[int, float] = None):
        def get_element(lists:list):
            return Base.force_int(lists[column])
        valid = _loads(_dumps(self.rowfirst))
        new = []
        newnew = []
        if excluderows is not None:
            if isinstance(excluderows,int):
                excluderows = [excluderows]
            excluderows.sort(reverse=True)
            for row in excluderows:
                valid.pop(row)
        if greaterthan is not None:
            origlen = len(valid)
            for bad_loc,val in enumerate(reversed(_loads(_dumps(valid)))):
                loc = origlen - 1 - bad_loc
                if not int(val[greaterthan[0]]) >= greaterthan[1]:
                    valid.pop(loc)

        if targetcol is not None:
            valid.sort(reverse=reverse, key=get_element)
            for x in range(0, len(valid)):
                self.updatevalue((x + 1), valid[x][0], targetcol, bypass=True)
        if ret:
            valid.sort(reverse=reverse, key=lambda y: y[column])
            for x in range((len(new) - 1), -1, -1):
                newnew.append(new[x])
            newnew.append(valid)
            return newnew

    def addrow(self, array: list):
        super(Csvnew,self).addrow(array)
        self.autosavefile()

    def addcol(self, array: list):
        super(Csvnew,self).addcol(array)
        self.autosavefile()

    def removerow(self, rownum: int):
        super(Csvnew,self).removerow(rownum)
        self.autosavefile()
    def autosavefile(self):
        breakpoint()
        filename = ''.join((self.universe, '-', str(self.session_start), '.csv'))
        folder = ''.join((path[0], '\\universes\\', self.universe, '\\'))
        cfile = ''.join((folder, filename))
        with open(cfile, 'w', newline='') as csvfile:  # saves the filr
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar=',', quoting=csv.QUOTE_MINIMAL)
            # print(len(self.currcolumn))
            for x in range(0, len(self.columnfirst[0])):  # number of rows # assembls the row
                spamwriter.writerow(self.rowfirst[x])  # writes the row  # clears the row for the next one
        if self.host_file_old.getcell(0, 1) == (self.prev_version_num + 1):  # checks how to record the temporry save
            with open(self.host_file, 'w', newline='') as csvfile:  # works as if its a second or more auto save
                spamwriter = csv.writer(csvfile, delimiter=',',
                                        quotechar=',', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow(self.host_file_old.getrow(0))
                row = self.host_file_old.getrow(1, miss=3)
                row.append(Base.hashfile(cfile))
                spamwriter.writerow(row)
                for x in range(2, len(self.host_file_old.rowfirst)):
                    spamwriter.writerow(self.host_file_old.getrow(x))
        else:
            with open(self.host_file, 'w', newline='') as csvfile:  # first auto save
                spamwriter = csv.writer(csvfile, delimiter=',',
                                        quotechar=',', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow(self.host_file_old.getrow(0))
                spamwriter.writerow([self.prev_version_num + 1, self.session_start, filename, Base.hashfile(cfile)])
                for x in range(1, len(self.host_file_old.rowfirst)):
                    spamwriter.writerow(self.host_file_old.getrow(x))
