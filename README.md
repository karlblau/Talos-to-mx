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

API_KEY = "REPLACE WITH YOUR DASHBOARD APIKEY"
network_id = "REPLACE WITH THE NETWORK ID YOU WISH TO UPDATE THE RULES ON"

The script will fetch current L3 Firewall rules, connect to Talos and download the the blacklist. Add a new rule with the blacklist and then update the Dashboard API wth the new rule(s).


# Note:
1. The Talos Blacklist is "LONG", at writing rougly 800 /32 prefixes, this creates a werry long rule in the dashboard GUI
2. During the implementation i found out the hardway that Talos are enforcing a ratelimiting with source ban if you request the blacklist to offen, Dont run this script more then one's an every hour. 

