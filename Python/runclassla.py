import requests, json, os, sys
from pathlib import Path
import classla
import sys, argparse

# Load the configuration settings
dir = os.path.dirname(sys.argv[0])
sys.path.append(dir)
import apistart
apiurl = apistart.apiurl + "?action=api"

argParser = argparse.ArgumentParser()
argParser.add_argument("-m", "--model", help="CLASSLA model", default="mk")
args, moreargs = argParser.parse_known_args()

model = args.model

print("Using TEITOK project: " + apiurl)
print("Using model: " + model)

classla.download("mk")
nlp = classla.Pipeline(lang='mk', tokenize_pretokenized='conllu')

# The URL to use to upload an RTF file
listurl = apiurl + "&act=list"

response = requests.get(listurl, cookies=apistart.cookies) # Upload the file
try:
    data = response.json()
except:
    print("Invalid response: " + response.text)
    exit()
    
filecnt = len(data["files"])
print(str(filecnt) + " files to treat")
i = 0

for file in data["files"]:
    i = i + 1
    file = file.split("/")[-1]
    print(str(i) + ": " + file)
    conf = file.replace('.xml', '.conllu')
    tagf = file.replace('.xml', '-tagged.conllu')
    resp = requests.get(apiurl+"&act=download&format=conllu&cid="+file, cookies=apistart.cookies)
    conllu_pretokenized = resp.text
    if conllu_pretokenized.strip() == "":
        print("no CoNLL-U result rendered (not tokenized?)")
    else:
        doc = nlp(conllu_pretokenized)
        with open(tagf, 'w') as f: f.write(doc.to_conll())
        files = {'infile': open(tagf, 'rb')}
        upload_url = apiurl+"&act=annotate&format=conllu&cid="+file
        response = requests.post(upload_url, cookies=apistart.cookies, files=files) # Upload the file
        print(response.text)
