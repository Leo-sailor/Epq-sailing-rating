from LocalDependencies.Main_core import Csvcode
from LocalDependencies.General import General
from LocalDependencies.Csv_custom import Csvnew
base = General()
universecsv = Csvcode()
import datetime

class HostScript:
    def __init__(self):
        self.inpmethod = ''
        self.inputmethodname = ''

    def torun(self):
        while True:
            base.help(1)
            choice = base.cleaninput('\nWhat would you like to do?','i',rangelow=1,rangehigh=4)
            match choice:
                case 1:
                    self.addevent()
                case 2:
                    self.makenewsailor()
                case 3:
                    self.getsailorinfo()
                case 4:
                    break

        # print('nationality: {}\nFist name: {}\nSurname: {}\nsail number {}'.format(nat, first, sur, sail))
        # print('\nsailor id is: {}'.format(sailorid[0]))

        # print('csv line is: {}'.format(base.csvlinegenerate(sailorid[0], nat, sail, first, sur, 'LSE', 317)))
        # print('it should be: gb-8153-leoya,317,48153,Leo,Yates,LSE,gbr,1500,1500,1500,1500,5,0')
    def getsailorinfo(self):
        print('\nSAILOR INFO WIZZARD\n')
        print('please enter type of information you would like to recive')
        print('(c) for champ number\n(s) for sail number\n(l) for light wind rating\n(n) for name\n(i) for sailor id\n'
              '(m) for medium wind rating\n(h) for high wind rating\n(o) for overall rating\n(r) for rank\n'
              '(e) for total events\n(d) for date of last event\n(z) for zone / region\n'
              '(t) for territory / country\n(a) for all\n(s) for sailor info (not including rating rank or events)')
        outtype = base.cleaninput("\nWhat would u like to recive?", 's')
        outtype.lower().strip()
        a = {'c': 'Championship Number', 's': 'Sail Number', 'l': 'Light wind rating', 'm': 'Medium wind rating',
             'h': 'Heavy wind rating', 'n': 'Name', 'i': 'sailorid', 'o': 'Overall rating', 'r': 'Rank',
             'e': 'Total events', 'd': 'Date of last event', 'z': 'Zone/Region', 't': 'Territory/country', 'a': 'All',
             'S': 'Sailor info'}
        outtypename = a[outtype]
        inpmethod = self.__getinputmethod()
        inp = base.cleaninput(f'Please enter the sailor\'s {self.inputmethodname}:', 's')
        sailorid = universecsv.getsailorid(inpmethod,inp)
        out = universecsv.getinfo(sailorid, outtype)
        if outtype == 'd':
            twothousand = datetime.date(2000, 1, 1)

            out = twothousand + datetime.timedelta(days=float(out))
        print(f'\n{inp}\'s {outtypename} is {out}')

    @staticmethod
    def makenewsailor(name=None, sailno=None, champ=None):
        print('\n NEW SAILOR WIZZARD')
        if name is None:
            name = base.cleaninput('Please enter the sailor\'s name:', 's', charlevel=3)
        name = name.split(' ', 1)
        first = name[0]
        sur = name[1]
        if champ is None:
            champ = str(base.cleaninput('Please enter the sailor\'s Championship number '
                                        '\n(Please enter (000) if the sailor does not have a Champ number):',
                                        'i', rangehigh=999))
        if sailno is None:
            sailno = str(base.cleaninput('Please enter the sailor\'s Sail number '
                                         '\n(Please ignore any letters):',
                                         'i', rangehigh=99999))
        nat = base.cleaninput('\n(enter) for automatic\nPlease enter the sailor\'s 3 letter country code:', 's', charlevel=3).upper()[:3]
        out = base.generatesailorid(nat, sailno, first, sur)
        sailorid = out[0]
        nat = out[1]
        if nat == 'GBR':
            region = base.cleaninput('\n SC - Scotland\n SE - London and South-east\n SW - South-west\n SO - South'
                                     '\n MD - Midlands\n NO - North\n NI - Northen Ireland\n WL - Wales\n EA - East'
                                     '\n NA - Unknown\nPlease enter {} {}\'s\'s 2 letter RYA region code:'.format(first, sur),
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
            racenum = base.cleaninput('\nPlease enter the number of races in the event (1-20):', 'i', rangelow=1,
                                      rangehigh=20)
            light = base.cleaninput('\nPlease enter the number of light wind (0-8kts) races in the event (0-{}):'.format(racenum), 'i', rangelow=0,
                                    rangehigh=racenum)
            racenum -= light
            med = base.cleaninput('Please enter the number of medium wind (9-16kts) races in the event (0-{}):'.format(racenum), 'i',
                                  rangelow=0, rangehigh=racenum)
            racenum -= med
            heavy = racenum
            inp = base.cleaninput(f'\nThat means there were\n{light} light wind races\n{med} medium wind races\n{heavy} strong wind races\n'
                                  f'press (1) to confirm or press (2) to try again:', 'i',
                                  rangelow=1, rangehigh=2)
        days = base.cleaninput(f'\nHow many days ago was the final race of the event(0-500):', 'i', rangehigh=500,
                               rangelow=0)
        info = self.__getranking('the event')
        for x in range(light):
            universecsv.addrace(1, info[0], info[1], days)
        for x in range(med):
            universecsv.addrace(2, info[0], info[1], days)
        for x in range(heavy):
            universecsv.addrace(3, info[0], info[1], days)
        universecsv.endevent(info[0], days)

    def addeventproper(self):
        racenum = base.cleaninput('\nPlease enter the number of races in the event (1-20):', 'i', rangelow=1, rangehigh=20)
        days = base.cleaninput(f'\nHow many days ago was the final race of the event(0-500):', 'i', rangehigh=500, rangelow=0)
        allsailors = []
        for x in range(racenum):
            racetext = ' '.join(['Race', str(x+1)])
            print(f'\n{racetext.upper()} ENTRY WIZZARD')
            wind = base.cleaninput(f'\nPlease enter the wind strength for {racetext}\n'
                                   f'(1) for light wind - 0-8kts\n'
                                   f'(2) for medium wind - 9-16kts\n'
                                   f'(3) for strong wind - 17+ kts:', 'i', rangehigh=3, rangelow=1)
            info = self.__getranking(racetext)
            universecsv.addrace(wind, info[0], info[1], days)
            for item in info[0]:
                if item not in allsailors:
                    allsailors.append(item)
        universecsv.endevent(allsailors, days)

    def addeventcsv(self):
        racenum = base.cleaninput('\nPlease enter the number of races in the event (1-20):', 'i', rangelow=1,
                                  rangehigh=20)
        days = base.cleaninput(f'\nHow many days ago was the final race of the event(0-500):', 'i', rangehigh=500,
                               rangelow=0)
        allsailors = []
        for x in range(racenum):
            racetext = ' '.join(['Race', str(x + 1)])
            print(f'\n{racetext.upper()} ENTRY WIZZARD')
            fileloc = base.cleaninput(f'Please enter the full file location of the file for {racetext}:','s',charlevel=0)
            currfile = Csvnew(fileloc)
            wind = int(currfile.getcell(0, 1))
            currsailorids = currfile.getcolumn(0, [0, 1])
            positions = currfile.getcolumn(1, [0, 1])
            for x in range(len(positions)):
                positions[x] = int(positions[x])

            for item in currsailorids:
                if item not in allsailors:
                    allsailors.append(item)
            universecsv.addrace(wind, currsailorids, positions, days, imported = True)

    def __getranking(self, eventname: str):
        self.__getinputmethod()
        working = True
        position = 0
        positions = []
        sailorids = []
        rawinps = []
        speedprint = []
        print("\nPlease do not include sailors that DNC but all other codes"
              "\nPress (d) when you are done\n"
              "Press (b) if you want to remove the last sailor\n")
        while working:
            if not speedprint == []:
                print("\nPosition:    {}:    Sailor-id:".format(self.inputmethodname))
                toprint = '\n'.join(speedprint)
                print(toprint)
            position += 1
            inp = base.cleaninput("\nPlease enter the {} of {} place in {}:".format(self.inputmethodname, base.ordinal(position), eventname),
                                  's', charlevel=0).lower()
            if inp == 'd':
                working = False
            elif inp == 'b':
                position -= 1
                positions.pop(-1)
                speedprint.pop(-1)
                sailorids.pop(-1)
                rawinps.pop(-1)
            else:
                inp.lower().strip()
                sailor = universecsv.getsailorid(self.inpmethod, inp)
                if sailor in sailorids:
                    print('\nThis sailor has already been entered, please try again')
                    position -= 1
                else:
                    sailorids.append(sailor)
                    positions.append(position)
                    rawinps.append(inp)
                    speedprint.append(f'{position}            {inp}           {sailor}')
        return sailorids, positions

    def __getinputmethod(self):
        print('\n INPUT METHOD SELECTION')
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
            inp = base.cleaninput((''.join(('\nYour current selected input method is: ', self.inputmethodname,
                                           '\nWould you like to change it?\n(0) for no\n(1) for yes:'))),
                                  'i', rangehigh=1, rangelow=0)
            if inp == 1:
                ip = ''
            else:
                ip = self.inpmethod
        else:
            ip = ''
        while ip not in inpmethods:
            ip = base.cleaninput('\nHow would you like to enter sailors information?\n'
                                 '(c) for Championship Number\n'
                                 '(i) for Sailor-id\n'
                                 '(n) for Name\n'
                                 '(s) for Sail Number:', 's').lower()
        self.inpmethod = ip
        if self.inpmethod == 'c':
            self.inputmethodname = 'Championship Number'
        elif self.inpmethod == 'n':
            self.inputmethodname = 'Name'
        elif self.inpmethod == 'i':
            self.inputmethodname = 'Sailor-id'
        else:
            self.inputmethodname = 'Sail Number'
        return ip

    def addevent(self):
        if not universecsv.admin:
            print('\nTo add an event you need admin rights')
            if not universecsv.adminrights():
                print('\nAdd event failed, please try with admin rights')
                return ''

        print("\nEVENT ENTRY WIZZARD")
        inp = base.cleaninput('\n(1) for entering overall event results (less accurate - quicker)\n'
                              '(2) for entering individual race results (higher accuracy - slower)\n'
                              '(3) for importing previous race (needs previously entered csv):',
                              'i', rangehigh=3, rangelow=1)
        if inp == 1:
            self.addeventlazy()
        elif inp == 2:
            self.addeventproper()
        elif inp == 3:
            self.addeventcsv()
        else:
            pass
