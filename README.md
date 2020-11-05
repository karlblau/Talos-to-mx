# Talos-to-mx
This Python3 code fetches the IP Blacklist from Talos and updates an Meraki MX device using the Meraki dashboard API

# Prerequisites for the code is :
Meraki Dashboard API key

And the following Python Librarys :
types
requests
re
meraki

(Meraki python Library can be found here on Github)

# Runtime:
Before launch.
1. Edit the API_KEY and network_id variables.
API_KEY = "REPLACE WITH YOUR DASHBOARD APIKEY"
network_id = "REPLACE WITH THE NETWORK ID YOU WISH TO UPDATE THE RULES ON"

The script will fetch current L3 Firewall rules, search the rule-set for any rule with the keyword "Default" or "Talos" in the comment field.
If it detects any of these words in the comment it will NOT add that specific rule to the update rule-set, preventing having multiple Default or Talos Rules. 
It will then connect to Talos and download the the blacklist. Add a new rule with the blacklist ip(s) to the rule-set and then update the Dashboard API with the rule-set.

# Note:
1. The Talos Blacklist is "LONG", at writing rougly 800 /32 prefixes, this creates a werry long rule in the dashboard GUI
2. During the implementation i found out the hardway that Talos are enforcing a ratelimiting with source ban if you request the blacklist to offen, Dont run this script more then one's an every hour. 

