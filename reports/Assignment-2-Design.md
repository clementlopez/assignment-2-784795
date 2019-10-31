# Part 1 : Batch Ingestion

This part has following components:

* mysimbdp-fetchdata
* Batchingest_manager
* Client_batchingestapp

The batch ingestion copies the files into Mysimbdp and enters the data from the files into the database.

## Architecture

The architecture of this part is composed of 3 pieces:
* A part specific to each user (local), which we will basically call Local for the rest of the report
* A first server on which the client files will be sent, which we will basically call Server for the rest of the report
* A second server, a Cassandra server, which is the database in which the data will be stored, which we will basically call Cassandra for the rest of the report

## FetchData

The role of this component is to move the data from the client-input-directory to staging destination.
I have chosen to consider that the client-input-directory is local on the client's machine.
The fetchdata script is given to each customer to be executed as soon as the customer wants it.
It is therefore generic and is the same for all customers.

When the customer wants to run it, he have to provide his username, his password and optionaly the name of the directory from which he wants to send the files (by default it is ```client-input-dir```) :
```python3 ./fetchdata.py -u <USERNAME> -p <PASSWORD> [-d <DIRECTORYNAME>]```

From there, the script sends a GET request to the Server to recover the informations of the client's file configuration constraints.
For every files in the client-input-directory the fetchdata component proceeds to check the client's configuration constraints.
As soon as a file validates the constraints it is sent to the server.

### Constraints into configuration file

I choose to use a JSON file in order to group the configuration constraints.
* Formats lists all file formats allowed for upload.
* Number_files is the total number of files allowed per upload. I was first thinking of making it the maximum number of files on the server for a given client. But my dataingestmanager script allows us to send in database the data of a file as soon as the file is uploaded on the Server.
* Data_sizes is for the maximum size for a file.

An example code of a configuration constraints file is :

```json
{
    "formats":[".csv"],
    "number_files":10,
    "data_sizes":4096
}
```

### Users authentification

For client authentication, I just have a json file on my Server that is checked each time a GET request is sent.
The password is encrypted on the Server.
For the moment I have configured my Server for 2 clients:
```customer-1 password-1```
```customer-2 password-2```

My users.json file is:
---json
{
    "customer-1":"97d0eed887efa9702fcba83a64ace149ea7923227a8649cbb01dc825f09118c8e0f95c5a4a496dd30d35554ef3984c697d3f7541d517e6c6c642189a23b21accfb8b5e7aa6b4b12f6e824ddca05818ff82c4df4799e083ff1a4d7957743070f8",
    "customer-2":"aa9e53cc66ff8252bb6d29a5829bc83802f320169c25170660537c55aedb8047ae0197077815317a1cb0af21149173f4293575332da4e3d12680d9c3e3f1d2a9f88cee90cda580be1221ba73ca18a2ab7d4f4558d08532c4b5cbff21a7471797"
}
---

## Batch Ingest Manager & ClientBatchingestapp

The batch ingest manager is responsible for calling/running the client's script whenever a file of that customer is upload into the Server.
To do this, I used the watchdog library of python which allows to create Observer that I activate as soon as a file to be inserted is uploaded on the Server.
Depending on the directory in which the file is uploaded (so depending on the client that has uploaded the file) it calls the corresponding dataingestclient script that was given by the client when creating his account (which was not processed in the implementation of this assignment but which is one of the first things I would like to implement in addition on this Server).

Each dataingestclient connects to Cassandra and uses the customer's own Keyspace.
Dataingestmanager allows us to collect logs on the speed of execution of the request as well as other information (size of the file, number of lines, the client concerned...).

Logs follow this structure :
```log

2019-10-31 15:16:22 - Ingestion of the file: Data1000lines.csv for customer-1 - size: 128.7978515625 KB - 999 lines ingested in 0.8234226703643799 seconds
2019-10-31 15:16:23 - Ingestion of the file: Data1000lines2.csv for customer-1 - size: 124.744140625 KB - 1000 lines ingested in 1.0246901512145996 seconds
2019-10-31 15:16:24 - Ingestion of the file: Data1000linesae.csv for customer-1 - size: 118.5966796875 KB - 1000 lines ingested in 0.8117904663085938 seconds
2019-10-31 15:16:25 - Ingestion of the file: Data1000linesai.csv for customer-1 - size: 111.1611328125 KB - 1000 lines ingested in 0.7847237586975098 seconds
2019-10-31 15:18:00 - Ingestion of the file: Data1000linesaf.csv for customer-2 - size: 112.677734375 KB - 1000 lines ingested in 1.019026517868042 seconds
2019-10-31 15:18:01 - Ingestion of the file: Data1000linesaj.csv for customer-2 - size: 111.49609375 KB - 1000 lines ingested in 0.9374134540557861 seconds
2019-10-31 15:18:02 - Ingestion of the file: Data1000linesak.csv for customer-2 - size: 91.70703125 KB - 841 lines ingested in 0.6262474060058594 seconds

```

For now, all ```dataingestclient``` have to be written in python, however, in the future my ```dataingestmanager``` has to allow any language code for it.





