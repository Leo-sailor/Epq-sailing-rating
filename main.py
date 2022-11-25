#imports
from ELO import EloCalculations


#initzalizations
elo = EloCalculations()
pos = [1,2,3,4]
currentrating = [1500,1500,1500,1500]
sailorid = [5,3,2,4]

print('the rating change for players are :{}'.format(elo.cycle(currentrating,sailorid,pos)))
