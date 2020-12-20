from netmiko import ConnectHandler

INTERFACE_MAP = {
    "csr1":
        {
            "interface": "GigabitEthernet4",
            "ipaddr": "10.100.12.1",
            "mask": "255.255.255.0",
            "description": "Connect to csr2"
        },
    "csr2":
        {
            "interface": "GigabitEthernet4",
            "ipaddr": "10.100.12.2",
            "mask": "255.255.255.0",
            "description": "Connect to csr1"
        }
  }

csr1 = ConnectHandler(host='csr1', username='automation', password='ansible', device_type='cisco_ios')
csr2 = ConnectHandler(host='csr2', username='automation', password='ansible', device_type='cisco_ios')

csr1_interface_command = "interface {}".format(INTERFACE_MAP['csr1']['interface'])
csr1_ipaddr_command = "ip address {} {}".format(INTERFACE_MAP['csr1']['ipaddr'], INTERFACE_MAP["csr1"]["mask"])
csr1_descr_command = "description {}".format(INTERFACE_MAP['csr1']['description'])

csr1_commands = [csr1_interface_command, csr1_ipaddr_command, csr1_descr_command]

csr2_interface_command = "interface {}".format(INTERFACE_MAP['csr2']['interface'])
csr2_ipaddr_command = "ip address {} {}".format(INTERFACE_MAP['csr2']['ipaddr'], INTERFACE_MAP["csr2"]["mask"])
csr2_descr_command = "description {}".format(INTERFACE_MAP['csr2']['description'])
csr2_commands = [csr2_interface_command, csr2_ipaddr_command, csr2_descr_command]

csr1.send_config_set(csr1_commands)
csr2.send_config_set(csr2_commands)

print(csr1.send_command("ping {}".format(INTERFACE_MAP['csr2']['ipaddr'])))
print(csr2.send_command("ping {}".format(INTERFACE_MAP['csr1']['ipaddr'])))

csr1.disconnect()
csr2.disconnect()