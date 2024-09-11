from sys import path
from time import time
import os
from LocalDependencies.ELO import EloCalculations
import LocalDependencies.Framework.base_func as base
import LocalDependencies.General as custom_funcs
from LocalDependencies.Csv_custom import csv_new, csv_base
import LocalDependencies.leo_dataclasses as dat
from LocalDependencies.Framework.constants import constants
from binascii import unhexlify
from pickle import dump as _dump
from LocalDependencies.Framework.base_ui import callback as ui_obj
from LocalDependencies.Framework.logger import log
from LocalDependencies.Imports import prep_table_info, clear_dnc
import random
c = constants()
UNIVERSES_ = '\\universes\\'
sys_path = path[0]
col_width = [15, 10, 9, 11, 9, 8, 5, 12, 11, 13, 15, 6, 8, 15, 10]
log = log()
log.queue(0, 'main_core imported successfully')


class UniverseHost:
    global sys_path

    def __init__(self, ui: ui_obj, universe: str = None, password: str = None):
        self.admin = False
        self.cfile = ''
        self.ui = ui
        self.ui.display_text('\n UNIVERSE SELECTION TOOL:\nAvailable universes are:')
        host = csv_base(''.join((sys_path, UNIVERSES_, 'host.csv',)))  # stores it in [column][row]

        self.ui.display_text(host.print_column(0, True, 0))  # prints all the names of the universes
        if universe is None:
            universe = self.ui.g_str(
                '\nPlease enter the name of the universe you would like to access or (n) for a new universe: ').lower()
        while not (universe in host.get_column(0) or universe.upper() == 'N'):
            self.ui.display_text('\nThat universe name was not valid, please try again')  # keeps trying until a
            # valid input is entered
            universe = self.ui.g_str('Please enter the name of the universe you would like to access or (n) for a new '
                                     'universe: ').lower()

        self.universe = self.__link_universe(universe)  # passes it to the link universe for the universe to be imported
        self.session_time = int(time())  # sets the time for any new files
        log.queue(0, 'session time set', self.session_time)

        if universe != self.universe:
            log.queue(2, 'new universe hase been created', self.universe)
            host = csv_base(''.join(
                (sys_path, UNIVERSES_, 'host.csv',)))  # if a new universe has been created, reopen the hist csv file

        universe_loc = host.get_row_num(self.universe, 0)  # gets the location of the universe inside the host file
        self.pass_hash = unhexlify(host.get_cell(universe_loc, 3))  # saves the universe password hash to the object
        self.pass_salt = unhexlify(host.get_cell(universe_loc, 5))  # saves the universe password salt to the object
        self.elo = EloCalculations(host.get_cell(universe_loc, 2), host.get_cell(universe_loc, 4))
        self.deviation = host.get_cell(universe_loc, 1)  # saves the deviation
        log.queue(0, 'all info extracted from host file', self.__dict__)
        self.admin_rights(password)  # sees whether the user should have admin rights
        self.file.similar_names(base.similar_names, col=3)

    def __link_universe(self, universe_name: str) -> str:
        if universe_name.upper() == 'N':
            universe_name = self.__make_universe()  # checks whether to make a universe and makes it if needed

        try:  # used to cath any file opening errors, probable too much inside of the 'try' tho
            self.folder = ''.join((sys_path, '\\universes\\', universe_name, '\\'))
            self.host_file = ''.join((self.folder, 'host-', universe_name, '.csv'))
            universe_host = csv_base(self.host_file)  # opens the csv with the [rows][columns]

            self.base_file = ''.join((self.folder, universe_host.get_cell(1, 2)))
            self.version_number = int(universe_host.get_cell(1, 0))
            self.ui.display_text('{} universe opened and running\n'.format(universe_name))
            self.file = csv_new(self.base_file, universe=universe_name)  # imports the current file
            log.queue(2, ' universe opened and running', universe_name)

        except FileNotFoundError as err:
            log.log(5, ' critical error in opening files - program will exit', err)
            raise FileNotFoundError('There was a error loading the file, the program will now exit ')
        # filters through the current file and ignores empty lines
        self.cleanup()
        return universe_name

    def __make_universe(self) -> str:

        name = self.ui.g_str('\nPlease enter your new ranking universe name: ',
                             char_level=1).lower()  # gets the universe name
        log.queue(2, 'making universe started', name)
        directory = ''.join((sys_path, UNIVERSES_, name,))  # figures out the path of the new universe
        if os.path.exists(directory):  # checks whether that universe exists
            log.log(5, 'adding universe failed - name already taken', directory)
            raise FileExistsError('This universe already exists, please try again')
        else:
            os.mkdir(directory)
        host_file = (directory, '\\', 'host-', name, '.csv')  # creates the universes host file
        cur_time = str(int(time()))  # gets the current time, rounded to an integer and in form of a string
        first_file_name = ''.join((name, '-', cur_time, '.csv'))  # creates the name for the first file
        first_file = ''.join((directory, '\\', first_file_name))  # creates the directory of that file
        universe = name  # sets the universe variable to name, so code later can be simple copied
        cfile = csv_base(first_file)
        cfile.add_row(['sailorID', 'champNum', 'sailNo', 'Firstname', 'Surname', 'Region', 'nat',
                       'lightRating', 'midRating', 'heavyRating', 'overallRating',
                       'rank', 'events', 'lastEventDate'])
        host = csv_base(''.join(host_file))
        host.add_row(['versionNumber', 'creationDate', 'fileName', 'md5'])
        host.add_row(['1', cur_time, first_file_name, base.hashfile(first_file)])

        self.pass_hash, self.pass_salt = self.ui.g_make_password_with_salt(
            '\nPlease enter a password for this universe: ', 'bcrypt')

        log.queue(0, 'password creation success', (self.pass_hash, self.pass_salt))
        starting = self.ui.g_int('\nWhat would you like the average rating of this universe to be?(450-3100)'
                                 '(default: 1500): ', range_high=3100, range_low=450, )
        k = self.ui.g_float('\nWhat would you like the speed of rating change to be?(0.3 - 4)(Recommended - 1): ',
                            range_low=0.3, range_high=4)  # random comment
        # generic input collecting
        big_host = csv_base(''.join((sys_path, '\\universes\\host.csv')))
        big_host.add_row([name, starting, (starting / 5 + 100), self.pass_hash, k, self.pass_salt, ''])
        log.queue(0, ' host file created')
        self.ui.display_text('{} universe has been created'.format(name))
        return universe

    def __str__(self, row_to_sort: int = 11) -> str:
        increasing_sort_vals = [11, 12, 0]
        if row_to_sort in increasing_sort_vals:
            table = base.sort_on_element(self.file.row_first, row_to_sort, False, zero_is_big=True)
        else:
            table = base.sort_on_element(self.file.row_first, row_to_sort, True, zero_is_big=True)
        return '\n'.join([''.join(
            [f'{"".join((item, "                        "))[:col_width[val]]}' for val, item in enumerate(row)]) for row
            in table])

    def admin_rights(self, password: str = None):
        if self.admin:
            self.ui.display_text('Admin rights already exits')
            return self.admin
        if password is not None:  # for when the password is passed into the system
            if base.password_hash(password, 'bcrypt', self.pass_salt)[0] == self.pass_hash:
                self.admin = True
                return True
            elif password == '':
                self.admin = False
                return False
            else:
                self.ui.display_text('\nThat password was incorrect, please try again')
        self.ui.display_text('\n ADMIN RIGHTS')
        self.admin = self.ui.g_password_receive(f'or enter the admin password for the universe {self.universe}: ',
                                                correct_hash=self.pass_hash, hash_method='bcrypt', salt=self.pass_salt)
        log.queue(2, 'password recived with bcrypt', self.admin)
        return self.admin  # checks whether the user should have admin eights

    def cleanup(self):
        log.queue(0, 'cleanup of identical host files triggerd')
        host = csv_base(self.host_file)
        length = host.num_rows()
        hashes = []
        to_remove = []
        to_remove_rows = []
        for x in range(1, length):
            hashed = host.get_cell(x, 3)
            if hashed in hashes:
                file_name = host.get_cell(x, 2)
                to_remove.append(file_name)
                to_remove_rows.append(x)
            else:
                hashes.append(hash)
        for x in range(len(to_remove) - 1, -1, -1):
            file_name = to_remove[x]
            file_loc = ''.join((self.folder, file_name))
            os.remove(file_loc)
            host.remove_row(to_remove_rows[x])
            host.save()
            log.queue(1, 'the following file has been removed in cleanup', to_remove[x])
        log.queue(0, 'cleanup complete')

    def getinfo(self, sailorid: str, result_type: str | int):
        if sailorid == '' or sailorid == 'nan':
            return 'aborted'
        sailorid = sailorid.replace(' ', '-')
        try:
            row = self.file.get_row_num(sailorid, 0)  # figures out what row the sailor id it
        except ValueError:
            log.queue(4, 'sailorid could not be found', sailorid)
            raise IndexError('the sailor id {} could not be found'.format(sailorid))

        find_type_loc = custom_funcs.get_field_number(result_type)

        if find_type_loc == -1:
            result = ' '.join(
                (self.file.get_cell(row, 3), self.file.get_cell(row, 4)))  # adds the 2 names with a space in the middle
        elif find_type_loc == -2:  # case for all info
            i = []
            for x in range(14):
                i.append(self.file.get_cell(row, x))
            result = ', '.join(i)
        elif find_type_loc == -3:  # case for sailor info
            i = []
            for x in [1, 2, 3, 4, 5, 6]:
                i.append(self.file.get_cell(row, x))
            result = ', '.join(i)
        elif find_type_loc > -1:  # pull the data from the row and column decided earlier
            result = self.file.get_cell(row, find_type_loc)
        else:
            result = '0.1'
        log.queue(1, 'sailor info taken without error', (sailorid, find_type_loc, result))
        return result

    def get_data_locations(self, term, field_num) -> list[int]:
        if isinstance(term, list):
            term = ' '.join(term)
        term = str(term)  # makes sure the term to be searched for is a string
        if term.endswith('.0'):
            term = term[:-2]
        if term.endswith('nan'):
            term = term[:-3]
        term.strip('0')
        term.strip()
        if type(field_num) == str:
            field_num = custom_funcs.get_field_number(field_num)
        log.queue(0, 'searching for info', (term, field_num))

        if field_num == -1:  # the exception for if it's a name
            new_term = term.lower().strip().split(' ', 1)
            new_term[0] = base.similar_names(new_term[0])
            try:
                new_term[1] = new_term[1].replace(' ', '-')
            except IndexError:
                breakpoint()
            locations = []
            # locations = [loc for loc,val in enumerate(self.file.get_column(3)) if val == new_term[0]]
            for loc, val in enumerate(self.file.get_column(3)):
                if val == new_term[0]:
                    locations.append(loc)
            locations = [loc for loc in locations if
                         new_term[1].replace('-', '') == (self.file.get_cell(loc, 4).replace('-', ''))]
        else:
            locations = base.multiindex(self.file.get_column(field_num), term)
        log.queue(0, 'sarch completed and found n items', len(locations))
        return locations

    def user_select_sailor(self, term, field_num, return_on_new: bool = False, *data) -> str | int:
        self.ui.display_text(f'\nA sailor could not be found with {term} in field number {field_num}')
        working = True
        log.queue(0, 'forcing user to select a sailor themslevs with no help')
        while working:
            inp = self.ui.g_str('\nPlease type in a sailor id \nor press (n) to make a new sailor'
                                '\nor press (t) to try again '
                                '\nor press (p) to get a list of all sailor id\'s: '
                                '\nor press (q) to exit', char_level=2).lower()
            if inp == 'q':
                log.queue(1, 'operatoin cancelled')
                raise InterruptedError('operation cancelled')
            elif inp == 'n':
                if return_on_new:
                    log.queue(0, 'special case for returning to prev funxton when a new sailor is made')
                    return 0
                log.queue(0, 'start of circular import')
                from LocalDependencies.Hosts import HostScript
                match field_num:
                    case -1:
                        a = HostScript.make_new_sailor(self.ui, name=term)
                    case 1:
                        a = HostScript.make_new_sailor(self.ui, champ=term)
                    case 2:
                        a = HostScript.make_new_sailor(self.ui, sailno=term)
                    case _:
                        a = HostScript.make_new_sailor(self.ui)
                del HostScript
                log.queue(0, 'end of circular import')
                if not a[0]:  # checks whether the sailor was successfully made
                    working = True
                    log.queue(3, 'error while making sailor')  # makes the user try again
                else:
                    return a[1]  # returns the sailor id just made
            elif inp in self.file.get_column(0):  # checks if what the user enter is a sailor id that exists
                return inp
            elif inp.strip() == 'p':  # lists all sailor id's
                self.ui.display_text(self.file.print_column(0, True))
            elif inp.lower().strip() == 't':
                inp = self.ui.g_str('\nPlease enter the search term again: ')
                res = self.get_sailor_id(field_num, inp, return_on_new, *data)
                self.ui.display_text("Success")
                return res
            else:
                self.ui.display_text('\n That sailor id could not be found')

        raise IndexError('That term could not be found')

    def get_sailor_id(self, field_num: str | int, term: str | int, *data) -> str:
        def user_tie_break(locs=None) -> str:
            if locs is None:
                locs = locations
            names = []
            for x in range(0, len(locs)):
                nameparts = (self.file.get_cell(locs[x], 3), self.file.get_cell(locs[x], 4))
                names.append(' '.join(nameparts))
            self.ui.display_text(f'\nThe search term \'{term}\' is ambiguous'
                                 f'\nBelow is a list of names for that sailor'
                                 f'\nThe search term also comes with the data: {data}')
            options = [' - '.join([names[x], self.file.get_cell(locs[x], 1), self.file.get_cell(locs[x], 2)])
                       for x in range(len(locs))]
            final_location = locs[(self.ui.g_choose_options(options, 'Which sailor do you want to select?'))]
            location = int(final_location)
            curr_sailorid = self.file.get_cell(location, 0)
            return curr_sailorid

        def auto_tie_break() -> str:
            log.queue(0, 'automatic tie break triggered')
            breakpoint()
            points_tracker = []
            sailorids = []
            dates = []
            sailor_infos = []
            sailors = len(locations)

            for x in range(sailors):
                points_tracker.append(0.0)
                sailorids.append(self.file.get_cell(locations[x], 0))
                dates.append(int(self.getinfo(sailorids[x], 'd')))
                sailor_infos.append([self.getinfo(sailorids[x], 'p')])
            diff = (max(dates) - min(dates)) / 365
            points_tracker[dates.index(max(dates))] += diff
            points_tracker[dates.index(min(dates))] -= diff

            for item in data:
                for x in range(sailors):
                    sailor_infos[x] = sailor_infos[x][0].split(', ')
                    if str(item) in sailor_infos[x][:7]:
                        points_tracker[x] += 1
            location = locations[
                points_tracker.index(max(points_tracker))]  # gets the location of the sailor with the most points
            if len(set(points_tracker)) != len(points_tracker):  # exception for if  locations have the same max score
                locs = [locations[loc] for loc in base.multiindex(points_tracker, max(points_tracker))]
                log.queue(3, 'failure to choose with automatic tie brek, resorting to user')
                return user_tie_break(locs)  # makes sure there are no duplicates
            curr_sailorid = self.file.get_cell(location, 0)
            log.queue(0, 'automatic tiebreak', (points_tracker, curr_sailorid))
            return curr_sailorid

        # main code for function
        locations = self.get_data_locations(term, field_num)
        log.queue(0, 'locations found for sailor', (locations, term, field_num, data))
        if len(locations) == 0:  # deals with no sailor being found with that data
            return self.user_select_sailor(term, field_num, *data)
        elif len(locations) == 1:  # if the sailor could be found
            index = int(str(locations[0]))
            sailorid = self.file.get_cell(index, 0)
            log.queue(0, 'saior id found', sailorid)
            return sailorid
        else:  # if  multiple sailors are found
            if data == ():
                return user_tie_break()
            else:
                return auto_tie_break()

    def add_sailor(self, sailorid: str, first: str, sur: str, champ, sailno: str, region: str, nat: str) -> tuple[
        bool, str]:
        log.queue(2, 'adding new sailor with info:', (sailorid, first, sur, champ, sailno, region, nat))
        starting = ((self.elo.deviation - 100) * 5)
        day = 0
        if not base.multiindex(self.file.get_column(0), sailorid):  # chcks the sailor id doesnt already exist
            self.file.add_row(
                [sailorid, base.force_int(champ), base.force_int(sailno), first, sur, region, nat, starting, starting,
                 starting,
                 starting,
                 0, 0, day])
            return True, sailorid
        else:
            log.queue(1, 'new sailor id already exists', sailorid)

            x = lambda field: self.getinfo(sailorid, field)
            if (sailorid, first, sur, champ, sailno) == (sailorid, x("f"), x("surname"), x("c"), x("s")):
                return False, sailorid  # TODO: make matcher here better so it catches that 0 == anything
            t = (f'That sailor id already exists \nThe original sailors information is: {self.getinfo(sailorid, "p")}',
                 f'\nThe new sailors information is: {sailorid}, {first} {sur}, {champ} and {sailno}')
            options = ['Append "-1" to the new sailor id and proceed to add', 'Abort adding new sailor id', 'overwrite']
            inp = self.ui.g_choose_options(options, ''.join(t), use_cache = True)
            if inp == 0:
                log.queue(0, 'adding "-1" to the sailor id')
                sailorid += '-1'
                count = 1
                unique = False
                while not unique:
                    if sailorid in self.file.get_column(0):
                        sailorid = sailorid[:-(len(str(count)))]
                        count += 1
                        sailorid += str(count)
                    else:
                        unique = True
                        self.file.add_row(
                            [sailorid, champ, sailno, first, sur, region, nat, starting, starting, starting, starting,
                             0, 0, day])
                return True, sailorid
            elif inp == 2:
                self.file.remove_row(self.file.get_row_num(sailorid, 0))
                self.file.add_row(
                    [sailorid, champ, sailno, first, sur, region, nat, starting, starting, starting, starting,
                     0, 0, day])
                return True, sailorid
            else:
                return False, sailorid

    def process_table(self, table: list[list[str]], event_title: str, nat: str, sailorids: list[str],
                      date: int = None, fullspeed: bool = False) -> dat.Event:
        race_columns = []
        numbers = '0123456789'
        for loc, val in enumerate(table[0]):  # goes through the headers looking for races and the search colum
            sample_val1, sample_val2, is_number = prep_table_info(table[1:], loc)
            if (val[0].upper() == 'R' and val[1] in numbers and is_number) or 'race' in val or \
                    ('unnamed:' in val and is_number and (len(sample_val1) < 2 or len(sample_val2) < 2)):
                race_columns.append(loc)
        table, sailorids = clear_dnc(table, race_columns, sailorids)

        races = []
        if date is None:
            date = self.ui.g_date_int(f"of the last day of {event_title}: ")
        if not fullspeed:
            self.ui.display_text('1 - Light\n2- Medium\n3 - Heavy')
        for race in race_columns:
            if fullspeed:
                wind = random.choice([1, 2, 3])
            else:
                wind = self.ui.g_int(f'What was the wind of {table[0][race]}: ', range_low=1, range_high=3)
            result = [base.force_int(table[x][race]) for x in range(1, len(table))]
            # goes through the table and gets the positions of people, knowing that the table order wont change
            # it them marrys them with theyre sailor ids in order with dat.results
            races.append(dat.Race(dat.Results(sailorids, result), wind, date))
        return dat.Event(races, date, event_title=event_title, nation=nat)

    def import_sailor(self, field: int, data: str, row: list[str], info: dict[str:slice | int | None], nat: str,
                      full_speed: bool = False,
                      *extra_info) -> str:
        if isinstance(data, list):
            data = ' '.join(data)
        sailor_info = [None if x is None else row[x] for x in info.values()]
        for loc, item in enumerate(sailor_info):
            if isinstance(item, list):
                sailor_info[loc] = ' '.join(item)
        if nat is not None:
            try:
                sailor_info[3] = nat
            except IndexError:
                sailor_info.append(nat)
        if data == 'nan':
            return 'nan'
        if data.endswith(' nan'):
            data = data[:-4]
        if len(self.get_data_locations(data, field)) == 0:
            self.ui.display_text(f'creating sailor from {data}')
            log.queue(1, 'creating new sailor', sailor_info)
            res = 0
            if not full_speed:
                res = self.user_select_sailor(data, field, True, full_speed)
            if isinstance(res,
                          int) or full_speed:  # if were going at full speed then we return when were making a new salor
                while True:
                    from LocalDependencies.Hosts import HostScript
                    a = HostScript.make_new_sailor(self.ui, *sailor_info, full_speed=full_speed)
                    del HostScript
                    if a[0] or full_speed:  # checks whether the sailor was successfully made
                        return a[1]  # returns the sailor id just made
            else:
                log.queue(0, 'sailor importing success')
                return res
        else:

            log.queue(0, 'sailor importing success')
            res = self.get_sailor_id(field, data, *sailor_info, *extra_info)
            self.ui.display_text(f'matched {data}, to sailor {res}')
            return res

    def add_event(self, event: dat.Event | None,print_rat_change=None):
        log.queue(2, 'adding event to universe', event)
        old_results = dat.old_results(self)
        if event is None:
            return None
        for race in event:
            self.__add_race(race, old_results)
        self.__end_event(event.all_sailors, event.date)
        if not event.imported:
            export_event(event, self.universe)
        if print_rat_change is None:
            out = self.ui.g_bool('Would you like to print the rating changes from this event')
        else:
            out = print_rat_change
        self.file.set_session()
        log.queue(2, 'event adding success')
        if out:
            self.ui.display_text('Event rating changes:')
            out = []
            for sailor in event.all_sailors:
                out.append(f'{sailor}: light: {old_results.getinfo(sailor, "l")} -> {self.getinfo(sailor, "l")}  '
                           f'medium: {old_results.getinfo(sailor, "m")} -> {self.getinfo(sailor, "m")}\n'
                           f'               heavy: {old_results.getinfo(sailor, "h")} -> {self.getinfo(sailor, "h")}  '
                           f'overall: {old_results.getinfo(sailor, "o")} -> {self.getinfo(sailor, "o")}\n'
                           f'               rank: {old_results.getinfo(sailor, "r")} -> {self.getinfo(sailor, "r")} ')
            self.ui.display_text('\n'.join(out))

    def __add_race(self, race: dat.Race, old_results):
        log.queue(0, ' adding race to the event')
        sailorids = race.results.sailorids
        positions = race.results.positions
        # serious logic error here with cur-rat ending up with 2x as many values
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
            for loc, sailor in enumerate(sailorids):  # gets the current information on all the current sailors
                old_rats.append((float(old_results.getinfo(sailor, column_num)) + (cur_rats[loc] * 3)) / 4)

            new_rat = self.elo.cycle(old_rats, curr_events, positions, cur_rats)  # executes the maths
            log.queue(1, 'race added to file', (sailorids, old_rats, new_rat))
            for z in range(0, len(new_rat)):
                self.file.update_value(new_rat[z], sailorids[z], column_num, bypass=True)
            self.file.auto_save_file()

    def __end_event(self, used_sailorids: list | set, days_ago: int):
        event_day = days_ago
        event_reward = 10
        total_sailors = len(self.file.get_column(0)) - 1
        total_cost = event_reward * len(used_sailorids)
        individual_cost = total_cost / (total_sailors - len(used_sailorids) + 1)
        if individual_cost > 50:
            individual_cost = 50
        for sailor in used_sailorids:
            curr = int(self.getinfo(sailor, 'e'))
            curr += 1
            temp = float(self.getinfo(sailor, 'o'))
            temp += event_reward
            self.file.update_value(curr, sailor, 12, bypass=True)
            if event_day > int(self.getinfo(sailor, 'd')):
                self.file.update_value(event_day, sailor, 13, bypass=True)
            self.file.update_value(temp, sailor, 10, bypass=True)

        for other_sailor in self.file.get_column(0, [0]):
            if other_sailor not in used_sailorids:
                temp = float(self.getinfo(other_sailor, 'o'))
                temp -= individual_cost
                temp = round(temp, 1)
                self.file.update_value(temp, other_sailor, 10, bypass=True)
            if float(self.getinfo(other_sailor, 'o')) < 0.1:
                self.file.update_value(0.1, other_sailor, 10, bypass=True)
            if float(self.getinfo(other_sailor, 'h')) < 0.1:
                self.file.update_value(0.1, other_sailor, 9, bypass=True)
            if float(self.getinfo(other_sailor, 'm')) < 0.1:
                self.file.update_value(0.1, other_sailor, 8, bypass=True)
            if float(self.getinfo(other_sailor, 'l')) < 0.1:
                self.file.update_value(0.1, other_sailor, 7, bypass=True)
        self.file.auto_save_file(force=True)
        self.file.sort_on_col(10, reverse=True, target_col=11, exclude_rows=0, greater_than=[12, c.get('events_till_rank')])
        self.file.auto_save_file()


def export_event(event: dat.Event, universe_name: str):
    directory = ''.join(
        (sys_path, UNIVERSES_, universe_name, '\\events'))  # figures out the path of the new universe
    if not (os.path.exists(directory)):  # checks whether that universe exists
        os.mkdir(directory)
    made = False
    if event.event_title is None:
        date = str((custom_funcs.two_thousand_to_datetime(event.date)))
    else:
        date = event.event_title
    count = 0
    while not made:
        new_directory = ''.join((directory, '\\', date, '-', str(count), '.event'))
        if os.path.exists(new_directory):
            count += 1
        else:
            with open(new_directory, 'xb', ) as event_file:
                _dump(event, event_file, -1)
            made = True
