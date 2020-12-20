from netmiko import ConnectHandler
from builtins import input
from getpass import getpass



def connect_to_device(hostname, username, password, device_type):
    message = "Connecting to device"
    print_logger(message, hostname)
    net_d = ConnectHandler(host=hostname, username=username, password=password, device_type=device_type)

    return net_d

def deploy_commands(device, hostname, config_file):
    print("Sending commands from file | {}".format(hostname))
    device.send_config_from_file(config_file)

def print_logger(message, hostname):
    print("{} | {}".format(message, hostname))

def main(device, username, password, device_type):
    config_file = '/home/ntc/network-automation/python-ntc/files/configs/snmp.cfg'

    net_device = connect_to_device(device, username, password, device_type)

    deploy_commands(net_device, device, config_file)

    print_logger("Disconnecting from device", device)
    net_device.disconnect()

if __name__ == "__main__":
    device = input("Please enter the hostname or IP: ")
    username = input("Please enter the username: ")
    password = getpass("Please enter the password: ")
    device_type = input("Please enter the device type: ")

    main(device, username, password, device_type)