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

import requests
import urllib3
from requests.auth import HTTPBasicAuth
import credentials
import pprint

# Disable the secure connection warning for demo purpose.
# This is not recommended in a production environment.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_session_id(vcenter_ip, username, password):
    # vCenter REST API URL for session creation
    url = f"https://{vcenter_ip}/rest/com/vmware/cis/session"

    try:
        # HTTP POST request to create session
        response = requests.post(url, auth=HTTPBasicAuth(username, password), verify=False)

        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            # Parse the JSON response and extract session ID
            session_id = response.json()["value"]
            return session_id
        else:
            print(f"Failed to create session. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Credentials to connect to vCenter
vcenter_ip = credentials.vcenter_ip
username = credentials.username
password = credentials.password

# Process of getting session ID
session_id = get_session_id(vcenter_ip, username, password)

# Check the result
if session_id is not None:
    print(f"Session ID successfully received: {session_id}")
else:
    print("Session ID not found")

def name_id_conversion (dst_datastore_name,dst_folder_name,dst_host_ip,dst_resource_pool_name,src_vm_name,dst_vm_name):
    # Find VM ID
    vm_list_url = f"https://{vcenter_ip}/api/vcenter/vm"
    response = requests.get(url=vm_list_url, headers={"vmware-api-session-id": session_id}, verify=False)
    if response.status_code == 200:
        vm_list = response.json()
        for vm in vm_list:
            if src_vm_name == vm["name"]:
                src_vm_id = vm["vm"]
            else:
                continue
    else:
        print(f"Failed to get VM list. Status code: {response.status_code}")

    # Find Folder ID
    folder_url = f"https://{vcenter_ip}/api/vcenter/folder"
    response = requests.get(url=folder_url, headers={"vmware-api-session-id": session_id}, verify=False)
    if response.status_code == 200:
        folder_list = response.json()
        for folder in folder_list:
            if dst_folder_name == folder["name"]:
                folder_id = folder["folder"]
            else:
                continue
    else:
        print(f"Failed to get folder list. Status code: {response.status_code}")

    # Find Datastore ID
    datastore_list_url = f"https://{vcenter_ip}/api/vcenter/datastore"
    response = requests.get(url=datastore_list_url, headers={"vmware-api-session-id": session_id}, verify=False)
    if response.status_code == 200:
        datastore_list = response.json()
        for datastore in datastore_list: 
            if dst_datastore_name == datastore["name"]:
                datastore_id = datastore["datastore"]
            else:
                continue
    else:
        print(f"Failed to get datastore list. Status code: {response.status_code}")
        
    # Find Host ID
    host_list_url = f"https://{vcenter_ip}/api/vcenter/host"
    response = requests.get(url=host_list_url, headers={"vmware-api-session-id": session_id}, verify=False)
    if response.status_code == 200:
        host_list = response.json()
        for host in host_list:
            if dst_host_ip == host["name"]:
                host_id = host["host"]
            else:
                continue
    else:
        print(f"Failed to get host list. Status code: {response.status_code}")

    # Find Resource Pool ID  
    resource_pool_url = f"https://{vcenter_ip}/api/vcenter/resource-pool"
    response = requests.get(url=resource_pool_url, headers={"vmware-api-session-id": session_id}, verify=False)
    if response.status_code == 200:
        rp_list = response.json()
        for rp in rp_list:
            if dst_resource_pool_name == rp["name"]:
                resource_pool_id = rp["resource_pool"]
            else:
                continue
    else:
        print(f"Failed to get resource pool list. Status code: {response.status_code}")
    
    json_data ={
    "name" : dst_vm_name,
    "source" : src_vm_id,
    "placement" : {
        "folder" : folder_id,
        "datastore" : datastore_id,
        "host" : host_id,
        "resource_pool": resource_pool_id
        }
    }
    return json_data

