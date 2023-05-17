import pandas
import tabula
import cProfile
import LocalDependencies.General as b

import unittest
from unittest.mock import patch

# Unit under test.
def get_input():
    my_input = input("Enter some string: ")
    if my_input == "bad":
        raise Exception("You were a bad boy...")
    return my_input

class MyTestCase(unittest.TestCase):
    # Force input to return "hello" whenever it's called in the following test
    @patch("builtins.input", return_value="hello")
    def test_input_good(self, mock_input):
        self.assertEqual(get_input(), "hello")

    # Force input to return "bad" whenever it's called in the following test
    @patch("builtins.input", return_value="bad")
    def test_input_throws_exception(self, mock_input):
        with self.assertRaises(Exception) as e:
            get_input()
            self.assertEqual(e.message, "You were a bad boy...")

if __name__ == "__main__":
    unittest.main()
def findandreplace(inp,find,replace):
    if type(inp) == str:
        findlength = len(find)
        locations = []
        replaceletters = list(replace)
        for x in range(0,len(inp)-findlength):
            if inp[x: x + findlength] == find:
                locations.append(list(range(x, x + findlength)))
        letters = list(inp)
        for x in range(len(locations) - 1,-1,-1):
            for y in range(len(locations[x]) - 1,-1,-1):
                letters.pop(locations[x][y])
            for z in range(len(replaceletters)):
                letters.insert(locations[x][y+z],replaceletters[z])

        return ''.join(letters)

    elif type(inp) == list:
        out = []
        for item in inp:
            out.append(findandreplace(item,find,replace))
        return out
    elif type(inp) == float or type(inp) == int:
        return findandreplace(str(inp),find,replace)
    else:
        raise TypeError('Expected type list or str not ' + str(type(inp)))

def megatablefrompdf(file):
    tables = tabula.read_pdf(file, pages="all")
    table = pandas.concat(tables)
    lists = table.values.tolist()
    head = [(table.columns.tolist())]
    for row in lists:
        head.append(row)
    head = findandreplace(head,"\r"," ")
    return head


