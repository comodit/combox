from comodit_client.api import Client

from combox.config import config
from helper import exec_cmds

def teardown():
    # Script
    print "Teardown of development environment"

    client = Client(config['api'], config['username'], config['password'])
    env = client.get_environment(config['organization'], "Development")

    # First detroy the VM
    exec_cmds(['VBoxManage controlvm "%s" poweroff' % config['vm']['name'],
               'VBoxManage unregistervm "%s" --delete' % config['vm']['name']],
              False)

    # Then delete the comodit hosts
    for h in env.hosts():
        try:
            print "Deleting instance of", h.name
            h.get_instance().delete()
        except Exception:
            print "Could not delete host ", h.name
        h.delete()
