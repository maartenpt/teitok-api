# TEITOK API Scripts

In this repository, we collect useful scripts to interact with TEITOK corpora using the TEITOK API. We attempt to provide some script in all popular programming languages, that can either be used directly or serve as inspiration to perform similar tasks. We invite people to contribute any scripts they develop themselves so that more and more scripts can become available.

## Structure

The general set-up of the scripts is that they are self-contained, minus the URL of the project you are working 
with, and the authorization token. The apistart script reads those from a config.ini file. 
The intended set-up is to run the script from a folder dedicated to the project, where the config.ini
will be stored, as well as any files written by the scripts.