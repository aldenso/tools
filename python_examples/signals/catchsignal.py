#!/usr/bin/env python
import sys
import signal
import time

class GetSignal:
    """Get signals."""
    term_now = False

    def __init__(self):
        signal.signal(signal.SIGTERM, self.exit_gracefully)
        signal.signal(signal.SIGINT, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.term_now = True


def main():
    signal_event = GetSignal()
    while True:
        print("doing something")
        time.sleep(1)
        if signal_event.term_now:
            sys.exit("terminating loop")

if __name__ == "__main__":
    main()
