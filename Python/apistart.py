import argparse
import os
import re
import requests
from getpass import getpass

# Default header to get the URL and token for the project
argParser = argparse.ArgumentParser()
argParser.add_argument("-t", "--token", help="Authorization token")
argParser.add_argument("-u", "--url", help="TEITOK corpus project URL")
argParser.add_argument("--settings", help="Settings file")
argParser.add_argument("-c", "--corpus", help="Corpus ID")
argParser.add_argument("-s", "--silent", help="silent mode", action='store_true')
argParser.add_argument("--user", help="TEITOK username")
argParser.add_argument("--password", help="TEITOK password")
args, moreargs = argParser.parse_known_args()

curdir = os.path.basename(os.getcwd())
inifile = args.settings or "./config.ini"

# The default corpus is [DEFAULT]
corpus = args.corpus or "DEFAULT"

# Emulate configparse
config = {}
if os.path.exists(inifile):
    sts = "DEFAULT"
    config[sts] = {}
    with open(inifile, "r") as file:
        for line in file:
            line = line.strip()
            m1 = re.match(r"^\[(.*)\]$", line)
            m2 = re.match(r"^(.*?) = (.*)$", line)
            if m1:
                sts = m1.group(1)
                if not sts in config.keys():
                    config[sts] = {}
            elif m2:
                config[sts][m2.group(1)] = m2.group(2)


# Establish the URL of the TEITOK endpoint
apiurl = args.url
if not apiurl and corpus in config.keys() and "url" in config[corpus].keys():
    apiurl = config[corpus]["url"]
token = args.token 
if not token and corpus in config.keys() and "token" in config[corpus].keys():
    token = config[corpus]["token"]
if not apiurl:
    print("Please provide the URL of a TEITOK API endpoint")
    exit()
if apiurl[-9:] != "index.php":
	if apiurl[-1] != '/':
		apiurl = apiurl + '/'
	apiurl = apiurl + 'index.php'


# Authenticate where needed
cookies = {}
username = ""
password = ""
if token:
	auth_url = f'{apiurl}?action=api&act=login'
	auth_payload = {'token': token}
	response = requests.post(auth_url, data=auth_payload)
	if "sessionId" in response.json().keys():
		access_token = response.json()['sessionId'];
	else:
		print("login failed: " + response.text)
		access_token = ""
	cookies = {'PHPSESSID': access_token}
elif args.user or ( corpus in config.keys() and "username" in config[corpus].keys() ):
	if args.user:
		username = args.user
		if not args.password:
			password = getpass("Please provide a password > ").strip()
		else:
			password = args.password
	else:
		username = config[corpus]['username']
		if "password" not in config[corpus].keys():
			password = getpass("Please provide a password > ").strip()
		else:
			password = config[corpus]['password']
	auth_url = f'{apiurl}?action=api&act=login'
	auth_payload = {'user': username, 'pw': password}
	response = requests.post(auth_url, data=auth_payload)
	if "sessionId" in response.json().keys():
		access_token = response.json()['sessionId'];
	else:
		print("login failed: " + response.text)
		access_token = ""
	cookies = {'PHPSESSID': access_token}
