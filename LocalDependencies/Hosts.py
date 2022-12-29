from LocalDependencies.csvcode import Csvcode
from LocalDependencies.General import General
base = General()
universecsv = Csvcode()


class Hosts:
    def torun(self):
        index = universecsv.getsailorid(2, '4036')
        print(index)

        print('\nWhat would you like to do?')
        base.help(1)
        choice = input()

        # new test caases
        universecsv.updatesinglevalue(217, 1, 1)
        universecsv.updatesinglevalue(317, 1, 1)

        # old test cases
        currentrating = [1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500]
        sailorid = [5, 3, 2, 4]

        nat = 'gbr'
        first = 'leo'
        sur = 'yates'
        sail = 48153

        sailorid[0] = base.generatesailorid(nat, sail, first, sur)

        # print('nationality: {}\nFist name: {}\nSurname: {}\nsail number {}'.format(nat, first, sur, sail))
        # print('\nsailor id is: {}'.format(sailorid[0]))

        # print('csv line is: {}'.format(base.csvlinegenerate(sailorid[0], nat, sail, first, sur, 'LSE', 317)))
        # print('it should be: gb-8153-leoya,317,48153,Leo,Yates,LSE,gbr,1500,1500,1500,1500,5,0')
    def makenewsailor(self):
        print('\n NEW SAILOR WIZZARD')
        first = base.cleaninput('Please enter the sailor\'s first name:', 's', charlevel=3)
        sur = base.cleaninput('Please enter the sailor\'s surname:', 's', charlevel=3)
        champ = str(base.cleaninput('Please enter the sailor\'s Championship number '
                                    '\n(Please enter (000) if the sailor does not have a Champ number):',
                                    'i', rangehigh=999))
        sailno = str(base.cleaninput('Please enter the sailor\'s Sail number '
                                     '\n(Please ignore any letters):',
                                     'i', rangehigh=99999))
        nat = base.cleaninput('Please enter the sailor\'s 3 letter country code:', 's', charlevel=3).upper()[:3]
        out = base.generatesailorid(nat, sailno, first, sur)
        sailorid = out[0]
        nat = out[1]
        if nat == 'GBR':
            region = base.cleaninput('\n SC - Scotland\n SE - London and South-east\n SW - South-west\n SO - South'
                                     '\n MD - Midlands\n NO - North\n NI - Northen Ireland\n WL - Wales\n EA - East'
                                     '\nPlease enter the sailor\'s 2 letter RYA region code:',
                                     's', charlevel=3).upper()[:2]
        else:
            region = 'NA'
        return universecsv.addsailor(sailorid, first, sur, champ, sailno, region, nat)
