# imports
import requests
from countryinfo import CountryInfo
from hashlib import md5
from bcrypt import gensalt, hashpw
from datetime import date


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
                            'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '-']
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
                    print('Password is correct')
                    return True
                elif inp == '':
                    print('Password entry is skipped')
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
        SUFFIXES = {1: 'st', 2: 'nd', 3: 'rd'}
        if 10 <= num % 100 <= 20:
            suffix = 'th'
        else:
            # the second parameter is a default.
            suffix = SUFFIXES.get(num % 10, 'th')
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

        first = self.__firstcap(first)
        surname = self.__firstcap(surname)
        region = region[:3].upper().strip()
        champnum = '000' + str(champnum)
        champnum = champnum[-3:]
        if nat not in self.validnat:
            nat.upper()
            nat.strip()

        parts = [sailorid, champnum, sailno, first, surname, region, nat, 1500, 1500, 1500, 1500, rank, 0]

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
        word = word[0].upper() + word[1:]
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

            inlist[x] = inlist[x].lower().trim()

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

    def hashfile(self, file):
        """
        This function takes a file adress and opens it as a text file and produces a md5 hash of it
        :param file: the file address of the file to be hashed
        :return: the string of the md5 hash
        """
        str2hash = open(file).read()
        result = md5(str2hash.encode()).hexdigest()
        return str(result)

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
            print('Detailed instructions and more details')
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
