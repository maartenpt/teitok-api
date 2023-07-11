import requests, json, os, sys
from pathlib import Path
import classla
import sys, argparse

# Load the configuration settings
dir = os.path.dirname(sys.argv[0])
sys.path.append(dir)
import apistart
apiurl = apistart.apiurl + "?action=api"
token = apistart.token

argParser = argparse.ArgumentParser()
argParser.add_argument("-m", "--model", help="CLASSLA model", default="mk")
args, moreargs = argParser.parse_known_args()


model = args.model

print("Using TEITOK project: " + apiurl)
print("Using model: " + model)

classla.download("mk")
nlp = classla.Pipeline(lang='mk', tokenize_pretokenized='conllu')

# The URL to use to upload an RTF file
listurl = apiurl + "&act=list&token="+token

response = requests.get(listurl) # Upload the file
try:
    data = response.json()
except:
    print("Invalid response: " + response.text)
    exit()
    
filecnt = len(data["files"])
print(str(filecnt) + " files to treat")
i = 0

for file in data["files"]:
    i = i = 1
    file = file.split("/")[-1]
    print(str(i) + ": " + file)
    conf = file.replace('.xml', '.conllu')
    tagf = file.replace('.xml', '-tagged.conllu')
    resp = requests.get(apiurl+"&act=download&format=conllu&token="+token+"&cid="+file)
    conllu_pretokenized = resp.text
    if conllu_pretokenized.strip() == "":
        print("no CoNLL-U result rendered")
    else:
        doc = nlp(conllu_pretokenized)
        with open(tagf, 'w') as f: f.write(doc.to_conll())
        cmd = "curl -F 'infile=@"+tagf+"' '"+apiurl+"&act=annotate&format=conllu&token="+token+"&cid="+file+"'"
        os.system(cmd)
