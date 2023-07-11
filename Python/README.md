# Python scripts

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
The script should be easy to adept to any parser that uses CoNLL-U as both input and output format. 

## HFNER

hfner.phy is a script to run NER on TEITOK documents with any transformer model from HuggingFace.
It will downloads all files from a given project in CoNLL-U format, and then
run the NER on that file (if it does not already contain names), with the specified model. 
For this to work, the files should have been previously tokenized. Once the
file has been ner'd, the annotated file 
will be uploaded back to the project, where the annotations will be loaded into the orginal TEITOK/XML file.  
