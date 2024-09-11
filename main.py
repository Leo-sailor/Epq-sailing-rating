from LocalDependencies.Framework.logger import log
location = __file__.split('\\')[:-1]
location += ['log', 'epq.log']
log = log('\\'.join(location))
from LocalDependencies.Hosts import HostScript
import sys
from LocalDependencies.Framework.constants import constants
from LocalDependencies.Framework import text_ui
from LocalDependencies.Framework.test_ui import test_ui, record
import traceback
log.log(0,'All imports complete')



# TODO: check lack of sorting in graphs




# initializations
def main(args):
    ui_options = {'text': text_ui.text_ui, 'pass':None}
    for _ in range(4):
        args.append('')
    match args[1]:
        case 'text':
            ui = text_ui.text_ui()
            log.log(1,'text ui selected')
        case 'test':
            log.log(1,'App initzialised for testing')
            if args[2] == '' or args[3] == '':
                log.log(4,'Missing arguments for testing',args)
                raise ArgsNotFoundError("Missing Arguments 2 and 3 for 'test'")
            func = ui_options.get(args[2])
            if func:
                orig_ui = func()
                log.log(1,'Ui chosen for testing',type(orig_ui))
            else:
                orig_ui = None
                log.log(3,'No ui chosen for testing - desired ui:',args[2])
            if args[4] == '':
                args[4] = None
            if args[5] == '':
                args[5] = None
            else:
                try:
                    args[5] = float(args[5])
                except ValueError:
                    args[5] = None
            ui = test_ui(args[3], args[4], orig_ui, args[5])
        case 'record':
            log.log(1, 'App initialized for recording inputs')
            if args[2] == '' or args[3] == '':
                raise ArgsNotFoundError("Missing Arguments 2,3 for 'record'")
            if args[4] == '':
                args[4] = None
            func = ui_options.get(args[2])
            if func:
                orig_ui = func()
            else:
                raise NotImplementedError('that uis not implemented yet')
            ui = record(args[3], args[4], orig_ui)
        case _:
            log.queue(2,'default ui: text - has been selected')
            ui = text_ui.text_ui()
    constants()
    host = HostScript(ui, *args)
    log.queue(0, 'constants and hosts loaded')
    try:
        host.torun()
    except Exception as e:
        log.queue(5,'Fatal error recived',(e, e.args,traceback.TracebackException.from_exception(e).print(),e.__context__))
    log.flush()


if __name__ == '__main__':
    log.log(2, 'Program Alive', sys.argv)
    main(sys.argv)


class ArgsNotFoundError(Exception):
    pass
