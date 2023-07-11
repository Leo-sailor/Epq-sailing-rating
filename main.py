# imports
from LocalDependencies.Hosts import HostScript
import sys
from LocalDependencies.Framework.constants import constants
from LocalDependencies.Framework import text_ui
from LocalDependencies.Framework.test_ui import test_ui


# TODO: come up with principle on newline usage
# TODO: Finnish unit tests
# TODO: make a table dataclass
# initializations
def main(args):
    #fix issue of config files
    for _ in range(4):
        args.append('')
    match args[1]:
        case 't':
            ui = text_ui.text_ui()
        case 'test':
            ui_options = {'t' : text_ui.text_ui,}
            if args[2] == '' or args[3] == '':
                raise FileNotFoundError("Missing Arguments 2 and 3 for 'test'")
            func = ui_options.get(args[2])
            if func:
                orig_ui = func()
            else:
                orig_ui = None
            if args[4] == '':
                args[4] = None
            ui = test_ui(args[3], args[4], orig_ui)
        case _:
            ui = text_ui.text_ui()
    constants()
    host = HostScript(ui, *args)
    host.torun()


if __name__ == '__main__':
    main(sys.argv)
