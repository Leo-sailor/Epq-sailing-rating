from sys import path,exit
import csv
import pandas as pd
from time import time
import os
from hashlib import md5,sha256


class Csvcode:

    def __init__(self, universe):
        if universe.upper() == 'N':
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

            starting = int(input('\nWhat would you like the average rating of this '
                                 'universe to be?(450-3100)(default: 1500)'))

            same = False
            while not(same):
                passwordA = ''
                passwordB = ''
                passwordA = input('\nPlease enter a password for this universe:')
                passwordB = input('Please it again to confirm:')
                same = passwordB == passwordA
                if not(same):
                    print('\nThose passwords did not match, Please try again')

            while starting > 3100 or starting < 450:
                print('\nThat value was not accepted, Please Try Again')
                starting = int(input('What would you like the average rating of this '
                                     'universe to be?(450-3100)(default: 1500)'))

            with open('../universes/host.csv', 'w', newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=',',
                                        quotechar=',', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow([name, 0, starting, (starting/5+100)])

            print('{} universe has been created'.format(name))

        try:
            self.folder = ''.join((path[0], '\\universes\\', universe, '\\'))
            self.hostfile = ''.join((self.folder,'host-', universe, '.csv'))

            with open(self.hostfile, newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                x = 0
                rows = []

                for row in spamreader:
                    rows.append(row[0])
                    rows[x] = rows[x].split(',')
                    x += 1

            self.basefile = ''.join((self.folder, rows[1][2]))
            print('{} universe opened and running\n'.format(universe))

            with open(self.basefile, newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                x = 0
                rows = []

                for row in spamreader:
                    rows.append(row[0])
                    rows[x] = rows[x].split(',')
                    x += 1

        except FileNotFoundError:
            exit('There was a error loading the file, the program will now exit ')

        self.basecolumn = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

        for x in range(0, len(rows)):
            for y in range(0, len(rows[0])):
                self.basecolumn[y].append(rows[x][y])
                
        #self.cleanup - this will go through universe host and look for identical md5 hash and if there is delete the older one

    def getinfo(self, findtype, finddata, resulttype):
        # what the fuck is this function doing here,
        # I started it and didn't know why or what for, watch me code this identically somewhere else
        findtype.lower().strip()
        if findtype == 'name' or '2':
            name = findtype.split(' ')
            # run the whole thing in here but different
            findtypeloc = 2
        elif findtype == 'sail number' or '1':
            findtypeloc = 2
        elif findtype == 'champ number' or '3' or 'championship number':
            findtypeloc = 1
        elif findtype == 'sailorid' or '4' or 'sailor id':
            findtypeloc = 0
        elif findtype == 'region' or '5':
            findtypeloc = 5
        elif findtype == 'nat' or '6' or 'nation' or 'nationality':
            findtypeloc = 6
        else:
            findtypeloc = 8
        result = findtypeloc
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
        from General import General
        base = General()

        term = str(term)
        locations = base.multiindex(self.column[fieldnum], term)
        if len(locations) == 0:
            return 'Error: Term not found'
        elif len(locations) == 1:
            return int(str(locations[0]))
        else:
            names = []
            for x in range(0, len(locations)):
                nameparts = (self.column[3][locations[x]], self.column[4][locations[x]])
                names.append(' '.join(nameparts))
            print('That search term is ambiguous\nBelow is a list of names for that sailor')
            for x in range(0, len(locations)):
                string = (str(x+1), ' - ', names[x])
                print((''.join(string)))
            finallocation = locations[int(input('Please enter the number of '
                                                'the correct sailor you are searching for: ')) - 1]
            return int(str(finallocation[0]))

    def updatevalue(self, term, row, column):
        db = pd.read_csv(self.uniloc, dtype=str)
        db.iloc[row-1, column] = term
        db.to_csv(self.uniloc, index=False)
