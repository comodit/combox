import time, sys, os

from comodit_client.api import Client
from comodit_client.api.exceptions import PythonApiException
from comodit_client.api.collection import EntityNotFoundException
from comodit_client.rest.exceptions import ApiException
from comodit_client.api.host import Host

from helper import create_host, get_short_hostname, exec_cmd, exec_cmds, fork_cmd


def deploy(config):

    # Script
    print "Deploying Development Host"
    start_time = time.time()

    # Connect to the ComodIT API
    client = Client(config['endpoint'], config['username'], config['password'])
    env = client.get_environment(config['organization'], 'Development')
    
    # Deploy Storytlr
    host = create_host(env, config['vm']['name'], config['platform'], config['distribution'], []) 
    host.provision()

    # Define the vm
    print "Creating the virtual machine"
    success = createvm(config['vm'])
    if not success:
        sys.exit(-1)


    # Start the vm
    print "Starting the virtual machine"
    fork_cmd('virtualbox --startvm "%s"' % config['vm']['name'])

    # Wait for server to be ready
    print "Waiting for host to be ready"
    host.wait_for_state('READY', config['time_out'])

    # Wait for hostname to be ready
    print "Waiting for hostname to be ready"
    host.get_instance().wait_for_address()

    # Install applications
    for app in config['applications']:
        print "Installing application %s" % app["name"]
        host.install(app["name"], app["settings"])
        host.wait_for_state('READY', config['time_out'])

    # Goodbye
    total_time = time.time() - start_time
    print "Deployment time: " + str(total_time)

def createvm(vm):
    ret = exec_cmds(['VBoxManage createvm --name "%s" --register' % vm['name'],
                     'VBoxManage modifyvm "%s" --memory %s --pae on --acpi on --boot1 disk --boot2 dvd' % (vm['name'], vm['memory']),
                     'VBoxManage modifyvm "%s" --nic1 bridged --bridgeadapter1 p5p1 --macaddress1 %s' % (vm['name'], vm['mac']),
                     'VBoxManage modifyvm "%s" --ostype Linux' % vm['name'],
                     'VBoxManage createhd --filename %s --size 10000' % vm['storage'],
                     'VBoxManage storagectl "%s" --name "IDE Controller" --add ide' % vm['name'],
                     'VBoxManage storageattach "%s" --storagectl "IDE Controller" --port 0 --device 0 --type hdd --medium %s' % (vm['name'], vm['storage']),
                     'VBoxManage storageattach "%s" --storagectl "IDE Controller" --port 1 --device 0 --type dvddrive --medium %s' % (vm['name'], vm['iso'])])
    # Return on errors
    if not ret:
        return False

    # Add the shares
    for share in vm['shares']:
        ret = exec_cmds(['VBoxManage sharedfolder add "%s" --name "%s" --hostpath "%s" --readonly' % (vm['name'], share['name'], share['target'])])
        if not ret:
            return False

    return True

