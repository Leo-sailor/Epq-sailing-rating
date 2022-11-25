#imports
from ELO import EloCalculations


#initzalizations
elo = EloCalculations()
print('new ratings are{}'.format(elo.calc(1500,16000,1,24)))
