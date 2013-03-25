from comodit_client.api import Client
from comodit_client.api.importer import Import

def cleanup(config):
    # Connect to the ComodIT API
    client = Client(config['endpoint'], config['username'], config['password'])
    org = client.get_organization(config['organization'])

    print "Cleaning up ComodIT..."

    # Delete applications
    for app in config['applications']:
        print "Removing application %s" % app["name"]
        try:
            org.applications().delete(app['name'])
        except Exception as e:
            print "Failed to remove application %s with error %s." % app[name], e

    print "Done."
