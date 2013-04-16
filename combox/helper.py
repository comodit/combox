import time, sys, os
import random
import urllib2

from subprocess import Popen, PIPE
from comodit_client.api.exceptions import PythonApiException
from comodit_client.rest.exceptions import ApiException

def create_host(env, name, platform, distribution, applications = []):
    print "Defining host %s" % name
    host = env.hosts().create(name, "", platform['name'], distribution['name'])

    # Configure platform
    context = host.get_platform()
    for key, value in platform['settings'].iteritems():
        context.settings().create(key, value)

    # Configure distribution
    context = host.get_distribution()
    for key, value in distribution['settings'].iteritems():
        context.settings().create(key, value)

    # Install applications
    for app in applications:
        host.install(app['name'], app['settings'])

    return host

def get_short_hostname(hostname):
    parts = hostname.split('.')
    return parts[0]

def get_latest_id(prefix, env):
    names = env.hosts_f
    last_id = -1
    for name in names:
        if name.startswith(prefix):
            i = int(name[len(prefix):].rstrip())
            if i > last_id:
                last_id = i
    return last_id

def exec_cmd(cmd):
    ret = {}
    proc = Popen(cmd,
                 shell=True,
                 stdout=PIPE,
                 stderr=PIPE)
    out, err = proc.communicate()
    ret['cmd'] = cmd
    ret['stdout'] = out
    ret['stderr'] = err
    ret['returncode'] = proc.returncode
    ret['pid'] = proc.pid
    return ret

def exec_cmds(commands, exit_on_fail=True):
    for cmd in commands:
        ret = exec_cmd(cmd)
        if ret["returncode"] > 0:
            print "Error executing command %s: %s", ret["cmd"], ret["stderr"]
            if exit_on_fail:
                return False
    return True

def fork_cmd(cmd):
    Popen(cmd, shell=True)

def download_iso(gpxe_url, file_name, access_key,
                 secret_key, org_name, comodit_host):
    url = gpxe_url + \
          '?access_key=%s' \
          '&secret_key=%s' \
          '&org_name=%s' \
          '&comodit_host=%s' % (access_key, secret_key, org_name, comodit_host)

    file_name += '.iso'
    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,

    f.close()
    return file_name

def randomMAC(sep=':'):
    mac = [ 0x00, 0x16, 0x3e,
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff) ]
    return sep.join(map(lambda x: "%02x" % x, mac)).upper()

def get_combox_images_directory():
    return os.path.join(os.path.expanduser('~'), '.combox')
