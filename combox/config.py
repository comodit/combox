import os
import json

from clint import args
from combox.helper import randomMAC
from combox.exception import FatalException


def is_executable(fpath):
    """ Returns True if the fpath is a file executable.
    """

    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)


def which(program):
    """ Searches after the executable in the PATH and returns the absolute
    path.
    """

    fpath, fname = os.path.split(program)
    if fpath:
        if is_executable(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_executable(exe_file):
                return exe_file


def configure():
    """ Configures Combox by verifying if all components is correctly installed
    (e.g. VBoxManage) and by loading the combox.conf configuration file.
    """

    if not len(args.all):
        raise FatalException("Missing command. You should try the --help "
                             "option!")

    if not which('VBoxManage'):
        err = "Combox requires VirtualBox.\nDownload it there: " \
              "https://www.virtualbox.org/wiki/Downloads"
        raise FatalException(err)

    path = os.path.join(os.getcwd(), 'combox.conf')
    config = {}

    with open(path, 'r') as fd:
        config = json.load(fd)

    if 'mac' not in config['vm'] or not config['vm']['mac']:
        config['vm']['mac'] = randomMAC()

    config['platform']['settings'] = {}
    config['platform']['settings']['mac_address'] = config['vm']['mac'].upper()

    return config


config = configure()
