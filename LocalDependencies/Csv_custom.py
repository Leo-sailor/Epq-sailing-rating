import csv
from LocalDependencies.General import General
from sys import path
from time import time
import os
base = General()

class Csvnew():
    def __init__(self, filelocation, protectedrows: list[int] = None, protectedcols: list[int] = None, universe=None):
        self.sessionstart = int(time())
        if universe is not None:
            folder = path[0]
            self.hostfile = ''.join((folder, '\\universes\\', universe, '\\host-', universe, '.csv'))
            self.hostfileold = Csvnew(self.hostfile)
            self.prevversionnum = int(self.hostfileold.getcell(1, 0))
            self.universe = universe
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
        self.columnfirst = column
        self.rowfirst = rows

    def getrow(self, row: int, miss: list[int] | int = None) -> list:
        if miss is None:
            return self.rowfirst[row]
        elif type(miss) == int:
            temp = self.rowfirst[row][:]
            temp.pop(miss)
            return temp
        elif type(miss) == list:
            miss.sort(reverse=True)
            temp = self.rowfirst[row][:]
            for index in miss:
                temp.pop(index)
            return temp
        else:
            raise TypeError

    def updatevaluesingle(self, term, row: int, column: bool, bypass: bool = False):
        self.updatevalue(term, row, column, 0, bypass)
        self.autosavefile()

    def getcell(self, row: int, column: int):
        return self.rowfirst[row][column]

    def protectrows(self, rows: int | list[int]):
        self.protectedrow.append(rows)

    def protectcols(self, columns: int | list[int]):
        self.protectedcol.append(columns)

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

    def sortoncol(self, column: int, ret: bool = False, reverse: bool = False,
                  targetcol: int = None, excluderows: int | list[int] = None, greaterthan: list[int, float] = None):
        valid = self.rowfirst[:]
        new = []
        newnew = []
        if excluderows is not None:
            if type(excluderows) == int:
                excluderows = [excluderows]
            for x in range((len(valid) - 1), -1, -1):
                try:
                    if x in excluderows:
                        new.append(valid.pop(x))
                except ValueError:
                    new.append(valid.pop(x))
        if greaterthan is not None:
            for x in range((len(valid) - 1), -1, -1):
                try:
                    if int(valid[x][greaterthan[0]]) < greaterthan[1]:
                        new.append(valid.pop(x))
                except ValueError:
                    new.append(valid.pop(x))
        if targetcol is not None:
            valid.sort(reverse=reverse, key=lambda y: y[column])
            for x in range(0, len(valid)):
                self.updatevalue((x + 1), valid[x][0], 11, bypass=True)
        valid.sort(reverse=reverse, key=lambda y: y[column])
        for x in range((len(new) - 1), -1, -1):
            newnew.append(new[x])
        newnew.append(valid)
        if ret:
            return newnew

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

    def getcolumn(self, column, excudedrows: int | list[int] = None):
        if excudedrows is None:
            return self.columnfirst[column][:]
        excudedrows.sort(reverse=True)
        toprint = self.columnfirst[column][:]
        for index in excudedrows:
            toprint.pop(index)
        return toprint

    def getrownum(self, term: str, col: int):
        return self.columnfirst[col].index(term)

    def numcolumns(self):
        return len(self.columnfirst)

    def numrows(self):
        return len(self.rowfirst)

    def addrow(self, array: list):
        for x in range(len(array)):
            self.columnfirst[x].append(str(array[x]))
        self.rowfirst.append(array)
        self.autosavefile()

    def addcol(self, array: list):
        for x in range(len(array)):
            self.rowfirst[x].append(str(array[x]))
        self.columnfirst.append(array)
        self.autosavefile()

    def removerow(self, rownum: int, save: bool = True):
        self.rowfirst.pop(rownum)
        for col in self.rowfirst:
            col.pop(rownum)
        if save:
            self.save()

    def save(self):
        with open(self.filelocation, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar=',', quoting=csv.QUOTE_MINIMAL)
            for x in range(0, len(self.rowfirst[0])):
                spamwriter.writerow(self.rowfirst[x])

    def autosavefile(self):
        filename = ''.join((self.universe, '-', str(self.sessionstart), '.csv'))
        folder = ''.join((path[0], '\\universes\\', self.universe, '\\'))
        cfile = ''.join((folder, filename))
        with open(cfile, 'w', newline='') as csvfile:  # saves the filr
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar=',', quoting=csv.QUOTE_MINIMAL)
            # print(len(self.currcolumn))
            for x in range(0, len(self.columnfirst[0])):  # number of rows # assembls the row
                spamwriter.writerow(self.rowfirst[x])  # writes the row  # clears the row for the next one
        if self.hostfileold.getcell(0, 1) == (self.prevversionnum + 1):  # checks how to record the temporry save
            with open(self.hostfile, 'w', newline='') as csvfile:  # works as if its a second or more auto save
                spamwriter = csv.writer(csvfile, delimiter=',',
                                        quotechar=',', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow(self.hostfileold.getrow(0))
                row = self.hostfileold.getrow(1, miss=3)
                row.append(base.hashfile(cfile))
                spamwriter.writerow(row)
                for x in range(2, len(self.hostfileold.rowfirst)):
                    spamwriter.writerow(self.hostfileold.getrow(x))
        else:
            with open(self.hostfile, 'w', newline='') as csvfile:  # first auto save
                spamwriter = csv.writer(csvfile, delimiter=',',
                                        quotechar=',', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow(self.hostfileold.getrow(0))
                spamwriter.writerow([self.prevversionnum + 1, self.sessionstart, filename, base.hashfile(cfile)])
                for x in range(1, len(self.hostfileold.rowfirst)):
                    spamwriter.writerow(self.hostfileold.getrow(x))

    def mansavefile(self):  # useful but i dont think is used
        self.autosavefile()
        newfilename = ''.join((path[0], '\\universes\\', self.universe, '\\', self.universe, '-', str(self.sessionstart - 1), '.csv'))
        os.rename(''.join((path[0], '\\universes\\', self.universe, '\\', self.universe, '-', str(self.sessionstart), '.csv')), newfilename)

        with open(self.hostfile, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar=',', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(self.hostfileold.getrow(0))
            spamwriter.writerow([self.hostfileold.getcell(0, 1), self.hostfileold.getcell(1, 1), newfilename, self.hostfileold.getcell(3, 1)])
            for x in range(2, len(self.hostfileold.rowfirst)):
                spamwriter.writerow(self.hostfileold.getrow(x))
        self.sessionstart = int(time())
        self.prevversionnum += 1

    def writefile(self):
        with open(self.filelocation, 'w', newline='') as csvfile:  # saves the filr
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar=',', quoting=csv.QUOTE_MINIMAL)
            # print(len(self.currcolumn))
            for x in range(0, len(self.columnfirst[0])):  # number of rows # assembls the row
                spamwriter.writerow(self.rowfirst[x])
