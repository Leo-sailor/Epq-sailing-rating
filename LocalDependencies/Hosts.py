import LocalDependencies.Aditional_func as addFunc
from LocalDependencies.Main_core import UniverseHost
import LocalDependencies.General as Base
from LocalDependencies.Framework import base_func as f_base
from LocalDependencies.Csv_custom import csv_base
import LocalDependencies.leo_dataclasses as dat
import datetime
from pickle import load as _load
from time import sleep as _sleep
from LocalDependencies.Imports import ImportManager
from LocalDependencies.Framework.text_ui import text_ui

global universe_csv


class HostScript:
    def __init__(self, ui: text_ui, *sys_args):
        self.inp_method = ''
        self.input_method_name = ''
        if sys_args is None:
            sys_args = []
        self.args = sys_args
        self.ui = ui

    def torun(self, *args):
        global universe_csv
        if len(args) > 2:
            universe_csv = UniverseHost(self.ui, args[1], args[2])
        else:
            universe_csv = UniverseHost(self.ui)
        while True:
            options = ['add a new event', 'add a new sailor', 'get a sailors information', 'quit',
                       'get sailor info over time', 'print the universe', 'exit the universe', 'import sailors',
                       'graph sailors over time']
            choice = self.ui.g_choose_options(options, 'What would you like to do: ') + 1
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
                    self.ui.display_table(universe_csv.file.row_first)
                    _sleep(0.5)
                case 7:
                    self.torun()
                    break
                case 8:
                    self.import_sailors(self.ui)
                case 9:
                    self.sailor_rating_over_time()

    @staticmethod
    def import_sailors(ui: text_ui):
        imp_mgr = ImportManager(ui)
        sailors = imp_mgr.import_sailors_to_universe(universe_csv)
        ui.display_text(f'The following {len(sailors)} sailors have been imported')
        for line in sailors:
            ui.display_text(universe_csv.getinfo(line, 'all'))

    def sailor_rating_over_time(self):
        global universe_csv
        inp_method = self.__get_input_method()
        inp = self.ui.g_str(f'Please enter the sailor\'s {self.input_method_name}: ')
        sailorid = universe_csv.get_sailor_id(inp_method, inp)
        universe_name = universe_csv.universe
        start_date = self.ui.g_date_int('of the first day of your range')
        end_date = self.ui.g_date_int('of the last day of your range')
        info_codes = ['Championship Number', 'Sail Number', 'Light wind rating', 'Medium wind rating',
                      'Heavy wind rating', 'sailorid', 'Overall rating', 'Rank', 'Total events', 'Zone/Region',
                      'Territory/country']
        out_codes = ['c', 's', 'l', 'm', 'h', 'i', 'o', 'r', 'e', 'z', 't']
        selected = self.ui.g_choose_options(info_codes, 'please enter type of information you would like to receive')
        addFunc.plot_sailors(start_date, sailorid, out_codes[selected], universe_name, end_date)

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
    def make_new_sailor(ui: text_ui, name=None, sailno=None, champ=None, nat=None, full_speed=False):
        if not full_speed:
            ui.display_text('\n NEW SAILOR WIZARD')
        if name is None:
            name = ui.g_str('Please enter the sailor\'s Full name: ', char_level=3)
        name = name.split(' ', 1)
        first = name[0]
        try:
            sur = name[1]
        except IndexError:
            sur = ui.g_str('Please enter the sailor\'s  surname: ', char_level=3)
        if champ is None:
            champ = str(ui.g_int('Please enter the sailor\'s Championship number '
                                 '\n(Please enter (000) if the sailor does not have a Champ number): ',
                                 range_high=999, range_low=0))
        else:
            champ = str(champ)
        if sailno is None:
            sailno = str(ui.g_int('Please enter the sailor\'s Sail number \n(Please ignore any letters): ',
                                  range_high=999, range_low=0))
        else:
            sailno = str(sailno)
        if nat is None:
            nat = ui.g_nat(f'{first} {sur}', 1)
        nat = str(nat)
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
            file_loc = self.ui.g_file_loc('r', title=f'Select the file location for {race_text}: ',
                                          filetypes=('csv files', '.csv'))
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
    def import_pickled_event(ui: text_ui):
        file_loc = '_________'
        while file_loc[-6:] != '.event':
            if file_loc != '_________':
                ui.display_text('that file is not of the correct type, please try again')
            file_loc = ui.g_file_loc(filetypes=('event files', '.event'))
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
                   'importing an local file (html/htm/pdf)', 'importing a .event file']
        inp = self.ui.g_choose_options(options, 'How would you like to import the event?')
        match inp:
            case 1:
                event = self.add_event_lazy()
            case 2:
                event = self.add_event_proper()
            case 3:
                event = self.add_event_csv()
            case 4:
                event = self.add_online_event(self.ui)
            case 5:
                event = self.add_event_local(self.ui)
            case 6:
                event = self.import_pickled_event(self.ui)
            case _:
                event = None
        return event

    @staticmethod
    def add_event_local(ui: text_ui) -> dat.Event:
        inp_mgr = ImportManager(ui, 'F')
        return inp_mgr.to_event(universe_csv)

    @staticmethod
    def add_online_event(ui: text_ui) -> dat.Event:
        inp_mgr = ImportManager(ui, 'L')
        return inp_mgr.to_event(universe_csv)
