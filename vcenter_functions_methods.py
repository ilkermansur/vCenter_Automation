import requests
import urllib3
from requests.auth import HTTPBasicAuth
import json
import credentials
import pprint

# Disable the secure connection warning for demo purpose.
# This is not recommended in a production environment.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


################################################# GET SESSION ID #################################################

def get_session_id(vcenter_ip, username, password):
    """
    The function `get_session_id` sends an HTTP POST request to a vCenter server to create a session and
    returns the session ID if successful.

    vcenter_ip    : Vcenter ip address      (mandatory)
    username      : Username of vCenter     (mandatory)
    password      : Password of vCenter     (mandatory)
    
    """
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

    except Exception as e:
        print(f"An error occurred: {e}")

    
################################################# GET VM LIST #################################################

def get_vm_list (vcenter_ip, username, password):
    """
    The function `get_vm_list` retrieves a list of virtual machines from a vCenter server using the
    provided credentials.
    
    vcenter_ip    : Vcenter ip address      (mandatory)
    username      : Username of vCenter     (mandatory)
    password      : Password of vCenter     (mandatory)

    """

    try:

        session_id = get_session_id(vcenter_ip, username, password)

        vm_list_url = f"https://{vcenter_ip}/api/vcenter/vm"
        response = requests.get(url=vm_list_url, headers={"vmware-api-session-id": session_id}, verify=False)

        if response.status_code == 200:
            vm_all_spec_list = response.json()
                
        else:
            print(f"Failed to get VM list. Status code: {response.status_code}")
        
        return vm_all_spec_list

    except Exception as e:
        print (f"error is occured {e}")

################################################# GET VM ID #################################################

def get_vm_id (vm_name, vcenter_ip, username, password):
    """
    The function `get_vm_id` retrieves the ID of a virtual machine by its name from a vCenter server
    using the provided credentials.

    vm_name       : VM name                 (mandatory)
    vcenter_ip    : Vcenter ip address      (mandatory)
    username      : Username of vCenter     (mandatory)
    password      : Password of vCenter     (mandatory)
    

    """

    try:

        session_id = get_session_id(vcenter_ip, username, password)
        # Find VM ID
        vm_list_url = f"https://{vcenter_ip}/api/vcenter/vm"
        response = requests.get(url=vm_list_url, headers={"vmware-api-session-id": session_id}, verify=False)
        if response.status_code == 200:
            vm_list = response.json()
            for item in vm_list:
                if vm_name == item["name"]:
                    vm_id = item["vm"]
                    break
                else:
                    continue
            return vm_id
        else:
            print(f"Failed to get VM list. Status code: {response.status_code}")

    except Exception as e:
        print (f"error is occured {e}")

################################################# GET FOLDER ID #################################################

def get_folder_id (folder_name, vcenter_ip, username, password):
    """
    The function `get_folder_id` retrieves the folder ID based on the folder name from a vCenter server
    using the provided credentials.

    folder_name   : Folder name             (mandatory)
    vcenter_ip    : Vcenter ip address      (mandatory)
    username      : Username of vCenter     (mandatory)
    password      : Password of vCenter     (mandatory)
    
    """

    try:

        session_id = get_session_id(vcenter_ip, username, password)

        folder_list_url = f"https://{vcenter_ip}/api/vcenter/folder"

        response = requests.get(url=folder_list_url, headers={"vmware-api-session-id": session_id}, verify=False)

        if response.status_code == 200:
            folder_list = response.json()
            for item in folder_list:
                if folder_name == item["name"]:
                    folder_id = item["folder"]
                    break
                else:
                    continue
            return folder_id
        else:
            print(f"Failed to get folder-id. Status code: {response.status_code}")
    
    except Exception as e:
        print (f"error is occured {e}")

################################################# GET FOLDER LIST #################################################

def get_folder_list (vcenter_ip, username, password):
    """
    The function `get_folder_list` retrieves a list of folders from a vCenter server using the provided
    credentials.

    vcenter_ip    : Vcenter ip address      (mandatory)
    username      : Username of vCenter     (mandatory)
    password      : Password of vCenter     (mandatory)
    
    """

    try:

        session_id = get_session_id(vcenter_ip, username, password)

        folder_list_url = f"https://{vcenter_ip}/api/vcenter/folder"

        response = requests.get(url=folder_list_url, headers={"vmware-api-session-id": session_id}, verify=False)

        if response.status_code == 200:
            folder_list = response.json()

            return folder_list
        else:
            print(f"Failed to get folder list. Status code: {response.status_code}")
    
    except Exception as e:
        print (f"error is occured {e}")

################################################# DATASTORE ID #################################################

def get_datastore_id(datastore_name, vcenter_ip, username, password):
    """
    The function `get_datastore_id` retrieves the ID of a specified datastore by name from a vCenter
    server using the provided credentials.

    ds_name       : Datastore name          (mandatory)
    vcenter_ip    : Vcenter ip address      (mandatory)
    username      : Username of vCenter     (mandatory)
    password      : Password of vCenter     (mandatory)
    
    """

    try:

        session_id = get_session_id(vcenter_ip, username, password)

        # Find Datastore ID
        datastore_list_url = f"https://{vcenter_ip}/api/vcenter/datastore"
        response = requests.get(url=datastore_list_url, headers={"vmware-api-session-id": session_id}, verify=False)

        if response.status_code == 200:
            datastore_list = response.json()

            for item in datastore_list: 
                if datastore_name == item["name"]:
                    datastore_id = item["datastore"]
                    break
                else:
                    continue
            return datastore_id
        else:
            print(f"Failed to get datastore list. Status code: {response.status_code}")

    except Exception as e:
        print (f"error is occured {e}")

################################################# DATASTORE LIST #################################################

def get_datastore_list(vcenter_ip, username, password):
    """
    The function `get_datastore_list` retrieves a list of datastores from a vCenter server using the
    provided credentials.

    vcenter_ip    : Vcenter ip address      (mandatory)
    username      : Username of vCenter     (mandatory)
    password      : Password of vCenter     (mandatory)
    

    """

    try:

        session_id = get_session_id(vcenter_ip, username, password)

        # Find Datastore ID
        datastore_list_url = f"https://{vcenter_ip}/api/vcenter/datastore"
        response = requests.get(url=datastore_list_url, headers={"vmware-api-session-id": session_id}, verify=False)

        if response.status_code == 200:
            datastore_list = response.json()
            return datastore_list
        else:
            print(f"Failed to get datastore list. Status code: {response.status_code}")

    except Exception as e:
        print (f"error is occured {e}")

################################################# HOST ID #################################################

def get_host_id (host_name, vcenter_ip, username, password):
    """
    The function `get_host_id` retrieves the ID of a host by its name from a vCenter server using the
    provided credentials.

    host_name     : ESXI Host name          (mandatory)
    vcenter_ip    : Vcenter ip address      (mandatory)
    username      : Username of vCenter     (mandatory)
    password      : Password of vCenter     (mandatory)
    
    """

    try:

        session_id = get_session_id(vcenter_ip, username, password)

        host_list_url = f"https://{vcenter_ip}/api/vcenter/host"
        response = requests.get(url=host_list_url, headers={"vmware-api-session-id": session_id}, verify=False)

        if response.status_code == 200:
            host_list = response.json()

            for item in host_list:
                if host_name == item["name"]:
                    host_id = item["host"]
                    break
                else:
                    continue
            return host_id
        else:
            print(f"Failed to get host list. Status code: {response.status_code}")
    except Exception as e:
        print (f"error is occured {e}")

################################################# HOST LIST #################################################

def get_host_list (vcenter_ip, username, password):
    """
    The function `get_host_list` retrieves a list of hosts from a vCenter server using the provided
    credentials.

    vcenter_ip    : Vcenter ip address      (mandatory)
    username      : Username of vCenter     (mandatory)
    password      : Password of vCenter     (mandatory)
    
    """

    try:

        session_id = get_session_id(vcenter_ip, username, password)

        host_list_url = f"https://{vcenter_ip}/api/vcenter/host"
        response = requests.get(url=host_list_url, headers={"vmware-api-session-id": session_id}, verify=False)

        if response.status_code == 200:
            host_list = response.json()

            return host_list
        else:
            print(f"Failed to get host list. Status code: {response.status_code}")
    except Exception as e:
        print (f"error is occured {e}")

################################################# RESOURCE POOL ID #################################################

def get_resource_pool_id (resource_pool_name, vcenter_ip, username, password):
    """
    The function `get_resource_pool_id` retrieves the ID of a specified resource pool from a vCenter
    server using the provided credentials.

    pool_name     : Resource Pool name      (mandatory)
    vcenter_ip    : Vcenter ip address      (mandatory)
    username      : Username of vCenter     (mandatory)
    password      : Password of vCenter     (mandatory)
    
    """

    try:

        session_id = get_session_id(vcenter_ip, username, password)

        resource_pool_url = f"https://{vcenter_ip}/api/vcenter/resource-pool"
        response = requests.get(url=resource_pool_url, headers={"vmware-api-session-id": session_id}, verify=False)

        if response.status_code == 200:
            resource_pool_list = response.json()
            for item in resource_pool_list:
                if resource_pool_name == item["name"]:
                    resource_pool_id = item["resource_pool"]
                    break
                else:
                    continue
            return resource_pool_id
        else:
            print(f"Failed to get resource pool list. Status code: {response.status_code}")

    except Exception as e:
        print (f"error is occured {e}")

################################################# RESOURCE POOL ID LIST #################################################

def get_resource_pool_list (vcenter_ip, username, password):
    """
    The function `get_resource_pool_list` retrieves a list of resource pools from a vCenter server using
    the provided credentials.

    vcenter_ip    : Vcenter ip address      (mandatory)
    username      : Username of vCenter     (mandatory)
    password      : Password of vCenter     (mandatory)
    
    """

    try:

        session_id = get_session_id(vcenter_ip, username, password)

        resource_pool_url = f"https://{vcenter_ip}/api/vcenter/resource-pool"
        response = requests.get(url=resource_pool_url, headers={"vmware-api-session-id": session_id}, verify=False)

        if response.status_code == 200:
            resource_pool_list = response.json()
            return resource_pool_list
        else:
            print(f"Failed to get resource pool list. Status code: {response.status_code}")

    except Exception as e:
        print (f"error is occured {e}")

################################################# DELETE VM #################################################

def delete_vm (vm_name, vcenter_ip, username, password):
    """
    The function `delete_vm` deletes a virtual machine by its name using VMware vCenter API
    authentication.
    
    vm_name       : VM name                 (mandatory)
    vcenter_ip    : Vcenter ip address      (mandatory)
    username      : Username of vCenter     (mandatory)
    password      : Password of vCenter     (mandatory)
    
    """

    try:

        session_id = get_session_id(vcenter_ip, username, password)
        vm_id = get_vm_id (vm_name, vcenter_ip=vcenter_ip, username=username, password=password)

        delete_vm_url = f"https://{vcenter_ip}/api/vcenter/vm/{vm_id}"

        response = requests.delete(url=delete_vm_url, headers={"vmware-api-session-id": session_id}, verify=False)

        if response.status_code == 200 or response.status_code == 204:
            print(f"VM {vm_name} with ID {vm_id} has been deleted successfully")
        else:
            print(f"Failed to delete VM with ID {vm_id}. Status code: {response.status_code}")

    except Exception as e:
        print (f"error is occured {e}")

################################################# CLONE VM #################################################

def clone_vm (src_vm_name, dst_vm_name, vcenter_ip, username, password, folder_name = None, datastore_name = None, esxi_host_name = None, resource_pool = None):
    """
    The `clone_vm` function clones a virtual machine in a VMware environment using specified parameters
    like source VM name, destination VM name, vCenter IP, credentials, and optional placement details.

    vcenter_ip    : Vcenter ip address      (mandatory)
    username      : Username of vCenter     (mandatory)
    password      : Password of vCenter     (mandatory)
    dest_vm_name  : Destination vm name     (mandatory)
    src_vm_name   : Source vm name          (mandatory)
    folder        : Destination folder name
    datastore     : Destination datastore name
    host          : Destination Host ESXI
    resource_pool : Destination Resource Pool

    """

    src_vm_id = get_vm_id(vcenter_ip=vcenter_ip, username=username, password=password,vm_name=src_vm_name)

    placement = {}

    if folder_name is not None:
        folder_id = get_folder_id(folder_name=folder_name,vcenter_ip=vcenter_ip, username=username, password=password)
        placement["folder"] = folder_id,
    elif datastore_name is not None:
        datastore_id = get_datastore_id(datastore_name=datastore_name, vcenter_ip=vcenter_ip, username=username, password=password)
        placement["datastore"] = datastore_id,
    elif esxi_host_name is not None:
        host_id = get_host_id(host_name=esxi_host_name,vcenter_ip=vcenter_ip, username=username, password=password)
        placement["host"] = host_id,
    elif resource_pool is not None:
        resource_pool_id = get_resource_pool_id(resource_pool,vcenter_ip=vcenter_ip, username=username, password=password)
        placement['resource_pool'] = resource_pool_id
    
    json_data ={
    "name" : dst_vm_name,
    "source" : src_vm_id,
    "placement" : placement
    }

    try:

        session_id = get_session_id(vcenter_ip, username, password)

        # Vm Clone URL
        clone_url = f"https://{vcenter_ip}/api/vcenter/vm?action=clone"

        # Getting Clone vm
        response = requests.post(url=clone_url, headers={"vmware-api-session-id": session_id}, json=json_data, verify=False)


        if response.status_code == 200:
            print(f"VM {src_vm_name} cloned successfully as {dst_vm_name} ")
        else:
            print(f"Failed to clone VM  {src_vm_name}. Status code: {response.status_code}")

    except Exception as e:
        print (f"error is occured {e}")

