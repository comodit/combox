import time, sys, os, helper

from comodit_client.api import Client
from comodit_client.api.exceptions import PythonApiException
from comodit_client.rest.exceptions import ApiException

from helper import create_host, get_short_hostname, exec_cmd, exec_cmds, fork_cmd

def stop(config):
    print "Stopping virtual machine"
    success = exec_cmds(['VBoxManage controlvm "%s" poweroff' % config['vm']['name']])

def start(config):
    print "Starting virtual machine"
    fork_cmd('VBoxManage startvm --type headless "%s"' % config['vm']['name'])

