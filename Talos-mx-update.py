import types
import requests
import re
import meraki

#dashboard API stuff
API_KEY = "REPLACE WITH YOUT API KEY"
dashboard = meraki.DashboardAPI(API_KEY)
network_id = "REPLACE WITH YOUR NETWORK ID (INLUDING N_) EXAMPLE:N_XYZXYZXYZXYXYZ "


#create finalRule
uRule = []


#Get current rules
response = dashboard.appliance.getNetworkApplianceFirewallL3FirewallRules(
        network_id
        )
#move response to oldRules
oldRules = response

print("__________________________________")
print("Current number of Rules including default rule --> ")
print(len(oldRules['rules']))
print("._______________begin loop__________________")

#loop counter start at 0
inC = 0

#workaround, as list is 0-2 and not 1-3
toLength = len(oldRules['rules']) -1

#if these comments show up in old rules, dont add them to the update as Default rule is automaticly updated, and the Talos rule will be updated below.
key1 ="Talos"
key2 ="Default"

#loop over oldRules mote to uRule
while inC <= toLength:
    #print(oldRules['rules'][inC])

    #check if SD is in rule
    if key1 in oldRules['rules'][inC]['comment']:
        print("Found old Talos Rule, dont add this to the update")
    elif key2 in oldRules['rules'][inC]['comment']:
        print("Found old Dedaul Rule, dont add this to the update")
    else:
        #print("Inte hittat nån KEY lägger till regeln")
        
        #add to uRule
        uRule.append(oldRules['rules'][inC])
    
    #increase
    inC = inC +1


#-..-.-.-.-.-.-. 
#get data from Talos
#-.-.-.-.-.-.-.-.
print("-.-.-.- Get data from Talos -.-.-.-.-.")


#Blacklisturl
url ='https://www.talosintelligence.com/documents/ip-blacklist'

try:
    r = requests.get(url,timeout=3)
    r.raise_for_status()
except requests.exceptions.HTTPError as errh:
    print ("Http Error:",errh)
except requests.exceptions.ConnectionError as errc:
    print ("Error Connecting:",errc)
except requests.exceptions.Timeout as errt:
    print ("Timeout Error:",errt)
except requests.exceptions.RequestException as err:
    print ("OOps: Something Else",err)

#Check if we have talked to Talos
if r:
    print("Success,Conection ok to WEB service!")
    print("-------------------------------")

#make a List
    ipDlist = r.content

    #remove 2 ending charecthers
    ipDlist = ipDlist[:-2]

    #replace newline with comma
    fixList = str(ipDlist).replace('\\n', ',')

    #match for ip address and comma
    strax = (re.findall(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})",fixList))

    #join list to a String
    sep = ","
    ipToMx = (sep.join(strax))

    if not ipToMx:
        print("Fatal error! Data contained no ip addresses, dying")
        quit()
    else:
        #make rule, include ipToMx
        newR = {'comment': 'IP-BLACKLIST FROM Talos.', 'policy': 'deny', 'protocol': 'any', 'destPort': 'any', 'destCidr':  ipToMx , 'srcPort': 'Any', 'srcCidr': 'Any', 'syslogEnabled': True}
        
        #add extra rules
        uRule.append(newR)

        #printout
        print("------------------")
        print("Number of rules to update excluding default rule:",len(uRule))
        print("------------------")
        
        #update API with uRule
        response = dashboard.appliance.updateNetworkApplianceFirewallL3FirewallRules(
                network_id,rules=uRule
                )
        print("Rules updated to Meraki API")
        print("-----------------")
    
else:
    print("somethingswrong")
