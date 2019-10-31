#!/usr/bin/python3
import os
try: #python3
    from urllib.request import urlopen
except: #python2
    from urllib2 import urlopen
import json
import tarfile
import docker
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Init authentication')
    #customer-X
    parser.add_argument('-u', type=str, help='You must provide a userId')
    #password-X
    parser.add_argument('-p', type=str, help='You must fill in a String')
    #dir-name
    parser.add_argument('--d', type=str, help='Provide the client directory name', default='client-input-dir')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    if args.u is None or args.p is None:
        exit(0)
    client = docker.from_env()
    fp = urlopen("http://localhost:5000/customer?id="+str(args.u)+"&password="+str(args.p))
    encodedContent = fp.read()
    decodedContent = encodedContent.decode("utf8")
    if decodedContent == "\"Wrong id and/or password\"\n":
        print("[WARNING] Wrong id and/or password")
    else:
        jsonContent = json.loads(decodedContent)
        nb_file_ingested = 0
        client_directory = os.getcwd()+"/"+args.d
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
            # Upload on the server
            os.system("docker cp " + os.path.join(client_directory, file) + " server:/app/"+str(args.u)+"/data/"+file)
            print("The file %s was uploaded successfully" %(file))
            nb_file_ingested += 1
    fp.close()
