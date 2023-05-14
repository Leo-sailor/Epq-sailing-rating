import datetime
class Results:
    def __init__(self,sailorids:[list[str]],positions : list[int] = None):
        self.sailorids = sailorids
        if positions is None:
            self.positions = list(range(len(sailorids)))
        else:
            self.positions = positions
class Race:
    def __init__(self,results: Results,wind:int,date: int | datetime.datetime):
        self.results = results
        self.wind = wind
        if date is int:
            self.date = date
        else:
            self.date = (date - datetime.datetime(2000,1,1)).days



class Event:
    def __init__(self,races : list[Race],date: int | datetime.datetime):
        self.races = races
        if date is int:
            self.date = date
        else:
            self.date = (date - datetime.datetime(2000,1,1)).days
    def append(self, race: Race):
        self.races.append(race)
def main():
    # theres not even any point doing tests
    pass
    
if __name__ == "__main__":
    main()
