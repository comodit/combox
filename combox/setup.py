import json

from comodit_client.api import Client
from comodit_client.api.importer import Import

from combox.config import config
from combox.exception import FatalException

def setup():
    print "Setting up ComodIT..."
    org = create_organization()
    create_platform(org)
    create_distribution(org)
    create_environment(org)
    upload_apps(org)
    print "Done."


def create_organization():
    # Connect to the ComodIT API
    client = Client(config['api'], config['username'], config['password'])
    org = None

    if config['organization']:
        org = client.get_organization(config['organization'])
    else:
        orgs = client.organizations().list()
        if orgs == 1:
            org = orgs[0]
        elif orgs == 0:
            raise FatalException("No organization found.")
        else:
            raise FatalException("Multiple organization defined. "
                    "Please specify one in your ~/.comoditrc with the key "
                    "\"default_organization\"")
    return org


def create_platform(org):
    # Create platform if not provided or not existent
    try:
        org.get_platform(config['platform']['name'])
    except:
        found_platform = False
        print "Looking for a physical platform..."
        for pl in org.platforms().list():
            if pl.driver.name == "com.guardis.cortex.server.driver.PxeDriver":
                config['platform']['name'] = pl.driver.name
                print "Found physical platform. Using \"%s\"" % pl.driver.name
                found_platform = True
        if not found_platform:
            print "Platform not found. Creating PXE platform named \"gPXE\"."
            org.platforms().create('gPXE',
                    driver_class="com.guardis.cortex.server.driver.PxeDriver")


def create_distribution(org):
    # Buy distribution from store if not present in organization
    try:
        org.get_distribution(config['distribution']['name'])
    except:
        uuid = config['distribution']['store_uuid']
        name = config['distribution']['name']
        try:
            dist = org.purchased_dists().create(uuid, name)
        except Exception as err:
            raise FatalException(err)


def create_environment(org):
    # Create environment (if not already present)
    try:
        org.environments().create("Development", "Development environment.")
    except:
        pass


def upload_apps(org):
    importer = Import()
    for app in config['applications']:
        print "Uploading application %s" % app["name"]
        try:
            importer.import_application(org, app['name'])
        except Exception as e:
            print "Failed to upload application %s " \
                  "with error %s." % (app['name'], e)
