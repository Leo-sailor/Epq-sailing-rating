from sys import path
import csv
from time import time
import os
from LocalDependencies.ELO import EloCalculations
from LocalDependencies.General import General
from LocalDependencies.Csv_custom import Csvnew  # implement this into current
from binascii import unhexlify
base = General()


class Csvcode:
    def __init__(self):
        self.admin = False
        self.cfile = ''
        print('\n UNIVERSE SELECTION TOOL:')
        print('Avalible universes are:')
        host = Csvnew(''.join((path[0], '\\universes\\', 'host.csv',)))  # imports the universes file and stores it in [column][row]

        host.printcolumn(0, True, 0)  # prints all the names of the universes

        universe = input('\nPlease enter the name of the universe you would like to acess or (n) for a new universe:').lower()
        while not(universe in host.getcolumn(0) or universe.upper() == 'N'):
            print('\nThat universe name was not valid, please try again')  # keeps trying unitl a valid input is entered
            universe = input('\nPlease enter the name of the universe you would like to acess or (n) for a new universe:').lower()

        self.universe = self.__linkuniverse(universe)  # passes it to the link unicerse for the universe to be imported
        self.sessiontime = int(time())  # sets the time for any new files

        if universe != self.universe:
            host = Csvnew(''.join((path[0], '\\universes\\', 'host.csv',)))  # if a new universe has been created, reopen the hist csv file
        # print(column) #--debuging line

        universeloc = host.getrownum(self.universe, 0)  # gets the location of the universe inside of the host file
        self.passhash = host.getcell(universeloc, 3)  # saves the universe password hash to the object
        self.passsalt = unhexlify(host.getcell(universeloc, 5))  # saves the universe password salt to the object
        self.elo = EloCalculations(host.getcell(universeloc, 2), host.getcell(universeloc, 4))  # initzallises the elo object with the universes numbers
        self.deviation = host.getcell(universeloc, 1)  # saves the deviation

        self.adminrights()  # sees whether the user should have admin rights

    def __linkuniverse(self, universename):
        if universename.upper() == 'N':
            universename = self.__makeuniverse()  # checks whether to make a universe and makes it if needed

        try:  # used to cath any file opening erros, probable to much inside of the 'try' tho
            self.folder = ''.join((path[0], '\\universes\\', universename, '\\'))
            self.hostfile = ''.join((self.folder, 'host-', universename, '.csv'))  # TODO make admin rights work

            universehost = Csvnew(self.hostfile)  # opens the csv with the [rows][columns]

            self.basefile = ''.join((self.folder, universehost.getcell(1, 2)))  # sets the objects current file location
            self.versionnumber = int(universehost.getcell(1, 0))  # sets the version number for the current open file
            mostrecentdatafilehash = universehost.getcell(1, 3)  # gets the hash of the most current file
            print('{} universe opened and running\n'.format(universename))
            self.file = Csvnew(self.basefile, universe=universename)  # imports the current file
            # print(self.basefile) # debugging line
            # print(mostrecentdatafilehash) # debugging line
            # print(base.hashfile(self.basefile)) # debugging line
            if base.hashfile(self.basefile) != mostrecentdatafilehash and mostrecentdatafilehash != '0':  # checks the integrity of the current file
                raise ValueError('The most recent data file is not as expected')

        except FileNotFoundError:
            raise 'There was a error loading the file, the program will now exit '
        # filters through the current file and ignores empty lines
        # self.cleanup - this will go through universe host and look for identical md5 hash and if there is, delete the older one TODO make this
        return universename

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

    def adminrights(self):
        print('\n ADMIN RIGHTS')
        self.admin = base.cleaninput(('Press (enter) to skip entering a password'
                                     '\nor enter the admin password for the universe {}:'.format(self.universe)),
                                     'pr', correcthash=self.passhash,
                                     salt=self.passsalt)
        return self.admin  # checks whether the user should have admin eights

    def getinfo(self, sailorid: str, resulttype: str):
        try:
            row = self.file.getrownum(sailorid, 0)  # figures out what row the sailor id it
        except ValueError:
            raise('the sailor id {} could not be found'.format(sailorid))

        findtypeloc = self.getfieldnumber(resulttype)

        if findtypeloc == -1:
            result = ' '.join((self.file.getcell(row, 3), self.file.getcell(row, 4)))  # adds the 2 names with a space in the middle
        elif findtypeloc == -2:
            i = []
            for x in range(14):
                i.append(self.file.getcell(row, x))
            result = ', '.join(i)  # bassicly outputs the raw csv line
        elif findtypeloc > -1:  # pull the data from the row and column decided earlier
            result = self.file.getcell(row, findtypeloc)
        else:
            result = '0.1'
        return result

    def getfieldnumber(self, resulttype):
        resulttype.lower()
        if resulttype == 'name' or resulttype == 'n':
            findtypeloc = -1  # makes sure the next bit will be bypassed
        elif resulttype == 'sail number' or resulttype == 's':
            findtypeloc = 2  # the column location of the data
        elif resulttype == 'champ number' or resulttype == 'championship number' or resulttype == 'c':
            findtypeloc = 1
        elif resulttype == 'region' or resulttype == 'z':
            findtypeloc = 5
        elif resulttype == 'nat' or resulttype == 'nation' or resulttype == 'nationality' or resulttype == 't':
            findtypeloc = 6
        elif resulttype == 'light wind rating' or resulttype == 'l':
            findtypeloc = 7
        elif resulttype == 'medium wind rating' or resulttype == 'm':
            findtypeloc = 8
        elif resulttype == 'high wind rating' or resulttype == 'h':
            findtypeloc = 9
        elif resulttype == 'ranking' or resulttype == 'r':
            findtypeloc = 11
        elif resulttype == 'overall rating' or resulttype == 'o':
            findtypeloc = 10
        elif resulttype == 'events completed' or resulttype == 'e':
            findtypeloc = 12
        elif resulttype == 'date of last event' or resulttype == 'd':
            findtypeloc = 13
        elif resulttype == '14' or resulttype == 'a' or resulttype == 'all':
            findtypeloc = -2  # bypasses next stage
        else:
            findtypeloc = 0
        return findtypeloc

    def getsailorid(self, fieldnum: str | int, term: str | int, *data) -> str:

        term = str(term)  # makes sure the term to be searched for is a string
        while term[0] == '0':
            term = term[1:]
        if type(fieldnum) == str:
            # print(fieldnum)
            fieldnum = self.getfieldnumber(fieldnum)
            # print(fieldnum)
        if fieldnum == -1:
            locationsnew = []
            newterm = term.split(' ', 1)
            locations = base.multiindex(self.file.getcolumn(3), newterm[0])
            print(newterm)
            print(locations)
            if len(locations) == 0:
                pass
            else:
                for location in locations:
                    if newterm[1] == (self.file.getcell(location, 4)):
                        locationsnew.append(location)
                locations = locationsnew
        else:
            locations = base.multiindex(self.file.getcolumn(fieldnum), term)  # finds all instances of the term in the data

        if len(locations) == 0:  # deals with no sailor being found with that data
            print(f'\nA sailor could not be found with {term} in field number {fieldnum}')
            working = True
            while working:
                inp = base.cleaninput('\nPlease type in a sailor id \nor press (enter) to make a new sailor'
                                      '\nor press (t) to try again ' 
                                      '\nor press (p) to get a list of all sailor id\'s:', 's', charlevel=2)
                if inp == '':
                    from LocalDependencies.Hosts import HostScript  # yes this is really bad becuse this is a dependency for the thing i imported so potential for circular reference
                    if fieldnum == -1:
                        a = HostScript.makenewsailor(name=term)
                    elif fieldnum == 1:
                        a = HostScript.makenewsailor(champ=term)
                    elif fieldnum == 2:
                        a = HostScript.makenewsailor(sailno=term)
                    else:
                        a = HostScript.makenewsailor()
                    del HostScript
                    # print(a)  # debug line
                    if not a[0]:  # checks whether the sailor was sucessfully made
                        working = True  # makes the user try again
                    else:
                        return a[1]  # returns the sailor id just made
                elif inp.lower() in self.file.getcolumn(0):  # checks if what the user eneter is a sailor id that exists
                    return inp
                elif inp.lower().strip() == 'p':  # lists all sailor id's
                    print('')
                    for line in self.file.getcolumn(0):
                        print(line)
                elif inp.lower().strip() == 't':
                    inp = input('\nPlease enter the search term again:')
                    return self.getsailorid(fieldnum, inp, data)
                else:
                    print('\n That sailor id could not be found')

            raise 'That term could not be found'
        elif len(locations) == 1:  # if the sailor could be found
            index = int(str(locations[0]))
            sailorid = self.file.getcell(index, 0)
            return sailorid
        else:  # if  multiple sailors are found
            if data == ():
                names = []
                for x in range(0, len(locations)):
                    nameparts = (self.file.getcell(locations[x], 3), self.file.getcell(locations[x], 4))
                    names.append(' '.join(nameparts))
                print(f'\nThe search term \'{term}\' is ambiguous'
                      '\nBelow is a list of names for that sailor')
                for x in range(0, len(locations)):
                    string = (str(x+1), ' - ', names[x])
                    print((''.join(string)))
                finallocation = locations[(base.cleaninput('\nPlease enter the number of the correct sailor you are '
                                                           'searching for: ', 'i',  1, len(locations))) - 1]
                index = int(finallocation)
                sailorid = self.file.getcell(index, 0)
                return sailorid
            else:
                pointstracker = []
                sailorids = []
                dates = []
                sailorinfos = []
                sailors = len(locations)

                for x in range(sailors):
                    pointstracker.append(0.0)
                    sailorids.append(self.file.getcell(locations[x], 0))
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
                sailorid = self.file.getcell(index, 0)
                return sailorid

    def addsailor(self, sailid: str, first: str, sur: str, champ, sailno, region: str, nat: str) -> tuple[bool, str]:
        starting = ((self.elo.deviation - 100) * 5)
        day = 0
        if not base.multiindex(self.file.getcolumn(0), sailid):
            self.file.addrow([sailid, champ, sailno, first, sur, region, nat, starting, starting, starting, starting,
                              0, 0, day])
            return True, sailid
        else:
            print('That sailor id already exists')
            print(f'The original sailors information is: {self.getinfo(sailid,"a")}')
            print('\n(1). Append "-1" to the new sailor id and proceed to add'
                  '\n(2). Abort adding new sailor id')
            inp = base.cleaninput('Which of those options do you want to use:', 'i', rangelow=1, rangehigh=2)
            if inp == 1:
                sailid += '-1'
                count = 1
                unique = False
                while not unique:
                    if sailid in self.file.getcolumn(0):
                        sailid = sailid[:-(len(str(count)))]
                        count += 1
                        sailid += count
                    else:
                        unique = True
                    self.file.addrow([sailid, champ, sailno, first, sur, region, nat, starting, starting, starting, starting,
                                      0, 0, day])
                return True, sailid
            else:
                return False, ''

    def addrace(self, wind: int, sailorids: list, postitions: list, days: int, imported: bool = False):
        for x in range(0, 2):
            currats = []
            currevents = []
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
                currats.append(float(self.getinfo(sailor, infocode)))
                currevents.append(int(self.getinfo(sailor, 'e')))
            newrat = self.elo.cycle(currats, currevents, postitions)
            for z in range(0, len(newrat)):
                self.file.updatevalue(newrat[z], sailorids[z], columnnum, bypass=True)
            self.file.autosavefile()
        direc = ''.join((path[0], '\\universes\\', self.universe, '\\events'))  # figures out the path of the new universe
        if not (os.path.exists(direc)):  # checks whether that universe exists
            os.mkdir(direc)
        made = False
        count = 0
        if not imported:
            while not made:
                newdirec = ''.join((direc, '\\', str(base.dayssincetwothousand()-days), '-', str(count), '.csv'))
                if os.path.exists(newdirec):
                    count += 1
                else:
                    with open(newdirec, 'w', newline='') as csvfile:
                        spamwriter = csv.writer(csvfile, delimiter=',',
                                                quotechar=',', quoting=csv.QUOTE_MINIMAL)
                        spamwriter.writerow(['wind', str(wind)])
                        spamwriter.writerow(['sailor-id', 'position'])
                        for x in range(len(sailorids)):
                            spamwriter.writerow([sailorids[x], postitions[x]])
                    made = True

    def endevent(self, sailorids: list, daysago: int):
        eventday = base.dayssincetwothousand() - daysago
        eventreward = 10
        totalsailors = len(self.file.getcolumn(0)) - 1
        totalcost = eventreward * len(sailorids)
        try:
            individualcost = totalcost / (totalsailors - len(sailorids))
        except ZeroDivisionError:
            individualcost = 10
        if individualcost > 50:
            individualcost = 50
        for sailor in sailorids:
            curr = int(self.getinfo(sailor, 'e'))
            curr += 1
            temp = float(self.getinfo(sailor, 'o'))
            temp += eventreward
            self.file.updatevalue(curr, sailor, 12, bypass=True)
            if eventday > int(self.getinfo(sailor, 'd')):
                self.file.updatevalue(eventday, sailor, 13, bypass=True)
            self.file.updatevalue(temp, sailor, 10, bypass=True)
        for x in range(1, len(self.file.getcolumn(0))):
            othersailor = self.file.getcell(x, 0)
            if othersailor not in sailorids:
                temp = float(self.getinfo(othersailor, 'o'))
                temp -= individualcost
                temp = round(temp, 1)
                self.file.updatevalue(temp, othersailor, 10, bypass=True)
            if float(self.getinfo(othersailor, 'o')) < 0.1:
                self.file.updatevalue(0.1, othersailor, 10, bypass=True)
            if float(self.getinfo(othersailor, 'h')) < 0.1:
                self.file.updatevalue(0.1, othersailor, 9, bypass=True)
            if float(self.getinfo(othersailor, 'm')) < 0.1:
                self.file.updatevalue(0.1, othersailor, 8, bypass=True)
            if float(self.getinfo(othersailor, 'l')) < 0.1:
                self.file.updatevalue(0.1, othersailor, 7, bypass=True)
        self.file.autosavefile()
        self.file.sortoncol(10, reverse=True, targetcol=11, excluderows=0, greaterthan=[12, 5])
        self.file.autosavefile()
