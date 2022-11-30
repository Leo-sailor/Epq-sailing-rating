import sys
import csv
import pandas as pd


class Csvcode:
    def __init__(self, universe):
        if universe.upper() == 'N':
            name = input('please enter your new ranking universe name')
            name.lower().strip()
            file = (name, '.csv')
            universe = name

            with open(''.join(file), 'w', newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=',',
                                        quotechar=',', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow(['sailorID', 'champNum', 'sailNo', 'Firstname', 'Surname', 'Region', 'nat',
                                     'lightRating', 'midRating', 'heavyRating', 'overallRating', 'rank', 'events'])

            starting = int(input('\nWhat would you like the average rating of this '
                                 'universe to be?(450-3100)(default: 1500)'))

            while starting > 3100 or starting < 450:
                print('\nThat value was not accepted, Please Try Again')
                starting = int(input('What would you like the average rating of this '
                                     'universe to be?(450-3100)(default: 1500)'))

            with open('host.csv', 'w', newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=',',
                                        quotechar=',', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow([name, 0, starting, (starting/5+100)])

            print('{}.csv has been created'.format(name))

        try:
            file = (universe, '.csv')
            self.uniloc = ''.join(file)
            with open(''.join(file), newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                x = 0
                rows = []

                for row in spamreader:
                    rows.append(row[0])
                    rows[x] = rows[x].split(',')
                    x += 1

            print('{}.csv opened and running\n'.format(universe))

        except:
            sys.exit('There was a error loading the file, the program will now exit ')

        self.column = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

        for x in range(0, len(rows)):
            for y in range(0, len(rows[0])):
                self.column[y].append(rows[x][y])

    def getinfo(self, findtype, finddata, resulttype):
        # what the fuck is this function doing here,
        # i started it and didnt know why or what for, watch me code this identically somewhere else
        findtype.lower().strip()
        if findtype == 'name' or '2':
            name = findtype.split(' ')
            # run the whole thing in here but different
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
        return result

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
