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

###
clone_url = f"https://{vcenter_ip}/api/vcenter/vm?action=clone"

# Use 'ID' instead of 'name' for the source VM
json_data ={
    "name" : "test-api-clone",
    "source" : "vm-796",
    "placement" : {
        "folder" : "group-v779",
        "datastore" : "datastore-707",
        "host" : "host-9",
        "resource_pool": "resgroup-292"
    }
}

response = requests.post(url=clone_url, headers={"vmware-api-session-id": session_id}, json=json_data, verify=False)
if response.status_code == 200:
    print ("VM cloned successfully")
else:
    print (f"VM clone failed : {response.text}")