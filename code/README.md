# This directory is about the code.
>Note: we must be able to compile and/or run the code. No BINARY files are within the code. External libraries should be automatically downloaded (e.g., via Maven, npm, pip, docker pull)

## Prerequisites

You need Python installed in your machine,
then run ```pip install -r requirements.txt```

## Run Servers

Run ```docker pull cassandra``` to download the official Cassandra image

In the file ```docker-compose.yaml``` change the volumes location in order to match with your local machine
```
    volumes:
      - /home/clement/WKS/AALTO/BigData/assignment-1-784795/data/cassandra/node1
```
```/home/clement/WKS/AALTO/BigData``` have to be changed


Then run ```docker-compose up -d``` to run the cassandra server in detached mode
