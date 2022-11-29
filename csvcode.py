import sys
import csv
from General import General
import pandas as pd
base = General()
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
                    x = x+1

            print('{}.csv opened and running\n'.format(universe))

        except:
            sys.exit('There was a error loading the file, the program will now exit ')

        self.column = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

        for x in range(0, len(rows)):
            for y in range(0, len(rows[0])):
                self.column[y].append(rows[x][y])

    def getinfo(self, findtype, finddata, resulttype):
        result = 5
        return result

    def getcolumn(self, columnNum):
        oneColumn = self.column[columnNum]
        return oneColumn

    def findsailor(self,fieldnum,term):
        term = str(term)
        locations = base.multiIndex(self.column[fieldnum],term)
        if len(locations)== 0:
            return 'Error: Term not found'
        elif len(locations) == 1:
            return int(str(locations[0]))
        else:
            names = []
            for x in range(0, len(locations)):
                nameparts = (self.column[3][locations[x]],self.column[4][locations[x]])
                names.append(' '.join(nameparts))
            print('That search term is ambiguous\nBelow is a list of names for that sailor')
            for x in range(0, len(locations)):
                string = (str(x+1),' - ',names[x])
                print((''.join(string)))
            finallocation = locations[int(input('Please enter the number of '
                                                'the correct sailor you are searching for: ')) - 1]
            return int(str(finallocation[0]))

    def updatevalue(self, term, row, column):
        db = pd.read_csv(self.uniloc, dtype=str)
        db.iloc[row-1,column] = term
        db.to_csv(self.uniloc, index=False)
