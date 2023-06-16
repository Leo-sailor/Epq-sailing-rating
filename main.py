# imports
from LocalDependencies.Hosts import HostScript
import sys
#TODO: force ': ' input styling
#TODO: use clean input boolen entering more
#TODO: come up with principle on newline usage
#TODO: refactor with an 'imports' class to reduce reused code
# initzalizations
host = HostScript()

host.torun(*sys.argv)

