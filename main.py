#imports
from ELO import EloCalculations
from General import General
import requests

#initzalizations
elo = EloCalculations()
base = General()

pos = [1,2,3,4]
currentrating = [1500,1500,1500,1500]
sailorid = [5,3,2,4]

print('the rating change for players are :{}'.format(elo.cycle(currentrating,sailorid,pos)))

nat = 'gbr'
first = 'ed'
sur = 'smith'
sail = 4


print('nationality: {}\nFist name: {}\nSurname: {}\nsail number {}'.format(nat,first,sur,sail))
print('\nsailor id is: {}'.format(base.GenerateSailorID(nat,sail,first,sur)))
