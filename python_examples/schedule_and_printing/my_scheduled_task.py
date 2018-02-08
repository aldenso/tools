#!/usr/bin/env python
# description: Just a program to check some changes on a directory and schedule
# a task, while still running something else.
import os
import threading
from datetime import datetime
import time
import schedule
import inotify.adapters

TIMER = 5  # seconds

def print_changes(directory):
    print("Something has changed in {}!".format(directory))
    print("Will schedule a task every {} seconds".format(TIMER))
    schedule.every(TIMER).seconds.do(print_schedule, "I'm a scheduled task.")

def print_schedule(message):
    print(message)

def just_running():
    print("I'm running.")

class ThreadingInotify(object):
    """ Threading inotify"""

    def __init__(self, directory, interval=1):
        self.directory = directory
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        while True:
            i = inotify.adapters.Inotify()

            i.add_watch(self.directory)

            for event in i.event_gen(yield_nones=False):
                (_, etype, _, _) = event

                if 'IN_DELETE' in etype or 'IN_MODIFY' in etype or 'IN_MOVED_TO' in \
                etype or 'IN_MOVED_FROM' in etype or 'IN_CREATE' in etype:
                    schedule.clear()
                    print("---- Removed previous schedules ----")
                    print_changes(self.directory)

            time.sleep(self.interval)


if __name__ == "__main__":
    print("Started at: {}".format(datetime.now()))
    directory = os.path.abspath('.')
    ThreadingInotify(directory)
    while True:
        schedule.run_pending()
        time.sleep(2)
        just_running()

# run the script and in another terminal create, remove or modify a file.
# output:
# Started at: 2018-02-08 10:12:53.212853
# I'm running.
# I'm running.
# ---- Removed previous schedules ----
# Something has changed in /home/aldenso/github/tools/python_examples/schedule_and_printing!
# Will schedule a task every 5 seconds
# I'm running.
# I'm running.
# I'm running.
# I'm a scheduled task.
# I'm running.
# ---- Removed previous schedules ----
# Something has changed in /home/aldenso/github/tools/python_examples/schedule_and_printing!
# Will schedule a task every 5 seconds
# ---- Removed previous schedules ----
# Something has changed in /home/aldenso/github/tools/python_examples/schedule_and_printing!
# Will schedule a task every 5 seconds
# I'm running.
# I'm running.
# I'm running.
# I'm a scheduled task.
# I'm running.
# ---- Removed previous schedules ----
# Something has changed in /home/aldenso/github/tools/python_examples/schedule_and_printing!
# Will schedule a task every 5 seconds
# I'm running.
# I'm running.
# I'm running.
# I'm a scheduled task.
