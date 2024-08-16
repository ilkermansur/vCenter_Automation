import requests
import urllib3
from requests.auth import HTTPBasicAuth
import json

# Disable the secure connection warning for demo purpose.
# This is not recommended in a production environment.

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class VCenterAuto:
    def __init__(self, vcenter_ip, username, password):
        self.vcenter_ip = vcenter_ip
        self.username = username
        self.password = password
        self.session_id = self.get_session_id()
    
    # Get Session ID
    def get_session_id (self):

        """
        The function `get_session_id` sends an HTTP POST request to a vCenter server to create a session and
        returns the session ID if successful.
        
        """

        url = f"https://{self.vcenter_ip}/rest/com/vmware/cis/session"
        response = requests.post(url, auth=HTTPBasicAuth(self.username, self.password), verify=False)
        if response.status_code == 200:

            # Parse the JSON response and extract session ID
            session_id = response.json()["value"]
        else:
            print (f"error is occured {response.status_code}")
        return session_id
    
    def get_vm_list (self):

        """
        The function `get_vm_list` retrieves a list of virtual machines from a vCenter server using the
        provided credentials.

        """

        vm_list_url = f"https://{self.vcenter_ip}/api/vcenter/vm"
        response = requests.get(url=vm_list_url, headers={"vmware-api-session-id": self.session_id}, verify=False)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get Data. Status code: {response.status_code}")
        
    def get_vm_id (self, vm_name):

        """
        The function `get_vm_id` retrieves the ID of a virtual machine by its name from a vCenter server
        using the provided credentials.

        vm_name       : VM name                 (mandatory)

        """

        vm_list = self.get_vm_list()
        for item in vm_list:
            if item['name'] == vm_name:
                vm_id = item['vm']
                break
            else:
                continue
        return vm_id
            
    def get_folder_list (self):

        """
        The function `get_folder_list` retrieves a list of folders from a vCenter server using the provided
        credentials.
        
        """

        folder_list_url = f"https://{self.vcenter_ip}/api/vcenter/folder"

        response = requests.get(url=folder_list_url, headers={"vmware-api-session-id": self.session_id}, verify=False)

        if response.status_code == 200 :
            return response.json()
        else:
            raise Exception(f"Failed to get Data. Status code: {response.status_code}")
        
    def get_folder_id (self, folder_name):

        """
        The function `get_folder_id` retrieves the folder ID based on the folder name from a vCenter server
        using the provided credentials.

        """

        folder_list = self.get_folder_list()
        for item in folder_list:
            if folder_name == item ['name']:
                folder_id = item ['folder']
                break
            else:
                continue
        return folder_id
    def get_datastore_list (self):
        """
        The function `get_datastore_list` retrieves a list of datastores from a vCenter server using the
        provided credentials.
        """

        datastore_list_url = f"https://{self.vcenter_ip}/api/vcenter/datastore"
        response = requests.get(url=datastore_list_url, headers={"vmware-api-session-id": self.session_id}, verify=False)

        if response.status_code == 200 :
            return response.json()
        else :
            raise Exception(f"Failed to get Data. Status code: {response.status_code}")
        
    def get_datastore_id (self,datastore_name):
        """
        The function `get_datastore_id` retrieves the ID of a specified datastore by name from a vCenter
        server using the provided credentials.

        ds_name       : Datastore name (mandatory)

        """

        datastore_list = self.get_datastore_list()
        for item in datastore_list:
            if datastore_name == item['name']:
                datastore_id = item['datastore']
                break
            else:
                continue
        return datastore_id

    def get_host_list (self):
        """
        The function `get_host_list` retrieves a list of hosts from a vCenter server using the provided
        credentials.
        """
        host_list_url = f"https://{self.vcenter_ip}/api/vcenter/host"
        response = requests.get(url=host_list_url, headers={"vmware-api-session-id": self.session_id}, verify=False)


        if response.status_code == 200 :
            return response.json()
        else:
            raise Exception(f"Failed to get Data. Status code: {response.status_code}")
        
    def get_host_id (self, host_name):
        """
        The function `get_host_id` retrieves the ID of a host by its name from a vCenter server using the
        provided credentials.

        host_name     : ESXI Host name          (mandatory)
        """
        
        host_list = self.get_host_list()
        for item in host_list:
            if host_name == item['name']:
                host_id = item['host']
                break
            else:
                continue
        return host_id
    
    def get_resource_pool_list (self):
        """
        The function `get_resource_pool_list` retrieves a list of resource pools from a vCenter server using
        the provided credentials.
        """

        resource_pool_url = f"https://{self.vcenter_ip}/api/vcenter/resource-pool"
        response = requests.get(url=resource_pool_url, headers={"vmware-api-session-id": self.session_id}, verify=False)

        if response.status_code == 200 :
            return response.json()
        else:
            raise Exception(f"Failed to get Data. Status code: {response.status_code}")
    
    def get_resource_pool_id (self,resource_pool_name):

        """
        The function `get_resource_pool_id` retrieves the ID of a specified resource pool from a vCenter
        server using the provided credentials.

        resource_pool_name: Resource Pool name (mandatory)
        """
        resource_pool_list = self.get_resource_pool_list()

        for item in resource_pool_list:
            if resource_pool_name == item['name']:
                resource_pool_id = item['resource_pool']
                break
            else:
                continue
        return resource_pool_id
    
    def delete_vm (self, vm_name):
        """
        The function `delete_vm` deletes a virtual machine by its name using VMware vCenter API
        authentication.
        
        vm_name : VM name (mandatory)
        """
        vm_id = self.get_vm_id(vm_name)
        delete_vm_url = f"https://{self.vcenter_ip}/api/vcenter/vm/{vm_id}"

        response = requests.delete(url=delete_vm_url, headers={"vmware-api-session-id": self.session_id}, verify=False)
        
        if response.status_code == 204 :
            print(f"VM {vm_name} with ID {vm_id} has been deleted successfully")
        else:
            print(f"Failed to delete VM with ID {vm_id}. Status code: {response.status_code}")

    def clone_vm (self, src_vm_name, dst_vm_name, folder_name = None, datastore_name = None, host_name = None, resource_name = None):
        """
        The `clone_vm` function clones a virtual machine in a VMware environment using specified parameters
        like source VM name, destination VM name, vCenter IP, credentials, and optional placement details.

        dest_vm_name  : Destination vm name     (mandatory)
        src_vm_name   : Source vm name          (mandatory)
        folder        : Destination folder name
        datastore     : Destination datastore name
        host          : Destination Host ESXI
        resource_pool : Destination Resource Pool

        """

        src_vm_id = self.get_vm_id(src_vm_name)

        placement = {}

        if folder_name is not None:
            folder_id = self.get_folder_id(folder_name)
            placement['folder'] = folder_id

        if datastore_name is not None:
            datastore_id = self.get_datastore_id(datastore_id)
            placement['datastore'] = datastore_id

        if host_name is not None:
            host_id = self.get_host_id(host_name)
            placement['host'] = host_id

        if resource_name is not None:
            resource_pool_id = self.get_resource_pool_id(resource_name)
            placement['resource_pool'] = resource_pool_id

        json_data = {
            'name' : dst_vm_name,
            'source' : src_vm_id,
            'placement' : placement
        }
    
        # Vm Clone URL
        clone_url = f"https://{self.vcenter_ip}/api/vcenter/vm?action=clone"

        # Getting Clone vm
        response = requests.post(url=clone_url, headers={"vmware-api-session-id": self.session_id}, json=json_data, verify=False)

        if response.status_code == 200 :
            print(f"VM {src_vm_name} cloned successfully as {dst_vm_name} ")
        else:
            print(f"Failed to clone VM  {src_vm_name}. Status code: {response.status_code}")


vmconnect = VCenterAuto(vcenter_ip='',username='',password='')

############################################################################################################################################
#                                                           Example Usage                                                                  #
############################################################################################################################################

vm_list = vmconnect.get_vm_list()
print (json.dumps(vm_list, indent=4))
