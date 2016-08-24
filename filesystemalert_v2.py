#!/usr/bin/python
# @Author: Aldo Sotolongo
# @Date:   2016-05-25T14:22:59-04:00
# @Email:  aldenso@gmail.com
# @Last modified by:   Aldo Sotolongo
# @Last modified time: 2016-08-23T21:47:23-04:00
# File: filesystemalert_v2.py
# Description: This script is useful to set filesystem alerts based on
# defined thresholds, also you can exclude fs from the alerts

from subprocess import Popen, PIPE
from email.MIMEText import MIMEText
import smtplib
import syslog

fromaddr = "root@localhost"
toaddrs = "aldo@localhost"
temporalfile = "/tmp/fsalert.txt"
# toaddrs=["aldo@localhost","aldo@aldoca.com","aldenso@gmail.com"]
# If you want to exclude some FS set then in the variable excludefs as a list
excludefs = None
# excludefs=["/boot","/fsdump"]

# Set thresholds fs
yellowfs = 85
orangefs = 90
redfs = 95
# Set thresholds inodes
yellowinode = 85
orangeinode = 90
redinode = 95
# FS in alert, the first element is the header
fsalert = ["Alert type\tFileSystem\tUsage\n"]
# FS in alert, the first element is the header
inodealert = ["Alert type\tFileSystem\tUsage\n"]

filesystems = []
# if some filesystem is a raid it may be shown more than once in the output.
cmd = "lsblk"
p = Popen(cmd, stdout=PIPE, shell=True)
output, error = p.communicate()
for line in output.splitlines():
    if len(line.split()) == 7:
        filesystems.append(line.split()[6])
for i in filesystems:
    if i == '[SWAP]' or i == 'MOUNTPOINT':
        filesystems.remove(i)


def checkusagefs(filesystems):
    print("### FS check ###")
    if excludefs:
        for e in excludefs:
            filesystems.remove(e)
    for fs in filesystems:
        cmd = "df {} | tail -1".format(fs)
        p = Popen(cmd, stdout=PIPE, shell=True)
        output, error = p.communicate()
        usage = int(output.split()[4][:-1])
        if usage >= yellowfs and usage < orangefs:
            fsalert.append("yellow FS ALERT\t{0}\t\t{1}\n".format(fs, usage))
        elif usage >= orangefs and usage < redfs:
            fsalert.append("orange FS ALERT\t{0}\t\t{1}\n".format(fs, usage))
        elif usage >= redfs:
            fsalert.append("red FS ALERT\t{0}\t\t{1}\n".format(fs, usage))
        else:
            print("{}:normal usage".format(fs))


def checkusageinode(filesystems):
    print("### Inode check ###")
    if excludefs:
        for e in excludefs:
            filesystems.remove(e)
    for fs in filesystems:
        cmd = "df -i {} | tail -1".format(fs)
        p = Popen(cmd, stdout=PIPE, shell=True)
        output, error = p.communicate()
        usage = int(output.split()[4][:-1])
        if usage >= yellowinode and usage < orangeinode:
            inodealert.append("yellow Inode ALERT\t{0}\t\t{1}\n"
                              .format(fs, usage))
        elif usage >= orangeinode and usage < redinode:
            inodealert.append("orange Inode ALERT\t{0}\t\t{1}\n"
                              .format(fs, usage))
        elif usage >= redinode:
            inodealert.append("red Inode ALERT\t{0}\t\t{1}\n"
                              .format(fs, usage))
        else:
            print("{}:normal usage".format(fs))


def sendmail(fsalert=None, inodealert=None):
    with open(temporalfile, "wb") as file:
        if fsalert is not None:
            fsalert.sort()
            for entry in fsalert:
                file.write(entry)
        if inodealert is not None:
            inodealert.sort()
            for entry in inodealert:
                file.write(entry)
    fp = open(temporalfile, "rb")
    msg = MIMEText(fp.read())
    msg['From'] = fromaddr
    msg['To'] = toaddrs
    msg['Subject'] = "FileSystem Alert"
    fp.close()

    server = smtplib.SMTP('localhost')
    # server.set_debuglevel(1)
    server.sendmail(fromaddr, toaddrs, msg.as_string())
    server.quit()


def main():
    checkusagefs(filesystems)
    checkusageinode(filesystems)
    if len(fsalert) > 1 and len(inodealert) > 1:
        sendmail(fsalert, inodealert)
        for entry in fsalert:
            print(entry)
        for entry in inodealert:
            print(entry)
        syslog.syslog("File System Alert, mail sent to admins")
    elif len(fsalert) > 1 and len(inodealert) == 1:
        sendmail(fsalert, None)
        for entry in fsalert:
            print(entry)
        syslog.syslog("File System Alert, mail sent to admins")
    elif len(fsalert) == 1 and len(inodealert) > 1:
        sendmail(None, inodealert)
        for entry in inodealert:
            print(entry)
        syslog.syslog("File System Alert, mail sent to admins")
    else:
        print("Nothing to report")

if __name__ == "__main__":
    main()
