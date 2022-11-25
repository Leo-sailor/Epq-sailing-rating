class EloCalculations:
    def __init__ (self):
        print('elo calculations are now imported and running')
    def calc (self,rat1,rat2,result,k):
        change = k*(result-self.pred(rat1,rat2))
        return change

    def pred(self, rata, ratb):
        return 1/(1+10**((ratb-rata)/400))

    def cycle(self, currat, sailorid, position):
        sailors = len(currat)
        ratchange = []
        for x in range (0,sailors):
            ratchange.append(0)
        for x in range(0,sailors-1):
            for y in range(x+1,sailors):
                Aloc = position.index(x+1)
                Bloc = position.index(y+1)
                Arat = currat[Aloc]
                Brat = currat[Bloc]
                kfac = self.k(sailorid,sailors,20)
                change = self.calc(Arat,Brat,1,kfac)
                ratchange[Aloc] = ratchange[Aloc] + change
                ratchange[Bloc] = ratchange[Bloc] - change
        return ratchange

    def k(self,sailorid,people,k):
        k = k/(people-1)
        return k

