class EloCalculations:
    def __init__(self, deviation, multiplier):
        self.deviation = int(deviation)
        self.changemultiplier = multiplier

    def calc(self, rat1, rat2, result, k):
        change = k*(result - self.pred(rat1, rat2))  # **(3))
        return change

    def pred(self, rata, ratb):
        prediction = 1/(1 + 10 ** ((ratb - rata) / self.deviation))
        return prediction

    def cycle(self, currat, sailorid, position):
        # no idea whether this work if the positions are not in the right order, but it should
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
                kfac = self.k(sailorid, sailors, 150)
                change = self.calc(arat, brat, 1, kfac)
                ratchange[aloc] = ratchange[aloc] + change
                ratchange[bloc] = ratchange[bloc] - change
        for x in range(0, len(ratchange)):
            ratchange[x] = round(ratchange[x], 1)
        return ratchange

    def k(self, sailorid, people, k):
        k = k * self.changemultiplier
        # will make this intresting later when i 'realise' its crap
        return k

    def updaterating(self, change, currat):
        for y in range(0, len(change)):
            currat[y] = currat[y] + change[y]
            if currat[y] <= 0:
                currat[y] = 0.1
        return currat
