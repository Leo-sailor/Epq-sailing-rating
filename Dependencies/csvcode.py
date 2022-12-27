from sys import path
import csv
from time import time
import os
from hashlib import md5, sha256
from Dependencies.ELO import EloCalculations


class Csvcode:
    def __init__(self):
        print('\nUniverse selection tool:')
        print('Avalible universes are:')

        column = self.opencsv(''.join((path[0], '\\universes\\', 'host.csv',)),transpose=True)

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

            rows = self.opencsv(self.basefile)
            if self.hashfile(self.basefile) != mostrecentdatafilehash and mostrecentdatafilehash != '0':
                raise 'The most recent data file is not as expected'

        except FileNotFoundError:
            raise 'There was a error loading the file, the program will now exit '

        self.basecolumn = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

        for x in range(0, len(rows)):
            for y in range(0, len(rows[0])):
                self.basecolumn[y].append(rows[x][y])
        self.basecolumn = [x for x in self.basecolumn if x != []]
        self.currcolumn = self.basecolumn
        #self.cleanup - this will go through universe host and look for identical md5 hash and if there is delete the older one
        return universe

    def __makeuniverse(self):
        name = input('please enter your new ranking universe name:').lower()
        allowed = ['a','b','c','d','e','f','g','h','i','j','k',
                   'l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5',
                   '6','7','8','9','.','_','\'','(',')',':']
        name = (x for x in name if x in allowed)
        name = ''.join(name)
        direc = ''.join((path[0], '\\universes\\', name,))
        if os.path.exists(direc):
            raise Exception('This universe already exists, please try again')
        else:
            os.mkdir(direc)
        hostfile = (direc, '\\', 'host-', name, '.csv')
        curtime = str(int(time()))
        firstfilename = ''.join((name, '-', curtime, '.csv'))
        firstfile = ''.join((direc, '\\',firstfilename))
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
            spamwriter.writerow(['1', curtime, firstfilename, self.hashfile(firstfile)])

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

        try:
            starting = int(input('\nWhat would you like the average rating of this '
                             'universe to be?(450-3100)(default: 1500):'))
        except ValueError:
            print('\nThat input was not a integer')
            starting = 50000
        while starting > 3100 or starting < 450:
            print('\nThat value was not accepted, Please Try Again')
            try:
                starting = int(input('What would you like the average rating of this '
                                 'universe to be?(450-3100)(default: 1500):'))
            except ValueError:
                print('\nThat input was not a integer')
                starting = 50000

        try:
            k = float(input('\nWhat would you like the speed of rating change '
                             'to be?(0.3 - 4)(Recomended: 1):'))
        except ValueError:
            print('\nThat input was not a number')
            k = 100
        while k > 4 or k < 0.3:
            print('\nThat value was not accepted, Please Try Again')
            try:
                k = float(input('\nWhat would you like the speed of rating change '
                                'to be?(0.3 - 4)(Recomended: 1):'))
            except ValueError:
                print('\nThat input was not a number')
                k = 500

        with open(''.join((path[0],'\\universes\\host.csv')), 'a', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar=',', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow([name, starting, (starting / 5 + 100), self.passhash, k, ''])

        print('{} universe has been created'.format(name))
        return universe

    def opencsv(self,fileloc,transpose=False):
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
        try:
            row = self.currcolumn[0].index(sailorid)
        except ValueError:
            raise('the sailor id {} could not be found'.format(sailorid))

        resulttype.lower().strip()

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
        return str(result)

    def passwordhash(self, password):
        hashed = sha256(password.encode()).hexdigest()
        return hashed

    def getcolumn(self, columnnum):
        onecolumn = self.currcolumn[columnnum]
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
        self.autosavefile()

    def autosavefile(self):
        filename = ''.join((self.universe, '-', str(self.sessiontime), '.csv'))
        file = ''.join((self.folder, filename))
        with open(file, 'w', newline='') as csvfile: #saves the filr
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar=',', quoting=csv.QUOTE_MINIMAL)
            curr = []
            # print(len(self.currcolumn))
            for x in range(0,len(self.currcolumn[0])): # number of rows
                for y in range(0,len(self.currcolumn)): # number of columns
                    # print(f'y = {y}  x = {x}')
                    curr.append(self.currcolumn[y][x]) # assembls the row
                spamwriter.writerow(curr)  #writes the row
                curr = [] #clears the row for the next one

        hostfileold = self.opencsv(self.hostfile)
        if hostfileold[1][0] == str((self.versionnumber + 1)): #checks how to record the temporry save
            with open(self.hostfile, 'w', newline='') as csvfile: # works as if its a second or more auto save
                spamwriter = csv.writer(csvfile, delimiter=',',
                                        quotechar=',', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow(hostfileold[0])
                spamwriter.writerow([hostfileold[1][0], hostfileold[1][1], hostfileold[1][2], self.hashfile(file)])
                for x in range(2,len(hostfileold)):
                    spamwriter.writerow(hostfileold[x])
        else:
            with open(self.hostfile, 'w', newline='') as csvfile: # first auto save
                spamwriter = csv.writer(csvfile, delimiter=',',
                                        quotechar=',', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow(hostfileold[0])
                spamwriter.writerow([self.versionnumber + 1, self.sessiontime, filename, self.hashfile(file)])
                for x in range(1,len(hostfileold)):
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

    def __updatevalue(self, term, row, column):
        self.currcolumn[column][row] = term
