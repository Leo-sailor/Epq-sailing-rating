import LocalDependencies.Framework.base_func as f_base
from LocalDependencies.Framework.base_ui import callback as ui_obj
from requests import get as _get
from os import remove as _remove
# noinspection PyPackageRequirements
from tabula import read_pdf as _read_pdf
import pandas as pd
from typing import Any, Literal
import LocalDependencies.leo_dataclasses as dat
from LocalDependencies.Framework.text_ui import valid_nat
from LocalDependencies.Framework.logger import log
from LocalDependencies.Framework.constants import constants
from LocalDependencies.Main_core import UniverseHost

log = log()
c = constants()


def table_size(table: list[list[Any]]) -> int:
    count = 0
    for row in table:
        count += len(row)
    return count


def process_link(ui: ui_obj) -> str:
    log.queue(0, 'downloading_link, and getting it from user')
    file_loc = '______'
    file_types = ['.htm', 'html', '.pdf']
    while file_loc[-4:] not in file_types:
        if file_loc != '______':
            ui.display_text('that file is not of the correct type')
        file_loc = ui.g_str("please enter the link to the webpage: ")
    log.queue(0, 'download in porgress')
    temp_file = ''.join(('webpage.temp', file_loc[-4:]))
    ui.display_text('Downloading_file')
    page = _get(file_loc)  # gets the page as a response object
    with open(temp_file, 'wb') as f:
        f.write(page.content)  # writes the contents of the response object to a field
    log.queue(0, 'file downloaded')
    return temp_file


def trim_table(table: list[list[str]], new_first_cell: str):
    first_col = [str(row[0]).upper() for row in table]
    new_first_row_index = first_col.index(new_first_cell.upper())
    return table[new_first_row_index:]


def remove_rows_including(table: list[list[Any]], term: Any):
    out_table = []
    for row in table:
        if not f_base.r_in(term, row):
            out_table.append(row)
    return out_table


def process_file(ui: ui_obj) -> str:
    file_loc = '______'
    file_types = ['.htm', 'html', '.pdf']
    while file_loc[-4:] not in file_types:
        if file_loc != '______':
            ui.display_text('that file is not of the correct type')
        file_loc = ui.g_file_loc()
    log.queue(0, 'file name and location selected', file_loc)
    return file_loc


def import_pdf(file_loc):
    log.queue(0, 'importing a pdf')
    all_pages = _read_pdf(file_loc, pages='all')
    log.queue(0, 'tabula passed', )
    header = list(all_pages[0].columns)
    for num, page in enumerate(all_pages):
        if f_base.r_in('Unnamed', page.columns.tolist()):
            length = len(page.columns.tolist())
            custom_header = header + ['new'] * length
            page.columns = custom_header[:length]
        else:
            header = list(all_pages[num].columns)

    dataframe = pd.concat(all_pages)
    table = dataframe.values.tolist()
    table.insert(0, dataframe.columns.tolist())
    log.queue(0, 'pdf sucessulyy parsed', table)
    return f_base.findandreplace(table, '\r', ' ', preserve_type=True)


def import_html(file_loc):
    log.queue(0, 'importing html')
    all_tables = pd.read_html(file_loc)
    mega_df = pd.concat(all_tables)
    mega_table = mega_df.values.tolist()
    mega_table.insert(0, mega_df.columns.values.tolist())
    log.queue(0, 'html sucesssfully parsed', mega_table)
    return mega_table


def check_for_alternate_nan(table: list[list[Any]]) -> bool:
    table = table[1:]
    if table[0][0] == 'nan' and table[2][0] == 'nan' and table[4][0] == 'nan':
        return True
    table = table[1:]
    if table[0][0] == 'nan' and table[2][0] == 'nan' and table[4][0] == 'nan':
        return True
    return False


def process_alternate_nan(table):

    out = []
    done = False
    prev = 0
    while not done:
        pair = [table[prev]]
        for loc, row in enumerate(table[prev + 1:]):
            if loc == len(table[prev + 1:]) - 1:
                done = True
                new = prev + 2 + loc
                break
            if row[0] != 'nan':
                new = prev + 1 + loc
                break
        pair += table[prev + 1:new]
        prev = new
        for big_loc, row in enumerate(pair[1:]):
            for loc, val in enumerate(row):
                if val == 'nan':
                    pair[big_loc + 1][loc] = ''
                else:
                    pair[big_loc + 1][loc] = ' ' + pair[big_loc + 1][loc]
        builder = []
        for loc in range(len(pair[0])):
            builder.append(''.join([row[loc] for row in pair]))
        out.append(builder)
    return out


def split_table(table: list[list[Any]]):
    if check_for_alternate_nan(table):
        table = process_alternate_nan(table)
    if table is None:
        return None
    table_start_points = [1]  # the array which stores the locations of each new set of data
    first_col = [f_base.force_int(row[0]) for row in table]
    log.queue(0, "splitting table with first col", first_col)
    previous = 0
    for val, curr in enumerate(first_col[1:]):
        if curr < previous:
            table_start_points.append(val + 1)
            if table[val][0] == 'nan' and table[val][1] == 'nan':
                table_start_points.pop()
        previous = curr
    end = len(table)
    tables = []
    for start_point in reversed(table_start_points):  # reverse order to make sure nothing gets messed with
        small_table = table[start_point:end]  # splits data
        small_table.insert(0, table[0][:])  # adds headers to each set
        tables.insert(0, small_table)  # adds new table to list of tables
        end = start_point

    for loc, tab in enumerate(tables):
        tables[loc] = f_base.clean_table(tab, str)
    return tables


def chose_source(ui: ui_obj, source: Literal['F', 'L'] = None) -> Literal['F', 'L']:
    while not source:
        source = ui.g_choose_options(['link', 'file(s)'], 'Which type would you like to import')
        if source == 'L' or source == 0:
            source = 'L'
            self.__files_to_remove.append(file_loc)
        elif source == 'F' or source == 1:
            source = 'F'
        else:
            ui.display_text('Please make sure to only enter either (L) or (F)')
            source = None
    return source


def prep_table_info(table, index):
    sample_val1 = table[1][index].strip()
    if sample_val1.endswith('.0'):
        sample_val1 = sample_val1[:-2]
    sample_val2 = table[2][index].strip()
    if sample_val2.endswith('.0'):
        sample_val2 = sample_val1[:-2]
    is_number = f_base.can_be_type(float, sample_val1.strip('() ')) and f_base.can_be_type(float,
                                                                                           sample_val2.strip('() '))
    return sample_val1, sample_val2, is_number


def discover_columns(table: list[list[str]], same_nat=None) -> dict:
    table = f_base.deep_copy(table)
    for row_num, row in enumerate(table):
        for col_num, cell in enumerate(row):
            table[row_num][col_num] = str(cell).lower().strip()
    info = {'name': [], 'sail num': None, 'champ num': None, 'nat': None}
    for index, item in enumerate(table[0]):  # round one of checks looking for the expected column names
        sample_val1, sample_val2, is_number = prep_table_info(table, index)
        if 'name' in item and not is_number and 'unnamed' not in item:
            info['name'] += [index]
        elif 'sail' in item and is_number and (4 <= len(sample_val1) <= 5 or 4 <= len(sample_val2) <= 5):
            info['sail num'] = index
        elif 'champ' in item and is_number and (2 <= len(sample_val1) <= 3 or 2 <= len(sample_val1) <= 3) \
                and 'age' not in item:
            info['champ num'] = index
        elif 'country' in item:
            info['nat'] = index
    log.queue(0, 'Info dict after strict pass', info)
    for index, item in enumerate(table[0]):
        sample_val1, sample_val2, is_number = prep_table_info(table, index)
        if len(info['name']) == 0:
            if ('sailor' in item or 'helm' in item) and not is_number:
                info['name'] = [index]
        if info['champ num'] is None:  # checks for other possible names
            if 'tally' in item and is_number:
                info['champ num'] = index

    if len(info['name']) == 2:
        info['name'] = slice(info['name'][0], info['name'][1] + 1)
    elif len(info['name']) == 1:
        info['name'] = info['name'][0]
    elif len(info['name']) == 0:
        info['name'] = None
    else:
        info['name'] = info['name'][0]
    log.log(0, 'Info dict after loose pass', info)
    return info


def remove_zeros(val):
    if val.endswith('.0'):
        val = val[:-2]
    return val


class ImportManager:
    def __init__(self, ui: ui_obj, source: Literal['F', 'L'] = None, remove_rows_with: str = None,
                 file_loc: str = None, full_speed: bool = False):
        self.full_speed = full_speed
        self.ui = ui
        self.chosen_data_type = None
        self.__files_to_remove = []
        self.chosen_table = None
        if file_loc is None:
            source = chose_source(ui, source)
            match source:
                case 'F':
                    file_loc = process_file(ui)
                case 'L':
                    file_loc = process_link(ui)
                    self.__files_to_remove.append(file_loc)
                case _:
                    raise NotImplementedError('Unsupported input method for import a file, should be link or file')
        log.queue(0, 'type of file source selected', source)
        match file_loc[-4:]:
            case '.pdf':
                self.type = 'pdf'
            case 'html' | '.htm':
                self.type = 'html'
            case _:
                self.type = 'Unknown'
        log.queue(0, 'file type chosen', self.type)
        if self.type == 'pdf':
            self.all = import_pdf(file_loc)
        elif self.type == 'html':
            self.all = import_html(file_loc)
        else:
            self.all = None
        self.all = trim_table(self.all, 'rank')
        if remove_rows_with is not None:
            self.all = remove_rows_including(self.all, remove_rows_with)
        self.tables = split_table(self.all)
        for table in self.tables:
            if str(table[0]) == str(table[1]):
                table.pop(0)
        log.queue(0, 'main import complete', self.tables)

    def __del__(self):
        for file in self.__files_to_remove:
            _remove(file)

    def __getitem__(self, item):
        return self.tables[item]

    def get_data_quantity(self):
        info = discover_columns(self.tables[self.choose_table()][:3])
        count = 0
        for key, val in info.items():
            if val is not None:
                count += 1
        return count

    def choose_data_type(self, columns: dict = None):
        table = self.choose_table()
        if columns is None:
            info = discover_columns(self.tables[table][:3])
        else:
            info = columns
        if self.chosen_data_type:
            for key, val in info.items():
                if val == self.chosen_data_type:
                    field = key
            return self.chosen_data_type, field
        options = []
        options_true = []
        for key, val in info.items():
            if val is not None:
                options_true.append(val)
                if isinstance(val, list):
                    val = val[0]
                elif isinstance(val, slice):
                    val = val.start
                options.append(f"field: '{key}' with column title: '{self.tables[table][0][val]}' "
                               f"with first row: '{self.tables[table][1][val]}'")
        option_chosen = self.ui.g_choose_options(options, 'Which column do you want to prioritize reading')
        self.chosen_data_type = options_true[option_chosen]
        for key, val in info.items():
            if val == self.chosen_data_type:
                field = key
        return self.chosen_data_type, field

    def choose_table(self):
        if self.chosen_table is not None:
            return self.chosen_table
        if self.full_speed:
            curr_size = -1
            curr_index = None
            for val, table in enumerate(self.tables):
                if table_size(table) > curr_size:
                    curr_index = val
                    curr_size = table_size(table)
            self.chosen_table = curr_index
            log.queue(0, 'fullspeed chosen theyre table', self.chosen_table)
            return self.chosen_table
        tab_len = len(self.tables)
        if tab_len == 1:
            self.chosen_table = 0
            return 0
        expected = False
        table_num = None
        while not expected:
            table_num = self.ui.g_int(
                f'Please enter the table number you would like to receive ((-{tab_len}) - {tab_len - 1}): ',
                range_low=0 - tab_len, range_high=tab_len - 1)
            table = self.tables[table_num]
            self.ui.display_table(table)
            expected = self.ui.g_bool('Was the table what you expected')
        self.chosen_table = table_num
        log.queue(0, 'user chosen theyre table', self.chosen_table)
        return self.chosen_table

    def to_event(self, universe: UniverseHost, nat = None) -> dat.Event:
        if nat is None or nat.upper() not in valid_nat:
            if self.ui.g_bool('Is everyone in the event from the same country'):
                nat = self.ui.g_nat('the majority of sailors')
            else:
                nat = None
        sailorids = self.import_sailors_to_universe(universe,nat)
        table = f_base.deep_copy(self[self.chosen_table])
        to_remove = []
        for loc,sailor in enumerate(sailorids):
            if sailor == 'nan':
                to_remove.append(loc)
        for loc in reversed(to_remove):
            sailorids.pop(loc)
            table.pop(loc +1)
        event_title = self.ui.g_str('What is the event called: ')
        log.queue(0, 'importing event with:', (table, self.chosen_data_type, event_title))
        return universe.process_table(table, event_title, nat, sailorids)

    def import_sailors_to_universe(self, universe, nat: str = None) -> list[str]:
        if nat is None or nat.upper() not in valid_nat:
            if self.ui.g_bool('Is everyone in the event from the same country'):
                nat = self.ui.g_nat('the majority of sailors')
            else:
                nat = None
        table_num = self.choose_table()
        info = discover_columns(self.tables[self.chosen_table][:3], nat)

        data_loc, field_name = self.choose_data_type(info)
        sailor_ids = []
        for line in self.tables[table_num][1:]:
            for loc, val in enumerate(line):
                line[loc] = remove_zeros(val)
            if not (line[0] == 'nan' and line[1] == 'nan'):
                log.queue(0, 'adding sailor with line', (line, data_loc))
                sailor_ids.append(
                    universe.import_sailor(field_name, line[data_loc], line, info, nat, full_speed=True))
                log.queue(0, 'sailor id added', sailor_ids[-1])
        return sailor_ids
