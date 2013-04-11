import os
import sys
import json

from os.path import expanduser, join
from clint import args
from combox.helper import randomMAC
from combox.exception import FatalException

if sys.version_info < (3, 0):
    from ConfigParser import RawConfigParser, Error as ConfigParserError
else:
    from configparser import RawConfigParser, Error as ConfigParserError


def _verify_args():
    """
    """

    if not len(args.all):
        raise FatalException("Missing command. You should try the --help "
                             "option!")

def _verify_binaries():
    """
    """

    if not which('VBoxManage'):
        err = "Combox requires VirtualBox.\nDownload it there: " \
              "https://www.virtualbox.org/wiki/Downloads"
        raise FatalException(err)


def _load_combox_conf():
    """
    """

    path = os.path.join(os.getcwd(), 'combox.conf')
    config = {}

    with open(path, 'r') as fd:
        config = json.load(fd)

    if 'mac' not in config['vm'] or not config['vm']['mac']:
        config['vm']['mac'] = randomMAC()

    config['platform']['settings'] = {}
    config['platform']['settings']['mac_address'] = config['vm']['mac'].upper()

    return config


def _load_comoditrc_conf():
    """
    """

    parser = RawConfigParser()
    parser.read(join(expanduser('~'), '.comoditrc'))

    default_section = parser.items('default')
    default_values = {}
    for k, v in default_section:
        default_values[k] = v

    return default_values


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

    _verify_args()
    _verify_binaries()
    combox_cfg = _load_combox_conf()
    comodit_cfg = _load_comoditrc_conf()

    # Merge configuration files.
    config = dict(combox_cfg.items() + comodit_cfg.items())
    return config


config = configure()
