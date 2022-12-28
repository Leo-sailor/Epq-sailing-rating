import csvcode
import General
csv = csvcode.Csvcode()
base = General.General()


class Hosts:
    def makenewsailor(self):
        print('\n NEW SAILOR WIZZARD')
        first = base.cleaninput('Please enter the sailor\'s first name:', 's', charlevel=3)
        sur = base.cleaninput('Please enter the sailor\'s surname:', 's', charlevel=3)
        champ = str(base.cleaninput('Please enter the sailor\'s Championship number '
                                    '\n(Please enter 000 if the sailor does not have a Champ number):',
                                    'i', rangehigh=999))
        sailno = str(base.cleaninput('Please enter the sailor\'s Sail number '
                                     '\n(Please ignore any letters):',
                                     'i', rangehigh=99999))
        nat = base.cleaninput('Please enter the sailor\'s 3 letter country code', 's', charlevel=3).upper()[:3]
        if nat == 'GBR':
            region = base.cleaninput('\n SC - Scotland\n SE - London and South-east\n SW - South-west\n SO - South'
                                     '\n MD - Midlands\n NO - North\n NI - Northen Ireland\n WL - Wales\n EA - East'
                                     '\nPlease enter the sailor\'s 2 letter RYA region code',
                                     's', charlevel=3).upper()[:2]
        else:
            region = 'NA'
        sailorid = base.generatesailorid(nat, sailno, first, sur)
        return csv.addsailor(sailorid, first, sur, champ, sailno, region, nat)
