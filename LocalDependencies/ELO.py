from numpy import sqrt
from LocalDependencies.Framework.constants import constants
c = constants()
k = c.get('k')
event_num = c.get('event_threshold')


def update_rating(change: list[float], cur_rat: list[float]):
    """
    This function will take a 32-bit float and add that to the current rating and round it correctly
    :param change: 32-bit float to be added to the current rating
    :param cur_rat: the current rating
    :return:
    """
    for y in range(0, len(change)):
        cur_rat[y] += change[y]
        cur_rat[y] = round(cur_rat[y], 1)
    return cur_rat


class EloCalculations:
    def __init__(self, deviation, multiplier):
        self.deviation = float(deviation)  # sets the rating difference that will deliver a 90% win chance
        self.change_multiplier = float(multiplier)  # sets the k factor multiplier

    def calc(self, rat1: float, rat2: float, result: float, k_fac: float) -> float:
        """
        Calculates the Elo change for sailor 1 (sailor 2's is inverted) after an event based
        off of the ratings going in and their results
        :param rat1: sailor ones original rating
        :param rat2: sailor 2 original rating
        :param result: the result of the mini event (1 sailor 1 win) (0 sailor 1 lose) (0.5 draw)
        :param k_fac: the k factor used for calculation
        :return: sailor 1 rating change
        """
        prediction = self.pred(rat1, rat2)

        change = k_fac * (result - prediction)  # **(3))
        return change

    def pred(self, rat_a: float, rat_b: float) -> float:
        """
        Calculate the predicted result of a mini event
        :param rat_a: rating of sailor 1
        :param rat_b: rating of sailor 2
        :return:
        """
        prediction = 1 / (1 + 10 ** ((rat_b - rat_a) / self.deviation))
        return prediction

    def cycle(self, old_rat: list[float], events: list[int], position: list[int], cur_rat: list[float]):
        """
        note: nth position's must be = to nth cur_rat = nth sailor id (more like a 2d table)
        This function take a list of ratings and their positions and returns their updated ratings after an event
        :param old_rat:
        :param events:
        :param position:
        :param cur_rat:
        :return:
        """
        # no idea whether this work if the positions are not in the right order, but it should
        # it does
        num_sailors = len(old_rat)
        rat_change = [0] *num_sailors
        for x in range(num_sailors-1):
            for y in range(x+1, num_sailors):
                if position[x] > position[y]:
                    result = 0
                elif position[x] < position[y]:
                    result = 1
                else:
                    result = 0.5
                res = self.calc(old_rat[x], old_rat[y], result, self.__k(events[x], events[y], num_sailors))
                rat_change[x] += res
                rat_change[y] -= res

        new_ratings = update_rating(rat_change, cur_rat)
        return new_ratings

    def __k(self, event_sailor1: int, event_sailor2: int, num_sailors: int):
        """
        A function which returns the correct k factor for the sailors involved in the comparison
        :param event_sailor1
        :param event_sailor2
        :param num_sailors
        :return:
        """
        kfac = (((event_num / (event_sailor1 + 1)) + (event_num / (event_sailor2 + 1))) * (1 / (sqrt(num_sailors)))) + k
        kfac *= self.change_multiplier
        # will make this interesting later when i 'realise' its crap
        return kfac
