# imports
import requests
from hashlib import md5
from bcrypt import gensalt, hashpw
from datetime import datetime, date, timedelta
from difflib import SequenceMatcher
from tkinter import filedialog
from numpy import diff as np_diff
from typing import Any

# class which contains basic funtions for the program not directly related to the elo calculations
basenat = ''
validnat = {'ALG', 'ASA', 'AND', 'ANT', 'ARG', 'ARM', 'ARU', 'AUS', 'AUT', 'AZE', 'BAH', 'ARN', 'BAR',
                         'BLR', 'BEL', 'BIZ', 'BER', 'BRA', 'BOT', 'IVB', 'BRU', 'BUL', 'CAM', 'CAN', 'CAY', 'CHI',
                         'CHN', 'TPE', 'COL', 'COK', 'CRO', 'CUB', 'CYP', 'CZE', 'DEN', 'DJI', 'DOM', 'ECU', 'EGY',
                         'ESA', 'EST', 'FIJ', 'FIN', 'FRA', 'GEO', 'GER', 'GBR', 'GRE', 'GRN', 'GUM', 'GUA', 'HKG',
                         'HUN', 'ISL', 'IND', 'INA', 'IRN', 'IRQ', 'IRL', 'ISR', 'ITA', 'JAM', 'JPN', 'KAZ', 'KE',
                         'PRK', 'KOR', 'KOS', 'KUW', 'KGZ', 'LAT', 'LIB', 'LBA', 'LIE', 'LTU', 'LUX', 'MAC', 'MAD',
                         'MAS', 'MLT', 'MRI', 'MEX', 'MDA', 'MON', 'MNE', 'MNT', 'MAR', 'MOZ', 'MYA', 'NAM', 'NED',
                         'AHO', 'NZL', 'NGR', 'MKD', 'NOR', 'OMA', 'PAK', 'PLE', 'PAN', 'PNG', 'PAR', 'PER', 'PHI',
                         'POL', 'POR', 'PUR', 'QAT', 'ROM', 'RUS', 'SAM', 'SMR', 'SEN', 'SRB', 'SEY', 'SGP', 'SVK',
                         'SLO', 'RSA', 'ESP', 'SRI', 'SKN', 'LCA', 'SUD', 'SWE', 'SUI', 'TAH', 'TAN', 'THA', 'TLS',
                         'TTO', 'TUN', 'TUR', 'TKS', 'UGA', 'UKR', 'UAE', 'USA', 'URU', 'ISV', 'VAN', 'VEN', 'ZIM'}
numbers = ['0','1','2','3','4','5','6','7','8','9']


def getfilename(mode = 'r',**args)->str:
    file_getter = filedialog.askopenfile(mode,**args)
    file_getter.close()
    return file_getter.name

def getdate(return_method:str = 'epoch', prompt:str = "")-> int | str | date:
    """

    :param return_method: epoch is seconds since epoch, text returns a text format, date returns a dateobject, datetime returns a datetime object
    :param prompt:
    :return:
    """
    if prompt[-2:] == ': ':
        prompt += ': '
    year = clean_input(f"Please enter the year {prompt}", int, 2000, 2100)
    month = clean_input(f"Please enter the month {prompt}", int, 1, 12)
    if month in [4,6,9,11]:
        day = clean_input(f"Please enter the day {prompt}", int, 1, 30)
    elif month in [1,3,5,7,8,10,12]:
        day = clean_input(f"Please enter the day {prompt}", int, 1, 31)
    else:
        day = clean_input(f"Please enter the day {prompt}", int, 1, 28)
    current = date(year,month,day)
    match return_method:
        case 'epoch':
            epoch = date(1970,1,1)
            return int((current-epoch).total_seconds())
        case 'text':
            return str(current)
        case 'date':
            return current
        case 'datetime':
            return datetime(year,month,day)
        case 'int':
            return days_since_two_thousand(current)

def getfieldnumber(self, resulttype: str) -> int:
    try:
        resulttype.lower()
    except AttributeError:
        pass
    match resulttype:
        case 'n' | 'name':
            findtypeloc = -1  # makes sure the next bit will be bypassed
        case 'sail number' | 's' | 'sail':
            findtypeloc = 2  # the column location of the data
        case 'champ number' | 'championship number' | 'c' | 'champ':
            findtypeloc = 1
        case 'region' | 'z':
            findtypeloc = 5
        case 'nat' | 'nation' | 'nationality' | 't':
            findtypeloc = 6
        case 'l' | 'light wind rating' | 7:
            findtypeloc = 7
        case 'medium wind rating' | 'm' | 8:
            findtypeloc = 8
        case 'high wind rating' | 'h'| 9:
            findtypeloc = 9
        case 'ranking' | 'r':
            findtypeloc = 11
        case 'overall rating' | 'o'| 10:
            findtypeloc = 10
        case 'events completed' | 'e':
            findtypeloc = 12
        case 'date of last event' | 'd':
            findtypeloc = 13
        case '14' | 'a' | 'all':
            findtypeloc = -2  # bypasses next stage
        case _:
            findtypeloc = 0
    return findtypeloc

def two_thousand_to_datetime(days:int) -> date:
    thousand = date(2000, 1, 1)
    delta = timedelta(days)
    return thousand + delta


def days_since_two_thousand(in_date: date | datetime = None) -> int:
    thousand = date(2000, 1, 1)
    if in_date is None:
        now = date.today()
    else:
        now = in_date
    day = now - thousand
    return day.days

def check_consecutive(l:list) -> bool:
    n = len(l) - 1
    return sum(np_diff(sorted(l)) == 1) >= n

def clean_input(prompt: str, datatype: type|str, rangelow: float = 0, rangehigh: float = 500, charlevel: int = 0,
                correcthash='', salt=''.encode(), length = None )-> str|float|int|bool|tuple[str,str]:
    """This function takes a prompt and a type and keeps taking an input from the user until it furfills the
    requirmetns attached
    char lever 0: all characters allowed
    char level 1: characters good for files allowed
    char level 2: character good for sailor id
    char level 3: character good for names
    for range high and range low, its less than or equal"""
    if datatype == str:
        if charlevel == 0 or charlevel == '0':
            if length is None:
                return input(prompt)
            inp = ''
            while len(inp) != length:
                if inp != '':
                    print(f'your string must have a length of {length} characters')
                inp = input(prompt)
            return inp
        elif charlevel == 1 or charlevel == '1': # file safe chars
            file_safe_chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                     'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
                     'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5',
                     '6', '7', '8', '9', '.', '_', '\'', '(', ')', ':']
            if length is None:
                return user_filterd_string(file_safe_chars,prompt)
            inp = ''
            while len(inp) != length:
                if inp != '':
                    print(f'your string must have a length of {length} characters')
                inp = user_filterd_string(file_safe_chars,prompt)
            return inp
        elif charlevel == 2 or charlevel == '2': # sailor id chars
            file_safe_chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K','L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V','W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5','6', '7', '8', '9', '-']
            if length is None:
                return user_filterd_string(file_safe_chars, prompt)
            inp = ''
            while len(inp) != length:
                if inp != '':
                    print(f'your string must have a length of {length} characters')
                inp = user_filterd_string(file_safe_chars, prompt)
            return inp
        elif charlevel == 3 or charlevel == '3':
            file_safe_chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '-', ' ']
            if length is None:
                return user_filterd_string(file_safe_chars, prompt)
            inp = ''
            while len(inp) != length:
                if inp != '':
                    print(f'your string must have a length of {length} characters')
                inp = user_filterd_string(file_safe_chars, prompt)
            return inp

    elif datatype == float:
        try:
            inp = float(input(prompt))
        except ValueError:
            print('\nThat input was not a number')
            inp = 5000000000
        while rangelow >= inp >= rangehigh:
            print('\nThat value was not accepted, Please Try Again')
            try:
                inp = float(input(prompt))
            except ValueError:
                print('\nThat input was not a number')
                inp = 5000000000
        return inp

    elif datatype == int:
        try:
            inp = int(input(prompt))
        except ValueError:
            print('\nThat input was not a integer, please enter a whole number')
            inp = 5000000000
        while inp < rangelow or inp > rangehigh:  # is it wrong
            print('\nThat value was not accepted, Please Try Again')

            try:
                inp = int(input(prompt))
            except ValueError:
                print('\nThat input was not a integer, please enter a whole number')
                inp = 5000000000
        return inp

    elif datatype == 'pn':
        passwordb = ''
        same = False
        while not same:
            passworda = input(prompt)
            passwordb = input('Please it again to confirm: ')
            same = passwordb == passworda
            if not same:
                print('\nThose passwords did not match, Please try again')
        return passwordhash(passwordb)

    elif datatype == 'pr':
        done = False
        while not done:
            inp = input(prompt)
            if passwordhash(inp, salt)[0] == correcthash:
                print('\nPassword is correct')
                return True
            elif inp == '':
                print('\nPassword entry is skipped')
                return False
            else:
                print('\nThat password was incorrect, please try again')

    elif datatype == bool:
        inp = clean_input(f'{prompt} - please enter 1 for yes and 0 for no: ',int,0,1)
        if inp == 1:
            return True
        else:
            return False


    else:
        return ''
def user_filterd_string(chars_allowed: list | tuple, prompt: str) -> str:

    new = []
    old = input(prompt)
    for char in old:
        if char.upper() in chars_allowed:

            new.append(char)
    new_str = ''.join(new)
    if old == new_str:
        return old
    choice = clean_input(f'\nYour string is "{new_str}". Is this what you expected?',bool)
    if choice:
        return new_str
    else:
        return user_filterd_string(chars_allowed,prompt)
def generate_sailor_id(nat: str | None, sailno: str | int, first: str, surname: str) -> tuple[str, str]:
    global basenat
    """
    This function generates a sailorid from its components
    :param nat: 3 letter sting or none
    :param sailno: 5 number string
    :param first: string
    :param surname: string
    :return: string
    """
    iden = ''
    if nat is None:
        nat = getnat()
    nat = nat.upper()
    if nat not in validnat:
        nat = getnat()
    if basenat == '':
        basenat = nat
    first += '000'
    surname += '000'
    sailno = str(sailno)
    newsailno = '0000' + sailno
    if newsailno[-2:] == '.0':
        newsailno = sailno[:-2]
    iden += nat[:2]
    iden += '-'
    iden += newsailno[-4:]
    iden += '-'
    iden += first[:3]
    iden += surname[:2]
    return iden.lower(), nat

def ordinal(num) -> str:
    suffixes = {1: 'st', 2: 'nd', 3: 'rd'}
    if 10 <= num % 100 <= 20:
        suffix = 'th'
    else:
        # the second parameter is a default.
        suffix = suffixes.get(num % 10, 'th')
    return str(num) + suffix

def is_iterable(inp:Any) -> bool:
    try:
        iter(inp)
    except TypeError:
        return False
    return True

def r_in(term, inp:list[Any]) -> bool:
    if not is_iterable(inp):
        if term == inp:
            return True
        else:
            return False
    else:
        if term in inp:
            return True
        for item in inp:
            if r_in(term, item):
                return True
        return False


def getnat() -> str:
    """
    This function gets the current computer's adress and uses that to generate a suggested 3 letter country code
    :return: 3 letter country code
    """
    from countryinfo import CountryInfo
    global basenat
    if basenat == '' :
        if __name__ == 'tests.py':
            print('starting network request')
        try:
            ip = requests.get('https://geolocation-db.com/json').json()
            natname = ip['country_name']
        except requests.exceptions.ConnectionError:
            natname = 'Netherlands'
        if __name__ == 'tests.py':
            print('ending network request')
        choice = clean_input(f'\nAre the majority of competitors from the {natname}?',bool)
        if choice:
            # use py pi country info to get country
            country = CountryInfo(natname)
            basenat = country.iso(3)
        else:
            while basenat == '':
                basenatposs = input('Please enter the majority of your competitors\' 3 Letter country code')
                if basenatposs.upper() in validnat:
                    basenat = basenatposs.upper()
                else:
                    print('Sorry, that country code is not valid please try again')
        return basenat
    else:
        return basenat

def csv_line_generate(sailorid: str, nat: str, sailno: str, first: str, surname: str, region: str, champnum: str) -> str:
    """
    This function generates a csv line from its components ready to be appended to a csv
    :param sailorid: sailorid
    :param nat: 3 letter sting
    :param sailno: 5 number string
    :param first: string
    :param surname: string
    :param region: 2 letter number string or ''
    :param champnum: 3 number stinf or ''
    :return:
    """
    rank = 0

    first.lower()
    surname.lower()
    region = region[:3].upper().strip()
    champnum = '000' + str(champnum)
    champnum = champnum[-3:]
    if nat not in validnat:
        nat.upper()
        nat.strip()

    parts = [sailorid, champnum, sailno, first, surname, region, nat, 1500, 1500, 1500, 1500, rank, days_since_two_thousand()]

    line = ','.join(parts)

    # print('{}'.format(line))

    return line

def firstcap(word: str) -> str:
    """
    This function takes a string and returns that string with a capitalized first letter
    :param word:
    :return: string with capitalized first letter
    """
    word = word.lower()
    word = word.strip()
    try:
        newword = word[0].upper() + word[1:]
        return newword
    except IndexError:
        return word

def sort_on_element(sub_li: list[list], element: int, reverse: bool = True,zero_is_big=True) -> list[list]:
    sub_li.sort(reverse=reverse, key=lambda x: x[element] if (x[element] == 0 and zero_is_big) else 9999999)
    return sub_li

def multiindex(inlist: list, term: Any) -> list[int]:
    """
    This function takes a list and finds all occourences of the term inside of that list,
    will not return the first one
    :param inlist: the list to be searched through
    :param term: the term to be searched for
    :return: all indexes of the term inside of that list
    """
    term = str(term)
    for x in range(len(inlist)):
        if type(inlist[x]) != str:
            inlist[x] = str(inlist[x])

        # inlist[x] = inlist[x].lower().strip()

    indexs = []
    start = 0
    end = False
    while not end:
        try:
            indexs.append(inlist.index(term, start))
            start = indexs[-1] + 1
        except ValueError:
            end = True
    return indexs

def passwordhash(password: str, salt: bytes=None)-> tuple[str,str]:
    """
    This function will hash a password using the password and a salt and will generate a salt if it is put in without one
    :param password:
    :param salt:
    :return:
    """
    if salt is None:
        salt = gensalt()
    hashed = hashpw(password.encode(), salt).hex()
    return hashed, salt.hex()


def hashfile(file: str) -> str:
    """
    This function takes a file adress and opens it as a text file and produces a md5 hash of it
    :param file: the file address of the file to be hashed
    :return: the string of the md5 hash
    """
    with open(file) as actualfile:
        str2hash = actualfile.read()
    result = md5(str2hash.encode()).hexdigest()
    return str(result)


def findandreplace(inp, find: str, replace: str, preserve_type=False):
    """
    a recussive find and replace algoritim which searchs through lists and thiers sub lits up to the recursion limit
    in search of strings, when a string is found, a normal find and replace algoritim on is applied to the string.
    intended side effect: all int
    THIS IS A TIME CRITICAL FUNCTION, TIME TO RUN > READABILTY OR MAINAINABILITY OR LOC (LINES OF CODE)
    :param inp:
    :param find:
    :param replace:
    :param preserve_type: if true, all types other than a string will stay in there origninal types, ohwise they will be converted
    :return:
    """
    match inp:
        case str():
            return inp.replace(find,replace)
        case list():
            out = []
            for item in inp:
                out.append(findandreplace(item, find, replace))
            return out
        case float() | int():
            if preserve_type:
                return inp
            return str(inp)
        case _:
            if preserve_type:
                return inp
            try:
                return str(inp)
            except ValueError:
                raise TypeError('Expected type list or str or struct which str() can be applied not ' + str(type(inp)))


def force_int(inp:str|float|int)->int:
    inp = str(inp)
    numbers_new = numbers[:]
    numbers_new.append('.')
    new_str = []
    for char in inp:
        if char in numbers_new:
            new_str.append(char)
    if len(new_str) == 0:
        return 0
    return int(float(''.join(new_str)))
def clean_table(table: list[list[Any]]):
    intial_vals = table[1]
    cols_to_remove = list(range(len(table[1])))
    for row_index in range(1, len(table)):
        good_cols = []
        for col in cols_to_remove:
            if table[row_index][col] != intial_vals[col]:
                good_cols.append(col)
        [cols_to_remove.pop(cols_to_remove.index(item)) for item in good_cols]
    cols_to_remove.sort(reverse=True)
    for loc,row in enumerate(table):
        for col in cols_to_remove:
            try:
                table[loc].pop(col)
            except AttributeError:
                table.pop(loc)
            except IndexError:
                pass
    return table

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def text_blocks(amount):
    """
    This function prints a help message
    :param amount: the type of help messages to be printed
    :return: prints the help
    """
    if amount == 0:
        # List of instructions for the user
        print('1 - view a sailor'
              '\n2 - ')
    elif amount == 1:
        # Detailed instructions
        print('\nDetailed instructions and more details')
        print('(1) to add a new event')
        print('(2) to add a new sailor')
        print('(3) to get a sailors information')
        print('(4) to quit')
        print('(5) to get sailor info over time')
        print('(6) to print the universe')
        print('(7) to exit the universe')
        print('(8) to import sailors')
        print('(9) to graph sailors over time')
    elif amount == 2:
        # developer instructions with methods locations objects and modes and other parameters and explainations
        print('\nclass: General method: help parameters: mode explaination: if the mode is 0 basic instructions '
              'will be printed, if its 1 detailed instructions will be printed, if its 2 developer '
              'instructions will be printed')
        print('class: General method: multiindex parameters: list(list), term(str or int) explaination: will return'
              ' the index of all the ocourances  of the term inside of the input list')
        print('class: General method: Rank sailor parameters: ratings(list) explaination: will take a list of '
              'ratings and sort them from high to low ')
        print('class: General method: generaterank parameters: rating(int) ratings(list) '
              'explaination: will find the rank of the rating in the unsorted list ratings')
        print('class: General method: __firstcap parameters: word(string) explaination: first letter to a capital')
        print('class: General method: Csvlinegenerate Parameters')

if __name__ == '__main__':
    import unittest
    import tests.tests as t

    suite = unittest.TestLoader().loadTestsFromModule(t)
    # run all tests with verbosity
    unittest.TextTestRunner(verbosity=2).run(suite)
