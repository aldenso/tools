#!/usr/bin/python

# Author: aldenso@gmail.com
# Description: simple cp script with progress status

from subprocess import Popen
from time import sleep
import os, sys

# Origin and destiny files are pass as arguments
argv1 = sys.argv[1]
argv2 = sys.argv[2]

orig_size = os.path.getsize(argv1)
size = 0


def porcent(size):
    x = (size*100)/orig_size
    return x


def main():
    task = 'RUNNING'
    Popen(["cp", argv1, argv2], shell=False)
    sleep(0.1)
    while task == 'RUNNING':
        sleep(0.5)
        size=os.path.getsize(argv2)
        if size == orig_size:
            sys.stdout.write("\rCopying File 100%")
            print("\nCopy done")
            task = 'DONE'
        else:
            value = porcent(size)
            sys.stdout.write("\rCopying File %d%%" % value)
            sys.stdout.flush()

if __name__ == "__main__":
    main()
