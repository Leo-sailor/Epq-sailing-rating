# imports
from ELO import EloCalculations
from General import General


# initzalizations
elo = EloCalculations()
base = General()

pos = [1, 2, 3, 4]
currentrating = [1500, 1500, 1500, 1500]
sailorid = [5, 3, 2, 4]

print('the rating change for players are :{}'.format(elo.cycle(currentrating, sailorid, pos)))

nat = 'gbr'
first = 'leo'
sur = 'yates'
sail = 48153

sailorid[0] = base.generatesailorid(nat, sail, first, sur)

print('nationality: {}\nFist name: {}\nSurname: {}\nsail number {}'.format(nat, first, sur, sail))
print('\nsailor id is: {}'.format(sailorid[0]))

print('csv line is: {}'.format(base.csvlinegenerate(sailorid[0], nat, sail, first, sur, 'LSE', 317)))
print('it should be: gb-8153-leoya,317,48153,Leo,Yates,LSE,gbr,1500,1500,1500,1500,5,0')
