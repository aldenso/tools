#!/usr/bin/env python
# On the shell just execute : "fab checkfs" or just one of the functions
import datetime
from fabric.api import local, run, env

env.hosts = ['192.168.125.100', '192.168.125.20']
datelog = datetime.datetime.now().strftime("%d%m%y-%H%M%S")

def log(command, msg):
    with open("output_"+datelog+".txt","a+") as logfile:
        logfile.write("server:" + env.host + ":command:" + command + "\n")
        logfile.write(msg + "\n")


def uptime():
    up = run('uptime')
    log('uptime', up)

def spacefs():
    space = run('df -h')
    log('df -h', space)

def inodefs():
    inode = run('df -i')
    log('df -i', inode)

def lsdir():
    ls = run('ls /root/re*')
    log('ls /root/re*', ls)

def checkfs():
    uptime()
    spacefs()
    inodefs()
    lsdir()
