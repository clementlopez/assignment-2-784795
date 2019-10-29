# Part 1 : Ingestion with batch

## Q1) Constraints into configuration file

I choose to use a JSON file in order to group the configuration constraints.
Formats lists all file formats allowed for upload.
Number_files and data_sizes are there for respectively the total number of files allowed for the user and the maximum size for a file.

---json
{
    "formats":[".csv"],
    "number_files":5,
    "data_sizes":64
}
---

And I have separated the constraints for files and information from the user profiles.
The customer id and password are there to allow client authentification.
Actual_counter is the current counter of the client's file number.

---json
{
    "customer_id":"name",
    "customer_password": "pass",
    "actual_counter":0
}
---