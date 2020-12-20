#! /usr/bin/env python

from netmiko import ConnectHandler

def ez_cisco(hostname, show_command, username='automation', password='ansible'):
    platform = "cisco_ios"
    device = ConnectHandler(ip=hostname, username=username, password=password, device_type=platform)

    output = device.send_command(show_command)
    device.disconnect()

    return output

response = ez_cisco('csr1', 'show version | in regi')
print (response)

response = ez_cisco('csr2', 'show ip int brief')
print (response)

response = ez_cisco('csr3', 'show run | inc vty')
print (response)