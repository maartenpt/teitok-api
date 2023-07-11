import argparse
import os
import re

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
    print("Please provide an API URL")
    exit()
