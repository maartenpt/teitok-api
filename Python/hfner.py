import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import argparse
import os, sys, requests, json
import lxml.etree as etree

argParser = argparse.ArgumentParser()
argParser.add_argument("-v", "--verbose", help="verbose mode", action='store_true')
argParser.add_argument("-m", "--model", help="ner model", required=True)
args, moreargs = argParser.parse_known_args()


# Load the configuration settings
dir = os.path.dirname(sys.argv[0])
sys.path.append(dir)
import apistart
apiurl = apistart.apiurl + "?action=api"
token = apistart.token

print("Using TEITOK project: " + apiurl)

print("Using NER model: " + args.model)

# Load the pretrained tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(args.model)
model = AutoModelForTokenClassification.from_pretrained(args.model)

ner = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="first")

listurl = apiurl + "&act=list&status=noner&token="+token
        
        
# Get the list of all the files on the server
response = requests.get(listurl) # Upload the file
try:
    list = response.json()
except:
    print('Error in request: ' + response.text)
    exit()
  
if "error" in list.keys():
    print('Error in request: ' + response.text)
    print (listurl)    
    exit()

def findpos(list,elm):
    if elm in list:
        index = list.index(elm) 
    else:
        index = 0
        while list[index] < elm:
            index = index + 1
    return index

def getform(node):
    if "form" in node.attrib:
        return node.attrib["form"]
    return ''.join(node.itertext())


for xmlfile in list["files"]:

    # create an empty dictionary to store the NER we encounter
    output = { "name": [] }
    namelist = output['name']
    
    if args.verbose:
        print ("parsing " + input_file)
    response = requests.get( apiurl + "&act=download&cid="+xmlfile+"&token="+token)
    xmlf = etree.fromstring(response.text.encode('utf-8'))
    
    # Check if this need to be NER'ed
    if xmlf.find(".//text//name") is not None:
        print("already NER'ed")
        continue
        
    # Go through each text slice in the XML to process the NER
    for slice in xmlf.findall(".//text//p"):

        toklist = slice.findall(".//tok")
        tokens = []
        dtoklist = []
        for tok in toklist:
            if tok.find("dtok") is not None:
                for dtok in tok.findall("dtok"):
                    tokens.append(getform(dtok))
                    dtoklist.append(dtok)
            else:
                tokens.append(getform(tok))
                dtoklist.append(tok)
        i=0
        tokpos = [0]
        for word in tokens:
            i=i+len(word)+1
            tokpos.append(i)
        raw_input = ' '.join(tokens)
        results = ner(raw_input)

        j=0
        for result in results:
          j = j + 1
          if args.verbose:
                print(result)
          start = result["start"]
          end = result["start"]+len(result["word"].replace("##", ""))
          tag = result["entity_group"]
      
          pos1 = findpos(tokpos, start)
          pos2 = findpos(tokpos, end+1)
          tok1 = dtoklist[pos1]
          corresp = []
          for i in range(pos1, pos2):
              corresp.append(dtoklist[i].attrib["id"])
          newname = {"sameAs": "#" + ' #'.join(corresp), "form": result["word"], "type": result["entity_group"], "cert": str(result["score"]) }
          namelist.append(newname)
            
    tagf = "ner.json"
    with open(tagf, 'w') as f: f.write(json.dumps(output, indent = 4))
    cmd = "curl -F 'infile=@"+tagf+"' '"+apiurl+"&act=annotate&format=json&token="+token+"&cid="+xmlfile+"'"
    print(cmd)
    os.system(cmd)
        