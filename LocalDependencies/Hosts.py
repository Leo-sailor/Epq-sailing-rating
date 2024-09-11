import pickle
import LocalDependencies.Aditional_func as addFunc
from LocalDependencies.Main_core import UniverseHost
import LocalDependencies.General as Base
from LocalDependencies.Framework import base_func as f_base
from LocalDependencies.Csv_custom import csv_base
import LocalDependencies.leo_dataclasses as dat
import datetime
from LocalDependencies.Framework.constants import constants
from pickle import load as _load
from time import sleep as _sleep
from LocalDependencies.Imports import ImportManager, chose_source
from LocalDependencies.Framework.base_ui import callback as ui_obj
from LocalDependencies.Framework.logger import log
import traceback

c = constants()
log = log()

global universe_csv


class HostScript:
    def __init__(self, ui: ui_obj, *sys_args):
        self.inp_method = ''
        self.input_method_name = ''
        if sys_args is None:
            sys_args = []
        self.args = sys_args
        self.ui = ui

    def set_nat(self):
        nat = None
        if self.ui.g_bool('\nIs everyone in this from the same country'):
            nat = self.ui.g_nat('all of the sailors')
        self.nat = nat

    def torun(self, *args):
        global universe_csv
        if len(args) > 2:
            universe_csv = UniverseHost(self.ui, args[1], args[2])
        else:
            universe_csv = UniverseHost(self.ui)
        self.universe = universe_csv
        self.set_nat()
        while True:
            options = ['add a new event', 'add a new sailor', 'get a sailors information', 'quit',
                       'get sailor info over time', 'print the universe', 'switch universe', 'import sailors',
                       'graph sailors over time', 'change a sailors information', 'Get admin rights',
                       'Add multiple events from files', 'predict a past event']
            choice = self.ui.g_choose_options(options, 'What would you like to do: ') + 1
            log.flush()
            log.queue(2, f'user choses {options[choice - 1]}')
            match choice:
                case 1:
                    event = self.import_event()
                    if event is None:
                        self.ui.display_text('null event')
                    universe_csv.add_event(event)
                case 2:
                    self.make_new_sailor(self.ui)
                case 3:
                    self.get_sailor_info()
                case 4:
                    break
                case 5:
                    self.sailor_rating_over_time()
                case 6:
                    if self.ui.__class__ in ['text_ui', 'test_ui', 'record']:
                        self.ui.display_text(str(universe_csv))
                    else:
                        self.ui.display_table(universe_csv.file.row_first)
                    _sleep(0.5)
                case 7:
                    self.torun()
                    break
                case 8:
                    self.import_sailors(self.ui)
                case 9:
                    self.sailor_rating_over_time()
                case 10:
                    self.edit_sailor_info(universe_csv)
                case 11:
                    universe_csv.admin_rights()
                case 12:
                    self.add_multiple_events()
                case 13:
                    self.pred_past_event()

    def import_sailors(self, ui: ui_obj):
        sailors = set()
        source = chose_source(ui)
        if source == 'F':
            files = ui.g_many_file_locs()
            imp_mgrs = []
            options = ['name', 'sail num', 'champ num']
            option_chosen = self.ui.g_choose_options(options, 'Which column do you want read as a default')
            chosen_data_type = options[option_chosen]
            for file_num, file in enumerate(files):
                ui.display_text(f"Now loading: {file_num + 1} / {len(files)}")
                try:
                    imp = ImportManager(ui, source, file_loc=file, full_speed=True)
                    imp.chosen_data_name = chosen_data_type
                    imp.choose_table()
                    imp_mgrs.append((file, imp))
                    log.flush()
                except Exception as err:
                    ui.display_text(f"Error importing {file}:")
                    traceback.print_exception(err)
                    ui.display_text('Program will now resume with next file')
                    if not c.get('production'):
                        breakpoint()
                        imp = ImportManager(ui, source, file_loc=file, full_speed=True)
                        imp.chosen_data_name = chosen_data_type
                        imp.choose_table()
                        imp_mgrs.append((file, imp))
                    log.flush()
            imp_mgrs.sort(key=lambda mgr: mgr[1].get_data_quantity() * 1000 + len(mgr[1][mgr[1].choose_table()]),
                          reverse=True)
            for num, imp in enumerate(imp_mgrs):
                ui.display_text(f'\nNow importing {num}/{len(imp_mgrs)} {imp[0]}')
                sailors.update(imp[1].import_sailors_to_universe(universe_csv, self.nat))
        else:
            imp_mgr = ImportManager(ui, source)
            sailors += imp_mgr.import_sailors_to_universe(universe_csv)
        ui.display_text(f'The following {len(sailors)} sailors have been imported')
        for line in sailors:
            ui.display_text(universe_csv.getinfo(line, 'p'))

    def pred_past_event(self):
        inp_mgr = ImportManager(self.ui, 'F', quiet = True)
        sailors = inp_mgr.import_sailors_to_universe(universe_csv,nat = self.nat)
        sailor_event_order = [
            (sailor, universe_csv.getinfo(sailor, 'o')) if universe_csv.getinfo(sailor, 'o') != '1500.0' else (
            sailor, '0.0') for sailor in sailors]
        sailor_with_rating = sorted(sailor_event_order,key=lambda x: float(x[1]), reverse=True)
        position_delta = []

        for pos, (sailor, rating) in enumerate(sailor_with_rating):
            if not universe_csv.getinfo(sailor, 'r') in [0, 0.0, '0']:
                position_delta.append((pos+1,sailor_event_order.index((sailor,rating)) +1,sailor,
                                       universe_csv.getinfo(sailor, "name")))
                self.ui.display_text(f'pos: {pos +1} name: {position_delta[-1][3]} sailor-id: {sailor} '
                                     f'rating: {universe_csv.getinfo(sailor, "o")} correct pos: {position_delta[-1][1]}'
                                     f' position delta: {abs(pos+1 - position_delta[-1][1])}')
        if len(position_delta) < 5:
            raise IndexError('Not enough ranked sailors to perform analysis')
        avg_pos_d = sum(abs(s[0]-s[1]) for s in position_delta)/len(position_delta)
        self.ui.display_text(f'Average position error: {avg_pos_d}')
        worst_guess = max(position_delta, key = lambda s: abs(s[0]-s[1]))
        self.ui.display_text(f'worse position delta: {abs(worst_guess[0]-worst_guess[1])} name: {worst_guess[3]} '
                             f'pred: {worst_guess[0]} correct: {worst_guess[1]}')
        self.ui.display_text('position delta: ', position_delta)
        correct_guesses = filter(lambda s: s[0]==s[1],position_delta)
        self.ui.display_text(f'Correct guesses: {len(list(correct_guesses))}')
        for good in list(correct_guesses):
            self.ui.display_text(f' pos: {good[0]} name: {good[3]} sailor-id: {good[2]} ')

        good_guesses = filter(lambda s: abs(s[0] -s[1]) <=2 , position_delta)
        self.ui.display_text(f'good guesses (within 2): {len(list(good_guesses))}')
        for good in list(good_guesses):
            self.ui.display_text(f' pos: {good[0]} name: {good[3]} sailor-id: {good[2]} ')


    def add_multiple_events(self):
        events = []
        files = self.ui.g_many_file_locs()
        imp_mgrs_list = []
        options = ['name', 'sail num', 'champ num']
        option_chosen = self.ui.g_choose_options(options, 'Which column do you want read as a default')
        chosen_data_type = options[option_chosen]
        for file_num, file in enumerate(files):
            self.ui.display_text(f"Now loading: {file_num + 1} / {len(files)}")
            try:
                imp = ImportManager(self.ui, 'F', file_loc=file, full_speed=True)

                imp.chosen_data_name = chosen_data_type
                imp.get_event_info()
                imp_mgrs_list.append((file, imp))
                log.flush()
            except Exception as err:
                self.ui.display_text(f"Error importing {file}:")
                traceback.print_exception(err)
                self.ui.display_text('Program will now resume with next file')
                loc = log.file.split('\\')[:-1]
                loc.append(file.replace('/', '--'))
                with open('\\'.join(loc), 'wb') as f:
                    try:
                        pickle.dump(imp, f)
                    except Exception:
                        pass
        imp_mgrs_list.sort(key=lambda mgr: mgr[1].date)
        for num, imp in enumerate(imp_mgrs_list):
            self.ui.display_text(f'\nNow importing {num}/{len(imp_mgrs_list)} {imp[0]}')
            try:
                events.append(imp[1].to_event(universe_csv, self.nat))
            except Exception as err:
                self.ui.display_text(f"Error importing {imp[1].file_loc}:")
                traceback.print_exception(err)
                self.ui.display_text('Program will now resume with next file')
                loc = log.file.split('\\')[:-1]
                loc.append(imp[1].file_loc.replace('/', '--'))
                with open('\\'.join(loc), 'wb') as f:
                    try:
                        pickle.dump(imp, f)
                    except Exception:
                        pass
        self.ui.display_text(f'The following {len(events)} events have been imported')
        print_rat_change = self.ui.g_bool('Do you want to print the rating changes for each of the events?')
        for event in events:
            self.universe.add_event(event, print_rat_change=print_rat_change)
            self.ui.display_text(f'{event.event_title}: {len(event)} races, {len(event.all_sailors)} sailors')

    def edit_sailor_info(self, universe: UniverseHost):
        info_codes = ['Championship Number', 'Sail Number', 'Name', 'sailorid', 'Total events',
                      'Date of last event', 'Zone/Region', 'Territory/country']
        out_codes = [1, 2, -1, 0, 12, 13, 5, 6]
        selected = self.ui.g_choose_options(info_codes, '\nSAILOR INFO WIZARD\nplease enter type of information you '
                                                        'would like to change')
        change_column = out_codes[selected]
        out_type_name = info_codes[selected]
        inp_method = self.__get_input_method()
        inp = self.ui.g_str(f'Please enter the sailor\'s {self.input_method_name}: ')
        sailorid = universe_csv.get_sailor_id(inp_method, inp)
        name = universe_csv.getinfo(sailorid, 'n')
        if selected in [0, 1, 4]:
            to_change = str(self.ui.g_int(f'What would you like to change {name}\'s {out_type_name} to:  '))
        elif selected == 5:
            to_change = str(self.ui.g_date_int(f'What would you like to change {name}\'s {out_type_name} to:  '))
        else:
            to_change = str(self.ui.g_str(f'What would you like to change {name}\'s {out_type_name} to:  ',
                                          char_level=1))
        if change_column == -1:
            name = to_change.split(' ', 1)
            universe.file.update_value(name[0], sailorid, 3, 0, universe.admin)
            universe.file.update_value(name[1], sailorid, 4, 0, universe.admin)
        else:
            try:
                universe.file.update_value(to_change, sailorid, change_column, 0, universe.admin)
            except PermissionError:
                self.ui.display_text('Permission denied to change this infomation')

    def sailor_rating_over_time(self):
        global universe_csv
        inp_method = self.__get_input_method()
        inp_list = self.ui.g_str(f'Please enter the sailor\'s {self.input_method_name} seperated by commas: ').split(
            ',')
        sailorid = []
        for inp in inp_list:
            sailorid.append(universe_csv.get_sailor_id(inp_method, inp.strip()))
        universe_name = universe_csv.universe
        choice = self.ui.g_choose_options(['All-Time', 'Specific range'], 'What date range would you like')
        if choice == 1:
            start_date = self.ui.g_date_int('of the first day of your range')
            end_date = self.ui.g_date_int('of the last day of your range')
        else:
            start_date = 1
            end_date = 10000000
        info_codes = ['Light wind rating', 'Medium wind rating',
                      'Heavy wind rating', 'Overall rating', 'Rank', 'Total events']
        out_codes = ['l', 'm', 'h', 'o', 'r', 'e']
        selected = self.ui.g_choose_options(info_codes, 'please enter type of information you would like to receive')
        file_loc = addFunc.plot_sailors(start_date, sailorid, out_codes[selected], universe_name, end_date,
                                        info_codes[selected])
        self.ui.display_text(f"Graph file has been saved to : {file_loc}")

    def get_sailor_info(self):
        info_codes = ['Championship Number', 'Sail Number', 'Light wind rating', 'Medium wind rating',
                      'Heavy wind rating', 'Name', 'sailorid', 'Overall rating', 'Rank', 'Total events',
                      'Date of last event', 'Zone/Region', 'Territory/country', 'All', 'Sailor info']
        out_codes = ['c', 's', 'l', 'm', 'h', 'n', 'i', 'o', 'r', 'e', 'd', 'z', 't', 'a', 'S']
        selected = self.ui.g_choose_options(info_codes, '\nSAILOR INFO WIZARD\nplease enter type of information you '
                                                        'would like to receive')
        out_type = out_codes[selected]
        out_type_name = info_codes[selected]

        inp_method = self.__get_input_method()
        inp = self.ui.g_str(f'Please enter the sailor\'s {self.input_method_name}: ')

        sailorid = universe_csv.get_sailor_id(inp_method, inp)
        out = universe_csv.getinfo(sailorid, out_type)

        if out_type == 'd':
            two_thousand = datetime.date(2000, 1, 1)
            out = two_thousand + datetime.timedelta(days=float(out))

        self.ui.display_text(f'\n{inp}\'s {out_type_name} is {out}')

    @staticmethod
    def make_new_sailor(ui: ui_obj, name=None, sailno=None, champ=None, nat=None, full_speed=False):
        if not full_speed:
            ui.display_text('\n NEW SAILOR WIZARD')
        if name is None:
            name = ui.g_str(f'[{sailno}]Please enter the sailor\'s Full name: ', char_level=3)
        try:
            name = name.split(' ', 1)
        except AttributeError:
            breakpoint()
        first = name[0]
        try:
            sur = name[1]
        except IndexError:
            sur = ui.g_str(f'[{name}]Please enter the sailor\'s  surname: ', char_level=3)
        if champ is None:
            if not full_speed:
                champ = str(ui.g_int(f'[{name}]Please enter the sailor\'s Championship number '
                                     '\n(Please enter (000) if the sailor does not have a Champ number): ',
                                     range_high=999, range_low=0))
            else:
                champ = '0'
        elif champ == 'nan':
            champ = '0'
        else:
            champ = str(champ)
        if sailno is None:
            if not full_speed:
                sailno = str(ui.g_int(f'[{name}]Please enter the sailor\'s Sail number \n(Please ignore any letters): ',
                                      range_high=99999, range_low=0))
            else:
                sailno = '0'
        elif sailno == 'nan':
            sailno = '0'
        else:
            sailno = str(sailno)
        if nat is None:
            nat = ui.g_nat(f'{first} {sur}', 1)
        nat = str(nat)
        first = f_base.similar_names(first)
        out = Base.generate_sailor_id(ui, nat, sailno, first, sur)
        sailorid = out[0]
        nat = out[1]
        if nat == 'GBR' and not full_speed:
            regions = ['Scotland', 'London and South-east', 'South-west', 'South', 'Midlands', 'North',
                       'Northern Ireland', 'Wales', 'East', 'Unknown']
            region_codes = ['SC', 'SE', 'SW', 'SO', 'MD', 'NO', 'NI', 'WL', 'EA', 'NA']

            region_index = ui.g_choose_options(regions, f'Please enter {first} {sur}\'s\'s 2 letter RYA region code: ')
            region = region_codes[region_index]

        else:
            region = 'NA'
        sur = sur.replace(' ', '-')
        sur = sur.strip('()0123456789-')
        sur = sur.replace('-nan', '')
        return universe_csv.add_sailor(sailorid, first, sur, champ, sailno, region, nat)

    def add_event_lazy(self):
        inp = 2
        light_race_num = 0
        med = 0
        heavy = 0
        while inp != 1:
            race_num = self.ui.g_int('\nPlease enter the number of races in the event (1-20): ',
                                     range_low=1, range_high=20)
            light_race_num = self.ui.g_int(f'\nPlease enter the number of light wind (0-8kts) races in the event '
                                           f'(0-{race_num}): ', range_high=race_num, range_low=0)
            race_num -= light_race_num
            med = self.ui.g_int(f'Please enter the number of medium wind (9-16kts) races in the event (0-{race_num}): ',
                                range_high=race_num, range_low=0)
            race_num -= med
            heavy = race_num
            inp = self.ui.g_bool(
                f'\nThat means there were\n{light_race_num} light wind races\n{med} medium wind races'
                f'\n{heavy} strong wind races\n')

        days = self.ui.g_date_int('of the last day of the event', latest=datetime.date.today())
        event = dat.Event([], days)
        results_obj = self.__get_ranking('the event')

        for _ in range(light_race_num):
            event.append(dat.Race(results_obj, 1, days))
        for _ in range(med):
            event.append(dat.Race(results_obj, 2, days))
        for _ in range(heavy):
            event.append(dat.Race(results_obj, 3, days))
        return event

    def add_event_proper(self):
        race_num = self.ui.g_int('\nPlease enter the number of races in the event (1-20): ',
                                 range_low=1, range_high=20)
        days = self.ui.g_date_int('of the last day of the event', latest=datetime.date.today())
        event = dat.Event([], days)
        for x in range(race_num):
            race_text = ' '.join(['Race', str(x + 1)])
            self.ui.display_text(f'\n{race_text.upper()} ENTRY WIZARD')
            wind = self.ui.g_choose_options(['light wind - 0-8kts', 'medium wind - 9-16kts', 'strong wind - 17+ kts'],
                                            f'\nPlease enter the wind strength for {race_text}\n')
            wind += 1
            info = self.__get_ranking(race_text)
            event.append(dat.Race(info, wind, days))
        return event

    def add_event_csv(self):  # Legacy function
        race_num = self.ui.g_int('\nPlease enter the number of races in the event (1-20): ',
                                 range_low=1, range_high=20)
        days = self.ui.g_date_int('of the last day of the event', latest=datetime.date.today())
        event = dat.Event([], days)
        for x in range(race_num):
            race_text = ' '.join(['Race', str(x + 1)])
            self.ui.display_text(f'\n{race_text.upper()} ENTRY WIZARD')
            file_loc = self.ui.g_file_loc('r', title=f'Select the file location for {race_text}: ', )
            curr_file = csv_base(file_loc)
            wind = int(curr_file.get_cell(0, 1))

            curr_sailorids = curr_file.get_column(0, excluded_rows=[0, 1])
            positions = [int(x) for x in curr_file.get_column(1, excluded_rows=[0, 1])]
            results_obj = dat.Results(curr_sailorids, positions)
            event.append(dat.Race(results_obj, wind, days))
        return event

    def __get_ranking(self, eventname: str) -> dat.Results:
        self.__get_input_method()
        working = True
        position = 0
        positions = []
        sailorids = []
        raw_inps = []
        speed_print = [['Position'], ['input info'], ['sailor-id']]
        self.ui.display_text("\nPlease do not include sailors that DNC but all other codes"
                             "\nPress (d) when you are done\n"
                             "Press (b) if you want to remove the last sailor\n")
        while working:
            self.ui.display_table(speed_print)
            position += 1
            inp = self.ui.g_str(f"\nPlease enter the {self.input_method_name} of {f_base.ordinal(position)} "
                                f"place in {eventname}: ", ).lower()
            if inp == 'd':
                working = False
            elif inp == 'b':
                position -= 1
                positions.pop(-1)
                speed_print.pop(-1)
                sailorids.pop(-1)
                raw_inps.pop(-1)
            else:
                inp.lower().strip()
                sailor = universe_csv.get_sailor_id(self.inp_method, inp)
                if sailor in sailorids:
                    self.ui.display_text('This sailor has already been entered, please try again')
                    position -= 1
                else:
                    sailorids.append(sailor)
                    positions.append(position)
                    raw_inps.append(inp)
                    speed_print[0].append(str(position))
                    speed_print[1].append(inp)
                    speed_print[2].append(sailor)
        return dat.Results(sailorids, positions)

    def __get_input_method(self):
        self.ui.display_text('INPUT METHOD SELECTION')
        inp_methods = ['c', 'i', 'n', 's']
        if self.inp_method in inp_methods:
            if self.inp_method == 'c':
                self.input_method_name = 'Championship Number'
            elif self.inp_method == 'n':
                self.input_method_name = 'Name'
            elif self.inp_method == 'i':
                self.input_method_name = 'Sailor-id'
            else:
                self.input_method_name = 'Sail Number'
            inp = self.ui.g_bool(f'Your current selected input method is: {self.input_method_name} '
                                 f'\nWould you like to change it?')
            if inp:
                ip = ''
            else:
                ip = self.inp_method
        else:
            ip = ''
        while ip not in inp_methods:
            long_options = ['championship Number', 'Sailor-id', 'Name', 'Sail Number']
            ip = inp_methods[self.ui.g_choose_options(long_options, 'How would you like to enter sailors information?')]
        self.inp_method = ip
        match ip:
            case 'c':
                self.input_method_name = 'Championship Number'
            case 'n':
                self.input_method_name = 'Name'
            case 'i':
                self.input_method_name = 'Sailor-id'
            case _:
                self.input_method_name = 'Sail Number'
        return ip

    @staticmethod
    def import_pickled_event(ui: ui_obj):
        file_loc = '_________'
        while file_loc[-6:] != '.event':
            if file_loc != '_________':
                ui.display_text('that file is not of the correct type, please try again')
            file_loc = ui.g_file_loc()
        with open(file_loc, 'rb') as f:
            event = _load(f)
        return event

    def import_event(self):
        if not universe_csv.admin:
            self.ui.display_text('\nTo add an event you need admin rights')
            if not universe_csv.admin_rights():
                self.ui.display_text('\nAdd event failed, please try with admin rights')
                return None

        self.ui.display_text("EVENT ENTRY WIZARD")
        options = ['cancel', 'entering overall event results (less accurate - quicker)',
                   'entering individual race results (higher accuracy - slower)'
                   'importing previous race csv (needs previously entered csv)',
                   'importing an online results file (needs internet - html/htm/pdf)',
                   'importing an local file (html/htm/pdf)', 'importing a .event file',
                   'importing multiple local files']
        inp = self.ui.g_choose_options(options, 'How would you like to import the event?') + 1
        match inp:
            case 1:
                event = self.add_event_lazy()
            case 2:
                event = self.add_event_proper()
            case 3:
                event = self.add_event_csv()
            case 4:
                event = self.add_online_event()
            case 5:
                event = self.add_event_local()
            case 6:
                event = self.import_pickled_event(self.ui)
            case 7:
                event = None
                self.add_multiple_events()
            case _:
                event = None
        return event

    def add_event_local(self) -> dat.Event:
        inp_mgr = ImportManager(self.ui, 'F', )
        return inp_mgr.to_event(universe_csv, self.nat)

    def add_online_event(self) -> dat.Event:
        inp_mgr = ImportManager(self.ui, 'L')
        return inp_mgr.to_event(universe_csv, self.nat)
