import requests
from countryinfo import CountryInfo
import json
class General:
    def __init__(self):
        print('basic function is working')
        self.basenat = ''
    def GenerateSailorID(self,nat,sailno,first,surname):
        id = ''
        self.validnat = ['ALG','ASA','AND','ANT','ARG','ARM','ARU','AUS','AUT','AZE','BAH','ARN','BAR','BLR','BEL','BIZ','BER','BRA','BOT','IVB','BRU','BUL','CAM','CAN','CAY','CHI','CHN','TPE','COL','COK','CRO','CUB','CYP','CZE','DEN','DJI','DOM','ECU','EGY','ESA','EST','FIJ','FIN','FRA','GEO','GER','GBR','GRE','GRN','GUM','GUA','HKG','HUN','ISL','IND','INA','IRN','IRQ','IRL','ISR','ITA','JAM','JPN','KAZ','KE','PRK','KOR','KOS','KUW','KGZ','LAT','LIB','LBA','LIE','LTU','LUX','MAC','MAD','MAS','MLT','MRI','MEX','MDA','MON','MNE','MNT','MAR','MOZ','MYA','NAM','NED','AHO','NZL','NGR','MKD','NOR','OMA','PAK','PLE','PAN','PNG','PAR','PER','PHI','POL','POR','PUR','QAT','ROM','RUS','SAM','SMR','SEN','SRB','SEY','SGP','SVK','SLO','RSA','ESP','SRI','SKN','LCA','SUD','SWE','SUI','TAH','TAN','THA','TLS','TTO','TUN','TUR','TKS','UGA','UKR','UAE','USA','URU','ISV','VAN','VEN','ZIM']

        nat = nat.upper()

        if not(nat in self.validnat):
            nat = self.getnat()
        first += '000'
        surname += '000'
        sailno = str(sailno)
        newsailno = '0000' + sailno
        id += nat[:2]
        id += newsailno[-4:]
        id += '-'
        id += first[:3]
        id += surname[:2]
        return id.lower()

    def getnat(self):
        if self.basenat == '':
            ip = requests.get('https://geolocation-db.com/json').json()
            natname = ip['country_name']
            choice = input('\nAre the majority of competitors from the {}?\ny for yes and n for no'.format(natname))
            if choice.upper() == 'Y':
                # use py py country info to get country
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
