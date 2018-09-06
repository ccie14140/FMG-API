import requests
import json


def main():
    url = "http://10.2.1.5/jsonrpc"
    headers = {'content-type': 'application/json'}
    #api-user = raw_input("Enter API username: ")
    #api-pwd = raw_input("Enter the API user password: ")


    # API login
    payload = {
        "method":"exec",
        "params": [ {
            "url":"/sys/login/user",
            "data": {
                "user": "rlnadmin",
                "passwd":"RLNfmg2018ZZ!!"
            }
        } ],
        "id":1
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()
    session_track = response['session']
    print(response)
    print(session_track)
main()

