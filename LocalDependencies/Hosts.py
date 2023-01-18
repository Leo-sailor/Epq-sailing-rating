from LocalDependencies.csvcode import Csvcode
from LocalDependencies.General import General
base = General()
universecsv = Csvcode()


class hostscript:
    def __init__(self):
        self.inpmethod = ''
        self.inputmethodname = ''

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

    @staticmethod
    def makenewsailor():
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

    def addeventlazy(self):
        pass

    def addeventproper(self):
        pass

    def __getranking(self):
        inpmethod = self.__getinputmethod()
        working = True
        position = 0
        positions = []
        sailorids = []
        rawinps = []
        speedprint = []
        print("Press (d) when you are done\n"
              "Press (b) if you want to remove the last sailor")
        while working:
            if not speedprint == []:
                print("Position:    {}:    Sailor-id:".format(self.inputmethodname))
                for line in speedprint:
                    print(line)
            position += 1
            inp = base.cleaninput("Please enter the {} of {} place:".format(self.inputmethodname, base.ordinal(position)),
                                  's',charlevel=2).lower()
            if inp == 'd':
                working = False
            elif inp == 'b':
                position -= 1
                positions.pop(-1)
                speedprint.pop(-1)
                sailorids.pop(-1)
                rawinps.pop(-1)
            else:
                universecsv.getsailorid()
    def __getinputmethod(self):
        inpmethods = ['c', 'n', 'i', 's']
        if self.inpmethod in inpmethods:
            if self.inpmethod == 'c':
                self.inputmethodname = 'Championship Number'
            elif self.inpmethod == 'n':
                self.inputmethodname = 'Name'
            elif self.inpmethod == 'i':
                self.inputmethodname = 'Sailor-id'
            else:
                self.inputmethodname = 'Sail Number'
            inp = base.cleaninput((''.join(('Your current selected input method is: ', self.inputmethodname,
                                           '\nWould you like to change it?\n(1) for yes\n(0) for no:'))),
                                  'i', rangehigh=2, rangelow=1)
            if inp == 1:
                ip = ''
            else:
                ip = self.inpmethod
        else:
            ip = ''
        while ip not in inpmethods:
            ip = base.cleaninput('How would you like to enter sailors information?\n'
                                 '(c) for Championship Number\n'
                                 '(i) for Sailor-id\n'
                                 '(n) for Name\n'
                                 '(s) for Sail Number:', 's').lower()
        self.inpmethod = ip
        return ip

    def addevent(self):
        inp = base.cleaninput('Please enter (1) for entering event results(less accurate - quicker)\n'
                              'Please enter (2) for entering individual race results (higher accuracy - slower)',
                              'i', rangehigh=2, rangelow=1)
        if inp == 1:
            self.addeventlazy()
        else:
            self.addeventproper()
