"""
This Python script is written for a specific purpose and reflects its current state. However, no warranty is provided. 
Usage of this script is entirely at the user's own risk. The developer  or  contributors cannot be held liable for any 
direct or indirect damages that may arise from the use or misuse of this script.

Developer: ilker MANSUR
Email: imansur@morten.com.tr
GitHub: github.com/ilkermansur

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

###
host_list_url = f"https://{vcenter_ip}/api/vcenter/host"

response = requests.get(url=host_list_url, headers={"vmware-api-session-id": session_id}, verify=False)
if response.status_code == 200:
    host_list = response.json()
    for host in host_list:
        host_id = host["host"]
        host_name = host["name"]
        print(f"Host ID: {host_id}, Host Name: {host_name}")
