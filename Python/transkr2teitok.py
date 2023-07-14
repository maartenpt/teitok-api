import glob, os, requests, sys, re, argparse, json
from pathlib import Path
from datetime import datetime
import urllib.parse
import lxml.etree as etree

# Load the configuration settings
dir = os.path.dirname(sys.argv[0])
sys.path.append(dir)
import apistart
apiurl = apistart.apiurl + "?action=api"
token = apistart.token

argParser = argparse.ArgumentParser()
argParser.add_argument("--collection", help="Collection ID", type=int)
argParser.add_argument("--document", help="Document ID", type=int)
argParser.add_argument("-s", "--server", help="Transkribus server", default="https://transkribus.eu/TrpServer/rest")
args, moreargs = argParser.parse_known_args()

baseurl = args.server

print("Using TEITOK project: " + apiurl)

username = apistart.config["transkribus"]['username']
password = apistart.config["transkribus"]['password']


# Authenticate and obtain an access token
auth_url = f'{baseurl}/auth/login'
auth_payload = {'user': username, 'pw': password}
response = requests.post(auth_url, data=auth_payload)
authx = etree.fromstring(response.text.encode('utf-8'))
access_token = authx.find(".//sessionId").text

# Set the authorization header for subsequent requests
trcookies = {'JSESSIONID': access_token}
cookies = apistart.cookies

# Create the output folder if it doesn't exist
os.makedirs("Originals", exist_ok=True)
os.makedirs("Facsimile", exist_ok=True)
os.makedirs("PageXML", exist_ok=True)

if not args.collection:
	coll_url = f'{baseurl}/collections/list'
	response = requests.get(coll_url, cookies=trcookies)  # , data={'JSESSIONID': access_token}
	collist = response.json()

	print("Choose a collection:")
	for collection in collist:
		print(f'{collection["colId"]}: {collection["colName"]}')
	exit()

collection_id = args.collection

docs_url = f'{baseurl}/collections/{collection_id}/list'
response = requests.get(docs_url, cookies=trcookies)  # , data={'JSESSIONID': access_token}
doclist = response.json()

docid = False
if args.document:
	docid = args.document
else:
	print("Choose a document (or 'all'):")

# Parse each document in the collection (unless a docId is provided)
for doce in doclist:
	doctit = doce['title'].replace(" ", "_")
	document_id = doce["docId"]
	
	# Skip this document if we are not asked to process it, or print out the choice
	if docid:
		if docid != document_id and docid != "all":
			continue
	else:
		print(f'-{document_id}: {doctit}' )
		continue
	
	print(f'Document: {doctit} ({document_id})' )

	# Get a list of pages for the document
	pages_url = f'{baseurl}/collections/{collection_id}/{document_id}/fulldoc'
	response = requests.get(pages_url, cookies=trcookies)
	pagelist = response.json()
	pages = pagelist['pageList']['pages']
	
	# Create a single PageXML file for the document
	docxml = etree.Element('PcGts')
	tree = etree.ElementTree(docxml)	
	
	# Download each page
	for page in pages:
		page_id = page['pageId']
		img_file = page['imgFileName']
		print(" - Page: " + str(page['pageNr']) + " ("+img_file+")")
		img_url = page['url']
		img_data = requests.get(img_url).content
		with open("Facsimile/" + img_file, 'wb') as handler:
			handler.write(img_data)
		# Upload the image
		upload_url = f'{apiurl}&act=upload&format=facsimile'
		files = {'infile': open("Facsimile/" + img_file, 'rb')}
		response = requests.post(upload_url, cookies=cookies, files=files) # Upload the file
		if "error" in response.json().keys():
			print ("Failed to upload image: " + response.text)
		latest = 0
		xml_data = ""
		# Download the most recent transcription of the page
		for trans in page['tsList']['transcripts']:
			ts = int(trans['timestamp'])
			if ts > latest:
				latest = ts
				xml_file = trans['fileName']
				print (" + Transcript: " + xml_file)
				xml_url = trans['url']
				xml_data = requests.get(xml_url).content
				with open("Originals/" + xml_file, 'wb') as handler:
					handler.write(xml_data)

		# Add the transcription to the full PageXML
		if xml_data != "" :
			xml_data = xml_data.decode().replace("xmlns:xsi", "xmlns_xsi").replace("xmlns", "xmlnsoff").replace("xsi:", "xsi_").encode("UTF-8")
			pagexml = etree.fromstring(xml_data)
			pagepage = pagexml.find(".//Page")
			pagepage.set("imageFilename", img_file)
			docxml.append(pagepage)

	tree.write("PageXML/"+doctit+'.xml', encoding="UTF-8")	
	
	# Upload the PageXML file
	upload_url = f'{apiurl}&act=upload&format=pagexml'
	files = {'infile': open("PageXML/"+doctit+'.xml', 'rb')}
	response = requests.post(upload_url, cookies=cookies, files=files) # Upload the file
	if "error" in response.json().keys():
		print ("Failed to PageXML file: " + response.text)
	
	# Set the source URL in the teiheader
	change_url = f'{apiurl}&act=metadata&cid={doctit}'
	sourceurl = doce['url']
	newdata = { '/TEI/teiHeader/profileDesc/sourceurl': pages_url }
	newheader = {'data': json.dumps(newdata)}
	response = requests.post(change_url, cookies=cookies, params=newheader) # Upload the file
	print (response.text)