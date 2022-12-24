# imports
import requests
from countryinfo import CountryInfo


# class which contains basic funtions for the program not directly related to the elo calculations
class General:
    def __init__(self):
        print('basic functions are working')
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
        try:
            champnum = champnum[:3]
        except:
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
        ratings = self.ranksailor(ratings)
        rank = ratings.index(rating) + 1
        return rank

    def ranksailor(self, ratings):
        ratings.sort(reverse=True)
        return ratings

    def multiindex(self, inlist, term):
        indexs = []
        start = -1
        end = False
        while not end:
            try:
                indexs.append(inlist.index(term, start + 1))
                start = indexs[len(indexs)-1]
            except ValueError:
                end = True
        return indexs

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
