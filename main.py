# imports
from Dependencies.ELO import EloCalculations
from Dependencies.General import General
from Dependencies.csvcode import Csvcode

# initzalizations
elo = EloCalculations()
base = General()
hostcsv = Csvcode('host')


pos = []
for x in range(0, 100):
    pos.append(x+1)
print('Universe selection tool:')
print('Avalible universes are:')
column = hostcsv.getcolumn(0)
for x in range(1, len(column)):
    print(column[x])
universe = input('\nPlease enter the name of the universe you would like to acess (N for a new universe):')
universecsv = Csvcode(universe)

index = universecsv.findsailor(2,'48153')
print(index)
universecsv.updatevalue('1700',1, 10)

print('\nWhat would you like to do?')
base.help(2)
choice = input()

# test cases
currentrating = [1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500]
sailorid = [5, 3, 2, 4]
for x in range(0, 10):
    change = elo.cycle(currentrating, sailorid, pos)
    currentrating = elo.updaterating(change, currentrating)
print('the rating change for players are :{}'.format(currentrating))

nat = 'gbr'
first = 'leo'
sur = 'yates'
sail = 48153

sailorid[0] = base.generatesailorid(nat, sail, first, sur)

print('nationality: {}\nFist name: {}\nSurname: {}\nsail number {}'.format(nat, first, sur, sail))
print('\nsailor id is: {}'.format(sailorid[0]))

print('csv line is: {}'.format(base.csvlinegenerate(sailorid[0], nat, sail, first, sur, 'LSE', 317)))
print('it should be: gb-8153-leoya,317,48153,Leo,Yates,LSE,gbr,1500,1500,1500,1500,5,0')
