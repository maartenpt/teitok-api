import argparse
import os
import re
import requests

# Default header to get the URL and token for the project
argParser = argparse.ArgumentParser()
argParser.add_argument("-t", "--token", help="Authorization token")
argParser.add_argument("-u", "--url", help="TEITOK corpus project URL")
argParser.add_argument("-d", "--settings", help="Settings file")
argParser.add_argument("-c", "--corpus", help="Corpus ID")
argParser.add_argument("-s", "--silent", help="silent mode", action='store_true')
# args = argParser.parse_args()
args, moreargs = argParser.parse_known_args()

curdir = os.path.basename(os.getcwd())
inifile = args.settings or "./config.ini"

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


apiurl = args.url
if not apiurl and corpus in config.keys() and "url" in config[corpus].keys():
    apiurl = config[corpus]["url"]
token = args.token 
if not token and corpus in config.keys() and "token" in config[corpus].keys():
    token = config[corpus]["token"]

if not apiurl:
    print("Please provide the URL of a TEITOK API endpoint")
    exit()

# Authenticate where needed
cookies = {}
if "username" in config[corpus].keys():
	username = config[corpus]['username']
	if "password" not in config[corpus].keys():
		print("Please type in your password for " + apiurl)
		password = input().strip()
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
