def generate_test_firewalls():
    global url,headers,session_ID,run_ID,host_in_adom,target_adom
    proceed = input("Do you want to generate test firewalls in the root domain?(y/n)")
    if proceed == "n":
        return
    num_firewalls = int(input("How many?"))
    target_adom = str(input("For which adom?"))
    #generate firewall list
    test_firewall_list = []
    for num in range(num_firewalls):
        test_firewall_list.append("FG50-API-TEST" + str(num + 1) + "-" + target_adom)
    for test_firewall in test_firewall_list:
        print(test_firewall)

generate_test_firewalls()