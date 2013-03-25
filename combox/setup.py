from comodit_client.api import Client
from comodit_client.api.collection import EntityNotFoundException
from comodit_client.api.importer import Import

def setup(config):
    # Connect to the ComodIT API
    client = Client(config['endpoint'], config['username'], config['password'])
    org = client.get_organization(config['organization'])

    print "Setting up ComodIT..."

    # Create environment (if not already present)
    try:
        org.environments().create("Development", "Development environment.")
    except:
        pass

    importer = Import()
    for app in config['applications']:
        print "Uploading application %s" % app["name"]
        try:
            importer.import_application(org, app['name'])
        except Exception as e:
            print "Failed to upload applicatin %s with error %s." % (app['name'], e)

    print "Done."
