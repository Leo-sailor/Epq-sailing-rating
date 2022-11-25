class EloCalculations:
    def __init__ (self):
        print('elo calculations are now imported and running')
    def calc (self,rat1,rat2,result,k):
        pred = 1/(1+10**(rat2-rat1))
        change = 5
        return [rat1-change,rat2+change]
