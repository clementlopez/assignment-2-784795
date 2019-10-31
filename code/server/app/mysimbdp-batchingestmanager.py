#!/usr/bin/python3

import time
import os
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

def on_created(event):
    print(f"hey, {event.src_path} has been created!")
    path = event.src_path.split('/')
    if (len(path) == 4) and (path[0] == ".") and (path[2] == "data"):
        print("python ./{path[1]}/clientbatchingestapp.py ./data/{path[3]}")
    else:
        print("detection of a file creation that does not require a call to clientbatchingestapp")

if __name__ == "__main__":
    patterns = "*"
    ignore_patterns = None
    ignore_directories = True
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    my_event_handler.on_created = on_created
    path = "."
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)
    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
    my_observer.join()

