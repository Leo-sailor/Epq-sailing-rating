from sys import path
import csv
from time import time
import os
from Dependencies.ELO import EloCalculations
from General import General
import datetime
base = General()


class Csvcode:
    def __init__(self):
        print('\nUniverse selection tool:')
        print('Avalible universes are:')

        column = self.opencsv(''.join((path[0], '\\universes\\', 'host.csv',)), transpose=True)

        for x in range(1, len(column[0])):
            print(column[0][x])

        universe = input('\nPlease enter the name of the universe you would like to acess (N for a new universe):').lower()
        while not(universe in column[0] or universe.upper() == 'N'):
            print('\nThat universe name was not valid, please try again')
            universe = input('Please enter the name of the universe you would like to acess (N for a new universe):').lower()

        self.universe = self.__linkuniverse(universe)
        self.sessiontime = int(time())

        if universe != self.universe:
            column = self.opencsv(''.join((path[0], '\\universes\\', 'host.csv',)), transpose=True)
        # print(column)

        universeloc = column[0].index(self.universe)
        self.passhash = column[3][universeloc]
        self.elo = EloCalculations(column[2][universeloc], column[4][universeloc])
        self.startingvalue = column[1][universeloc]

        self.adminrights()

    def __linkuniverse(self, universe):
        if universe.upper() == 'N':
            universe = self.__makeuniverse()

        try:
            self.folder = ''.join((path[0], '\\universes\\', universe, '\\'))
            self.hostfile = ''.join((self.folder, 'host-', universe, '.csv'))

            rows = self.opencsv(self.hostfile)

            self.basefile = ''.join((self.folder, rows[1][2]))
            self.versionnumber = int(rows[1][0])
            mostrecentdatafilehash = rows[1][3]
            print('{} universe opened and running\n'.format(universe))
            rows = self.opencsv(self.basefile, transpose=True)
            if base.hashfile(self.basefile) != mostrecentdatafilehash and mostrecentdatafilehash != '0':
                raise 'The most recent data file is not as expected'

        except FileNotFoundError:
            raise 'There was a error loading the file, the program will now exit '

        basecolumn = [x for x in rows if x != []]
        self.currcolumn = basecolumn
        # self.cleanup - this will go through universe host and look for identical md5 hash and if there is, delete the older one
        return universe

    def __makeuniverse(self):
        name = base.cleaninput('please enter your new ranking universe name:', 's', charlevel=1)

        direc = ''.join((path[0], '\\universes\\', name,))
        if os.path.exists(direc):
            raise Exception('This universe already exists, please try again')
        else:
            os.mkdir(direc)
        hostfile = (direc, '\\', 'host-', name, '.csv')
        curtime = str(int(time()))
        firstfilename = ''.join((name, '-', curtime, '.csv'))
        firstfile = ''.join((direc, '\\', firstfilename))
        universe = name

        with open(firstfile, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar=',', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['sailorID', 'champNum', 'sailNo', 'Firstname', 'Surname', 'Region', 'nat',
                                 'lightRating', 'midRating', 'heavyRating', 'overallRating',
                                 'rank', 'events', 'lastEventDate'])

        with open(''.join(hostfile), 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar=',', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['versionNumber', 'creationDate', 'fileName', 'md5'])
            spamwriter.writerow(['1', curtime, firstfilename, base.hashfile(firstfile)])

        self.passhash = base.cleaninput('\nPlease enter a password for this universe:', 'pn')
        starting = base.cleaninput('\nWhat would you like the average rating of this '
                                   'universe to be?(450-3100)(default: 1500):',
                                   'i', rangehigh=3100, rangelow=450)
        k = base.cleaninput('\nWhat would you like the speed of rating change '
                            'to be?(0.3 - 4)(Recomended: 1):',
                            'f', rangelow=0.3, rangehigh=4)

        with open(''.join((path[0], '\\universes\\host.csv')), 'a', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar=',', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow([name, starting, (starting / 5 + 100), self.passhash, k, ''])

        print('{} universe has been created'.format(name))
        return universe

    def opencsv(self, fileloc, transpose=False):
        with open(fileloc, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            x = 0
            rows = []

            for row in spamreader:
                rows.append(row[0])
                rows[x] = rows[x].split(',')
                x += 1
        if transpose:
            column = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
            for x in range(0, len(rows)):
                for y in range(0, len(rows[0])):
                    column[y].append(rows[x][y])
            return column
        else:
            return rows

    def adminrights(self):
        self.admin = base.cleaninput(('press enter to skip entering a password'
                                     '\nor enter the admin password for the universe {}:'.format(self.universe)),
                                     'pr', correcthash=self.passhash,
                                     failhash='e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')

    def getinfo(self, sailorid, resulttype):
        try:
            row = self.currcolumn[0].index(sailorid)
        except ValueError:
            raise('the sailor id {} could not be found'.format(sailorid))

        resulttype.lower().strip()

        result = ''

        if resulttype == 'name' or '2':
            findtypeloc = -1
            result = ' '.join((self.currcolumn[3][row], self.currcolumn[4][row]))
        elif resulttype == 'sail number' or '1' or 's':
            findtypeloc = 2
        elif resulttype == 'champ number' or '3' or 'championship number' or 'c':
            findtypeloc = 1
        elif resulttype == 'region' or '5' or 'z':
            findtypeloc = 5
        elif resulttype == 'nat' or '6' or 'nation' or 'nationality' or 't':
            findtypeloc = 6
        elif resulttype == 'light wind rating' or '7' or 'l':
            findtypeloc = 7
        elif resulttype == 'medium wind rating' or '8' or 'm':
            findtypeloc = 8
        elif resulttype == 'high wind rating' or '9' or 'h':
            findtypeloc = 9
        elif resulttype == 'ranking' or '10' or 'r':
            findtypeloc = 11
        elif resulttype == 'overall rating' or '11' or 'o':
            findtypeloc = 10
        elif resulttype == 'events completed' or '12' or 'e':
            findtypeloc = 12
        elif resulttype == 'date of last event' or '13' or 'd':
            findtypeloc = 13
        elif resulttype == '14' or 'a':
            findtypeloc = -1
            i = []
            for x in range(14):
                i.append(self.currcolumn[x][row])
            result = ', '.join(i)
        else:
            findtypeloc = 0

        if findtypeloc > -1:
            result = self.currcolumn[findtypeloc][row]
        return result

    def getcolumn(self, columnnum):
        onecolumn = self.currcolumn[columnnum]
        return onecolumn

    def getsailorid(self, fieldnum, term, *data):

        term = str(term)
        locations = base.multiindex(self.currcolumn[fieldnum], term)
        if len(locations) == 0:
            print(f'A sailor could not be found with {term} in field number {fieldnum}')
            working = True
            while working:
                inp = base.cleaninput('Please type in a sailor id \nor press enter to make a new sailor '
                                      '\nor press \'p\' to get a list of all sailor id\'s', 's', charlevel=2)
                if inp == '':
                    from Hosts import Hosts
                    host = Hosts()
                    a = host.makenewsailor()
                    if not a[0]:
                        working = True
                    else:
                        return a[1]
                elif inp.lower() in self.currcolumn[0]:
                    return inp
                elif inp.lower().strip() == 'p':
                    for line in self.currcolumn[0]:
                        print(line)
                else:
                    print('\n That sailor id could not be found')

            raise 'That term could not be found'
        elif len(locations) == 1:
            index = int(str(locations[0]))
            sailorid = self.currcolumn[0][index]
            return sailorid
        else:
            if data == ():
                names = []
                for x in range(0, len(locations)):
                    nameparts = (self.currcolumn[3][locations[x]], self.currcolumn[4][locations[x]])
                    names.append(' '.join(nameparts))
                print(f'The search term \'{term}\' is ambiguous'
                      '\nBelow is a list of names for that sailor')
                for x in range(0, len(locations)):
                    string = (str(x+1), ' - ', names[x])
                    print((''.join(string)))
                finallocation = locations[int(input('Please enter the number of '
                                                    'the correct sailor you are searching for: ')) - 1]
                index = int(finallocation[0])
                sailorid = self.currcolumn[0][index]
                return sailorid
            else:
                pointstracker = []
                sailorids = []
                dates = []
                sailorinfos = []
                sailors = len(locations)

                for x in range(sailors):
                    pointstracker.append(0.0)
                    sailorids.append(self.currcolumn[0][locations[x]])
                    dates = self.getinfo(sailorids[x], 'd')
                    sailorinfos.append(self.getinfo(sailorids[x], 'a'))

                diff = (max(dates) - min(dates)) / 100
                pointstracker[dates.index(max(dates))] += diff
                pointstracker[dates.index(min(dates))] -= diff

                for item in data:
                    for x in range(sailors):
                        if item in sailorinfos[x]:
                            pointstracker[x] += 1
                index = locations[pointstracker.index(max(pointstracker))]
                sailorid = self.currcolumn[0][index]
                return sailorid

    def updatesinglevalue(self, term, row, column, bypass=False):
        if 1 <= column <= 6 or bypass or column == 13:
            self.currcolumn[column][row] = term
            self.autosavefile()
        else:
            print('this change is not allowed please try again')

    def autosavefile(self):
        filename = ''.join((self.universe, '-', str(self.sessiontime), '.csv'))
        file = ''.join((self.folder, filename))
        with open(file, 'w', newline='') as csvfile:  # saves the filr
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar=',', quoting=csv.QUOTE_MINIMAL)
            curr = []
            # print(len(self.currcolumn))
            for x in range(0, len(self.currcolumn[0])):  # number of rows
                for y in range(0, len(self.currcolumn)):  # number of columns
                    # print(f'y = {y}  x = {x}')
                    curr.append(self.currcolumn[y][x])  # assembls the row
                spamwriter.writerow(curr)  # writes the row
                curr = []  # clears the row for the next one

        hostfileold = self.opencsv(self.hostfile)
        if hostfileold[1][0] == str((self.versionnumber + 1)):  # checks how to record the temporry save
            with open(self.hostfile, 'w', newline='') as csvfile:  # works as if its a second or more auto save
                spamwriter = csv.writer(csvfile, delimiter=',',
                                        quotechar=',', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow(hostfileold[0])
                spamwriter.writerow([hostfileold[1][0], hostfileold[1][1], hostfileold[1][2], base.hashfile(file)])
                for x in range(2, len(hostfileold)):
                    spamwriter.writerow(hostfileold[x])
        else:
            with open(self.hostfile, 'w', newline='') as csvfile:  # first auto save
                spamwriter = csv.writer(csvfile, delimiter=',',
                                        quotechar=',', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow(hostfileold[0])
                spamwriter.writerow([self.versionnumber + 1, self.sessiontime, filename, base.hashfile(file)])
                for x in range(1, len(hostfileold)):
                    spamwriter.writerow(hostfileold[x])

    def mansavefile(self):
        self.autosavefile()
        newfilename = ''.join((self.folder, self.universe, '-', str(self.sessiontime - 1), '.csv'))
        os.rename(''.join((self.folder, self.universe, '-', str(self.sessiontime), '.csv')), newfilename)

        hostfileold = self.opencsv(self.hostfile)
        with open(self.hostfile, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar=',', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(hostfileold[0])
            spamwriter.writerow([hostfileold[1][0], hostfileold[1][1], newfilename, hostfileold[1][3]])
            for x in range(2, len(hostfileold)):
                spamwriter.writerow(hostfileold[x])
        self.sessiontime = time()
        self.versionnumber += 1

    def __updatevalue(self, term, row, column, bypass=False):
        if 1 <= column <= 6 or bypass or column == 13:
            self.currcolumn[column][row] = term

    def addsailor(self, sailid, first, sur, champ, sailno, region, nat):
        starting = (self.elo.deviation - 100 * 5)
        thousand = datetime.date(2000, 1, 1)
        now = datetime.date.today()
        day = now - thousand
        if not base.multiindex(self.currcolumn[0], sailid):
            self.__addline([sailid, champ, sailno, first, sur, region, nat, starting, starting, starting, starting,
                            (len(self.currcolumn[0])), 1, day.days])
            return True
        else:
            print('That sailor id already exists')
            print(f'The original sailors information is: {self.getinfo(sailid,"a")}')
            print('\n1. Append "-1" to the new sailor id and proceed to add'
                  '\n2. Abort adding new sailor id')
            inp = base.cleaninput('Which of those options do you want to use:', 'i', rangelow=1, rangehigh=2)
            if inp == 1:
                sailid += '-1'
                count = 1
                unique = False
                while not unique:
                    if sailid in self.currcolumn[0]:
                        sailid = sailid[:-(len(str(count)))]
                        count += 1
                        sailid += count
                    else:
                        unique = True
                self.__addline([sailid, champ, sailno, first, sur, region, nat, starting, starting, starting, starting,
                               (len(self.currcolumn[0])), 1, day.days])
                return True, sailid
            else:
                return False, ''

    def __addline(self, array):
        for x in range(len(array)):
            self.currcolumn[x].append(str(array[x]))
        self.autosavefile()
