#/usr/bin/python3

import requests
import json
import pprint
from random import *
import sys
import logging
import logging.handlers

logger = logging.getLogger('FROM-API')
logger.setLevel(logging.INFO)

#add handler to the logger
handler = logging.handlers.SysLogHandler('/dev/log')

#add formatter to the handler
formatter = logging.Formatter('%(asctime)s %(name)-12s %(message)s')

handler.formatter = formatter
logger.addHandler(handler)
#
#Add line below to log status
#logger.info("insert message here")
#
#----------------LOGIN--------------------
def login():
    print("Logging in...")
    global url,run_ID,session_ID,headers,FMG_API_USER,FMG_API_PWD
    run_ID += 1
    #api-user = raw_input("Enter API username: ")
    #api-pwd = raw_input("Enter the API user password: ")
    # API login
    payload = {
        "method":"exec",
        "params": [ {
            "url":"/sys/login/user",
            "data": {
                "user": FMG_API_USER,
                "passwd": FMG_API_PWD
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
    logger.info("LOGIN: Session status: " + session_status)

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
    print("-" * 20)
    logger.info("LOGOUT: Session status: " + session_status)
    print("End of script reached")
    print("-" * 20)
    quit()

#--------------------get ADOM membership---------------

def get_adom_membership():
    global url,headers,session_ID,run_ID,host_in_adom,target_adom
    adom2scan = input("Enter ADOM you wish to scan (default is root):")
    if adom2scan == "":
        adom2scan = "root"
    run_ID += 1
    payload = {
        "method":"get",
        "params": [ {
            "url": "/dvmdb/adom/"+ adom2scan +"/device"
        } ],
        "id":run_ID,
        "session": session_ID
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()
    session_status = response['result'][0]['status']['message']
    if session_status == "Invalid url":
        print("This adom does not exist, please try again.")
        get_adom_membership()
    # Interpret hostnames found in output
    # create dict for their storage
    #
    #pprint.pprint(response)
    #define keys for host_in_adom
    keys = ['hostname','SN','adom']
    print("Getting root ADOM members:")
    for host in response['result'][0]['data']:
        found_host = (host['name'])
        serial_num = (host['sn'])
        target_adom = found_host[-2:]
        print(found_host)
        #print(target_adom)
        #Build dict format hostname:adom
        host_list = (found_host,serial_num,target_adom)
        host_in_adom.append(dict(zip(keys,host_list)))
    if host_in_adom == []:
        print("There are currently no firewalls in this ADOM.")
        print('-' * 20)
        logout()
    elif adom2scan == target_adom:
        print("-" * 20)
        print("No need to move these devices, as they are already in the correct ADOM.")
        print("-" * 20)
        logout()
    print('-' * 20)
    return host_in_adom

# ----------------- TESTING TOOL -------------------
def generate_test_firewalls():
    global url,headers,session_ID,run_ID
    proceed = input("Do you want to generate test firewalls in the root domain? (y/n) ")
    if proceed == "n":
        print("-" * 20)
        return
    while True:
        try:
            num_firewalls = int(input("How many? "))
        except ValueError:
            print("Please enter only numbers.")
            continue
        else:
            break
    target_adom = str(input("For which adom? "))
    #-----generate firewall list
    test_firewall_list = []
    for num in range(num_firewalls):
        test_firewall_list.append("FG50-API-TEST" + str(num + 1) + "-" + target_adom)
    #
    # ----- ADD test list to ADOM
    # Adding only to the root ADOM
    #
    for test_firewall in test_firewall_list:
        random_sn = randint(100000,999999)
        test_fw_sn = "FGT50E3U16" + str(random_sn)
        print("FW " + test_firewall + " with sn: " + str(test_fw_sn) + " will be added to the root ADOM")
        run_ID += 1
        payload = {
            "id":run_ID,
            "method":"exec",
            "params": [ {
                "url": "/dvm/cmd/add/device",
                "data": {
                    "adom": "root",
                    "flags":["create_task"],
                    "device": {
                        "name": test_firewall,
                        "hostname": test_firewall,
                        "adm_usr": "admin",
                        "adm_pass": "testing",
                        "sn": test_fw_sn,
                        "platform_str": "FortiGate-50E",
                        "os_type": 0,
                        "os_ver": 5,
                        "build": 1111,
                        "patch": 3,
                        "mr": 4,
                        "device action": "add_model",
                        "mgmt_mode": "fmg",
                        "version": 500 
                    }
                }
            } ],
            "session": session_ID
        }
        response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()
        #pprint.pprint(response)
        session_status = response['result'][0]['status']['message']       
        print("Add status: " + session_status)
    print("-" * 20)
# -----------------------------------------------
#--------------RUN below--------------------------
# -----------------------------------------------
#
# Retrieve credentials
# 
with open("FMG_connection_data.json") as data_file:
    data = json.load(data_file)
    
FMG_IP = data["FMG-IP"]
FMG_API_USER = data["API-username"]
FMG_API_PWD = data["API-password"]
FGT_ADMIN = data["FGT-admin"]
FGT_PWD = data["FGT-password"]
#
# End data load
#
#-------setting global veriables
session_ID = 0
run_ID = 0
name = 0
url = "http://" + FMG_IP + "/jsonrpc"
headers = {'content-type': 'application/json'}
host_in_adom = []
#
#
login()
generate_test_firewalls()
logout()


