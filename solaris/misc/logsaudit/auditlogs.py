#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: Aldo Sotolongo
# @Date:   2016-06-26 18:04:58
# @Last modified by:   Aldo Sotolongo
# @Last modified time: 2016-09-28T11:27:51-04:00
# Note: Must run with a user with privileges on the dirs

import os
import csv
from os.path import join, getsize
from datetime import datetime, date

# Size 10 MB
SIZEALERT = 10 * (1024 * 1024)
COUNTALERT = 100
DATETIME = datetime.now().strftime("%d%m%y_%H%M%S")

# Set your values
DIRS = [
    ["/u01/app/oracle/admin", 1000 * 1024 * 1024, 1000],
    ["/u01/app/oracle/diag", 1000 * 1024 * 1024, 1000],
    ["/u01/app/grid/diag"],
    ["/var", 10485760, 250],
    ["/opt"]
]
EXT = [".log", ".xml", ".aud", ".trm", ".trc"]


def hash(caracter="#"):
    print ("%s" % (caracter)) * 79


def alert(directory, count, size, dirsdict):
    print """@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@********** WARNING ********** WARNING ********** WARNING **********@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
CHECK LOG SIZE UTILIZATION
Alertsize: %dMB || Alertcount: %s
directory: %s
size: %dMB || count: %d
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@********** WARNING ********** WARNING ********** WARNING **********@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Logs distribution:""" % ((directory[1] / (1024 * 1024)), directory[2], directory[0],
                          (size / (1024 * 1024)), count)
    for k, v in dirsdict.iteritems():
        print "Dir: %2s || size: %2s || Count: %2s" % (k, v[0], v[1])
    hash("*")


def getinfo(dir):
    dirsdict = {}
    count = 0
    size = 0
    for path, dirs, files in os.walk(dir):
        for file in files:
            fullfile = join(path, file)
            if fullfile.endswith(tuple(EXT)):
                filesize = getsize(fullfile)
                size += filesize
                count += 1
                if path not in dirsdict:
                    dirsdict[path] = (filesize, 1)
                else:
                    oldfilesize = dirsdict[path][0]
                    newfilesize = oldfilesize + filesize
                    oldcount = dirsdict[path][1]
                    newcount = oldcount + 1
                    dirsdict[path] = (newfilesize, newcount)
    return size, count, dirsdict


def main():
    for d in DIRS:
        if len(d) == 1:
            d.extend([SIZEALERT, COUNTALERT])
        elif len(d) != 3:
            print "X" * 79
            print "Directory definition error length for: %s" % d
            print "X" * 79
            continue
        size, count, dirsdict = getinfo(d[0])
        hash()
        if size > d[1] or count > d[2]:
            alert(d, count, size, dirsdict)
            with open("warning_" + d[0].strip("/").replace("/", "_") +
                      "_" + DATETIME + ".log", "wb") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["directory", "size in bytes",
                                 "number of logs"])
                for k, v in dirsdict.iteritems():
                    writer.writerow([k, v[0], v[1]])
        else:
            print "logs for %s:\nCount: %d\nFull size: %dMB" \
                   % (d[0], count, (size / (1024 * 1024)))



if __name__ == '__main__':
    main()
