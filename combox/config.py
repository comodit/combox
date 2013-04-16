import os
import sys
import json

from os.path import expanduser, join
from optparse import OptionParser
from comodit_client.config import Config, ConfigException
from combox.helper import randomMAC
from combox.exception import FatalException

if sys.version_info < (3, 0):
    from ConfigParser import RawConfigParser, Error as ConfigParserError
else:
    from configparser import RawConfigParser, Error as ConfigParserError


def _verify_args(args):
    """
    """

    if not len(args):
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


    if 'gpxe_url' not in config or not config['gpxe_url']:
        config['gpxe_url'] = "https://my.comodit.com/gpxe"

    if 'time_out' not in config or not config['time_out']:
        config['timeout'] = 3600

    if 'distribution' not in config or not config['distribution'].get('name'):
        raise FatalException('Distribution not defined')

    if 'shares' not in config['vm']:
        config['vm']['shares'] = []

    if 'mac' not in config['vm'] or not config['vm']['mac']:
        config['vm']['mac'] = randomMAC()

    default_share = {"name":"default", "target": os.path.abspath(os.curdir)}
    config['vm']['shares'].insert(0, default_share)

    if 'platform' not in config:
        config['platform'] = {
            'name': 'gPXE',
            'settings': {
                'mac_address':config['vm']['mac'].upper()
            }
        }

    elif 'settings' not in config['platform']:
        config['platform']['settings'] = {}
        config['platform']['settings']['mac_address'] = config['vm']['mac'].upper()

    return config


def _load_comoditrc_conf(options):
    """
    """

    profile_name = None
    if options.profile:
        profile_name = options.profile

    config = Config()
    try:
        org = config._get_value(profile_name, 'default_organization')
    except:
        pass

    return {
        'api': config.get_api(profile_name),
        'username': config.get_username(profile_name),
        'password': config.get_password(profile_name)
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


def _configure_parser():
    parser = OptionParser()
    parser.add_option("-p", "--profile", dest="profile",
                      help="Comodit-client profile name")

    return parser.parse_args()


def create_combox_images_directory():
    combox_images_path = os.path.join(os.path.expanduser('~'), '.combox')
    if not os.path.exists(combox_images_path):
        os.mkdir(combox_images_path)


def configure():
    """ Configures Combox by verifying if all components is correctly installed
    (e.g. VBoxManage) and by loading the combox.conf configuration file.
    """
    create_combox_images_directory()
    options, args = _configure_parser()
    _verify_args(args)
    _verify_binaries()
    combox_cfg = _load_combox_conf()
    comodit_cfg = _load_comoditrc_conf(options)

    # Merge configuration files.
    config = dict(combox_cfg.items() + comodit_cfg.items())
    config['platform']['settings']['mac_address'] = config['vm']['mac'].upper()
    return config


try:
    config = configure()
except FatalException as err:
    sys.exit(err)
