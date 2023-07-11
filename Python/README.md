# Python scripts

## BACKUP

backup.py is a script that makes a local backup of all the files in a given project. Each backup will only 
download the files that have been added or modified since the last backup, and existing local files will be overwritten.
The project URL and the authorization token for that project should be stored in a file config.ini in the folder where 
the script is run from, and the timestamp of the last backup is kept in a file lastbu.txt in that same folder, which is to 
determine which files were modified since that date. Files are downloaded in their unmodified TEITOK/XML format, with the
file structure mimicking that on the server.
 

## CLASSLA

classla.py is a script that downloads all thusfar untagged files from a given project in CoNLL-U format, and the
runs the CLASSLA tagger on that file, with the specified language (with Macedonian being the default). 
For this, the files should have been previously tokenized. Once the
file has been tagged (and parsed where available), the annotated file 
will be uploaded back to the project, where the annotations will be loaded into the orginal TEITOK/XML file.   