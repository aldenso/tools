#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Aldo Sotolongo
# @Date:   2016-07-12 11:22:10
# @Last modified by:   Aldo Sotolongo
# @Last modified time: 2016-08-12T23:08:35-04:00

import datetime
import os
import sys
from fabric.api import local, run, sudo, env, parallel, hosts, execute, \
    runs_once, roles, settings

# env.hosts = ['192.168.125.100', '192.168.125.20']
DATE = datetime.datetime.now().strftime("%d%m%y-%H%M%S")
TODAYDIR = "reports/" + datetime.datetime.now().strftime("%d%m%y")
# env.disable_known_hosts = True  # use with systems with floating IPs

env.hosts = [
    'solarisserver1', 'solarisserver2', 'solarisserver3', 'solarisserver4',
    'solarisserver5', 'solarisserver6', 'solarisserver7', 'solarisserver8',
    'linuxserver1', 'linuxserver2', 'linuxserver3', 'linuxserver4',
    'linuxserver5', 'linuxserver6', 'linuxserver7', 'linuxserver8'
]

env.roledefs['solaris'] = [
    'solarisserver1', 'solarisserver2', 'solarisserver3', 'solarisserver4',
    'solarisserver5', 'solarisserver6', 'solarisserver7', 'solarisserver8'
]
env.roledefs['linux'] = [
    'linuxserver1', 'linuxserver2', 'linuxserver3', 'linuxserver4',
    'linuxserver5', 'linuxserver6', 'linuxserver7', 'linuxserver8'
]
env.roledefs['linuxBD'] = [
    'linuxserver1', 'linuxserver2', 'linuxserver3', 'linuxserver4'
]

direxist = os.path.exists(TODAYDIR)
if direxist is False:
    try:
        os.mkdir(TODAYDIR, 0755)
    except Exception as err:
        print(str(err))


def log(command, msg):
    with open(TODAYDIR + "/" + env.host + "_" + command +
              ".log", "w") as logfile:
        logfile.write(msg + "\n")


def errorlog(command, error):
    with open(TODAYDIR + "/" + env.host + "_" + command +
              ".err", "w") as logfile:
        logfile.write(error + "\n")


@roles('solaris')
@parallel(pool_size=4)
def solarisspacereport():
    CMD = 'df -h | cat'
    try:
        backups = sudo(CMD)
        log('solaris_space_report', backups)
    except Exception as err:
        errorlog('solaris_space_report', str(err))


@roles('linux')
@parallel(pool_size=4)
def linuxsomescript():
    CMD = 'cd $HOME; source .someenvfile; ./somescript.sh'
    # warn_only if the running job fails, it can continue with next jobs
    with settings(warn_only=True):
        try:
            report = sudo(CMD)
            log('linux_somescript', report)
        except Exception as err:
            errorlog('linux_somescript', str(err))


@roles('linuxBD')
@parallel(pool_size=2)
def checktablespace():
    CMD = '. $HOME/.myinst1db.env ; cd $HOME/DBA_SCRIPTS; ./CHK_SPACE.sh'
    with settings(warn_only=True):
        try:
            report = sudo(CMD, user='oracle')
            log('tablespace_myinst1db', report)
        except Exception as err:
            errorlog('tablespace_myinst1db', str(err))
    CMD = '. $HOME/.myinst2db.env ; cd $HOME/DBA_SCRIPTS; ./CHK_SPACE.sh'
    with settings(warn_only=True):
        try:
            report = sudo(CMD, user='oracle')
            log('tablespace_myinst2db', report)
        except Exception as err:
            errorlog('tablespace_myinst2db', str(err))


@runs_once
def dailyreports():
    try:
        # here we don't care about the ouput report
        local('cd ~/dailyreports; ./solaris_spaces.sh > /dev/null')
        local('cd ~/dailyreports; ./linux_spaces.sh > /dev/null')
    except Exception as err:
        errorlog('daily_reports', str(err))


@roles('localhost')
@runs_once
def reportZFSSA():
    controllers = ['zfssa_anode1', 'zfssa_anode2', 'zfssa_anode3']
    for controller in controllers:
        try:
            logname = 'zfssa_{}'.format(controller)
            cmd = 'ssh {} < zfssa_spaces.aksh > {}/{}'.format(controller,
                                                              TODAYDIR,
                                                              logname
                                                              )
            local(cmd)
        except Exception as err:
            logname = 'zfssa_{}'.format(controller)
            errorlog(logname, str(err))


@runs_once
def runallcheckfs():
    execute(solarisspacereport)
    execute(linuxsomescript)
    execute(checktablespace)


@runs_once
def runallreports():
    execute(dailyreports)
    execute(reportZFSSA)
