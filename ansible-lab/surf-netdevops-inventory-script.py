#!/usr/bin/env python
# 2020-09-2020
from __future__ import absolute_import, division, print_function, unicode_literals
import os
import sys
import argparse
import json
import re

if sys.version.startswith("3"):
    import urllib.parse
if sys.version.startswith("2"):
    import urllib
import requests

DEVICE_MAPPING = {
    "pan": "firewall",
    "acc": "access",
    "cor": "core",
    "dis": "distribution",
    "rtredge": "edgerouters",
    "rtrborder": "borderrouters",
}

DEVICE_SYSPARM_LOOKUP = [
    "name",
    "operational_status",
    "ip_address",
    "location",
    "model_id",
    "manufacturer",
    "sys_class_name",
]

DEVICE_QUERY = "sys_class_name=cmdb_ci_ip_router^ORsys_class_name=cmdb_ci_ip_switch^ORsys_class_name=cmdb_ci_ip_network^ORsys_class_name=cmdb_ci_netgear^ORsys_class_name=cmdb_ci_ip_firewall^operational_status=1"


class SnowInventory(object):
    """Service Now Ansible dynamic inventory plugin.

    Inventory Plugin to build out an Ansible inventory.
    """

    def __init__(
        self,
        snow_instance=os.getenv("SNOW_INSTANCE"),
        device_table="cmdb_ci_netgear",
        username=os.getenv("SNOW_USERNAME"),
        password=os.getenv("SNOW_PASSWORD"),
        api_version="v2",
        panorama_hostname=os.getenv("PANORAMA_HOSTNAME"),
        panorama_ip=os.getenv("PANORAMA_IP"),
    ):
        """Init of SnowInventory."""
        self.username = username
        self.password = password
        self.snow_instance = snow_instance
        self.api_version = api_version
        self.device_table = device_table
        self.panorama_hostname = panorama_hostname
        self.panorama_ip = panorama_ip

        # Check for required information
        if not isinstance(self.username, str):
            print("Please verify username is sent in or is configured in the environment.")
            sys.exit(1)

        if not isinstance(self.password, str):
            print("Please verify password is sent in or is configured in the environment.")
            sys.exit(1)

        if not isinstance(self.snow_instance, str):
            print("Please verify ServiceNow instance is sent in or is configured in the environment.")
            sys.exit(1)

        self.inventory = {}
        self._generate_inventory()

        self.return_func()

    def return_func(self):
        """Returns the inventory for testing.

        Returns:
            [dict]: Result of the action
        """
        return self.inventory

    # Read the command line args passed to the script.
    def read_cli_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--list", action="store_true")
        parser.add_argument("--host", action="store")
        self.args = parser.parse_args()

    def _generate_inventory(self):
        """Generate inventory dictionary."""
        device_types = []
        temp_inventory = {}
        self.inventory["_meta"] = {"hostvars": {}}

        # Get the device list from Service Now, and populate the device type
        for device in self._get_service_now_info(
            table=self.device_table, sysparm_fields=",".join(DEVICE_SYSPARM_LOOKUP), query=DEVICE_QUERY
        ):
            # Check if in a status other than operational, move on if so
            if device["operational_status"] != "1":
                continue

            # Get the device name, lookup characters, and device_type from the mappings
            device_name = device["name"]
            lookup = re.match(r"^([a-zA-Z]+)", device_name)
            if lookup is None:
                continue
            lookup = lookup.group()
            device_type = DEVICE_MAPPING.get(lookup, None)

            # Check for the device type of None, if None move on
            if device_type is None:
                continue

            # Check if the device is in the platforms
            device_type = "role__" + device_type
            if device_type not in device_types:
                device_types.append(device_type)

            # Build the inventory information
            temp_inventory[device["name"]] = {
                "device_type": device_type,
                "ip_address": device.get("ip_address", None),
                # "location": lcl_location,
            }

        # Create device type groups
        for device_type in device_types:
            group_vars = {}
            if device_type in [
                "role__access",
                "role__borderrouters",
                "role__core",
                "role__distribution",
                "role__edgerouters",
            ]:
                group_vars["ansible_network_os"] = "ios"
                group_vars["ansible_connection"] = "network_cli"
            if device_type in ["role__firewall"]:
                group_vars["ansible_network_os"] = "panos"
                group_vars["ansible_connection"] = "local"
            self.inventory[device_type] = {"hosts": [], "vars": group_vars}

        if self.panorama_hostname is not None:
            self.inventory["role__panorama"] = {
                "hosts": [self.panorama_hostname], "vars": {
                    "ansible_network_os": "panos",
                    "ansible_connection": "local"
                }
            }
            self.inventory["_meta"]["hostvars"][self.panorama_hostname] = {
                "ansible_host": self.panorama_ip
            }

        # Add devices to inventory
        for hostname, data in temp_inventory.items():
            self.inventory[data["device_type"]]["hosts"].append(hostname)
            # self.inventory[data["location"]]["hosts"].append(hostname)

            # Add to host vars and add any host specific information
            host_vars = {}

            # Check for an IP address assignment
            if data["ip_address"] not in (None, ""):
                host_vars["ansible_host"] = data["ip_address"]
            self.inventory["_meta"]["hostvars"][hostname] = host_vars

        self.inventory.pop("", None)

    def _get_service_now_info(self, table, sysparm_fields=None, query=None):
        """Method to get the information from Service Now API endpoints.
        
        Args:
            table (string): Table to query
            sysparm_fields (string): Comma separated list of fields to return
        """

        # Set the request URL
        url = "https://{}.service-now.com/api/now/table/{}?".format(self.snow_instance, table)

        # Check for the sysparm fields
        if sysparm_fields is not None:
            url = "{}&sysparm_fields={}".format(url, sysparm_fields)

        # Add any query setup
        if query is not None:
            if sys.version.startswith("3"):
                url = "{}&sysparm_query={}".format(url, urllib.parse.quote(query))
            elif sys.version.startswith("2"):
                url = "{}&sysparm_query={}".format(url, urllib.quote(query))

        # Set proper headers
        headers = {"Accept": "application/json"}

        # Do the HTTP request
        response = requests.get(url, auth=(self.username, self.password), headers=headers)

        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print(self.username, self.password)
            print(
                "Status:", response.status_code, "Headers:", response.headers, "Error Response:", response.content,
            )
            sys.exit(1)

        # Decode the JSON response into a dictionary and use the data
        return dict(response.json())["result"]


def main():
    """Main code block."""
    snow_obj = SnowInventory()
    print(json.dumps(snow_obj.inventory))


if __name__ == "__main__":
    main()
