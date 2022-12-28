# imports
import requests
from countryinfo import CountryInfo
from hashlib import md5, sha256


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

    def cleaninput(self, prompt, datatype, rangelow=0, rangehigh=500, charlevel=0, correcthash='', failhash=''):
        """char lever 0: all characters allowed
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
                    name = input(prompt).lower()
                    name = (x for x in name if x in files)
                    name = ''.join(name)
                    num = self.cleaninput((f'Your string is now {name} \nDo you want to change this'
                                           f'\nPlease type 1 for yes\nPlease type 2 for no'),
                                          'i', rangelow=1, rangehigh=2)
                    if num == 2:
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
                    name = input(prompt).lower()
                    name = (x for x in name if x in files)
                    name = ''.join(name)
                    num = self.cleaninput((f'Your string is now {name} \nDo you want to change this'
                                           f'\nPlease type 1 for yes\nPlease type 2 for no'),
                                          'i', rangelow=1, rangehigh=2)
                    if num == 2:
                        same = True
                return name
            elif charlevel == 3 or charlevel == '3':
                alphebet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                            'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '-']
                name = ''
                same = False
                while not same:
                    name = input(prompt)
                    name = (x for x in name if x.upper() in alphebet)
                    name = ''.join(name)
                    name = self.__firstcap(name)
                    num = self.cleaninput((f'Your string is now {name} \nDo you want to change this'
                                           f'\nPlease type 1 for yes\nPlease type 2 for no'),
                                          'i', rangelow=1, rangehigh=2)
                    if num == 2:
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
            while rangelow >= inp >= rangehigh:
                print('\nThat value was not accepted, Please Try Again')

                try:
                    inp = int(input(prompt))
                except ValueError:
                    print('\nThat input was not a integer, please enter a whole number')
                    inp = 5000000000
            return inp

        elif datatype == 'pn':
            passwordB = ''
            same = False
            while not same:
                passwordA = input(prompt)
                passwordB = input('Please it again to confirm:')
                same = passwordB == passwordA
                if not same:
                    print('\nThose passwords did not match, Please try again')
            return self.passwordhash(passwordB)

        elif datatype == 'pr':
            done = False
            while not done:
                inp = input(prompt)
                if self.passwordhash(inp) == correcthash:
                    print('Password is correct')
                    return True
                elif self.passwordhash(inp) == failhash:
                    print('Password entry is skipped')
                    return False
                else:
                    print('\nThat password was incorrect, please try again')

        else:
            return ''

    def generatesailorid(self, nat, sailno, first, surname):
        iden = ''

        nat = nat.upper()

        if not(nat in self.validnat):
            nat = self.getnat()
        first += '000'
        surname += '000'
        sailno = str(sailno)
        newsailno = '0000' + sailno
        iden += nat[:2]
        iden += newsailno[-4:]
        iden += '-'
        iden += first[:3]
        iden += surname[:2]
        return iden.lower()

    def getnat(self):
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

    def csvlinegenerate(self, sailorid, nat, sailno, first, surname, region, champnum):
        line = ''
        rank = self.generaterank(1500, [1700, 1600, 1500, 1400])

        first = self.__firstcap(first)
        surname = self.__firstcap(surname)
        region = region[:3].upper().strip()
        champnum = '000' + str(champnum)
        champnum = champnum[-3:]
        if not(nat in self.validnat):
            nat.upper()
            nat.strip()

        parts = [sailorid, champnum, sailno, first, surname, region, nat, 1500, 1500, 1500, 1500, rank, 0]

        for x in range(0, 12):
            line += str(parts[x])
            line += ','

        line += str(parts[12])

        print('{}'.format(line))

        return line

    def __firstcap(self, word):
        word = word.lower()
        word = word.strip()
        word = word[0].upper() + word[1:]
        return word

    def generaterank(self, rating, ratings):
        ratings = self.__ranksailor(ratings)
        rank = ratings.index(rating) + 1
        return rank

    def __ranksailor(self, ratings):
        ratings.sort(reverse=True)
        return ratings

    def multiindex(self, inlist, term):
        indexs = []
        start = -1
        end = False
        while not end:
            try:
                indexs.append(inlist.index(term, start + 1))
                start = indexs[-1]
            except ValueError:
                end = True
        return indexs

    def passwordhash(self, password):
        hashed = sha256(password.encode()).hexdigest()
        return hashed

    def hashfile(self, file):
        str2hash = open(file).read()
        result = md5(str2hash.encode()).hexdigest()
        return str(result)

    def help(self, amount):
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
