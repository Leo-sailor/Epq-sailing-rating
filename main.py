# imports
from Dependencies.General import General
from Dependencies.csvcode import Csvcode

# initzalizations
base = General()
universecsv = Csvcode()


index = universecsv.getsailorid(2, '44036')
print(index)


print('\nWhat would you like to do?')
base.help(2)
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

print('nationality: {}\nFist name: {}\nSurname: {}\nsail number {}'.format(nat, first, sur, sail))
print('\nsailor id is: {}'.format(sailorid[0]))

print('csv line is: {}'.format(base.csvlinegenerate(sailorid[0], nat, sail, first, sur, 'LSE', 317)))
print('it should be: gb-8153-leoya,317,48153,Leo,Yates,LSE,gbr,1500,1500,1500,1500,5,0')
