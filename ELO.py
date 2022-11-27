class EloCalculations:
    def __init__(self):
        print('elo calculations are now imported and running')

    def calc(self, rat1, rat2, result, k):
        change = k*(result-self.pred(rat1, rat2))
        return change

    def pred(self, rata, ratb):
        prediction = 1/(1+10**((ratb - rata)/400))
        return prediction

    def cycle(self, currat, sailorid, position):
        sailors = len(currat)
        ratchange = []
        for x in range(0, sailors):
            ratchange.append(0)
        for x in range(0, sailors-1):
            for y in range(x+1, sailors):
                aloc = position.index(x + 1)
                bloc = position.index(y + 1)
                arat = currat[aloc]
                brat = currat[bloc]
                kfac = self.k(sailorid, sailors, 20)
                change = self.calc(arat, brat, 1, kfac)
                ratchange[aloc] = ratchange[aloc] + change
                ratchange[bloc] = ratchange[bloc] - change
        return ratchange

    def k(self, sailorid, people, k):
        k = k/(people-1)
        return k
