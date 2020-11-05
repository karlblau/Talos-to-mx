# Talos-to-mx
This Python3 code fetches the IP Blacklist from Talos and updates an Meraki MX device using the Meraki dashboard API

# Prerequisites for the code is :
Meraki Dashboard API key

And the following Python Librarys :
types
requests
re
meraki

# Note:
Dont run this script more then one's an every hour. 
During the implementation i found out the hardway that Talos are enforcing a ratelimiting with source ban if you request the blacklist to offen.
