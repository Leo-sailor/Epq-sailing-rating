import matplotlib.pyplot as plt
import datetime
if __name__ == '__main__':
    x1 = [1, 2, 3]
    y1 = [2, 4, 1]
    # plotting the line 1 points
    plt.plot(x1, y1, label="line 1")

    # line 2 points
    x2 = [1, 2, 3]
    y2 = [4, 1, 3]
    # plotting the line 2 points
    plt.plot(x2, y2, label="line 2")

    # naming the x axis
    plt.xlabel('x - axis')
    # naming the y axis
    plt.ylabel('y - axis')
    # giving a title to my graph
    plt.title('Two lines on same graph!')

    plt.show()


class add_func():
    def __init__(self):
        pass
    def plotsailors(self,startdate: datetime,sailorids: str | list[str], fieldnum: int,enddate: datetime = datetime.datetime.now()):
        pass
