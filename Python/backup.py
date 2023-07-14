import glob, os, requests, sys, re
from pathlib import Path
from datetime import datetime
import urllib.parse

# Load the configuration settings
dir = os.path.dirname(sys.argv[0])
sys.path.append(dir)
import apistart
apiurl = apistart.apiurl + "?action=api"
token = apistart.token

print("Using TEITOK project: " + apiurl)

if not "PHPSESSID" in apistart.cookies.keys():
	print("Please provide correct credentials")
	exit()

# The URL to use to upload an RTF file
listurl = apiurl + "&act=list"

if os.path.exists("lastbu.txt"):
    with open("lastbu.txt", "r") as file:
         last = file.read().strip()
    print(" - backing up new files since " + last)
    listurl = listurl + "&since=" + urllib.parse.quote_plus(last)
        
# Get the list of all the files on the server
response = requests.get(listurl, cookies=apistart.cookies) # Upload the file
try:
    list = response.json()
except:
    print('Error in request: ' + response.text)
    exit()
  
if "error" in list.keys():
    print('Error in request: ' + response.text)
    print (listurl)	
    exit()
    
for filename in list['files']:
    print(filename)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    response = requests.get( apiurl + "&act=download&cid="+filename, cookies=apistart.cookies)
    with open(filename, "w") as f:
        f.write(response.text)    
        
with open("lastbu.txt", "w") as f:
	f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))    
