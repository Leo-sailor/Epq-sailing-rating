from LocalDependencies.csvcode import Csvcode
from LocalDependencies.General import General
base = General()
universecsv = Csvcode()


class HostScript:
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
        inp = 2
        light = 0
        med = 0
        heavy = 0
        while inp != 1:
            racenum = base.cleaninput('Please enter the number of races in the event (1-20):', 'i', rangelow=1,
                                      rangehigh=20)
            light = base.cleaninput('Please enter the number of light wind (0-8kts) races in the event (0-{}):'.format(racenum), 'i', rangelow=0,
                                      rangehigh=racenum)
            racenum -= light
            med = base.cleaninput('Please enter the number of medium wind (9-16kts) races in the event (0-{}):'.format(racenum), 'i',
                                   rangelow=0, rangehigh=racenum)
            racenum -= med
            heavy = racenum
            inp = base.cleaninput(f'That means there were\n{light} light wind races\n{med}  medium wind races\n{heavy} strong wind races\n'
                                  f'press (1) to confirm or press (2) to try again:', 'i',
                                   rangelow=1, rangehigh=2)
        days = base.cleaninput(f'How many days ago was the final race of the event(0-30):', 'i', rangehigh=30,
                               rangelow=0)
        info = self.__getranking('the event')
        for x in range(light):
            universecsv.addrace(1, info[0], info[1])
        for x in range(med):
            universecsv.addrace(2, info[0], info[1])
        for x in range(heavy):
            universecsv.addrace(3, info[0], info[1])
        universecsv.endevent(info[0], days)
    def addeventproper(self):
        racenum = base.cleaninput('Please enter the number of races in the event (1-20):', 'i', rangelow=1, rangehigh=20)
        days = base.cleaninput(f'How many days ago was the final race of the event(0-30):', 'i', rangehigh=30, rangelow=0)
        allsailors = []
        info = []
        for x in range(racenum):
            racetext = ' '.join(['Race', str(x+1)])
            wind = base.cleaninput(f'Please enter the wind strength for {racetext}\n'
                                   f'(1) for light wind - 0-8kts\n'
                                   f'(2) for medium wind - 9-16kts\n'
                                   f'(3) for strong wind - 17+ kts', 'i', rangehigh=3, rangelow=1)
            info = self.__getranking(racetext)
            universecsv.addrace(wind, info[0], info[1])
            for item in info[0]:
                if item not in allsailors:
                    allsailors.append(item)
        universecsv.endevent(allsailors, days)

    def __getranking(self,eventname: str):
        inpmethod = self.__getinputmethod()
        working = True
        position = 0
        positions = []
        sailorids = []
        rawinps = []
        speedprint = []
        print("Press (d) when you are done\n"
              "Press (b) if you want to remove the last sailor\n"
              "Please do not include sailors that DNC but all other codes")
        while working:
            if not speedprint == []:
                print("Position:    {}:    Sailor-id:".format(self.inputmethodname))
                toprint = '\n'.join(speedprint)
                print(toprint)
            position += 1
            inp = base.cleaninput("Please enter the {} of {} place in {}:".format(self.inputmethodname, base.ordinal(position),eventname),
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
                inp.trim().lower()
                sailor = universecsv.getsailorid(self.inpmethod, inp)
                sailorids.append(sailor)
                positions.append(position)
                rawinps.append(inp)
                speedprint.append(f'{position}     {inp}    {sailor}')
        return (sailorids,positions)

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
