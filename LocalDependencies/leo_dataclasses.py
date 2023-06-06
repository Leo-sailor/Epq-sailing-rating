import datetime
import LocalDependencies.General as Base


class Results:

    def __init__(self, sailorids: [list[str]], positions: list[int] = None):
        self.sailorids = sailorids
        if positions is None:
            self.positions = list(range(len(sailorids)))
        else:
            self.positions = positions
        if len(self.sailorids) != len(self.positions):
            raise ValueError("Sailorids and positions must be the same length")
        if not(all(isinstance(x, str) for x in self.sailorids)):
            raise ValueError("Sailorids must be strings")
        if not(all(isinstance(x, int) for x in self.positions)):
            raise ValueError("Positions must be integers")
        if len(set(positions)) != len(self.positions):
            raise ValueError("Positions must be unique")
        if len(set(sailorids)) != len(self.sailorids):
            raise ValueError("Sailorids must be unique")
        if not(Base.check_consecutive(positions)):
            raise ValueError("Positions must be consecutive")

    def __str__(self):
        things_to_join = []
        for x in range(1, len(self.positions)+1):
            things_to_join.append(str(x) + " - " + str(self.sailorids[self.positions.index(x)]))
        return "\n".join(things_to_join)

    def __len__(self) -> int:
        return len(self.sailorids)

    def __getitem__(self, item) -> tuple[str, int]:
        return self.sailorids[self.positions.index(item)], item
    def __make_proxy_for_sort(self, sailorid):
        return self.positions[self.sailorids.index(sailorid)]
    def __iter__(self):
        return iter(sorted(self.sailorids, key=self.__make_proxy_for_sort))

class Race:
    def __init__(self, results: Results, wind: int, date: int | datetime.datetime):
        self.results = results
        self.wind = wind
        if date is int:
            self.date = date
        else:
            self.date = (date - datetime.datetime(2000, 1, 1)).days
        if not(wind is int and 3 >= wind >= 1):
            raise ValueError("Wind must be between 1 and 3")
        if not(self.date is int and 3500 <= self.date <= Base.dayssincetwothousand()):
            raise ValueError("Date is not between 2010 and today")

    def __str__(self) -> str:
        wind_codes = {1: "1 - Light", 2: "2 - Medium", 3: "3 - Heavy"}
        things_to_join = ["date:" + str(Base.twothousandtodatetime(self.date)) + " wind:" + wind_codes[self.wind],
                          str(self.results)]
        return "\n".join(things_to_join)

    def __len__(self) -> int:
        return len(self.results)

    def __getitem__(self, item) -> tuple[str, int]:
        return self.results[item]

    def __iter__(self):
        return iter(self.results)

    def __add__(self, other):
        return Event([self, other], max(self.date, other.date))

class Event:
    def __init__(self, races: list[Race], date: int | datetime.datetime, imported: bool = False, event_title: str = ''):
        self.imported = imported
        self.races = races
        if date is int:
            self.date = date
        else:
            self.date = (date - datetime.datetime(2000, 1, 1)).days
        if not(self.date is int and 3500 <= self.date <= Base.dayssincetwothousand()):
            raise ValueError("Date is not between 2010 and today")
        self.all_sailors = set()
        for race in self.races:
            for sailor in race:
                self.all_sailors.add(sailor)
        self.event_title = event_title

    def append(self, race: Race):
        self.races.append(race)
        for sailor in race:
            self.all_sailors.add(sailor)

    def __str__(self):
        things_to_join = []
        for race_num, race in enumerate(self.races):
            things_to_join.append(str(race_num+1) + ":\n " + str(race) + "\n")
        return "\n".join(things_to_join)

    def __len__(self) -> int:
        return len(self.races)

    def __iter__(self):
        return iter(self.races)


def main():
    # theres not even any point doing tests
    pass
    

if __name__ == "__main__":
    main()