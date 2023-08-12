# imports
from LocalDependencies.Hosts import HostScript
import sys
from LocalDependencies.Framework.constants import constants
from LocalDependencies.Framework import text_ui
from LocalDependencies.Framework.test_ui import test_ui, record
from LocalDependencies.Framework.logger import log




# TODO: come up with principle on newline usage
# TODO: Finnish unit tests
# TODO: make a table dataclass
# TODO: fix issue of config files
# initializations
def main(args):
    ui_options = {'text': text_ui.text_ui}
    for _ in range(4):
        args.append('')
    match args[1]:
        case 'text':
            ui = text_ui.text_ui()
        case 'test':
            if args[2] == '' or args[3] == '':
                raise ArgsNotFoundError("Missing Arguments 2 and 3 for 'test'")
            func = ui_options.get(args[2])
            if func:
                orig_ui = func()
            else:
                orig_ui = None
            if args[4] == '':
                args[4] = None
            ui = test_ui(args[3], args[4], orig_ui)
        case 'record':
            if args[2] == '' or args[3] == '' or args[4] == '':
                raise ArgsNotFoundError("Missing Arguments 2,3 or 4 for 'record'")
            func = ui_options.get(args[2])
            if func:
                orig_ui = func()
            else:
                raise NotImplementedError('that uis not implemented yet')
            ui = record(args[3], args[4], orig_ui)
        case _:
            ui = text_ui.text_ui()
    constants()
    host = HostScript(ui, *args)
    host.torun()


if __name__ == '__main__':
    location = __file__.split('\\')[:-1]
    location += ['log', 'epq.log']
    log = log('\\'.join(location))
    log.log(2, 'Program Alive', sys.argv)
    main(sys.argv)


class ArgsNotFoundError(Exception):
    pass
