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
from hpOneView.oneview_client import OneViewClient
from hpOneView.exceptions import HPOneViewException
from config_loader import try_load_from_file

config = {
    "ip": "",
    "credentials": {
        "userName": "administrator",
        "password": ""
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

options = {
    "type": "Range",
    "startAddress": "VCUS6EI000",
    "endAddress": "VCUS6EIZZZ",
    "rangeCategory": "Custom"
}

options_additional = {
    "type": "Range",
    "name": "VSN",
    "prefix": None,
    "enabled": True,
    "startAddress": "VCGV2Y4000",
    "endAddress": "VCGV2Y4ZZZ",
    "rangeCategory": "Generated",
    "totalCount": 46656,
    "freeIdCount": 46656,
    "allocatedIdCount": 0,
    "defaultRange": True,
    "allocatorUri":
        "/rest/id-pools/vsn/ranges/ae2df099-5570-4f9e-9503-16531324d9a4/allocator",
    "collectorUri":
        "/rest/id-pools/vsn/ranges/ae2df099-5570-4f9e-9503-16531324d9a4/collector",
    "reservedIdCount": 0,
    "freeFragmentUri":
        "/rest/id-pools/vsn/ranges/ae2df099-5570-4f9e-9503-16531324d9a4/free-fragments?start=0&count=-1",
    "allocatedFragmentUri":
        "/rest/id-pools/vsn/ranges/ae2df099-5570-4f9e-9503-16531324d9a4/allocated-fragments?start=0&count=-1",
    "category": "id-range-VSN",
    "uri":
        "/rest/id-pools/vsn/ranges/ae2df099-5570-4f9e-9503-16531324d9a4",
    "eTag": None,
    "created": "2013-04-08 18:11:17.862",
    "modified": "2013-04-08 18:11:17.862"
}

# Create VSN Range for id pools
vsn_range = oneview_client.id_pools_vsn_ranges.create(options)
pprint(vsn_range.data)

# Get vsn range by uri
vsn_range_byuri = vsn_range.get_by_uri(vsn_range.data['uri'])
print("Got vsn range from '{}' to '{}' by uri:\n   '{}'".format(vsn_range_byuri.data[
      'startAddress'], vsn_range_byuri.data['endAddress'], vsn_range_byuri.data['uri']))

# Enable a vSN range
information = {
    "type": "Range",
    "enabled": True
}
vsn_range = vsn_range.enable(information)
print("Successfully enabled vsn range at\n   'uri': {}\n   with 'enabled': {}".format(
    vsn_range.data['uri'], vsn_range.data['enabled']))

# Allocate a set of IDs from vsn range
information = {
    "count": 10
}
successfully_allocated_ids = vsn_range.allocate(information)
print("Successfully allocated IDs:")
pprint(successfully_allocated_ids)

# Get all allocated fragments in vsn range
print("Get all allocated fragments in vsn range")
allocated_fragments = vsn_range.get_allocated_fragments()
pprint(allocated_fragments)

# Get all free fragments in vsn range
print("Get all free fragments in vsn range")
allocated_fragments = vsn_range.get_free_fragments()
pprint(allocated_fragments)

# Collect a set of IDs back to vsn range
try:
    information = {
        "idList": successfully_allocated_ids['idList']
    }
    successfully_collected_ids = vsn_range.collect(information)
except HPOneViewException as e:
    print(e.msg)

# Disable a vsn range
information = {
    "type": "Range",
    "enabled": False
}
vsn_range = vsn_range.enable(information)
print("Successfully disabled vsn range at\n   'uri': {}\n   with 'enabled': {}".format(
    vsn_range.data['uri'], vsn_range.data['enabled']))

# Delete vsn_range
vsn_range.delete()
print("Successfully deleted vsn range")

# Create vsn Range for id pools with more options specified
print("Create vsn range with more options specified for id pools")
vsn_range = oneview_client.id_pools_vsn_ranges.create(options_additional)
pprint(vsn_range.data)

# Delete vsn_range
vsn_range.delete()
print("Successfully deleted newly created vsn range")
