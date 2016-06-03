#!/usr/bin/env python
<<<<<<< HEAD
# On the shell just execute : "fab fabfile checkfs" or just one of the functions.
# run and sudo are almost equal but of course sudo if used with sudo privileges
# you can set an optional sudo users privileges ex: sudo("ls", user="www") or
# sudo("ls", user=1001)
=======
# On the shell just execute : "fab checkfs" or just one of the functions
>>>>>>> 100959db53df1d9545633ef96f4ba114404da9f9
import datetime
from fabric.api import local, run, sudo, env, parallel

env.hosts = ['192.168.125.100', '192.168.125.20']
datelog = datetime.datetime.now().strftime("%d%m%y-%H%M%S")

def log(command, msg):
    with open("output_"+env.host+"_"+command+"_"+datelog+".log","a+") as logfile:
        logfile.write(msg + "\n")

def errorlog(command, error):
    with open("error_"+env.host+"_"+command+"_"+datelog+".err","a+") as logfile:
        logfile.write(error + "\n")


def uptime():
    try:
        up = run('uptime')
        log('uptime', up)
    except Exception, e:
        errorlog('uptime', str(e))


def spacefs():
    try:
        space = run('df -h')
        log('dfspace', space)
    except Exception, e:
        errorlog('dfspace', str(e))

def inodefs():
    try:
        inode = run('df -i')
        log('dfinodes', inode)
    except Exception, e:
        errorlog('dfinodes', str(e))

def lsdir():
    try:
        ls = sudo('ls /root/re*')
        log('lsdir_root_re', ls)
    except Exception, e:
        errorlog('lsdir_root_re', str(e))

#set parallel execution for 5 servers
@parallel(pool_size=5)
def checkfs():
    uptime()
    spacefs()
    inodefs()
    lsdir()
