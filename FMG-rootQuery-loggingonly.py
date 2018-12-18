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
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)s %(message)s')

handler.formatter = formatter
logger.addHandler(handler)
#
#Add line below to log status
#logger.info("insert message here")
#
#----------------LOGIN--------------------
def login():
    #print("Logging in...")
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
    #print("Session status: " + session_status)
    #print("-"*20)
    logger.info("LOGIN: Session: " + session_ID + " : " + session_status)

#--------------------- Logout----------------------

def logout():
    global url,headers,session_ID,run_ID
    run_ID += 1
    #print("Logging out.")
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
    #print("Session status: " + session_status)
    #print("-" * 20)
    logger.info("LOGOUT: Session: " + session_ID + " : " + session_status)
    #print("End of script reached")
    #print("-" * 20)
    quit()
#--------------------END logout------------------------
#
#--------------------get ADOM list---------------------
#
def get_adom_list():
    global url,headers,session_ID,run_ID,host_in_adom,target_adom,list_of_adoms
    run_ID += 1
    payload = {
        "method":"get",
        "params": [ {
            "url": "/dvmdb/adom/"
        } ],
        "id":run_ID,
        "session": session_ID
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()
    #pprint.pprint(response)
    for adom in response['result'][0]['data']:
        adoms = adom['name']
        list_of_adoms.append(adoms)
    return list_of_adoms

#--------------------get ADOM membership---------------
# Query only the root ADOM
#
def get_adom_membership():
    global url,headers,session_ID,run_ID,host_in_adom,target_adom,list_of_adoms
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
    #define keys for host_in_adom
    keys = ['hostname','SN','adom']
    logger.info("STATUS: Getting root ADOM members:")
    for host in response['result'][0]['data']:
        found_host = (host['hostname'])
        serial_num = (host['sn'])
        target_adom = found_host[-2:]
        #print(found_host)
        #print(target_adom)
        #Validate ADOM existence
        if target_adom not in list_of_adoms:
            logger.info("ERROR: ADOM does not exist, cannot continue.")
            logout()
        else:
        #print(target_adom)
        #Build dict format hostname:adom
            host_list = (found_host,serial_num,target_adom)
            host_in_adom.append(dict(zip(keys,host_list)))
    #print(host_in_adom)
    if host_in_adom == []:
        logger.info("ERROR: There are currently no FGTs in the root ADOM.")
        logout()
    else:
        return host_in_adom
#
# ----------------Move sequence--------------------
#
def destination_adom_move():
    global url,headers,session_ID,run_ID,name,host_in_adom
    admin_username=""
    admin_password=""
    for host in host_in_adom:
        destination_adom = host['adom']
        hostname = host['hostname']
        serial_num = host['SN']
        if destination_adom == "VM":
            admin_username = "rlnadmin"
            admin_password = "RLNfgt2018ZZ!!"
        else:
            admin_username = FGT_ADMIN
            admin_password = FGT_PWD
        # First promote unregistered device
        run_ID += 1
        payload = {
            "id": run_ID,
            "method":"exec",
            "session": session_ID,
            "params": [ {
                "url": "/dvm/cmd/add/device",
                "data": {
                    "adom": "root",
                    "flags":["create_task"],
                    "device": {
                        "name": hostname,
                        "adm_usr": admin_username,
                        "adm_pass": admin_password,
                        "device action": "promote_unreg",
                        "mgmt_mode": "fmg"
                    }
                }
            } ]
        }
        #Debug payload
        print("-----------request-----------")
        pprint.pprint(payload)
        response = requests.post(url, data=json.dumps(payload), headers=headers).json()
        #Debug response
        print("-----------response-----------")
        pprint.pprint(response)
        session_status = response['result'][0]['status']['message']       
        logger.info("STATUS: Promotion of " + hostname + " : " + session_status)
# Now to move to the right ADOM
# Moving -------------------
        run_ID += 1
        payload = {
            "id": run_ID,
            "session": session_ID,
            "method":"add",
            "params": [ {
                "url": "/dvmdb/adom/" + destination_adom + "/object member",
                "data": {
                    "name": hostname,
                    "vdom": "root"
                   }
            } ]
        }
        #Debug payload
        print("-----------request-----------")
        pprint.pprint(payload)
        response = requests.post(url, data=json.dumps(payload), headers=headers).json()
        #Debug response
        print("-----------response-----------")
        pprint.pprint(response)
        session_status = response['result'][0]['status']['message']       
        logger.info("STATUS: Moved: " + hostname + " : " + session_status)
#
# --------------------------------------------------
# --------------START BELOW-------------------------
# --------------------------------------------------
#
# Retrieve credentials and target from file
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
list_of_adoms = list()
#
#
login()
get_adom_list()
get_adom_membership()
destination_adom_move()
logout()


