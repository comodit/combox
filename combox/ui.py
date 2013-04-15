from clint import args
from clint.textui import colored, puts, indent, columns


def error(msg):
    """
    """

    puts(colored.red(msg))


def print_help():
    """
    """

    col = 10
    thehelp = {
        "cleanup": "Remove uploaded application from ComodIT.",
        "deploy": "Define the host on ComodIT and deploy it on VirtualBox.",
        "setup": "Create a ComodIT environment and upload applications.",
        "start": "Start the VirtualBox VM.",
        "stop": "Stop the VirtualBox VM.",
        "teardown": "Power off the VirtualBox VM, unregister it, then delete "
                    "the comodit host.",
    }

    puts()
    for cmd, desc in sorted(thehelp.iteritems()):
        with indent(4):
            puts(columns([colored.green(cmd), col], [(desc), 80]))
