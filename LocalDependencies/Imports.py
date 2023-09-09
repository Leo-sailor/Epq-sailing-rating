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
    log.queue(0, 'tabula passed', all_pages)
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


def split_table(table: list[list[Any]]):
    if table is None:
        return None
    table_start_points = [1]  # the array which stores the locations of each new set of data
    first_col = [f_base.force_int(row[0]) for row in table]
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


class ImportManager:
    reading_data_type = None
    def __init__(self, ui: ui_obj, source: Literal['F', 'L'] = None, remove_rows_with: str = None,
                 file_loc: str = None, full_speed: bool = False):
        self.full_speed = full_speed
        self.ui = ui
        self.__files_to_remove = []
        self.chosen_table = None
        self.chosen_data_type = self.reading_data_type
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
        log.queue(0, 'main import complete', self.tables)

    def __del__(self):
        for file in self.__files_to_remove:
            _remove(file)

    def __getitem__(self, item):
        return self.tables[item]

    def user_select_table(self):
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

    def to_event(self, universe) -> dat.Event:
        if self.chosen_table is None:
            self.user_select_table()
        table = self[self.chosen_table]
        data_types_long = ['sail number', 'champ number', 'name']
        data_types_short = ['s', 'c', 'n']
        if self.chosen_data_type is None:
            self.chosen_data_type = data_types_short[self.ui.g_choose_options(data_types_long,
                                                                              'What field would you like to read?')]
        event_title = self.ui.g_str('What is the event called: ')
        log.queue(0, 'importing event with:', (table, self.chosen_data_type, event_title))
        return universe.process_table(table, self.chosen_data_type, event_title)

    def import_sailors_to_universe(self, universe, nat: str = None) -> list[str]:
        info = {'name': None, 'sail': None, 'champ': None, 'nat': None}  # made so ti would work with draycote 2021 open
        if nat is None or nat.upper() not in valid_nat:
            if self.ui.g_bool('Is everyone in the event from the same country'):
                nat = self.ui.g_nat('the majority of sailors')
        table_num = self.user_select_table()
        for val, item in enumerate(self.tables[table_num][0]):
            for key in info:
                if key.upper() in item.upper() and info[key] is None:
                    info[key] = val
                if key == 'champ' and info[key] is None and 'TALLY' in item.upper():
                    info[key] = val
                if key == 'name' and info[key] is None and 'HELM' in item.upper():
                    info[key] = val
        if self.chosen_data_type is None:
            data_types_long = ['sail number - most reliable', 'champ number - depends on event',
                               'name - spelling issues abound']
            data_types_short = ['s', 'c', 'n']
            self.chosen_data_type = data_types_short[self.ui.g_choose_options(data_types_long,
                                                                              'What field would you like to read?')]
            self.reading_data_type = self.chosen_data_type
        match self.chosen_data_type:
            case 'c':
                data_loc = info['champ']
            case 'n':
                data_loc = info['name']
            case 's':
                data_loc = info['sail']
            case _:
                data_loc = 1
        sailor_ids = []
        for line in self.tables[table_num][1:]:
            if not (line[0] == 'nan' and line[1] == 'nan'):
                log.queue(0, 'adding sailor with line', (line, data_loc))
                sailor_ids.append(
                    universe.import_sailor(self.chosen_data_type, line[data_loc], line, info, nat, full_speed=True))
                log.queue(0, 'sailor id added', sailor_ids[-1])
        return sailor_ids
