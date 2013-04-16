import time, sys, os
import uuid

from urlparse import urlparse

from comodit_client.api import Client
from combox.config import config
from helper import create_host, exec_cmds, fork_cmd
from helper import download_iso, get_combox_images_directory


def deploy():

    # Script
    print "Deploying Development Host"
    start_time = time.time()

    # Connect to the ComodIT API
    client = Client(config['api'], config['username'], config['password'])
    org = client.get_organization(config['organization'])
    env = org.get_environment('Development')

    # Deploy host
    host = create_host(env, config['vm']['name'], config['platform'], config['distribution'], [])
    host.provision()

    # Download gPXE ISO
    if 'iso' not in config['vm'] or not os.path.exists(config['vm']['iso']):
        config['vm']['iso'] = download_iso(config['gpxe_url'],
                                           config['vm']['name'],
                                           org.access_key,
                                           org.secret_key,
                                           org.name,
                                           urlparse(config['api']).netloc)

    # Define the vm
    print "Creating the virtual machine"
    success = create_combox(config['vm'])
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
        app_name = app['name'].split('/')[-1]
        print "Installing application %s" % app_name
        host.install(app_name, app['settings'])
        host.wait_for_state('READY', config['time_out'])

    # Goodbye
    total_time = time.time() - start_time
    print "Deployment time: " + str(total_time)

def create_combox(vm):
    import pdb; pdb.set_trace()
    cmds = createvm(vm)
    cmds += modifyvm(vm)
    if not config['vm'].get('storage'):
        storage_path = os.path.join(get_combox_images_directory(),
                                    config['vm']['name'] + '-' +
                                    str(uuid.uuid1()) +
                                    ".vmdk")
    cmds += createhd(vm, storage_path)
    cmds += storagectl(vm)
    cmds += storageattach(vm, storage_path)

    ret = exec_cmds(cmds)

    # Return on errors
    if not ret:
        return False

    # Add the shares
    for share in vm['shares']:
        ret = exec_cmds(['VBoxManage sharedfolder add "%s" --name "%s" --hostpath "%s" --readonly' % (vm['name'], share['name'], share['target'])])
        if not ret:
            return False

    return True

def createvm(vm):
    return ['VBoxManage createvm --name "%s" --register' % vm['name']]

def modifyvm(vm):
    cmds = []
    cmds.append('VBoxManage modifyvm "%s" --ostype Linux' % vm['name'])
    cmds.append('VBoxManage modifyvm "%s" --memory %s --pae on --acpi on --ioapic on --boot1 disk --boot2 dvd' % (vm['name'], vm['memory']))

    mac = ''.join(vm['mac'].split(':'))
    cmds.append('VBoxManage modifyvm "%s" --nic1 nat --macaddress1 %s' % (vm['name'], mac))
    for item in vm['ports_fw']:
        cmds.append('VBoxManage modifyvm "%s" --natpf1 "%s,tcp,%s,%s,,%s"' %
                (vm['name'], "guestssh" + item[1], item[0],item[1],item[2]))
    return cmds

def createhd(vm, storage):
    return ['VBoxManage createhd --filename %s --size 10000 --format VMDK' %
        storage]

def storagectl(vm):
     return ['VBoxManage storagectl "%s" --name "IDE Controller" --add ide' % vm['name']]

def storageattach(vm, storage):
    cmds = []
    cmds.append('VBoxManage storageattach "%s" --storagectl "IDE Controller" --port 0 --device 0 --type hdd --medium %s' % (vm['name'], storage))
    cmds.append('VBoxManage storageattach "%s" --storagectl "IDE Controller" --port 1 --device 0 --type dvddrive --medium %s' % (vm['name'], vm['iso']))
    return cmds
