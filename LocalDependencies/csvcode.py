from sys import path
import csv
from time import time
import os
from LocalDependencies.ELO import EloCalculations
from LocalDependencies.General import General
from binascii import unhexlify
base = General()


class Csvcode:
    def __init__(self):
        print('\nUniverse selection tool:')
        print('Avalible universes are:')

        column = self.opencsv(''.join((path[0], '\\universes\\', 'host.csv',)), transpose=True)  # imports the universes file and stores it in [column][row]

        for x in range(1, len(column[0])):
            print(column[0][x])  # prints all the names of the universes

        universe = input('\nPlease enter the name of the universe you would like to acess or (n) for a new universe:').lower()
        while not(universe in column[0] or universe.upper() == 'N'):
            print('\nThat universe name was not valid, please try again')  # keeps trying unitl a valid input is entered
            universe = input('\nPlease enter the name of the universe you would like to acess or (n) for a new universe:').lower()

        self.universe = self.__linkuniverse(universe)  # passes it to the link unicerse for the universe to be imported
        self.sessiontime = int(time())  # sets the time for any new files

        if universe != self.universe:
            column = self.opencsv(''.join((path[0], '\\universes\\', 'host.csv',)), transpose=True)  # if a new universe has been created, reopen the hist csv file
        # print(column) #--debuging line

        universeloc = column[0].index(self.universe)  # gets the location of the universe inside of the host file
        self.passhash = column[3][universeloc]  # saves the universe password hash to the object
        self.passsalt = unhexlify(column[5][universeloc])  # saves the universe password salt to the object
        self.elo = EloCalculations(column[2][universeloc], column[4][universeloc])  # initzallises the elo object with the universes numbers
        self.deviation = column[1][universeloc]  # saves the deviation

        self.adminrights()  # sees whether the user should have admin rights

    def __linkuniverse(self, universe):
        if universe.upper() == 'N':
            universe = self.__makeuniverse()  # checks whether to make a universe and makes it if needed

        try:  # used to cath any file opening erros, probable to much inside of the 'try' tho
            self.folder = ''.join((path[0], '\\universes\\', universe, '\\'))  # TODO comments from here
            self.hostfile = ''.join((self.folder, 'host-', universe, '.csv'))  # TODO make admin rights work

            rows = self.opencsv(self.hostfile)  # opens the csv with the [rows][columns]

            self.basefile = ''.join((self.folder, rows[1][2]))  # sets the objects current file location
            self.versionnumber = int(rows[1][0])  # sets the version number for the current open file
            mostrecentdatafilehash = rows[1][3]  # gets the hash of the most current file
            print('{} universe opened and running\n'.format(universe))
            rows = self.opencsv(self.basefile, transpose=True)  # imports the current file
            # print(self.basefile) # debugging line
            # print(mostrecentdatafilehash) # debugging line
            # print(base.hashfile(self.basefile)) # debugging line
            if base.hashfile(self.basefile) != mostrecentdatafilehash and mostrecentdatafilehash != '0':  # checks the integrity of the current file
                raise ValueError('The most recent data file is not as expected')

        except FileNotFoundError:
            raise 'There was a error loading the file, the program will now exit '

        basecolumn = [x for x in rows if x != []]  # filters through the current file and ignores empty lines
        self.currcolumn = basecolumn  # saves the filtered version to the object
        # self.cleanup - this will go through universe host and look for identical md5 hash and if there is, delete the older one TODO make this
        return universe

    def __makeuniverse(self):
        name = base.cleaninput('\nPlease enter your new ranking universe name:', 's', charlevel=1)  # gets the universe name

        direc = ''.join((path[0], '\\universes\\', name,))  # figures out the path of the new universe
        if os.path.exists(direc):  # checks whether that universe exists
            raise Exception('This universe already exists, please try again')
        else:
            os.mkdir(direc)
        hostfile = (direc, '\\', 'host-', name, '.csv')  # creats the universes host file
        curtime = str(int(time()))  # gets the current time, rounded to an integar and in form of a string
        firstfilename = ''.join((name, '-', curtime, '.csv'))  # creats the name for the first file
        firstfile = ''.join((direc, '\\', firstfilename))  # creats the directory of that file
        universe = name  # sets the universe variable to name, so code later can be simple copied

        with open(firstfile, 'w', newline='') as csvfile:  # writes the current file  without any sailors
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar=',', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['sailorID', 'champNum', 'sailNo', 'Firstname', 'Surname', 'Region', 'nat',
                                 'lightRating', 'midRating', 'heavyRating', 'overallRating',
                                 'rank', 'events', 'lastEventDate'])

        with open(''.join(hostfile), 'w', newline='') as csvfile:  # creats the host file
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar=',', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['versionNumber', 'creationDate', 'fileName', 'md5'])
            spamwriter.writerow(['1', curtime, firstfilename, base.hashfile(firstfile)])  # adds the row and has hashed the file

        temp = base.cleaninput('\nPlease enter a password for this universe:', 'pn')  # makes a passowrd and returns the hash and salt
        self.passhash = temp[0]  # saves the salt and hash
        self.passsalt = temp[1]

        starting = base.cleaninput('\nWhat would you like the average rating of this '
                                   'universe to be?(450-3100)(default: 1500):',
                                   'i', rangehigh=3100, rangelow=450)
        k = base.cleaninput('\nWhat would you like the speed of rating change '
                            'to be?(0.3 - 4)(Recomended: 1):',
                            'f', rangelow=0.3, rangehigh=4)  # random comment
        # generic input collecting

        with open(''.join((path[0], '\\universes\\host.csv')), 'a', newline='') as csvfile:  # writes all the inputs to the master host file
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar=',', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow([name, starting, (starting / 5 + 100), self.passhash, k, self.passsalt, ''])

        print('{} universe has been created'.format(name))
        return universe

    def opencsv(self, fileloc, transpose=False):
        with open(fileloc, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            x = 0
            rows = []

            for line in spamreader:  # for each line in the csv
                rows.append(line[0])  # append the raw string of the line to the output
                rows[x] = rows[x].split(',')  # takes the raw string and splits itnto an array
                x += 1

        if transpose:  # if this param is true it will turn the method of adressing from [row][column] to [column][row]
            column = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
            for x in range(0, len(rows)):
                for y in range(0, len(rows[0])):
                    column[y].append(rows[x][y])
            return column
        else:
            return rows

    def adminrights(self):
        self.admin = base.cleaninput(('Press (enter) to skip entering a password'
                                     '\nor enter the admin password for the universe {}:'.format(self.universe)),
                                     'pr', correcthash=self.passhash,
                                     salt=self.passsalt)  # checks whether the user should have admin eights

    def getinfo(self, sailorid: str, resulttype: str):
        try:
            row = self.currcolumn[0].index(sailorid)  # figures out what row the sailor id it
        except ValueError:
            raise('the sailor id {} could not be found'.format(sailorid))

        resulttype.lower().strip()  # turns the result type sting into the best format

        result = ''  # pycharm doesnt like me if i dont put this

        if resulttype == 'name' or '2':
            findtypeloc = -1  # makes sure the next bit will be bypassed
            result = ' '.join((self.currcolumn[3][row], self.currcolumn[4][row]))  # adds the 2 names with a space in the middle
        elif resulttype == 'sail number' or '1' or 's':
            findtypeloc = 2  # the column location of the data
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
        elif resulttype == '14' or 'a' or 'all':
            findtypeloc = -1  # bypasses next stage
            i = []
            for x in range(14):
                i.append(self.currcolumn[x][row])
            result = ', '.join(i)  # bassicly outputs the raw csv line
        else:
            findtypeloc = 0

        if findtypeloc > -1:  # pull the data from the row and column decided earlier
            result = self.currcolumn[findtypeloc][row]
        return result

    def getcolumn(self, columnnum):  # no idea why this is here
        onecolumn = self.currcolumn[columnnum]
        return onecolumn

    def getsailorid(self, fieldnum, term, *data):

        term = str(term)  # makes sure the term to be searched for is a string

        locations = base.multiindex(self.currcolumn[fieldnum], term)  # finds all instances of the term in the data

        if len(locations) == 0:  # deals with no sailor being found with that data
            print(f'\nA sailor could not be found with {term} in field number {fieldnum}')
            working = True
            while working:
                inp = base.cleaninput('\nPlease type in a sailor id \nor press (enter) to make a new sailor'
                                      '\n or press (t) to try again '  # TODO code the try again mode
                                      '\nor press (p) to get a list of all sailor id\'s:', 's', charlevel=2)
                if inp == '':
                    from LocalDependencies.Hosts import Hosts  # yes this is really bad becuse this is a dependency for the thing i imported so potential for circular reference
                    host = Hosts()  # initzalises a new object of it
                    a = host.makenewsailor()  # makes a new sailor
                    # print(a)  # debug line
                    if not a[0]:  # checks whether the sailor was sucessfully made
                        working = True  # makes the user try again
                    else:
                        return a[1]  # returns the sailor id just made
                elif inp.lower() in self.currcolumn[0]:  # checks if what the user eneter is a sailor id that exists
                    return inp
                elif inp.lower().strip() == 'p':  # lists all sailor id's
                    print('')
                    for line in self.currcolumn[0]:
                        print(line)
                elif inp.lower().strip() == 't':
                    pass
                else:
                    print('\n That sailor id could not be found')

            raise 'That term could not be found'
        elif len(locations) == 1:  # if the sailor could be found
            index = int(str(locations[0]))
            sailorid = self.currcolumn[0][index]
            return sailorid
        else:  # if  multiple sailors are found
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

    def __updatevalue(self, term: float | str | int | bool | bytes, row: str | int, column: int, bypass=False):
        term = str(term)
        if type(row) == str:
            row = self.currcolumn[0].index(row)
        if 1 <= column <= 6 or bypass or column == 13:
            self.currcolumn[column][row] = term

    def addsailor(self, sailid, first, sur, champ, sailno, region, nat) -> tuple[bool, str]:
        starting = ((self.elo.deviation - 100) * 5)
        day = base.dayssincetwothousand()
        if not base.multiindex(self.currcolumn[0], sailid):
            self.__addline([sailid, champ, sailno, first, sur, region, nat, starting, starting, starting, starting,
                            (len(self.currcolumn[0])), 0, day])
            return True, sailid
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
                               (len(self.currcolumn[0])), 1, day])
                return True, sailid
            else:
                return False, ''

    def __addline(self, array):
        for x in range(len(array)):
            self.currcolumn[x].append(str(array[x]))
        self.autosavefile()

    def addrace(self, wind: int, sailorids: list, postitions: list,):
        emptylist = [['', 50, 50]]

        for x in range(0, 2):
            currats = []
            if x == 0:
                if wind == 1:
                    infocode = 'l'
                    columnnum = 7
                elif wind == 2:
                    infocode = 'm'
                    columnnum = 8
                else:
                    infocode = 'h'
                    columnnum = 9
            else:
                infocode = 'o'
                columnnum = 10
            for sailor in sailorids:
                currats.append(self.getinfo(sailor, infocode))
            newrat = self.elo.cycle(currats, emptylist, postitions)
            for z in range(0, len(newrat)):
                self.__updatevalue(newrat[z], sailorids[z], columnnum, bypass=True)
            self.autosavefile()

    def endevent(self, sailorids: list, daysago: int):
        eventday = base.dayssincetwothousand() - daysago
        eventreward = 10
        totalsailors = len(self.currcolumn[0]) - 1
        totalcost = eventreward * len(sailorids)
        individualcost = totalcost / (totalsailors - len(sailorids))
        if individualcost > 50:
            individualcost = 50
        for sailor in sailorids:
            curr = int(self.getinfo(sailor, 'e'))
            curr += 1
            temp = float(self.getinfo(sailor, 'o'))
            temp += eventreward
            self.__updatevalue(curr, sailor, 12, bypass=True)
            self.__updatevalue(eventday, sailor, 13, bypass=True)
            self.__updatevalue(temp, sailor, 10, bypass=True)
        for othersailor in self.currcolumn[0]:
            if othersailor not in sailorids:
                temp = float(self.getinfo(othersailor, 'o'))
                temp -= individualcost
                self.__updatevalue(temp, othersailor, 10, bypass=True)
        self.autosavefile()
        self.ranksailors()
        direc = ''.join((path[0], '\\universes\\', self.universe,'\\events'))  # figures out the path of the new universe
        if os.path.exists(direc):  # checks whether that universe exists
            raise Exception('This universe already exists, please try again')
        else:
            os.mkdir(direc)

    def ranksailors(self):
        valid = self.currcolumn
        for x in range((len(valid)-1), 0, -1):  # goes through backwards
            if valid[x][12] < 5:
                valid.pop(x)
        valid = base.SortOnElement(valid, 10)
        for x in range(0, len(valid)):
            self.__updatevalue((x+1), valid[x][0], 11, bypass=True)
        self.autosavefile()
