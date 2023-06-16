import LocalDependencies.General as Base
from requests import get as _get
from os import remove as _remove
from tabula import read_pdf as _read_pdf
import pandas as pd
from typing import Any


def __process_link() -> str:
    fileloc = '______'
    file_types = ['.htm', 'html', '.pdf']
    while fileloc[-4:] not in file_types:
        if fileloc != '______':
            print('that file is not of the correct type')
        fileloc = Base.clean_input("please enter the link to the webpage: ", 'str')
    temp_file = '.'.join(('webpage.temp', fileloc[-4:]))
    print('Downloading_file')
    page = _get(fileloc)  # gets the page as a response object
    open(temp_file, 'wb').write(page.content)  # writes the contents of the response object to a field
    return temp_file


def __process_file() -> str:
    fileloc = '______'
    file_types = ['.htm', 'html', '.pdf']
    while fileloc[-4:] not in file_types:
        if fileloc != '______':
            print('that file is not of the correct type')
        fileloc = Base.getfilename()
    return fileloc


def __import_pdf(file_loc):
    all_pages = _read_pdf(file_loc, pages='all')
    dataframe = pd.concat(all_pages)
    table = dataframe.values.tolist()
    table.insert(0, df.columns.tolist())
    return Base.findandreplace(table, '\r', ' ', preserve_type=True)


def __import_html(file_loc):
    all_tables = pd.read_html(file_loc)
    mega_df = pd.concat(all_tables)
    mega_table = mega_df.values.tolist()
    mega_table.insert(0, mega_df.columns.values.tolist())
    return mega_table


def __split_table(table: list[list[Any]]):
    table_start_points = [1]  # the array which stores the locations of each new set of data
    first_col = [Base.force_int(row[0]) for row in table]
    previous = 0
    for curr in first_col[1:]:
        if curr < previous:
            table_start_points.append(curr)
        previous = curr

    end = len(table)
    tables = []
    for start_point in reversed(table_start_points):  # reverse order to make sure nothing gets messed with
        small_table = table[start_point:end]  # splits data
        small_table.insert(0, header)  # adds headers to each set
        tables.insert(0, new_table)  # adds new table to list of tables
        end = table_start_points[x]

    for loc, tab in tables:
        tables[loc] = Base.clean_table(tab)
    return tables


class Import_manager:
    def __init__(self, source: str = None):
        self.__files_to_remove = []
        self.chosen_table = None
        self.chosen_data_type = None
        file_loc = None
        while not fileloc:
            if source is None:
                source = Base.clean_input('Would you linke to import a link (L) or a file (F): ', 'str',
                                          length=1).upper()
            if source == 'L':
                file_loc = __process_link()
                self.__files_to_remove.append(file_loc)
            elif source == 'F':
                file_loc = __process_file()
            else:
                print('Please make sure to only enter either (L) or (F)')
                source = None
        match file_loc[-4:]:
            case '.pdf':
                self.type = 'pdf'
            case '.html' | 'htm':
                self.type = 'html'
            case _:
                self.type = 'Unknown'
        if type == 'pdf':
            self.all = __import_pdf(file_loc)
        elif type == 'html':
            self.all = __import_html(file_loc)
        else:
            self.all = None
        self.tables = __split_table(self.all)

    def __del__(self):
        for file in self.__files_to_remove:
            _remove(file)

    def __getitem__(self, item):
        return self.tables[item]

    def user_select_table(self):
        tab_len = len(self.tables)
        expected = False
        while not expected:
            table_num = Base.clean_input(
                f'Please eneter the table number you would like to recive (-{tab_len} - {tab_len - 1}): ', 'int',
                0 - tab_len, tab_len - 1)
            table = self[table_num]
            for line in table:
                print(line)
            expected = Base.clean_input('Was the table what you exepected', 'bool')
        self.chosen_table = table_num
        return self.chosen_table

    def to_event(self, universe: Universe_host) -> dat.Event:
        if self.chosen_table is None:
            self.user_select_table()
        table = self[self.chosen_table]
        if self.chosen_data_type is None:
            self.chosen_data_type = Base.clean_input('What field would you like to read on the file (s,c,n): ', 'str',
                                                     length=1)
        event_title = Base.clean_input('What is the event called: ', 'str')
        return universe.processtable(table, self.chosen_data_type, event_title)

    def import_sailors_to_universe(self, universe: Universe_host) -> list[str]:
        info = {'name': None, 'sail ': None, 'champ': None, 'nat': None}
        same_nat = Base.clean_input('Is everyone in the event from the same country', 'bool')
        nat = None
        if same_nat:
            nat = Base.getnat()
        for val, item in enumerate(self.all[0]):
            for key in info:
                if key.upper() in item.upper():
                    info[key] = val
        if self.chosen_data_type is None:
            self.chosen_data_type = Base.clean_input('What field would you like to prioritise (s,c,n): ', 'str',
                                                     length=1)
        match self.chosen_data_type:
            case 'c':
                data_loc = info['champ']
            case 'n':
                data_loc = info['name']
            case 's':
                data_loc = info['sail ']
            case _:
                data_loc = 1
        sailorids = []
        for line in self.all[1:]:
            sailor_ids.append(
                universe.import_sailor(self.chosen_data_type, line[data_loc], line, info, nat, full_speed=True))
        return sailorids
