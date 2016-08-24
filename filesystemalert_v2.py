#!/usr/bin/python
# @Author: Aldo Sotolongo
# @Date:   2016-05-25T14:22:59-04:00
# @Email:  aldenso@gmail.com
# @Last modified by:   Aldo Sotolongo
# @Last modified time: 2016-08-23T20:34:17-04:00
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

# Set thresholds
yellow = 85
orange = 90
red = 95
# FS in alert, the first element is the header
fsalert = ["Alert type\tFileSystem\tUsage\n"]

filesystems = []
cmd = "lsblk"
p = Popen(cmd, stdout=PIPE, shell=True)
output, error = p.communicate()
for line in output.splitlines():
    if len(line.split()) == 7:
        filesystems.append(line.split()[6])
for i in filesystems:
    if i == '[SWAP]' or i == 'MOUNTPOINT':
        filesystems.remove(i)


def checkusage(filesystems):
    if excludefs:
        for e in excludefs:
            filesystems.remove(e)
    for fs in filesystems:
        cmd = "df {} | tail -1".format(fs)
        p = Popen(cmd, stdout=PIPE, shell=True)
        output, error = p.communicate()
        usage = int(output.split()[4][:-1])
        if usage >= yellow and usage < orange:
            fsalert.append("YELLOW ALERT\t{0}\t\t{1}\n".format(fs, usage))
        elif usage >= orange and usage < red:
            fsalert.append("ORANGE ALERT\t{0}\t\t{1}\n".format(fs, usage))
        elif usage >= red:
            fsalert.append("RED ALERT\t{0}\t\t{1}\n".format(fs, usage))
        else:
            print("{}:normal usage".format(fs))


def sendmail(fsalert):
    fsalert.sort()
    with open(temporalfile, "wb") as file:
        for entry in fsalert:
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
    checkusage(filesystems)
    if len(fsalert) > 1:
        sendmail(fsalert)
        for entry in fsalert:
            print(entry)
        syslog.syslog("File System Alert, mail sent to admins")
    else:
        print("Nothing to report")

if __name__ == "__main__":
    main()
