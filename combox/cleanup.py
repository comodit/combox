from comodit_client.api import Client
from combox.config import config

def cleanup():
    # Connect to the ComodIT API
    client = Client(config['api'], config['username'], config['password'])
    org = client.get_organization(config['organization'])

    print "Cleaning up ComodIT..."

    # Delete applications
    for app in config['applications']:
        print "Removing application %s" % app["name"]
        app_name = app['name'].split('/')[-1]
        try:
            org.applications().delete(app_name)
        except Exception as e:
            print "Failed to remove application %s with error %s." % app['name'], e

    print "Done."
