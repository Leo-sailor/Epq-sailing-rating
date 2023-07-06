# imports
from LocalDependencies.Hosts import HostScript
import sys
from LocalDependencies.leo_dataclasses import constants
#TODO: come up with principle on newline usage
#TODO: Refactor to a frontend-backend architecture
#TODO: Finnish unit tests
#TODO: singleton constants class
# initzalizations
if __name__ == '__main__':
    constants()
    host = HostScript()
    host.torun(*sys.argv)

