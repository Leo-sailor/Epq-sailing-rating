from datetime import datetime
from typing import Literal, Any, Callable
import os
import sys

log_levels = {0: 'Debug', 1: 'Info', 2: 'Event', 3: 'Warning', 4: 'ERROR', 5: 'FATAL'}


def line_factory(level: Literal[0, 1, 2, 3, 4, 5], message: str, data: Callable[[], str] = None, stack: list = None,
                 time_str: str = None) -> str:
    if data is None:
        data = ''
    if stack is None:
        stack = get_stack()
    if time_str is None:
        time_str = time()
    return f'{time_str}, {level}-{log_levels.get(level)}, {len(stack)}, {stack[0]}, {message}, {data}, {stack}\n'


def get_stack_waster(to_waste):
    if to_waste < 2:
        return get_stack()
    else:
        return get_stack_waster(to_waste - 1)


def get_stack():
    stack = []
    start = 2
    while True:
        frame = sys._getframe(start + 1)
        res = f"{os.path.basename(frame.f_code.co_filename)}/{frame.f_lineno} {frame.f_code.co_name}()"
        stack.append(res)
        start += 1
        if '<module>' in res:
            break
    return stack


def time(detail: Literal[0, 1] = 1, date=None) -> str:
    """
    Returns the current time in UTC as a formatted string.
    """
    if date is None:
        date = datetime.utcnow()
    if detail == 0:
        return date.strftime('%Y-%m-%d--%H-%M-%S')
    elif detail == 1:
        return date.strftime('%Y-%m-%d %H:%M:%S %F')
    else:
        return time(date=date)


class log:
    _self = None
    def __new__(cls, file_loc: str):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self

    def __init__(self, file_loc: str):
        self.to_write = None
        self.log_levels = log_levels
        file_loc = '    ' + file_loc
        if file_loc[-4:] != '.log':
            file_loc += '.log'
        file_loc = file_loc.split('\\')
        if len(file_loc) == 0:
            file_loc = file_loc[0].split('/')
        file_loc[-1] = time(0) + '-' + file_loc[-1]
        self.file = '\\'.join(file_loc)[4:]
        with open(self.file, 'x') as f:
            f.write(line_factory(2, 'Logging Initialized'))
        self.queue_list = []
        self.open = open

    def log(self, level, message, data):
        self.to_write = line_factory(level, message, data)
        self.flush()
        self.to_write = None

    def queue(self, level, message, data):
        self.queue_list.append((level, message, data, get_stack_waster(1), datetime.utcnow()))

    def flush(self):
        completed_queue = [line_factory(*args) for args in self.queue_list]
        if self.to_write:
            completed_queue.append(self.to_write)
        with self.open(self.file, 'a') as f:
            f.write(''.join(completed_queue))
            f.write(line_factory(0, 'Logging queue flush'))
        self.queue_list = []
