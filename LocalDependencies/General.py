# imports
import time

import requests
from countryinfo import CountryInfo
from hashlib import md5
from bcrypt import gensalt, hashpw
from datetime import datetime, date, timedelta
import pandas as pd
from difflib import SequenceMatcher
from tkinter import filedialog
from os import remove
from tabula import read_pdf

# class which contains basic funtions for the program not directly related to the elo calculations
class General:
    def __init__(self):
        # print('basic functions are working')
        self.basenat = ''
        self.validnat = {'ALG', 'ASA', 'AND', 'ANT', 'ARG', 'ARM', 'ARU', 'AUS', 'AUT', 'AZE', 'BAH', 'ARN', 'BAR',
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
        self.numbers = ['0','1','2','3','4','5','6','7','8','9']

    @staticmethod
    def getfilename(mode='r'):
        file = filedialog.askopenfile(mode)
        file.close()
        return file.name

    def getdate(self,returnmethod='epoch'):
        """

        :param returnmethod: epoch is seconds since epoch, text returns a text format, date returns a dateobject, datetime returns a datetime object
        :return:
        """
        year = self.cleaninput("Please enter the year", 'i', 2000,2100)
        month = self.cleaninput("Please enter the month", 'i', 1, 12)
        if month in [4,6,9,11]:
            day = self.cleaninput("Please enter the day", 'i', 1, 30)
        elif month in [1,3,5,7,8,10,12]:
            day = self.cleaninput("Please enter the day", 'i', 1, 31)
        else:
            day = self.cleaninput("Please enter the day", 'i', 1, 28)
        current = date(year,month,day)
        match returnmethod:
            case 'epoch':
                epoch = date(1970,1,1)
                return (current-epoch).total_seconds()
            case 'text':
                return current.strftime()
            case 'date':
                return current
            case 'datetime':
                return datetime(year,month,day,0,0,0,0)
    @staticmethod
    def twothousandtodatetime(days):
        thousand = date(2000,1,1)
        delta = timedelta(days)
        return (thousand + delta)


    @staticmethod
    def dayssincetwothousand(self) -> int:
        thousand = date(2000, 1, 1)
        now = date.today()
        day = now - thousand
        return day.days

    def cleaninput(self, prompt: str, datatype: str, rangelow: float = 0, rangehigh: float = 500, charlevel: int = 0,
                   correcthash='', salt=''.encode(),):
        """This function takes a prompt and a type and keeps taking an input from the user until it furfills the
        requirmetns attached
        char lever 0: all characters allowed
        char level 1: characters good for files allowed
        char level 2: character good for sailor id
        char level 3: character good for names
        for range high and range low, its less than or equal"""
        if datatype == 's':
            if charlevel == 0 or charlevel == '0':
                return input(prompt)
            elif charlevel == 1 or charlevel == '1':
                files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                         'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
                         'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5',
                         '6', '7', '8', '9', '.', '_', '\'', '(', ')', ':']
                same = False
                name = ''
                while not same:
                    origname = input(prompt).lower()
                    name = (x for x in origname if x in files)
                    name = ''.join(name)
                    if origname.upper() != name.upper():
                        num = input(f'\nYour string is {name}\nPlease press (enter) to continue or (1) to retype')

                        if num == '':
                            same = True
                    else:
                        same = True
                return name
            elif charlevel == 2 or charlevel == '2':
                files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                         'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
                         'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5',
                         '6', '7', '8', '9', '-']
                name = ''
                same = False
                while not same:
                    origname = input(prompt).lower()
                    name = (x for x in origname if x in files)
                    # print(f'name =\'{name}\'')
                    name = ''.join(name)
                    # print(f'name =\'{name}\'')
                    if origname.upper() != name.upper():
                        num = input(f'\nYour string is {name}\nPlease press (enter) to continue or (1) to retype')

                        if num == '':
                            same = True
                    else:
                        same = True
                return name
            elif charlevel == 3 or charlevel == '3':
                alphebet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                            'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '-', ' ']
                name = ''
                same = False
                while not same:
                    origname = input(prompt)
                    name = (x for x in origname if x.upper() in alphebet)
                    name = ''.join(name)
                    name = self.__firstcap(name)
                    if origname.upper() != name.upper():
                        num = input(f'\nYour string is {name}\nPlease press (enter) to continue or (1) to retype')

                        if num == '':
                            same = True
                    else:
                        same = True
                return name

        elif datatype == 'f':
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

        elif datatype == 'i':
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
                passwordb = input('Please it again to confirm:')
                same = passwordb == passworda
                if not same:
                    print('\nThose passwords did not match, Please try again')
            return self.passwordhash(passwordb)

        elif datatype == 'pr':
            done = False
            while not done:
                inp = input(prompt)
                if self.passwordhash(inp, salt)[0] == correcthash:
                    print('\nPassword is correct')
                    return True
                elif inp == '':
                    print('\nPassword entry is skipped')
                    return False
                else:
                    print('\nThat password was incorrect, please try again')

        else:
            return ''

    def generatesailorid(self, nat: str, sailno: str | int, first: str, surname: str) -> tuple[str, str]:
        """
        This function generates a sailorid from its components
        :param nat: 3 letter sting or none
        :param sailno: 5 number string
        :param first: string
        :param surname: string
        :return: string
        """
        iden = ''

        nat = nat.upper()

        if nat not in self.validnat:
            nat = self.getnat()
        first += '000'
        surname += '000'
        sailno = str(sailno)
        newsailno = '0000' + sailno
        iden += nat[:2]
        iden += '-'
        iden += newsailno[-4:]
        iden += '-'
        iden += first[:3]
        iden += surname[:2]
        return iden.lower(), nat

    def ordinal(self, num):
        suffixes = {1: 'st', 2: 'nd', 3: 'rd'}
        if 10 <= num % 100 <= 20:
            suffix = 'th'
        else:
            # the second parameter is a default.
            suffix = suffixes.get(num % 10, 'th')
        return str(num) + suffix

    def getnat(self) -> str:
        """
        This function gets the current computer's adress and uses that to generate a suggested 3 letter country code
        :return: 3 letter country code
        """
        if self.basenat == '':
            ip = requests.get('https://geolocation-db.com/json').json()
            natname = ip['country_name']
            choice = input('\nAre the majority of competitors from the {}?\ny for yes and n for no'.format(natname))
            if choice.upper() == 'Y':
                # use py pi country info to get country
                country = CountryInfo(natname)
                self.basenat = country.iso(3)
            else:
                while self.basenat == '':
                    basenatposs = input('Please enter the majority of your competitors\' 3 Letter country code')
                    if basenatposs.upper() in self.validnat:
                        self.basenat = basenatposs.upper()
                    else:
                        print('Sorry, that country code is not valid please try again')
            return self.basenat
        else:
            return self.basenat

    def csvlinegenerate(self, sailorid: str, nat: str, sailno: str, first: str, surname: str, region: str, champnum: str) -> str:
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
        if nat not in self.validnat:
            nat.upper()
            nat.strip()

        parts = [sailorid, champnum, sailno, first, surname, region, nat, 1500, 1500, 1500, 1500, rank, self.dayssincetwothousand()]

        line = ','.join(parts)

        # print('{}'.format(line))

        return line

    def __firstcap(self, word: str):
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

    def SortOnElement(self, sub_li, element):
        sub_li.sort(reverse=True, key=lambda x: x[element])
        return sub_li

    def multiindex(self, inlist: list, term: int | str) -> list:
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

            inlist[x] = inlist[x].lower().strip()

        indexs = []
        start = 0
        end = False
        while not end:
            try:
                indexs.append(inlist.index(term, start + 1))
                start = indexs[-1]
            except ValueError:
                end = True
        return indexs

    def passwordhash(self, password, salt=None):
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

    @staticmethod
    def hashfile(file):
        """
        This function takes a file adress and opens it as a text file and produces a md5 hash of it
        :param file: the file address of the file to be hashed
        :return: the string of the md5 hash
        """
        with open(file) as actualfile:
            str2hash = actualfile.read()
        result = md5(str2hash.encode()).hexdigest()
        return str(result)


    def gettablefromhtmlfile(self,file, tablenum = 0):
        df_list = pd.read_html(file)
        lists = df_list[tablenum].values.tolist()
        header = [list(df_list[tablenum].columns.values)]
        lists.insert(0,header)
        return lists

    def gettablefromweb(self,url,tablenum=0):
        page = requests.get(url)
        g = open('webpage.temp', 'w').write(page.text)
        del g
        out = self.gettablefromhtmlfile('webpage.temp',tablenum)
        remove('webpage.temp')
        return out

    def findandreplace(self, inp, find: str, replace: str, preserve_type=False):
        """
        a recussive find and replace algoritim which searchs through lists and thiers sub lits up to the recursion limit
        in search of strings, when a string is found, a normal find and replace algoritim on is applied to the string.
        intended side effect: all int
        THIS IS A TIME CRITICAL FUNCTION, TIME TO RUN > READABILTY OR MAINAINABILITY OR LOC (LINES OF CODE)
        :param inp:
        :param find:
        :param replace:
        :return:
        """
        match inp:
            case str():
                return inp.replace(find,replace)
            case list():
                out = []
                for item in inp:
                    out.append(self.findandreplace(item, find, replace))
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

    def tablefrompdf(self, file: str, tablenum: int = -1,purge_nan_col:bool = True) -> list[list]:
        df_list = read_pdf(file, pages="all") # reads pdf with tabula, is a utter shit module tho caus eof java requirements
        # use this stack overfolw page to get it working on your computer: https://stackoverflow.com/questions/54817211/java-command-is-not-found-from-this-python-process-please-ensure-java-is-inst
        print('2. Read')
        df = pd.concat(df_list) # each page comes as a spererate table, this puts them all into one
        lists = df.values.tolist() # gets the raw data as a python array
        header = self.findandreplace([(df.columns.tolist())],'\r',' ') # cleans the header
        lists.insert(0,header)
        big_table = self.findandreplace(lists, "\r", " ") # cleans the table
        print('3. cleaned')
        if tablenum == -1 : # if we want all the tables
            return big_table
        table_start_point = [1] # the array which stores the locations of each new set of data
        first_col = [row[0] for row in big_table]
        old = 0
        for x in range(1,len(first_col)): # assumes new set of data begins, when place field (always column 1) goes downwards, (differnt to normal)
            try:
                new = int(first_col[x])
            except ValueError:
                new = ['0']
                for char in first_col[x]:
                    if char in self.numbers:
                        new.append(char)
                new = int(''.join(new))
            if old > new:
                table_start_point.append(x)
            old = new


        end = len(big_table)
        tables = []
        for x in range(len(table_start_point)-1,-1,-1): # reverse order to make sure nothing gets messed with
            new_table = big_table[table_start_point[x]:end] # splits data
            new_table.insert(0,header[0]) # adds headers to each set
            # new_table = [new_table]
            tables.insert(0,new_table) # adds new table to list of tables
            end = table_start_point[x] - 1
        print('4. Split')
        if not(purge_nan_col):
            return tables[tablenum]

        table = tables[tablenum]
        cols_to_remove = list(range(len(table[0])))
        for x in range(1,len(table)):
            data = []
            for y in cols_to_remove:
                if table[x][y] != 'nan':
                    data.append(y)
            for item in data:
                index = cols_to_remove.index(item)
                cols_to_remove.pop(index)
        cols_to_remove.sort(reverse=True)
        for row in table:
            for col in cols_to_remove:
                row.pop(col)
        print('5. clean nan')
        return table


    def url_to_pdf_to_table(self,url,tablenum: int =-1,purge_nan_col:bool = True) -> list[list]:
        page = requests.get(url) # gets the page as a response object
        print('1. Internet')
        start_time = time.perf_counter_ns()
        g = open('webpage.temp', 'wb').write(page.content) # writes the contents of the response object to a field
        del g # deletes an unused variable, it didnt work for me without this
        out = self.tablefrompdf('webpage.temp', tablenum, purge_nan_col) # gets the outpu as if a local file
        remove('webpage.temp') # removes the temp file
        end_time = time.perf_counter_ns()
        print((end_time-start_time)/1000000)
        return out


    @staticmethod
    def similar(a, b):
        return SequenceMatcher(None, a, b).ratio()

    def help(self, amount):
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
