import time, sys, os 

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

