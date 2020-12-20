import json

# platforms = ['nexus', 'catalyst', 'asa', 'csr', 'aci']

# supported_platforms = ['nexus', 'catalyst']

# for platform in platforms:
#     if platform in supported_platforms:
#         print("Platform {} -- SUPPORTED".format(platform))
#     else:
#         print("Platform {} -- NOT SUPPORTED".format(platform))

# vlans = [{'name': 'web', 'id': 10}, { 'id': 20}, {'name': 'db', 'id': 30}]


# for item in vlans:
#     vlan_id = item['id']
#     vlan_name = item.get('name')
#     print("vlan {}".format(vlan_id))
#     if vlan_name:
#         print(" name {}".format(vlan_name))

devices = [{'platform': 'nexus', 'hostname': 'nycr01'}, {'platform': 'catalyst', 'hostname': 'nycsw02'}, {'platform': 'mx', 'hostname': 'nycr03'}, {'platform': 'srx', 'hostname': 'nycfw01'}, {'platform': 'asa', 'hostname': 'nycfw02'}]

# for item in devices:
#     platform = item.get('platform')
#     if platform == 'nexus':
#         print("Vendor is Cisco")
#     elif platform == 'catalyst':
#         print("Vendor is Cisco")   
#     elif platform == 'aci':
#         print("Vendor is Cisco")   
#     elif platform == 'srx':
#         print("Vendor is Juniper")
#     else:
#         print("Unknown Vendor")   

cisco_platforms = ['catalyst', 'nexus', 'aci']
juniper_platforms = ['mx', 'srx']

for item in devices:
    platform = item.get('platform')
    if platform in cisco_platforms:
        print("Vendor of {} is Cisco".format(platform))
    elif platform in juniper_platforms:
        print("Vendor of {} is Juniper".format(platform))
    else:
        print("Vendor of {} is UNKNOW".format(platform))













# print(json.dumps(devices, indent=4))