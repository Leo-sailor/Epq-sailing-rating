#imports
from ELO import EloCalculations


#initzalizations
elo = EloCalculations()


print('the rating change for player 1 :{}'.format(elo.calc(1500,1600,0,20)))
