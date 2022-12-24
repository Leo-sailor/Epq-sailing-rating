from sys import path, exit
import csv
from time import time
import os
from hashlib import md5, sha256
import datetime
from Dependencies.ELO import EloCalculations

class Csvcode:
    def __init__(self):
        print('\nUniverse selection tool:')
        print('Avalible universes are:')

        column = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
        rows = self.opencsv(''.join((path[0], '\\universes\\', 'host.csv',)))
        for x in range(0, len(rows)):
            for y in range(0, len(rows[0])):
                column[y].append(rows[x][y])

        for x in range(1, len(column[0])):
            print(column[0][x])

        universe = input('\nPlease enter the name of the universe you would like to acess (N for a new universe):').lower()
        while not(universe in column[0] or universe.upper() == 'N'):
            print('\nThat universe name was not valid, please try again')
            universe = input('Please enter the name of the universe you would like to acess (N for a new universe):').lower()
        self.universe = universe
        self.__linkuniverse(universe)

        universeloc = column[0].index(universe)
        self.passhash = column[4][universeloc]
        elo = EloCalculations(column[3][universeloc],column[6][universeloc])


        self.adminrights()


    def __linkuniverse(self, universe):
        if universe.upper() == 'N':
            universe = self.__makeuniverse

        try:
            self.folder = ''.join((path[0], '\\universes\\', universe, '\\'))
            self.hostfile = ''.join((self.folder,'host-', universe, '.csv'))

            rows = self.opencsv(self.hostfile)

            self.basefile = ''.join((self.folder, rows[1][2]))
            print('{} universe opened and running\n'.format(universe))

            rows = self.opencsv(self.basefile)

        except FileNotFoundError:
            exit('There was a error loading the file, the program will now exit ')

        self.basecolumn = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

        for x in range(0, len(rows)):
            for y in range(0, len(rows[0])):
                self.basecolumn[y].append(rows[x][y])
        self.currcolumn = self.basecolumn
        #self.cleanup - this will go through universe host and look for identical md5 hash and if there is delete the older one

    def __makeuniverse(self):
        name = input('please enter your new ranking universe name')
        name.lower().strip()
        direc = ''.join((path[0], '\\universes\\', name,))
        if os.path.exists(direc):
            raise Exception('This universe already exists, please try again')
        else:
            os.mkdir(direc)
        hostfile = (direc, '\\', 'host-', name, '.csv')
        curtime = str(time())
        firstfile = (direc, '\\', name, '-', curtime, '.csv')
        universe = name

        with open(''.join(firstfile), 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar=',', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['sailorID', 'champNum', 'sailNo', 'Firstname', 'Surname', 'Region', 'nat',
                                 'lightRating', 'midRating', 'heavyRating', 'overallRating',
                                 'rank', 'events', 'lastEventDate'])

        with open(''.join(hostfile), 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar=',', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['versionNumber', 'creationDate', 'fileName', 'md5'])
            spamwriter.writerow(['1', curtime, firstfile, self.hashfile(firstfile)])

        same = False
        while not (same):
            passwordA = ''
            passwordB = ''
            passwordA = input('\nPlease enter a password for this universe:')
            passwordB = input('Please it again to confirm:')
            same = passwordB == passwordA
            if not (same):
                print('\nThose passwords did not match, Please try again')
        self.passhash = self.passwordhash(passwordB)

        starting = int(input('\nWhat would you like the average rating of this '
                             'universe to be?(450-3100)(default: 1500)'))
        while starting > 3100 or starting < 450:
            print('\nThat value was not accepted, Please Try Again')
            starting = int(input('What would you like the average rating of this '
                                 'universe to be?(450-3100)(default: 1500)'))

        k = float(input('\nWhat would you like the speed of rating change '
                             'to be?(0.3 - 4)(Recomended: 1)'))
        while k > 4 or k < 0.3:
            print('\nThat value was not accepted, Please Try Again')
            k = float(input('\nWhat would you like the speed of rating change '
                             'to be?(0.3 - 4)(Recomended: 1)'))

        with open('../universes/host.csv', 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar=',', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow([name, 0, starting, (starting / 5 + 100), self.passhash, self.hashfile(hostfile), k])

        print('{} universe has been created'.format(name))
        return universe

    def opencsv(self,fileloc):
        with open(fileloc, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            x = 0
            rows = []

            for row in spamreader:
                rows.append(row[0])
                rows[x] = rows[x].split(',')
                x += 1
        return rows

    def adminrights(self):
        done = False
        while not(done):
            print('press enter to skip entering a password')
            inp = input('or enter the admin password for the universe {}:'.format(self.universe))
            if inp == '':
                self.admin = False
                done = True
            elif self.passwordhash(inp) == self.passhash:
                self.admin = True
                done = True
            else:
                print('\nThat password was incorrect, please try again')


    def getinfo(self, sailorid, resulttype):
        # what the fuck is this function doing here,
        # I started it and didn't know why or what for, watch me code this identically somewhere else
        try:
            row = self.currcolumn[0].index(sailorid)
        except ValueError:
            raise('the sailor id {} could not be found'.format(sailorid))

        resulttype.lower().strip()
        done = False
        if resulttype == 'name' or '2':
            findtypeloc = -1
            result = ' '.join((self.currcolumn[3][row],self.currcolumn[4][row]))
        elif resulttype == 'sail number' or '1' or 's':
            findtypeloc = 2
        elif resulttype == 'champ number' or '3' or 'championship number' or 'c':
            findtypeloc = 1
        elif resulttype == 'region' or '5' or 'z':
            findtypeloc = 5
        elif resulttype == 'nat' or '6' or 'nation' or 'nationality' or 't':
            findtypeloc = 6
        elif resulttype == 'Light wind rating' or '7' or 'l':
            findtypeloc = 7
        elif resulttype == 'medium wind rating' or '8' or 'm':
            findtypeloc = 8
        elif resulttype == 'High wind rating' or '9' or 'h':
            findtypeloc = 9
        elif resulttype == 'ranking' or '10' or 'r':
            findtypeloc = 11
        elif resulttype == 'Overall rating' or '11' or 'o':
            findtypeloc = 10
        elif resulttype == 'Events completed' or '12' or 'e':
            findtypeloc = 12
        elif resulttype == 'Date of last event' or '13' or 'd':
            findtypeloc = 13
        else:
            findtypeloc = 0

        if findtypeloc > -1:
            result = self.currcolumn[findtypeloc][row]
        return result

    def hashfile(self, file):
        str2hash = open(file).read()
        result = md5(str2hash.encode()).hexdigest()
        return result

    def passwordhash(self, password):
        hashed = sha256(password.encode()).hexdigest()
        return hashed

    def getcolumn(self, columnnum):
        onecolumn = self.column[columnnum]
        return onecolumn

    def findsailor(self, fieldnum, term):
        from Dependencies.General import General
        base = General()

        term = str(term)
        locations = base.multiindex(self.currcolumn[fieldnum], term)
        if len(locations) == 0:
            return 'Error: Term not found'
        elif len(locations) == 1:
            return int(str(locations[0]))
        else:
            names = []
            for x in range(0, len(locations)):
                nameparts = (self.currcolumn[3][locations[x]], self.currcolumn[4][locations[x]])
                names.append(' '.join(nameparts))
            print('That search term is ambiguous'
                  '\nBelow is a list of names for that sailor')
            for x in range(0, len(locations)):
                string = (str(x+1), ' - ', names[x])
                print((''.join(string)))
            finallocation = locations[int(input('Please enter the number of '
                                                'the correct sailor you are searching for: ')) - 1]
            return int(str(finallocation[0]))

    def updatesinglevalue(self, term, row, column):
        self.currcolumn[column][row] = term
        self.savefile()

    def savefile(self):
        curtime = time()
        with open(''.join((self.folder, self.universe, '-', curtime, '.csv')), 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar=',', quoting=csv.QUOTE_MINIMAL)
            curr = []
            for x in range(0,len(self.currcolumn[0])): #number of rows
                for y in range(0,len(self.currcolumn)): # number of columns
                    curr.append(self.currcolumn[y][x])
                spamwriter.writerow(curr)
                curr = []
    def __updatevalue(self, term, row, column):
        self.currcolumn[column][row] = term

