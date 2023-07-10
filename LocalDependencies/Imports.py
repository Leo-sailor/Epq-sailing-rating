import LocalDependencies.Framework.base_func as f_base
from LocalDependencies.Framework.text_ui import text_ui as text_ui
from requests import get as _get
from os import remove as _remove
from tabula import read_pdf as _read_pdf
import pandas as pd
from typing import Any
import LocalDependencies.leo_dataclasses as dat


def process_link(ui: text_ui) -> str:
    file_loc = '______'
    file_types = ['.htm', 'html', '.pdf']
    while file_loc[-4:] not in file_types:
        if file_loc != '______':
            ui.display_text('that file is not of the correct type')
        file_loc = ui.g_str("please enter the link to the webpage: ")
    temp_file = ''.join(('webpage.temp', file_loc[-4:]))
    ui.display_text('Downloading_file')
    page = _get(file_loc)  # gets the page as a response object
    open(temp_file, 'wb').write(page.content)  # writes the contents of the response object to a field
    return temp_file


def remove_rows_including(table: list[list[Any]], term: Any):
    out_table = []
    for row in table:
        if not f_base.r_in(term, row):
            out_table.append(row)
    return out_table


def process_file(ui: text_ui) -> str:
    file_loc = '______'
    file_types = ['.htm', 'html', '.pdf']
    while file_loc[-4:] not in file_types:
        if file_loc != '______':
            ui.display_text('that file is not of the correct type')
        file_loc = ui.g_file_loc(file_types=('importable', '.htm .html .pdf'))
    return file_loc


def import_pdf(file_loc):
    all_pages = _read_pdf(file_loc, pages='all')
    dataframe = pd.concat(all_pages)
    table = dataframe.values.tolist()
    table.insert(0, dataframe.columns.tolist())
    return f_base.findandreplace(table, '\r', ' ', preserve_type=True)


def import_html(file_loc):
    all_tables = pd.read_html(file_loc)
    mega_df = pd.concat(all_tables)
    mega_table = mega_df.values.tolist()
    mega_table.insert(0, mega_df.columns.values.tolist())
    return mega_table


def split_table(table: list[list[Any]]):
    if table is None:
        return None
    table_start_points = [1]  # the array which stores the locations of each new set of data
    first_col = [f_base.force_int(row[0]) for row in table]
    previous = 0
    for val, curr in enumerate(first_col[1:]):
        if curr < previous:
            table_start_points.append(val+1)
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
        tables[loc] = f_base.clean_table(tab)
    return tables


class ImportManager:
    def __init__(self, ui: text_ui, source: str = None, remove_rows_with=None):
        self.ui = ui
        self.__files_to_remove = []
        self.chosen_table = None
        self.chosen_data_type = None
        file_loc = None
        while not file_loc:
            if source is None:
                source = ui.g_choose_options(['link', 'file'], 'Which type would you like to import')
            if source == 'L' or source == 0:
                file_loc = process_link(ui)
                self.__files_to_remove.append(file_loc)
            elif source == 'F' or source == 1:
                file_loc = process_file(ui)
            else:
                ui.display_text('Please make sure to only enter either (L) or (F)')
                source = None
        match file_loc[-4:]:
            case '.pdf':
                self.type = 'pdf'
            case '.html' | 'htm':
                self.type = 'html'
            case _:
                self.type = 'Unknown'
        if self.type == 'pdf':
            self.all = import_pdf(file_loc)
        elif self.type == 'html':
            self.all = import_html(file_loc)
        else:
            self.all = None
        if remove_rows_with is not None:
            self.all = remove_rows_including(self.all, remove_rows_with)
        self.tables = split_table(self.all)

    def __del__(self):
        for file in self.__files_to_remove:
            _remove(file)

    def __getitem__(self, item):
        return self.tables[item]

    def user_select_table(self):
        tab_len = len(self.tables)
        expected = False
        table_num = None
        while not expected:
            table_num = self.ui.g_int(
                f'Please enter the table number you would like to receive ((-{tab_len}) - {tab_len - 1}): ',
                range_low=0 - tab_len, range_high=tab_len - 1)
            table = self.all[table_num]
            self.ui.display_table(table)
            expected = self.ui.g_bool('Was the table what you expected')
        self.chosen_table = table_num
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
        return universe.processtable(table, self.chosen_data_type, event_title)

    def import_sailors_to_universe(self, universe) -> list[str]:
        info = {'name': None, 'sail ': None, 'champ': None, 'nat': None}
        same_nat = self.ui.g_bool('Is everyone in the event from the same country')
        nat = None
        if same_nat:
            nat = self.ui.g_nat('the majority of sailors')
        if self.chosen_table is None:
            table_num = self.user_select_table()
        else:
            table_num = self.chosen_table
        for val, item in enumerate(self.tables[table_num]):
            for key in info:
                if key.upper() in item.upper():
                    info[key] = val
        if self.chosen_data_type is None:
            data_types_long = ['sail number', 'champ number', 'name']
            data_types_short = ['s', 'c', 'n']
            self.chosen_data_type = data_types_short[self.ui.g_choose_options(data_types_long,
                                                                              'What field would you like to read?')]
        match self.chosen_data_type:
            case 'c':
                data_loc = info['champ']
            case 'n':
                data_loc = info['name']
            case 's':
                data_loc = info['sail ']
            case _:
                data_loc = 1
        sailor_ids = []
        for line in self.tables[table_num]:
            if not(line[0] == 'nan' and line[1] == 'nan'):
                sailor_ids.append(
                    universe.import_sailor(self.chosen_data_type, line[data_loc], line, info, nat, full_speed=True))
        return sailor_ids
