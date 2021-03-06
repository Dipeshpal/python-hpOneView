# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2017) Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###

from pprint import pprint

from config_loader import try_load_from_file
from hpOneView.oneview_client import OneViewClient

# To run this example fill the ip and the credentials bellow or use a configuration file
config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<oneview_administrator_name>",
        "password": "<oneview_administrator_password>",
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# To run this example you can define an logical interconnect uri (logicalInterconnectUri) and the ethernet network uri
# or the example will attempt to retrieve those automatically from the appliance.
logical_interconnect_uri = None
ethernet_network_uri = None

# Attempting to get first LI and Ethernet uri and use them for this example
if logical_interconnect_uri is None:
    logical_interconnect_uri = oneview_client.logical_interconnects.get_all()[0]['uri']
if ethernet_network_uri is None:
    ethernet_network_uri = oneview_client.ethernet_networks.get_all()[0]['uri']

options = {
    "name": "Uplink Set Demo",
    "status": "OK",
    "logicalInterconnectUri": logical_interconnect_uri,
    "networkUris": [
        ethernet_network_uri
    ],
    "fcNetworkUris": [],
    "fcoeNetworkUris": [],
    "portConfigInfos": [],
    "connectionMode": "Auto",
    "networkType": "Ethernet",
    "manualLoginRedistributionState": "NotSupported",
}

# Create an uplink set
print("\nCreate an uplink set")
created_uplink_set = oneview_client.uplink_sets.create(options)
print("Created uplink set '{name}' successfully.\n  uri = '{uri}'".format(**created_uplink_set))

# Update an uplink set
print("\nUpdate an uplink set")
created_uplink_set['name'] = 'Renamed Uplink Set Demo'
updated_uplink_set = oneview_client.uplink_sets.update(created_uplink_set)
print("Updated uplink set name to '{name}' successfully.\n  uri = '{uri}'".format(**updated_uplink_set))

# Get a paginated list of uplink set resources sorting by name ascending and filtering by status
print("\nGet a list of uplink sets")
uplink_sets = oneview_client.uplink_sets.get_all(0, 15, sort='name:ascending')
for uplink_set in uplink_sets:
    print('  %s' % uplink_set['name'])

# Get an uplink set resource by name
print("\nGet uplink set by name")
uplink_set = oneview_client.uplink_sets.get_by('name', 'Renamed Uplink Set Demo')[0]
print("Found uplink set at uri '{uri}'\n  by name = '{name}'".format(**uplink_set))

# Add an ethernet network to the uplink set
# To run this example you must define an ethernet network uri or ID below
ethernet_network_id = None
if ethernet_network_id:
    print("\nAdd an ethernet network to the uplink set")
    uplink_set = oneview_client.uplink_sets.add_ethernet_networks(created_uplink_set['uri'], ethernet_network_id)
    print("The uplink set with name = '{name}' have now the networkUris:\n {networkUris}".format(**uplink_set))

# Get an uplink set resource by uri
print("\nGet an uplink set by uri")
uplink_set = oneview_client.uplink_sets.get(created_uplink_set['uri'])
pprint(uplink_set)

# Remove an ethernet network from the uplink set
# To run this example you must define an ethernet network uri or ID below
ethernet_network_id = None
if ethernet_network_id:
    print("\nRemove an ethernet network of the uplink set")
    uplink_set = oneview_client.uplink_sets.remove_ethernet_networks(created_uplink_set['uri'], ethernet_network_id)
    print("The uplink set with name = '{name}' have now the networkUris:\n {networkUris}".format(**uplink_set))

# Get the associated ethernet networks of an uplink set
print("\nGet the associated ethernet networks of the uplink set")
networks = oneview_client.uplink_sets.get_ethernet_networks(created_uplink_set['uri'])
pprint(networks)

# Delete the recently created uplink set
print("\nDelete the uplink set")
oneview_client.fc_networks.delete(updated_uplink_set)
print("Successfully deleted the uplink set")
