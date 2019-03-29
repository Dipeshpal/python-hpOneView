# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2019) Hewlett Packard Enterprise Development LP
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
from hpOneView.oneview_client import OneViewClient
from config_loader import try_load_from_file

config = {
    "ip": "10.50.4.100",
    "credentials": {
        "userName": "kattumun",
        "password": "P@ssw0rd!"
    }
}

# These variables must be defined according with your environment
server_hardware_type_uri = "/rest/server-hardware-types/F8FE8F99-47A5-480C-B11D-C63DAF55C089"
enclosure_group_uri = "/rest/enclosure-groups/cf1e3026-26d6-43f2-8646-0c30760bc157"
enclosure_group_uri_for_transformation = "/rest/enclosure-groups/bb1fbca0-2289-4b75-adbb-0564cdc4995d"
server_hardware_type_uri_for_transformation = "/rest/server-hardware-types/34A3A0B2-66C7-4657-995E-60895C1F8F96"

server_profile_name = "ProfileTemplate101"

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Create a server profile template
print("Create a basic connection-less server profile template ")
basic_template_options = dict(
    name=server_profile_name,
    serverHardwareTypeUri=server_hardware_type_uri,
    enclosureGroupUri=enclosure_group_uri
)
basic_template = oneview_client.server_profile_templates.create(basic_template_options)
pprint(basic_template)

# Update bootMode from recently created template
print("\nUpdate bootMode from recently created template")
template_to_update = basic_template.copy()
template_to_update["bootMode"] = dict(manageMode=True, mode="BIOS")
updated = oneview_client.server_profile_templates.update(
    resource=template_to_update,
    id_or_uri=template_to_update["uri"]
)
pprint(updated)

# Get all
print("\nGet list of all server profile templates")
all_templates = oneview_client.server_profile_templates.get_all()
for template in all_templates:
    print('  %s' % template['name'])

# Get by property
print("\nGet a list of server profile templates that matches the specified macType")
template_mac_type = all_templates[1]["macType"]
templates = oneview_client.server_profile_templates.get_by('macType', template_mac_type)
for template in templates:
    print('  %s' % template['name'])

# Get by name
print("\nGet a server profile templates by name")
template = oneview_client.server_profile_templates.get_by_name(server_profile_name)
pprint(template)

# Get by uri
print("\nGet a server profile template by uri")
template_uri = all_templates[0]["uri"]
template = oneview_client.server_profile_templates.get(template_uri)
pprint(template)

# Get new profile
print("\nGet new profile")
profile = oneview_client.server_profile_templates.get_new_profile(template_uri)
pprint(profile)

if oneview_client.api_version >= 300:
    # Get server profile template transformation
    print("\nGet a server profile template transformation")

    transformation = oneview_client.server_profile_templates.get_transformation(
        template["uri"], server_hardware_type_uri_for_transformation, enclosure_group_uri_for_transformation)
    pprint(transformation)

# Get available networks
print("\nGet available networks")
available_networks = oneview_client.server_profile_templates.get_available_networks(
    enclosureGroupUri=enclosure_group_uri, serverHardwareTypeUri=server_hardware_type_uri)
print(available_networks)

# Get Server Profile Template by scope_uris
if oneview_client.api_version >= 600:
    server_profile_templates_by_scope_uris = oneview_client.server_profile_templates.get_all(
        scope_uris="\"'/rest/scopes/3bb0c754-fd38-45af-be8a-4d4419de06e9'\"")
    if len(server_profile_templates_by_scope_uris) > 0:
        print("Found %d Server profile Templates" % (len(server_profile_templates_by_scope_uris)))
        i = 0
        while i < len(server_profile_templates_by_scope_uris):
            print("Found Server Profile Template Group by scope_uris: '%s'.\n  uri = '%s'" % (server_profile_templates_by_scope_uris[i]['name'],
                                                                                              server_profile_templates_by_scope_uris[i]['uri']))
            i += 1
        pprint(server_profile_templates_by_scope_uris)
    else:
        print("No Server Profile Template Group found.")

# Delete the created template
print("\nDelete the created template")
oneview_client.server_profile_templates.delete(basic_template)
print("The template was successfully deleted.")
