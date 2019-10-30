#!/usr/bin/env python3
import os
try: #python3
    from urllib.request import urlopen
except: #python2
    from urllib2 import urlopen
import json

fp = urlopen("http://localhost:5000/customer/customer-1")

encodedContent = fp.read()
decodedContent = encodedContent.decode("utf8")

print(decodedContent)
jsonContent = json.loads(decodedContent)

nb_file_ingested = 0
client_directory = os.getcwd()+"/client-input-dir"

for file in os.listdir(client_directory):
    if nb_file_ingested >= jsonContent["number_files"]:
        print("The maximum number of files on the server is reached")
        break
    extension = os.path.splitext(file)[1]
    if not extension in jsonContent["formats"]:
        print("The extension of the file %s is not allowed" %(file))
        continue
    file_size = os.path.getsize(os.path.join(client_directory, file)) / 1024
    if file_size > jsonContent["data_sizes"]:
        print("The file %s is bigger than your maximum authorized size of %s KB" %(file, jsonContent["data_sizes"]))
        continue
    print("TODO envoyer file")


fp.close()
