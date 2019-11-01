#!/usr/bin/python3

import time
import os
import logging
import subprocess
import argparse

logging.basicConfig(filename='../server/stream_logs.log',
                        level=logging.DEBUG,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

def stop_stream_watcher(prog_pid):
    logging.info("Stopping process %s" %(str(prog_pid)))
    pro_to_kill = int(prog_pid)
    ret_val = subprocess.call(["kill", "-9", "%d" % pro_to_kill])
    if ret_val == 0:
        logging.info("Successfully killed process %s" %(str(prog_pid)))
    else:
        logging.error("Error in stopping process %s - Action not achieve" %(str(prog_pid)))
    return ret_val

def start_stream_watcher(customer):
    script_file = "./"+str(customer)+"/clientstreamingestapp.py"
    launched_proc = subprocess.Popen("python", 100, script_file)
    if launched_proc < 0:
        logging.error("Error in launching stream watcher for %s - Action not achieve" %(str(customer)))
    else:
        logging.info("Successfully launched stream watcher for %s - Process id %s" %(str(customer), str(prog_pid)))
    return launched_proc

# def parse_arguments():
#     parser = argparse.ArgumentParser(description='Init authentication')
#     #customer-X
#     parser.add_argument('-cust', type=str, help='You must provide a customer')
#     #action
#     parser.add_argument('-action', type=str, help='You must provide an action to perform [start or stop]')
#     #action
#     parser.add_argument('--pid', type=str, help='In case you want to stop a watcher - You must provide his id', default=0)
#     return parser.parse_args()

def validate_command(customer, action, proc_id):
    if action not in ["start", "stop"]:
        logging.error("The action asked is unvalid")
        return 1
    if action == "stop":
        try:
            int(proc_id)
        except:
            logging.error("The Process ID is not an integer")
            return 1
        if int(proc_id) < 1:
            logging.error("Wrong Process ID")
            return 1
    if not os.path.exists("/app/"+customer+"/"):
        logging.error("Customer does not exists")
        return 1
    return 0

#if __name__ == "__main__": #change to a function
def run_manager(customer, action, proc_id=0):
    # args = parse_arguments()
    # if args.cust is None:
    #     logging.debug("Customer unspecified when launching ingestmessagestructure")
    #     exit(1)
    # if args.action is None:
    #     logging.debug("User unspecified when launching ingestmessagestructure")
    #     exit(1)
    validation = validate_command(customer, action, proc_id)
    if validation == 1:
        logging.error("Unable to manage the command")
        exit(1)
    logging.info("Command validated. Command processing...")
    if action == "start":
        return start_stream_watcher(customer)
    else:
        return stop_stream_watcher(proc_id)