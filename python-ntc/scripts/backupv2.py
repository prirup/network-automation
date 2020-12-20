#! /usr/bin/env python

from netmiko import ConnectHandler

devices = ['csr1','csr2','csr3']

for device in devices:

    print("Connecting to device | {}".format(device))

    net_device = ConnectHandler(host=device, username='automation', password='ansible', device_type='cisco_ios')

    print("Saving configuration | {}".format(device))

    net_device.send_command("wr mem")

    print("Backing up configuration | {}".format(device))

    net_device.send_command("term len 0")
    config = net_device.send_command("show run")

    print("Writing config to file | {}\n".format(device))

    with open("/home/ntc/network-automation/python-ntc/files/configs/{}.cfg".format(device), "w") as config_file:
        config_file.write(config)

    net_device.disconnect()