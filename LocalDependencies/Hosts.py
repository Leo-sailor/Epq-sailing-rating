from LocalDependencies.Main_core import Csvcode
import LocalDependencies.General as Base
from LocalDependencies.Csv_custom import Csvnew
import LocalDependencies.dataclasses as dat
universecsv = Csvcode()
import datetime


class HostScript:
    def __init__(self):
        self.inpmethod = ''
        self.inputmethodname = ''

    def torun(self):
        g = Base.url_to_pdf_to_table("https://gbrtopper.ourclubadmin.com/docs/1185/53_After_Race_5_Provisional.pdf", 0)
        print(g)



        while True:
            Base.text_blocks(1)
            choice = Base.cleaninput('\nWhat would you like to do?', 'i', rangelow=1, rangehigh=4)
            match choice:
                case 1:
                    self.addevent()
                case 2:
                    self.makenewsailor()
                case 3:
                    self.getsailorinfo()
                case 4:
                    break
                case 5:
                    self.sailorratingovertime()


    def sailorratingovertime(self):
        inpmethod = self.__getinputmethod()
        inp = Base.cleaninput(f'(enter (_a) for all) \nPlease enter the sailor\'s {self.inputmethodname}:', 's')
        sailorid = universecsv.getsailorid(inpmethod, inp)
        # TODO make this work and finnish it
    def getsailorinfo(self):
        info_codes = {'c': 'Championship Number', 's': 'Sail Number', 'l': 'Light wind rating', 'm': 'Medium wind rating',
             'h': 'Heavy wind rating', 'n': 'Name', 'i': 'sailorid', 'o': 'Overall rating', 'r': 'Rank',
             'e': 'Total events', 'd': 'Date of last event', 'z': 'Zone/Region', 't': 'Territory/country', 'a': 'All',
             'S': 'Sailor info'}
        print('\nSAILOR INFO WIZZARD\n')
        print('please enter type of information you would like to recive')
        for key,val in info_codes.items(): # prints all the info_codes
            print(f'({key}) for {val}')

        outtype = Base.cleaninput("\nWhat would u like to recive?", 's')
        outtype.lower().strip()
        outtypename = info_codes[outtype]

        inpmethod = self.__getinputmethod()
        inp = Base.cleaninput(f'Please enter the sailor\'s {self.inputmethodname}:', 's')

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
            name = Base.cleaninput('Please enter the sailor\'s Full name:', 's', charlevel=3)
        name = name.split(' ', 1)
        first = name[0]
        try:
            sur = name[1]
        except IndexError:
            sur = Base.cleaninput('Please enter the sailor\'s  surname:', 's', charlevel=3)
        if champ is None:
            champ = str(Base.cleaninput('Please enter the sailor\'s Championship number '
                                        '\n(Please enter (000) if the sailor does not have a Champ number):',
                                        'i', rangehigh=999))
        if sailno is None:
            sailno = str(Base.cleaninput('Please enter the sailor\'s Sail number '
                                         '\n(Please ignore any letters):',
                                         'i', rangehigh=99999))
        nat = Base.cleaninput('\n(enter) for automatic\nPlease enter the sailor\'s 3 letter country code:', 's', charlevel=3).upper()[:3]
        out = Base.generatesailorid(nat, sailno, first, sur)
        sailorid = out[0]
        nat = out[1]
        if nat == 'GBR':
            region = Base.cleaninput('\n SC - Scotland\n SE - London and South-east\n SW - South-west\n SO - South'
                                     '\n MD - Midlands\n NO - North\n NI - Northen Ireland\n WL - Wales\n EA - East'
                                     '\n NA - Unknown\nPlease enter {} {}\'s\'s 2 letter RYA region code:'.format(first, sur),
                                     's', charlevel=3).upper()[:2]
        else:
            region = 'NA'
        return universecsv.addsailor(sailorid, first, sur, champ, sailno, region, nat)

    def addeventlazy(self):
        inp = 2
        light_race_num = 0
        med = 0
        heavy = 0
        while inp != 1:
            racenum = Base.cleaninput('\nPlease enter the number of races in the event (1-20):', 'i', rangelow=1,
                                      rangehigh=20)
            light_race_num = Base.cleaninput(
                '\nPlease enter the number of light wind (0-8kts) races in the event (0-{}):'.format(racenum), 'i',
                rangehigh=racenum)
            racenum -= light_race_num
            med = Base.cleaninput(
                'Please enter the number of medium wind (9-16kts) races in the event (0-{}):'.format(racenum), 'i',
                rangehigh=racenum)
            racenum -= med
            heavy = racenum
            inp = Base.cleaninput(f'\nThat means there were\n{light_race_num} light wind races\n{med} medium wind races\n{heavy} strong wind races\n'
                                  f'press (1) to confirm or press (2) to try again:', 'i',
                                  1, rangehigh=2)

        days = Base.cleaninput('\nHow many days ago was the final race of the event(0-500):', 'i')

        results_obj = self.__getranking('the event')

        for _ in range(light_race_num):
            universecsv.addrace(dat.Race(results_obj, 1, days))
        for _ in range(med):
            universecsv.addrace(dat.Race(results_obj, 2, days))
        for _ in range(heavy):
            universecsv.addrace(dat.Race(results_obj, 3, days))
        universecsv.endevent(results_obj.sailorids, days)

    def addeventproper(self):
        racenum = Base.cleaninput('\nPlease enter the number of races in the event (1-20):', 'i', rangelow=1, rangehigh=20)
        days = Base.cleaninput('\nHow many days ago was the final race of the event(0-500):', 'i')
        allsailors = set()
        for x in range(racenum):
            racetext = ' '.join(['Race', str(x+1)])
            print(f'\n{racetext.upper()} ENTRY WIZZARD')
            wind = Base.cleaninput(f'\nPlease enter the wind strength for {racetext}\n'
                                   f'(1) for light wind - 0-8kts\n'
                                   f'(2) for medium wind - 9-16kts\n'
                                   f'(3) for strong wind - 17+ kts:', 'i', rangehigh=3, rangelow=1)
            info = self.__getranking(racetext)
            universecsv.addrace(dat.Race(info, wind, days))
            for item in info.sailorids:
                if item not in allsailors:
                    allsailors.add(item)
        universecsv.endevent(allsailors, days)

    def addeventcsv(self):
        racenum = Base.cleaninput('\nPlease enter the number of races in the event (1-20):', 'i', rangelow=1,
                                  rangehigh=20)
        days = Base.cleaninput('\nHow many days ago was the final race of the event(0-500):', 'i')
        allsailors = set()
        for x in range(racenum):
            racetext = ' '.join(['Race', str(x + 1)])
            print(f'\n{racetext.upper()} ENTRY WIZZARD')
            fileloc = Base.cleaninput(f'Please enter the full file location of the file for {racetext}:', 's')
            currfile = Csvnew(fileloc)
            wind = int(currfile.getcell(0, 1))

            currsailorids = currfile.getcolumn(0, excudedrows= [0, 1])
            positions = currfile.getcolumn(1, excudedrows= [0, 1])
            for y in range(len(positions)):
                positions[y] = int(positions[y])
            results_obj = dat.Results(currsailorids,positions)

            for item in currsailorids:
                allsailors.add(item)
            universecsv.addrace(dat.Race(results_obj, wind, days), imported = True)
        universecsv.endevent(allsailors, days)

    def __getranking(self, eventname: str) -> dat.Results:
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
            if speedprint != []:
                print("\nPosition:    {}:    Sailor-id:".format(self.inputmethodname))
                toprint = '\n'.join(speedprint)
                print(toprint)
            position += 1
            inp = Base.cleaninput(
                "\nPlease enter the {} of {} place in {}:".format(self.inputmethodname, Base.ordinal(position),
                                                                  eventname), 's').lower()
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
        return dat.Results(sailorids, positions)

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
            inp = Base.cleaninput((''.join(('\nYour current selected input method is: ', self.inputmethodname,
                                            '\nWould you like to change it?\n(0) for no\n(1) for yes:'))), 'i',
                                  rangehigh=1)
            if inp == 1:
                ip = ''
            else:
                ip = self.inpmethod
        else:
            ip = ''
        while ip not in inpmethods:
            ip = Base.cleaninput('\nHow would you like to enter sailors information?\n'
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
        inp = Base.cleaninput('\n(1) for entering overall event results (less accurate - quicker)\n'
                              '(2) for entering individual race results (higher accuracy - slower)\n'
                              '(3) for importing previous race (needs previously entered csv):',
                              'i', rangehigh=3, rangelow=1)
        if inp == 1:
            self.addeventlazy()
        elif inp == 2:
            self.addeventproper()
        elif inp == 3:
            self.addeventcsv()

