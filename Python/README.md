# Python scripts

This folder provides a collection of Python scripts to interact with the TEITOK API. They have not been extensively tested
and might contain occassional bugs or uncaught errors.

The Python scripts provided by the TEITOK team all use the apistart.py script to connect to the TEITOK corpus (although
scripts provided by contributors might not). The set-up provides the option to either use an authentication token (which 
can be generated via the GUI), or use the TEITOK login and password. Both can be given either as an argument, or stored in 
a config.ini file. The intended use is to run the script from a folder containing congif.ini file, and the script will use that 
folder for any files stored in the process. So we should for instance create a file `/home/mine/myproject/config.ini` containing 
the TEITOK project endpoint and the authorization data:

```
[DEFAULT]
url = http://myserver.com/teitok/myproject/index.php
username = me@mydomain.com
password = my_password
```

And then we can simply run the scripts from the folder where that config.ini is stored, so to backup just run:

``
cd /home/mine/myproject ; python /home/git/teitok-api/Python/backup.py
``

But it is also possible to define multiple corpora and indicate the corpus you want to use (``--corpus corpusid``), provide
a token instead of a username and password, provide the token (``--token token``) as an argument, or the username 
as an argument (``--user userid``) which will ask for the password when running the script. Upon login, apistart.py creates
a cookie, which should then be sent along with each subsequent request.

## BACKUP

backup.py is a script that makes a local backup of all the files in a given project. Each backup will only 
download the files that have been added or modified since the last backup, and existing local files will be overwritten.
The project URL and the authorization token for that project should be stored in a file config.ini in the folder where 
the script is run from, and the timestamp of the last backup is kept in a file lastbu.txt in that same folder, which is to 
determine which files were modified since that date. Files are downloaded in their unmodified TEITOK/XML format, with the
file structure mimicking that on the server.
 

## RUNCLASSLA

classla.py is a script to tag/parse TEITOK documents with the [CLASSLA](https://pypi.org/project/classla/) spinoff of Stanza.
It will downloads all thusfar untagged files from a given project in CoNLL-U format, and then
run the CLASSLA tagger on that file, with the specified model (language, with Macedonian being the default). 
For this to work, the files should have been previously tokenized. Once the
file has been tagged (and parsed where available), the annotated file 
will be uploaded back to the project, where the annotations will be loaded into the orginal TEITOK/XML file.  
The script should be easy to adept to any parser that can use CoNLL-U as both input and output format, or forced into doing so. 

## HFNER

hfner.phy is a script to run NER on TEITOK documents with any transformer model from HuggingFace.
It will downloads all files from a given project in CoNLL-U format, and then
run the NER on that file (if it does not already contain names), with the specified model. 
For this to work, the files should have been previously tokenized. Once the
file has been ner'd, the annotated file 
will be uploaded back to the project, where the annotations will be loaded into the orginal TEITOK/XML file.  

## TRANSKR2TEITOK

transkr2teitok.py is a script to create TEITOK documents out of Transkribus collections. It downloads the indicated file(s)
from the Transkribus API, and then uploads the results to the TEITOK corpus. The Transkribus login data should be provided in 
a [transkribus] section in the config.ini file.
