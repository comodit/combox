import os
import sys
import json

from os.path import expanduser, join
from clint import args
from comodit_client.config import Config
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

    path = os.path.join(os.getcwd(), '.combox/combox.conf')
    config = {}

    with open(path, 'r') as fd:
        config = json.load(fd)

    if 'mac' not in config['vm'] or not config['vm']['mac']:
        config['vm']['mac'] = randomMAC()

    if 'gpxe_url' not in config:
        config['gpxe_url'] = "https://my.comodit.com/gpxe"

    if 'shares' not in config['vm']:
        config['shares'] = []

    default_share = {"name":"default", "target": os.path.abspath(os.curdir)}
    config['vm']['shares'].insert(0, default_share)

    config['platform'] = {'settings':
            {'mac_address':config['vm']['mac'].upper()}
    }

    return config


def _load_comoditrc_conf():
    """
    """

    profile_name = None
    if '--profile' in args.flags:
        profile_name = args.value_after('--profile')

    config = Config()
    return {
        'api': config.get_api(profile_name),
        'username': config.get_username(profile_name),
        'password': config.get_password(profile_name),
        'organization': config._get_value(profile_name, 'default_organization'),
        'platform': {
            'name': config._get_value(profile_name, 'default_platform'),
            'settings' : {}
        },
        'time_out': config._get_value(profile_name, 'time_out'),
        'gpxe_url': config._get_value(profile_name, 'gpxe_url')
    }


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
    config['platform']['settings']['mac_address'] = config['vm']['mac'].upper()
    from pprint import pprint; pprint(config)
    return config


try:
    config = configure()
except FatalException as err:
    sys.exit(err)
