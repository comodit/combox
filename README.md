# Introduction

Combox enables you to easily deploy and manage development environments
on your own system. Combox is part of the ComodIT IT Automation platform. See
the related post on [the ComodIT blog](http://www.comodit.com/blog.html).

# Pre-requisite

1. Have a working comodit-client setup. See [here](https://github.com/comodit/comodit-client/blob/master/README.md).
2. Have a working VirtualBox setup.

# Install

## Fedora/CentOS Users

1. Add ComodIT repository by executing the following command:
    - On CentOS 6: `rpm -ivh http://dl.comodit.com/pub/centos/6/x86_64/comodit-release-6-3.el6.noarch.rpm`
    - On Fedora 16: `rpm -ivh http://dl.comodit.com/pub/fedora/16/x86_64/comodit-release-16-1.fc16.noarch.rpm`
    - On Fedora 17: `rpm -ivh http://dl.comodit.com/pub/fedora/17/x86_64/comodit-release-17-1.fc17.noarch.rpm`
    - On Fedora 18: `rpm -ivh http://dl.comodit.com/pub/fedora/18/x86_64/comodit-release-18-1.fc18.noarch.rpm`
2. Install client with command `yum install comodit-combox`.

# Usage
Usage: combox \<action\>
- deploy    : Define the host on ComodIT and deploy it on VirtualBox.
- teardown  : Power off the VirtualBox VM, unregister it, then delete the comodit host.
- setup     : Create a ComodIT environment and upload applications.
- stop      : Stop the VirtualBox VM.
- start     : Start the VirtualBox VM.
- cleanup   : Remove uploaded application from ComodIT

# Configuration
Everything takes place in the `.combox/combox.conf` configuration file.
You can look at the sample provided [in this repository](https://github.com/comodit/combox/blob/master/.combox/combox.conf.sample).

```json
{
    "vm" : {
        "name": "combox-host",
        "memory": "512",
        "ports_fw" : [["127.0.0.1", "2222", "22"]],
        "shares" : []
    },
    "applications":  [{
            "name": ".combox/virtualbox-guest-additions",
            "settings": {"shares":[{"name":"default", "mount":"/mnt"}]}
        }
    ],
    "distribution": {
        "name" : "CentOS 6",
        "store_uuid": "EA09D3703EC811E28139D51B7F000001"
        "settings" : {
            "root_password": "secret"
        }
    }
}
```

### vm

The virtualbox virtual machines settings.
- `name`: the name of the virtualbox machine
- `memory`: memory set for the virtualbox machine
- `ports_fw`: port forwarding on [\<host\>, \<local_port\>, \<remote_port\>]
- `shares`: arrays of arrays [\<share_name\>, \<path_to_folder_to_share\>]

### applications

Array of exported Comodit applications. See [here](https://github.com/comodit/comodit-client#advanced-import-export-and-synchronization) to export your ComodIT applications. Usually, a developer using combox will provide the necessary recipes.
- `name`: the path to the application
- `settings`: the application settings

### distribution

This will be used to define the operating system that will be installed on the virtualbox machine.
Two possibilities: either you specify a name of a distribution that already
exists in your ComodIT organization, or you can specify the store uuid of a
distribution. Combox will automatically purchase it (don't worry, it's free),
from the ComodIT store and install it in your organization.

- `name`: the distribution name as in your ComodIT organization.
- `store_uuid`: the uuid of the distribution you want to purchase
- `settings`: specific settings for the distribution. In the example above, the
  root password.

