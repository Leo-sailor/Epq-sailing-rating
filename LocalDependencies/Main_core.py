from sys import path
from time import time
import os
from LocalDependencies.ELO import EloCalculations
import LocalDependencies.General as Base
from LocalDependencies.Csv_custom import Csvnew, csvBase
import LocalDependencies.leo_dataclasses as dat
from binascii import unhexlify
from pickle import dump as _dump

UNIVERSES_ = '\\universes\\'
sys_path = path[0]
if "teststttt" in sys_path:
    sys_path = sys_path.replace('tests', '')
col_width = [15,10,9,11,9,8,5,12,11,13,15,6,8,15,10]


class UniverseHost:
    global sys_path
    def __init__(self, universe: str=None, password:str=None):
        self.admin = False
        self.cfile = ''
        print('\n UNIVERSE SELECTION TOOL:')
        print('Avalible universes are:')
        host = csvBase(''.join((sys_path, UNIVERSES_, 'host.csv',)))  # stores it in [column][row]

        host.printcolumn(0, True, 0)  # prints all the names of the universes
        if universe is None:
            universe = input(
                '\nPlease enter the name of the universe you would like to acess or (n) for a new universe: ').lower()
        while not (universe in host.getcolumn(0) or universe.upper() == 'N'):
            print('\nThat universe name was not valid, please try again')  # keeps trying unitl a valid input is entered
            universe = input(
                '\nPlease enter the name of the universe you would like to acess or (n) for a new universe: ').lower()

        self.universe = self.__linkuniverse(universe)  # passes it to the link unicerse for the universe to be imported
        self.sessiontime = int(time())  # sets the time for any new files

        if universe != self.universe:
            host = csvBase(''.join(
                (sys_path, UNIVERSES_, 'host.csv',)))  # if a new universe has been created, reopen the hist csv file
        # print(column) #--debuging line

        universeloc = host.getrownum(self.universe, 0)  # gets the location of the universe inside of the host file
        self.passhash = host.getcell(universeloc, 3)  # saves the universe password hash to the object
        self.passsalt = unhexlify(host.getcell(universeloc, 5))  # saves the universe password salt to the object
        self.elo = EloCalculations(host.getcell(universeloc, 2), host.getcell(universeloc, 4))
        self.deviation = host.getcell(universeloc, 1)  # saves the deviation

        self.adminrights(password)# sees whether the user should have admin rights

    def __linkuniverse(self, universe_name: str) -> str:
        if universe_name.upper() == 'N':
            universe_name = self.__makeuniverse()  # checks whether to make a universe and makes it if needed

        try:  # used to cath any file opening erros, probable to much inside of the 'try' tho
            self.folder = ''.join((sys_path, '\\universes\\', universe_name, '\\'))
            self.host_file = ''.join((self.folder, 'host-', universe_name, '.csv'))
            universe_host = csvBase(self.host_file)  # opens the csv with the [rows][columns]

            self.base_file = ''.join((self.folder, universe_host.getcell(1, 2)))  # sets the objects current file location
            self.version_number = int(universe_host.getcell(1, 0))  # sets the version number for the current open file
            most_recent_data_file_hash = universe_host.getcell(1, 3)  # gets the hash of the most current file
            print('{} universe opened and running\n'.format(universe_name))
            self.file = Csvnew(self.base_file, universe=universe_name)  # imports the current file

            if Base.hashfile(self.base_file) != most_recent_data_file_hash and most_recent_data_file_hash != '0':
                raise ValueError('The most recent data file is not as expected')

        except FileNotFoundError:
            raise FileNotFoundError('There was a error loading the file, the program will now exit ')
        # filters through the current file and ignores empty lines
        self.cleanup()
        return universe_name

    def __makeuniverse(self) -> str:
        name = Base.clean_input('\nPlease enter your new ranking universe name: ', str,
                                charlevel=1)  # gets the universe name

        direc = ''.join((sys_path, UNIVERSES_, name,))  # figures out the path of the new universe
        if os.path.exists(direc):  # checks whether that universe exists
            raise FileExistsError('This universe already exists, please try again')
        else:
            os.mkdir(direc)
        hostfile = (direc, '\\', 'host-', name, '.csv')  # creats the universes host file
        curtime = str(int(time()))  # gets the current time, rounded to an integar and in form of a string
        firstfilename = ''.join((name, '-', curtime, '.csv'))  # creats the name for the first file
        firstfile = ''.join((direc, '\\', firstfilename))  # creats the directory of that file
        universe = name  # sets the universe variable to name, so code later can be simple copied
        cfile = csvBase(firstfile)
        cfile.addrow(['sailorID', 'champNum', 'sailNo', 'Firstname', 'Surname', 'Region', 'nat',
                                 'lightRating', 'midRating', 'heavyRating', 'overallRating',
                                 'rank', 'events', 'lastEventDate'])
        host = csvBase(''.join(hostfile))
        host.addrow(['versionNumber', 'creationDate', 'fileName', 'md5'])
        host.addrow(['1', curtime, firstfilename, Base.hashfile(firstfile)])


        temp = Base.clean_input('\nPlease enter a password for this universe: ',
                               'pn')  # makes a passowrd and returns the hash and salt
        self.passhash = temp[0]  # saves the salt and hash
        self.passsalt = temp[1]

        starting = Base.clean_input('\nWhat would you like the average rating of this '
                                   'universe to be?(450-3100)(default: 1500): ',
                                   int, rangehigh=3100, rangelow=450)
        k = Base.clean_input('\nWhat would you like the speed of rating change '
                            'to be?(0.3 - 4)(Recomended - 1): ',
                            float, rangelow=0.3, rangehigh=4)  # random comment
        # generic input collecting
        big_host = csvBase(''.join((sys_path, '\\universes\\host.csv')))
        big_host.addrow([name, starting, (starting / 5 + 100), self.passhash, k, self.passsalt, ''])

        print('{} universe has been created'.format(name))
        return universe

    def __str__(self, row_to_sort: int = 11) -> str:
        header = str(self.file.getrow(0)) + '\n'
        increasing_sort_vals = [11,12,0]
        if row_to_sort in increasing_sort_vals:
            table = Base.sort_on_element(self.file.rowfirst, row_to_sort,False,zero_is_big=True)
        else:
            table = Base.sort_on_element(self.file.rowfirst, row_to_sort,True, zero_is_big=True)
        return header + '\n'.join([''.join([f'{"".join((item,"                        "))[:col_width[val]]}' for val,item in enumerate(row)]) for row in table])

    def adminrights(self, password:str=None):
        if password is not None:
            if Base.passwordhash(password, self.passsalt)[0] == self.passhash:
                self.admin = True
                return True
            elif password == '':
                self.admin = False
                return False
            else:
                print('\nThat password was incorrect, please try again')
        print('\n ADMIN RIGHTS')
        self.admin = Base.clean_input((f'Press (enter) to skip entering a password'
                                      f'\nor enter the admin password for the universe {self.universe}: '),
                                     'pr', correcthash=self.passhash,
                                      salt=self.passsalt)
        return self.admin  # checks whether the user should have admin eights

    def cleanup(self):
        host = csvBase(self.host_file)
        length = host.numrows()
        hashes = []
        toremove = []
        toremoverows = []
        for x in range(1, length):
            hashed = host.getcell(x, 3)
            if hashed in hashes:
                file_name = host.getcell(x, 2)
                toremove.append(file_name)
                toremoverows.append(x)
            else:
                hashes.append(hash)
        for x in range(len(toremove) - 1, -1, -1):
            file_name = toremove[x]
            fileloc = ''.join((self.folder, file_name))
            os.remove(fileloc)
            host.removerow(toremoverows[x])
            host.save()

    def getinfo(self, sailorid: str, resulttype: str|int):
        try:
            row = self.file.getrownum(sailorid, 0)  # figures out what row the sailor id it
        except ValueError:
            raise IndexError('the sailor id {} could not be found'.format(sailorid))

        findtypeloc = Base.getfieldnumber(resulttype)

        if findtypeloc == -1:
            result = ' '.join(
                (self.file.getcell(row, 3), self.file.getcell(row, 4)))  # adds the 2 names with a space in the middle
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

    def get_data_locations(self,term, fieldnum) -> list[int]:

        term = str(term)  # makes sure the term to be searched for is a string
        if term[-2:] == '.0':
            term = term[:-2]
        term.strip('0')
        if type(fieldnum) == str:
            fieldnum = Base.getfieldnumber(fieldnum)

        if fieldnum == -1:  # the exception for if its a name
            newterm = term.lower().split(' ', 1)
            locations = []
            for loc, val in enumerate(self.file.getcolumn(3)):
                score = Base.similar(newterm[0], val)
                if score > 0.7 or val[:2] == newterm[0][:2]:
                    locations.append(loc)
            if len(locations) != 1:
                locations = [loc for loc in locations if newterm[1] == (self.file.getcell(loc, 4))]
        else:
            locations = Base.multiindex(self.file.getcolumn(fieldnum), term)
        return locations

    def user_select_sailor(self,term,fieldnum,return_on_new:bool = False,*data) -> str|int:
        print(f'\nA sailor could not be found with {term} in field number {fieldnum}')
        working = True
        while working:
            inp = Base.clean_input('\nPlease type in a sailor id \nor press (n) to make a new sailor'
                                   '\nor press (t) to try again '
                                   '\nor press (p) to get a list of all sailor id\'s: ', str, charlevel=2).lower()
            if inp == 'n':
                if return_on_new:
                    return 0
                from LocalDependencies.Hosts import HostScript
                match fieldnum:
                    case -1:
                        a = HostScript.makenewsailor(name=term)
                    case 1:
                        a = HostScript.makenewsailor(champ=term)
                    case 2:
                        a = HostScript.makenewsailor(sailno=term)
                    case _:
                        a = HostScript.makenewsailor()
                del HostScript
                # print(a)  # debug line
                if not a[0]:  # checks whether the sailor was sucessfully made
                    working = True  # makes the user try again
                else:
                    return a[1]  # returns the sailor id just made
            elif inp in self.file.getcolumn(0):  # checks if what the user eneter is a sailor id that exists
                return inp
            elif inp.strip() == 'p':  # lists all sailor id's
                print('')
                for line in self.file.getcolumn(0):
                    print(line)
            elif inp.lower().strip() == 't':
                inp = input('\nPlease enter the search term again: ')
                return self.getsailorid(fieldnum, inp,return_on_new, *data)
            else:
                print('\n That sailor id could not be found')

        raise IndexError('That term could not be found')

    def getsailorid(self, fieldnum: str | int, term: str | int, *data) -> str:
        def user_tie_break(locs = None) -> str:
            if locs is None:
                locs = locations
            names = []
            for x in range(0, len(locs)):
                nameparts = (self.file.getcell(locs[x], 3), self.file.getcell(locs[x], 4))
                names.append(' '.join(nameparts))
            print(f'\nThe search term \'{term}\' is ambiguous'
                  '\nBelow is a list of names for that sailor')
            for x in range(0, len(locs)):
                string = (str(x + 1), ' - ', names[x], ' - ', self.file.getcell(locs[x], 1), ' - ',
                          self.file.getcell(locs[x], 2))
                print((''.join(string)))
            finallocation = locs[(Base.clean_input('\nPlease enter the number of the correct sailor you are '
                                                  'searching for: ', int, 1, len(locs))) - 1]
            location = int(finallocation)
            curr_sailorid = self.file.getcell(location, 0)
            return curr_sailorid

        def auto_tie_break() -> str:
            pointstracker = []
            sailorids = []
            dates = []
            sailorinfos = []
            sailors = len(locations)

            for x in range(sailors):
                pointstracker.append(0.0)
                sailorids.append(self.file.getcell(locations[x], 0))
                dates.append(int(self.getinfo(sailorids[x], 'd')))
                sailorinfos.append([self.getinfo(sailorids[x], 'a')])
            diff = (max(dates) - min(dates)) / 365
            pointstracker[dates.index(max(dates))] += diff
            pointstracker[dates.index(min(dates))] -= diff

            for item in data:
                for x in range(sailors):
                    sailorinfos[x] = sailorinfos[x][0].split(', ')
                    if str(item) in sailorinfos[x][:7]:
                        pointstracker[x] += 1
            location = locations[
                pointstracker.index(max(pointstracker))]  # gets the location of the sailor witht he most points
            if len(set(pointstracker)) != len(pointstracker):
                locs = [locations[loc] for loc in Base.multiindex(pointstracker,max(pointstracker))]
                return user_tie_break(locs)# makes sure there are no duplicates
            curr_sailorid = self.file.getcell(location, 0)
            return curr_sailorid
        # main code for function
        locations = self.get_data_locations(term,fieldnum)
        if len(locations) == 0:  # deals with no sailor being found with that data
            return self.user_select_sailor(term, fieldnum,*data)
        elif len(locations) == 1:  # if the sailor could be found
            index = int(str(locations[0]))
            sailorid = self.file.getcell(index, 0)
            return sailorid
        else:  # if  multiple sailors are found
            if data == ():
                return user_tie_break()
            else:
                return auto_tie_break()

    def addsailor(self, sailid: str, first: str, sur: str, champ, sailno, region: str, nat: str) -> tuple[bool, str]:
        starting = ((self.elo.deviation - 100) * 5)
        day = 0
        if not Base.multiindex(self.file.getcolumn(0), sailid):
            self.file.addrow([sailid, int(float(champ)), int(float(sailno)), first, sur, region, nat, starting, starting, starting, starting,
                              0, 0, day])
            return True, sailid
        else:
            print('That sailor id already exists')
            print(f'The original sailors information is: {self.getinfo(sailid, "a")}')
            print('\n(1). Append "-1" to the new sailor id and proceed to add'
                  '\n(2). Abort adding new sailor id')
            inp = Base.clean_input('Which of those options do you want to use: ', int, rangelow=1, rangehigh=2)
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
                    self.file.addrow(
                        [sailid, champ, sailno, first, sur, region, nat, starting, starting, starting, starting,
                         0, 0, day])
                return True, sailid
            else:
                return False, ''

    def processtable(self, table: list[list[str]], field: str, event_title = "the event") -> dat.Event:
        info = {'name': None, 'sail ': None, 'champ': None}
        same_nat = Base.clean_input('Is everyone in the event from the same country',bool)
        nat = None

        if same_nat:
            nat = Base.getnat()
        for val,item in enumerate(table[0]):
            for key in info:
                if key.upper() in item.upper():
                    info[key] = val
        fullspeed = Base.clean_input('do you want sailors to be autocreated to speed up entry ', bool)
        race_columns = []
        fields = {'c': 'champ', 's': 'sail', 'n': 'name'}
        try:
            search_term = fields[field]
        except KeyError:
            search_term = 'name'
        info_column = -255
        numbers = '0123456789'
        for loc,val in enumerate(table[0]): # goes through the headers looking for races and the search colum
            if (val[0]).upper() == 'R' and val[1] in numbers:
                race_columns.append(loc)
            if search_term in val.lower():
                info_column = loc
        if info_column == -255:
            raise IndexError('That term could not be found')
        extra_data_cols = list(range(1, min(race_columns)))

        sailorids = []
        for count,row in enumerate(table[1:]):
            print(f'{count}/{len(table)-1} sailors enterd')
            sailorids.append(self.import_sailor(field, row[info_column],row,info,nat,fullspeed, *[row[item].lower() for item in extra_data_cols]))

        races = []
        chars_to_strip = "abcdefghijklmnopqrstuvwxyz()"
        date = Base.days_since_two_thousand(Base.getdate("date", f"of the last day of {event_title}: "))
        print('1 - Light\n2- Medium\n3 - Heavy')
        for race in race_columns:
            wind = Base.clean_input(f'What was the wind of {table[0][race]}: ', int, 1, 3)
            result = [int(float(table[x][race].lower().strip(chars_to_strip))) for x in range(1, len(table))]
            races.append(dat.Race(dat.Results(sailorids, result), wind, date))
        return dat.Event(races, date,event_title=event_title,nation = nat)

    def import_sailor(self, field, data, row, info,nat,fullspeed=False, *extra_info) -> str:
        sailor_info = [None if x is None else row[x] for x in info.values()]

        if nat is not None:
            sailor_info.append(nat)
        if len(self.get_data_locations(data,field)) == 0:
            res = 0
            if not fullspeed:
                res = self.user_select_sailor(data,field,True,fullspeed)
            if isinstance(res,int) or fullspeed:
                while True:
                    from LocalDependencies.Hosts import HostScript
                    a = HostScript.makenewsailor(*sailor_info,fullspeed=fullspeed)
                    del HostScript
                    if a[0]:  # checks whether the sailor was sucessfully made
                        return a[1]  # returns the sailor id just made
            else:
                return res
        else:
            return self.getsailorid(field,data,*extra_info)

    def add_event(self,event: dat.Event|None):
        old_results = dat.oldResults(self)
        if event is None:
            return None
        for race in event:
            self.__addrace(race,old_results)
        self.__endevent(event.all_sailors, event.date)
        if not event.imported:
            export_event(event)
        to_print = Base.clean_input('Would you like to print the rating chnages from this event', bool)
        self.file.set_session()
        if to_print:
            print('Event rating changes:')
            for sailor in event.all_sailors:
                print(f'{sailor}: light: {old_results.getinfo(sailor, "l")} -> {self.getinfo(sailor,"l")}'
                      f'medium: {old_results.getinfo(sailor, "m")} -> {self.getinfo(sailor, "m")}\n'
                      f'               heavy: {old_results.getinfo(sailor, "h")} -> {self.getinfo(sailor, "h")}'
                      f'overall: {old_results.getinfo(sailor, "o")} -> {self.getinfo(sailor, "o")}\n'
                      f'               rank: {old_results.getinfo(sailor,"r")} -> {self.getinfo(sailor,"r")} ')


    def __addrace(self, race: dat.Race,old_results):
        sailorids = race.results.sailorids
        positions = race.results.positions
        # serious logic error here with currat ending up with 2x as many values
        wind = race.wind
        for x in range(0, 2):
            curr_events = []
            # if this is the run for wind specific rankings
            column_num = wind + 6
            if x == 1:  # override if the run for overalls
                column_num = 10
            cur_rats = []
            old_rats = []
            for sailor in sailorids:  # gets the current information on all the current sailors
                cur_rats.append(float(self.getinfo(sailor, column_num)))
                curr_events.append(int(self.getinfo(sailor, 'e')))
            for sailor in sailorids:  # gets the current information on all the current sailors
                old_rats.append(float(old_results.getinfo(sailor, column_num)))


            newrat = self.elo.cycle(old_rats, curr_events, positions, cur_rats)  # executes the maths

            for z in range(0, len(newrat)):
                self.file.updatevalue(newrat[z], sailorids[z], column_num, bypass=True)
            self.file.autosavefile()

    def __endevent(self, used_sailorids: list | set, daysago: int):
        eventday = daysago
        eventreward = 10
        totalsailors = len(self.file.getcolumn(0)) - 1
        totalcost = eventreward * len(used_sailorids)
        individualcost = totalcost / (totalsailors - len(used_sailorids) + 1)
        if individualcost > 50:
            individualcost = 50
        for sailor in used_sailorids:
            curr = int(self.getinfo(sailor, 'e'))
            curr += 1
            temp = float(self.getinfo(sailor, 'o'))
            temp += eventreward
            self.file.updatevalue(curr, sailor, 12, bypass=True)
            if eventday > int(self.getinfo(sailor, 'd')):
                self.file.updatevalue(eventday, sailor, 13, bypass=True)
            self.file.updatevalue(temp, sailor, 10, bypass=True)

        for othersailor in self.file.getcolumn(0, [0]):
            if othersailor not in used_sailorids:
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

def export_event(self, event: dat.Event):

    direc = ''.join(
        (sys_path, UNIVERSES_, self.universe, '\\events'))  # figures out the path of the new universe
    if not (os.path.exists(direc)):  # checks whether that universe exists
        os.mkdir(direc)
    made = False
    if event.event_title is None:
        date = str((Base.two_thousand_to_datetime(event.date)))
    else:
        date = event.event_title
    count = 0
    while not made:
        newdirec = ''.join((direc, '\\', date, '-', str(count), '.event'))
        if os.path.exists(newdirec):
            count += 1
        else:
            with open(newdirec, 'xb',) as eventfile:
                _dump(event,eventfile,-1)
            made = True
