#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: Aldo Sotolongo
# @Date:   2017-01-13 15:17:37
# @Last Modified by:   Aldo Sotolongo
# @Last Modified time: 2017-01-15 21:04:43
# Description: Small program to get some info about shares in ZFS Storage Appliance.

from __future__ import print_function
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# to disable warning
#InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate
#verification is strongly advised. See:
#https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

URL = "https://192.168.100.150:215/api"
ZAUTH = ("useradm", "password")
HEADER = {"Content-Type": "application/json"}


def getpools():
    """Get all Pools"""
    pools = []
    req = requests.get(URL + "/storage/v1/pools", auth=ZAUTH, verify=False, headers=HEADER)
    j = json.loads(req.text)
    req.close()
    for item in j.values():
        for pool in item:
            pools.append(pool["name"])
    pools = [str(x) for x in pools]
    return sorted(pools)

def getprojects(poolname):
    """Get all projects in a pool"""
    projects = []
    req = requests.get(URL + "/storage/v1/pools/{}/projects".format(poolname), auth=ZAUTH,
                       verify=False, headers=HEADER)
    j = json.loads(req.text)
    req.close()
    for item in j.values():
        for project in item:
            projects.append(project["name"])
    projects = [str(x) for x in projects]
    return sorted(projects)

def printlunsinproject(poolname, project):
    """Print LUNS info for a project"""
    req = requests.get(URL + "/storage/v1/pools/{}/projects/{}/luns".format(poolname, project),
                       auth=ZAUTH, verify=False, headers=HEADER)
    j = json.loads(req.text)
    req.close()
    for item in j.values():
        if item:
            for lun in sorted(item):
                initiatorgroup = [str(i) for i in lun["initiatorgroup"]]
                print("{:15} {:8.2f} {:15} {:20} {:10} {:34} {:8} {:25} {:8} {:4}"
                      .format(lun["name"], (lun["volsize"]/(1024*1024*1024)), lun["targetgroup"],
                              initiatorgroup, lun["status"], lun["lunguid"], lun["pool"],
                              lun["project"], lun["logbias"], lun["assignednumber"]))


def printfsinproject(poolname, project):
    """Print Filesystems info for a project"""
    req = requests.get(URL + "/storage/v1/pools/{}/projects/{}/filesystems"
                       .format(poolname, project), auth=ZAUTH, verify=False, headers=HEADER)
    j = json.loads(req.text)
    req.close()
    for item in j.values():
        if item:
            for fs in sorted(item):
                print("{:20} {:8.2f} {:40} {:8} {:22} {:8.2f} {:8.2f} {:10} {:10} {:5} {:40} {:50}"
                      .format(fs["name"], (fs["space_total"]/(1024*1024*1024)), fs["mountpoint"],
                              fs["pool"], fs["project"], (fs["quota"]/(1024*1024*1024)),
                              (fs["reservation"]/(1024*1024*1024)), fs["root_user"],
                              fs["root_group"], fs["root_permissions"], fs["sharesmb"],
                              fs["sharenfs"]))

def main():
    """Main function for script"""
    pools = getpools()
    projects4pool = {}

    # Get LUN Info
    print("="*230)
    print("{:15} {:8} {:15} {:20} {:10} {:34} {:8} {:25} {:8} {:4}"
          .format("LUN", "Size(GB)", "TargetGroup", "InitiatorGroup", "status", "lunguid", "Pool",
                  "Project", "logbias", "assignednumber"))
    print("="*230)
    for pool in pools:
        projects4pool[pool] = getprojects(pool)
        for keypool, values in projects4pool.iteritems():
            for projvalue in values:
                printlunsinproject(keypool, projvalue)

    # Get Filesystems Info
    print("="*230)
    print("{:20} {:8} {:40} {:8} {:22} {:8} {:8} {:10} {:10} {:5} {:40} {:50}"
          .format("FSNAME", "space(GB)", "mountpoint", "pool", "project", "quota",
                  "reserv", "root_user", "root_group", "perm", "sharesmb", "sharenfs"))
    print("="*230)
    for pool in pools:
        for keypool, values in projects4pool.iteritems():
            for projvalue in values:
                printfsinproject(keypool, projvalue)

if __name__ == "__main__":
    main()
