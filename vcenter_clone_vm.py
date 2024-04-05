"""
This Python script is written for a specific purpose and reflects its current state. However, no warranty is provided. 
Usage of this script is entirely at the user's own risk. The developer  or  contributors cannot be held liable for any 
direct or indirect damages that may arise from the use or misuse of this script.

Developer: ilker MANSUR
Email: imansur@morten.com.tr
GitHub: github.com/ilkermansur

Arguments:

dst_folder_name = ""            # Destination folder name
dst_datastore_name = ""         # Destination datastore name
dst_host_ip = ""                # Destination host IP
dst_resource_pool_name = ""     # Destination resource pool name
src_vm_name = ""                # Source VM name
dst_vm_name = ""                
 
"""

from vcenter_name2id import name_id_conversion, get_session_id
from credentials import vcenter_ip,username,password
import requests

json_data =  (name_id_conversion(dst_datastore_name="LAB-1",
                                dst_folder_name="IM-POD-VM-01",
                                dst_host_ip="192.168.49.21",
                                dst_resource_pool_name="IM-POD-VM-01",
                                src_vm_name="HQ-CUBE-A-00",
                                dst_vm_name="TEST-API-VM"
                                ))

# Getting the session ID
session_id = get_session_id(username=username, password=password, vcenter_ip=vcenter_ip)

# Vm Clone URL
clone_url = f"https://{vcenter_ip}/api/vcenter/vm?action=clone"

# Getting clone vm
response = requests.post(url=clone_url, headers={"vmware-api-session-id": session_id}, json=json_data, verify=False)
if response.status_code == 200:
    print ("VM cloned successfully")
else:
    print (f"VM clone failed : {response.text}")
