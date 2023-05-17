import unittest
import LocalDependencies.General as g
from LocalDependencies.Main_core import Csvcode
from unittest.mock import patch
import datetime
class Test:
    def __init__(self, inps: tuple,out: any,keyboard_input: str = None,func:str = None):
        if isinstance(inps, tuple):
            self.inps = inps
        else:
            try:
                self.inps = tuple(inps)
            except TypeError:
                self.inps = (inps,)
        self.out = out
        if keyboard_input is None:
            self.keyboard_input = ""
        else:
            self.keyboard_input = keyboard_input
        self.func = func
    def __str__(self):
        if self.func:
            return f"func: {self.func} inputs: {self.inps}, expected: {self.out}, keyboard_input: {self.keyboard_input}"
        else:
            return f"inputs: {self.inps}, expected: {self.out}, keyboard_input: {self.keyboard_input}"

class TestSum(unittest.TestCase):
    def test_for_multiindex(self):
        with open("multiindex.tests") as f:
            for line_num,line in enumerate(f):
                line_parts = line.split(':')
                a, b = eval(line_parts[0]),eval(line_parts[1])
                if len(line_parts) == 3:
                    c = eval(line_parts[2])
                else:
                    c = None
                test = Test(a,b,c)
                with patch('builtins.input', return_value=test.keyboard_input):
                    output = g.multiindex(*test.inps)
                    self.assertEqual(output, test.out, f"Failed - {test}")
                    print(f"Passed - {line_num+1} - with output: {output}")

    def test_for_get_sailor_id(self):
        csv = Csvcode("testing_uni", "Leo")
        with open("get_sailor_id.tests") as f:
            for line_num,line in enumerate(f):
                line_parts = line.split(':')
                a, b = eval(line_parts[0]),eval(line_parts[1])
                if len(line_parts) == 3:
                    c = eval(line_parts[2])
                else:
                    c = None
                test = Test(a,b,c)
                with patch('builtins.input', return_value=test.keyboard_input):
                    output = csv.getsailorid(*test.inps)
                    self.assertEqual(output, test.out, f"Failed - {test}")
                    print(f"Passed - {line_num+1} - with output: {output}")


    def test_small(self):

        with open("small.tests") as f:
            for line_num, line in enumerate(f):
                line_parts = line.split(':')
                func = line_parts[0]
                a, b = eval(line_parts[1]), eval(line_parts[2])
                if len(line_parts) == 4:
                    c = eval(line_parts[3])
                else:
                    c = None
                test = Test(a, b, c,func)
                with patch('builtins.input', return_value=test.keyboard_input):

                    output = eval(''.join(('g.',func,line_parts[1])))
                    self.assertEqual(output, test.out, f"Failed - {test}")
                    print(f"Passed - {line_num + 1} - with output: {output}")

if __name__ == '__main__':
    unittest.main()
