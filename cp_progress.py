#!/usr/bin/python
# @Author: Aldo Sotolongo
# @Date:   2016-05-25T14:22:58-04:00
# @Email:  aldenso@gmail.com
# @Last modified by:   Aldo Sotolongo
# @Last modified time: 2016-08-21T23:49:39-04:00
# Description: simple cp script with progress status, make sure you set the
# filename for destiny.
# example: cp_progress.py ../../file1.txt /tmp/file1.txt

import os
import sys
from subprocess import Popen
from time import sleep

# Origin and destiny files are pass as arguments
argv1 = sys.argv[1]
argv2 = sys.argv[2]

orig_size = os.path.getsize(argv1)
size = 0


def porcent(size):
    x = (size * 100) / orig_size
    return x


def main():
    task = 'RUNNING'
    Popen(["cp", argv1, argv2], shell=False)
    sleep(0.1)
    while task == 'RUNNING':
        sleep(0.5)
        size = os.path.getsize(argv2)
        if size == orig_size:
            sys.stdout.write("\rCopying File 100%")
            print("\nCopy done")
            task = 'DONE'
        else:
            value = porcent(size)
            sys.stdout.write("\rCopying File {}%".format(value))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
