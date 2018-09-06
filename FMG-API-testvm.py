import requests
import json

session_ID = 0
url = "http://10.2.1.5/jsonrpc"
headers = {'content-type': 'application/json'}


#----------------LOGIN--------------------
def login():
    print("Logging in...")
    global url,session_ID,headers
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
        "id":1
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()
    session_ID = response['session']
    session_status = response['result'][0]['status']['message']
    #print(response['result'])
    #print(response['result'][0]['status']['message'])#[1]['message'])    
    #print("Session ID is: " + session_ID)
    print("Session status: " + session_status)
    print("-"*20)

#--------------------Discover VM---------------

def discover_fgt():
    global url,headers,session_ID
    print("Discovering device: ")
    payload = {
        "method":"exec",
        "params": [ 
	{
            "url": "/dvm/cmd/discover/device",
            "data":{
		"adom": "VM",
		"device": {
			"adm_pass": "rlnfgt2018ZZ!!",
			"adm_usr": "rlnadmin",
			"ip": "10.2.1.8"
			}
		}
        } ],
        "id":1,
        "session": session_ID
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()
    print(response)
    print("-"*20)



#--------------------- Logout----------------------

def logout():
    global url,headers,session_ID
    print("Logging out.")
    payload = {
        "method":"exec",
        "params": [ {
            "url":"/sys/logout"
        } ],
        "id":1,
        "session": session_ID
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()
    #session_status = response['status']
    session_status = response['result'][0]['status']['message']    
    #print(response)    
    print("Session status: " + session_status)

login()
discover_fgt()
logout()

