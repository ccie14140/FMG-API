import requests
import json
import pprint

session_ID = 0
run_ID = 0
url = "http://10.2.1.5/jsonrpc"
headers = {'content-type': 'application/json'}

#----------------LOGIN--------------------
def login():
    print("Logging in...")
    global url,run_ID,session_ID,headers
    run_ID += 1
    #api-user = raw_input("Enter API username: ")
    #api-pwd = raw_input("Enter the API user password: ")
    # API login
    payload = {
        "method":"exec",
        "params": [ {
            "url":"/sys/login/user",
            "data": {
                "user": "api-user",
                "passwd":"apiuser2018ZZ!!"
            }
        } ],
        "id":run_ID
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()
    session_ID = response['session']
    session_status = response['result'][0]['status']['message']
    print("Session status: " + session_status)
    print("-"*20)

#--------------------get ADOM membership---------------

def get_adom_membership():
    global url,headers,session_ID,run_ID
    run_ID += 1
    payload = {
        "method":"get",
        "params": [ {
            "url": "/dvmdb/adom/root/device"
        } ],
        "id":run_ID,
        "session": session_ID
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()
    #print(response)
    #pprint.pprint(response)
    #
    # Interpret hostnames found in output
    #
    for host in response['result'][0]['data']:
        hostnames = host['hostname']
    hosts_found = len(hostnames)
    print("Getting root ADOM members (found: " + str(hosts_found) + ")")
    print(hostnames)
    print('-' * 20)



#--------------------- Logout----------------------

def logout():
    global url,headers,session_ID,run_ID
    run_ID += 1
    print("Logging out.")
    payload = {
        "method":"exec",
        "params": [ {
            "url":"/sys/logout"
        } ],
        "id":run_ID,
        "session": session_ID
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()
    #session_status = response['status']
    session_status = response['result'][0]['status']['message']    
    #print(response)    
    print("Session status: " + session_status)

login()
get_adom_membership()
logout()

