from typing import Any
from LocalDependencies.Framework.base_ui import callback
from LocalDependencies.Framework.text_ui import text_ui
from LocalDependencies.Framework import base_func as base
import pickle
import datetime


class Fake_Input_Error(TypeError):
    pass


class custom_string(str):
    def lower(self) -> str:
        self = custom_string(super().lower())
        return self

    def upper(self) -> str:
        self = custom_string(super().upper())
        return self

    def find_and_replace(self, find, replace):
        self = base.findandreplace(self, find, replace, True)
        return self

    def strip(self, chars=None):
        self = custom_string(super().strip(chars))
        return self


def compare_strings(a: str, b: str) -> bool:
    a = custom_string(a)
    b = custom_string(b)
    a.strip()
    b.strip()
    a.lower()
    b.lower()
    a.find_and_replace('\n', ' | ')
    b.find_and_replace('\n', ' | ')
    return a == b


def call_default(func: callable, *args, **kwargs):
    return func(*args, **kwargs)


class test_ui(callback):
    def __init__(self, inp_file: str, out_file: str = None, display_outs: callback | bool = None):
        if isinstance(display_outs, bool):
            if display_outs:
                display_outs = text_ui()
            else:
                display_outs = None
        self.out_obj = display_outs
        self.inp_index = -1
        self.inps = []
        self.out_index = -1
        self.outs = []
        self.use_canned_inps = True
        self.use_canned_outs = True
        inp_file = '    ' + inp_file
        if inp_file[-4] not in ['ckle', 'inps', '.inp', 'puts', 'nput']:  # .pickle, .inps, .inp, .inputs, .input
            with open(inp_file.strip(), encoding='utf-8') as f:
                for line in f:
                    self.inps.append(eval(line))
        else:
            with open(inp_file) as f:
                self.inps = pickle.load(f)
        if out_file is not None:
            out_file = '    ' + out_file
            if out_file[-4] not in ['ckle', 'outs', '.out', 'puts', 'tput']:  # .pickle, .outs, .out, .outputs . output
                with open(out_file.strip(), encoding='utf-8') as f:
                    for line in f:
                        self.inps.append(eval(line))
            else:
                with open(out_file) as f:
                    self.inps = pickle.load(f)
        else:
            self.use_canned_outs = False
            self.outs = []
        if len(self.inps) == 0:
            self.use_canned_inps = False
        if len(self.outs) == 0:
            self.use_canned_outs = False

    def canned_user_input(self,expected_type:type,func:callable, *args, **kwargs) -> Any:
        if self.use_canned_inps:
            self.inp_index += 1
            if self.inp_index == len(self.inps):
                if self.out_obj:
                    self.out_obj.display_text('OUT OF PRE-PROGRAMMED INPUTS')
                else:
                    print('Out of PRE-PROGRAMMED INPUTS')
                self.use_canned_inps = False
                res = call_default(func, *args, **kwargs)
            else:
                res = self.inps[self.inp_index]
                print(f'--Input {self.inp_index +1}: {res}')
        else:
            res = call_default(func, *args, **kwargs)
        if isinstance(res, expected_type):
            return res
        else:
            raise Fake_Input_Error(f'input number: {self.response_index} using canned inps: {self.use_canned_inps}\n'
                                   f'expected type: {expected_type} got type: {type(res)}\n with input: {res}')

    def force_output(self,out):
        if self.out_obj:
            self.out_obj.display_text(out)
        else:
            print(out)

    def check_output(self, out, func,*args, **kwargs):
        if self.use_canned_outs:
            self.out_index += 1
            if self.out_index == len(self.inps):
                self.force_output('OUT OF EXPECTED OUTPUTS')
                self.use_canned_outs = False
            elif not compare_strings(self.outs[self.out_index], out):
                raise AssertionError(f"Output is not as expected, expected: {self.answer[self.answer_index]} actual: {out}")
            else:
                print(f'Test line: {self.out_index +1} passed')
        if self.out_obj:
            return call_default(func,out,*args,**kwargs)
        elif not self.use_canned_outs:
            print("All tests passed")
            exit(0)
        else:
            return None

    def g_date_int(self, *args,**kwargs) -> int:
        return self.canned_user_input(int, self.out_obj.g_date_int, *args, **kwargs)

    def display_text(self, obj, *args, **kwargs):
        return self.check_output(obj, self.out_obj.display_text, *args, **kwargs)

    def display_table(self, obj, *args, **kwargs):
        return self.check_output(obj, self.out_obj.display_text, *args, **kwargs)

    def display_dict(self, obj, *args, **kwargs):
        return self.check_output(obj, self.out_obj.display_text, *args, **kwargs)

    def g_str(self, *args, **kwargs) -> str:
        return self.canned_user_input(str, self.out_obj.g_str, *args, **kwargs)

    def g_int(self, *args, **kwargs) -> int:
        return self.canned_user_input(int, self.out_obj.g_int, *args, **kwargs)

    def g_list(self, *args, **kwargs) -> list:
        return self.canned_user_input(list, self.out_obj.g_list, *args, **kwargs)

    def g_float(self, *args, **kwargs) -> float:
        return self.canned_user_input(float, self.out_obj.g_float, *args, **kwargs)

    def g_date(self, *args, **kwargs) -> datetime.date:
        return self.canned_user_input(datetime.date, self.out_obj.g_date, *args, **kwargs)

    def g_datetime(self, *args, **kwargs) -> datetime.datetime:
        return self.canned_user_input(datetime.datetime, self.out_obj.g_datetime, *args, **kwargs)

    def g_bool(self, *args, **kwargs) -> bool:
        return self.canned_user_input(bool, self.out_obj.g_bool, *args, **kwargs)

    def g_choose_options(self, *args, **kwargs) -> int:
        return self.canned_user_input(int, self.out_obj.g_choose_options, *args, **kwargs)

    def g_file_loc(self, *args, **kwargs) -> str:
        return self.canned_user_input(str, self.out_obj.g_file_loc, *args, **kwargs)

    def g_nat(self, *args, **kwargs) -> str:
        """
        This function gets the current computer's address and uses that to generate a suggested 3-letter country code
        :param obj_of_nationality:
        :param return_type: 1 for 3-letter country code, 2 for country name, 3 for 2-letter code, 4 for telephone code
        5 for capital, and 6 for location, 7 for boarders
        """
        return self.canned_user_input(str, self.out_obj.g_nat, *args, **kwargs)
