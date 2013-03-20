import time, sys, os, helper

from comodit_client.api import Client
from comodit_client.api.exceptions import PythonApiException
from comodit_client.rest.exceptions import ApiException

from helper import create_host, get_short_hostname, exec_cmd, exec_cmds

def teardown(config):
    # Script
    print "Teardown of development environment"

    client = Client(config['endpoint'], config['username'], config['password'])
    env = client.get_environment(config['organization'], "Development")

    # First detroy the VM
    success = exec_cmds(['VBoxManage controlvm "%s" poweroff' % config['vm']['name'],
                         'VBoxManage unregistervm "%s" --delete' % config['vm']['name']], False)

    # Then delete the comodit hosts
    for h in env.hosts():
        try:
            print "Deleting instance of", h.name
            h.get_instance().delete()
        except Exception as e:
            print "Could not delete host ", h.name
        h.delete()
