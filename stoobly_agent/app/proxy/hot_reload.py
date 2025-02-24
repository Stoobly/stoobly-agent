import os
import time

from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

def current_working_directory():
    return os.path.dirname(os.path.realpath(__file__))

def trigger_reload(event):
    print('Hot reloading...')

    cwd = current_working_directory()
    Path(os.path.join(current_working_directory(), 'record.py')).touch()

cwd = current_working_directory()
lib_path = os.path.join(cwd, 'lib')

patterns = "*"
ignore_patterns = ""
ignore_directories = False
case_sensitive = True
event_handler = PatternMatchingEventHandler(
    patterns=patterns, 
    ignore_patterns=ignore_patterns, 
    ignore_directories=ignore_directories, 
    case_sensitive=case_sensitive
)

event_handler.on_modified = trigger_reload

observer = Observer()
observer.schedule(event_handler, lib_path, recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
finally:
    observer.stop()
    observer.join()
