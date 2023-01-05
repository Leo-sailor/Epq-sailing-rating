class EloCalculations:
    def __init__(self, deviation, multiplier):
        self.deviation = int(deviation)
        self.changemultiplier = multiplier

    def calc(self, rat1, rat2, result, k):
        """
        Calculates the Elo change for sailor 1 (sailor 2's is inverted) after an event based
        off of the ratings going in and their results
        :param rat1: sailor ones origninal rating
        :param rat2: sailor 2 orignial rating
        :param result: the result of the mini event (1 sailor 1 win) (0 sailor 1 lose) (0.5 draw)
        :param k: the k factor used for caluclation
        :return: sailor 1 rating chnage
        """
        change = k*(result - self.pred(rat1, rat2))  # **(3))
        return change

    def pred(self, rata, ratb):
        """
        Calculate the predicted result of a mini event
        :param rata: rating of sailor 1
        :param ratb: rating of sailor 2
        :return:
        """
        prediction = 1/(1 + 10 ** ((ratb - rata) / self.deviation))
        return prediction

    def cycle(self, currat, sailorid, position):
        """
        note: nth position's must be = to nth currat = nth sailor id (more like a 2d table)
        This function take a list of ratings and their positions and returns thier updated ratings after an event
        :param currat:
        :param sailorid:
        :param position:
        :return:
        """
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
        """
        A function which returns the correct k factor for the sailors involved in the comparison
        :param sailorid: list of the 2 sailors IDs of the sailors in the mnin event
        :param people:
        :param k:
        :return:
        """
        k = k * self.changemultiplier
        # will make this intresting later when i 'realise' its crap
        return k

    def updaterating(self, change, currat):
        """
        This function will take a 32 bit float and add that to the current rating and round it correctly
        :param change: 32 bit float to be added to the current rating
        :param currat: the current rating
        :return:
        """
        for y in range(0, len(change)):
            currat[y] = currat[y] + change[y]
            if currat[y] <= 0:
                currat[y] = 0.1
        return currat
