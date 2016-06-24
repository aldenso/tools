centoslocalrepo
===============

Scripts to create a local repo for centos.

As you don't have a previous repo yet, we are going to run the script without the variables, so it downloads the mirrorlist.csv and then we can pick a mirror.

```
# ./createlocalrepo.sh
Program started on 2016-06-24/00:37:48
You didn't set a remote repo, the mirror list have been
downloaded for you, please check csv file on current directory
and select an rsync one to set on $localrepodir variable.
```

Now lets use the python script to choose one.

```
# python selectmirror.py
### Select Global Location ###
(1) ==> Africa
(2) ==> Asia
(3) ==> Canada
(4) ==> EU
(5) ==> Middle East
(6) ==> Oceania
(7) ==> South America
(8) ==> US
Press number of choice and Enter:8
### Select specific Location  ###
(1) ==>
(2) ==> AZ
(3) ==> CA
(4) ==> FL
(5) ==> GA
(6) ==> ID
(7) ==> IL
(8) ==> MA
(9) ==> MD
(10) ==> ME
(11) ==> MI
(12) ==> MN
(13) ==> MO
(14) ==> NC
(15) ==> NJ
(16) ==> NY
(17) ==> OH
(18) ==> OK
(19) ==> OR
(20) ==> PA
(21) ==> TX
(22) ==> UT
(23) ==> VA
(24) ==> VT
(25) ==> WA
(26) ==> WI
(0) ==> Return to previous Menu
Press number of choice and Enter:17
### Select specific Site ###
(1) ==> CISP / Yocolo
(0) ==> Return to previous Menu
Press number of choice and Enter:1
Site has the next urls:
http://mirror.cisp.com/CentOS/
rsync://mirror.cisp.com/CentOS
############################################################
Set the variable urlremoterepo in script createrepolocal:
############################################################
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
urlremoterepo=//mirror.cisp.com/CentOS
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
```

Now set the variables with your values.

```
#####################################
# Configuration
#####################################
urlremoterepo="//mirror.cisp.com/CentOS"                #ex: "//mirror.cisp.com/CentOS"
localrepodir="/share"                                   #ex: "/share"
outputfile="/tmp/localrepo.$(date +%F-%T)"
dirdistros="7.2.1511 6.8"                               #ex: 7.2.1511 or "7.2.1511 6.8"
dirdistrossubset="extras"                               #ex: "os" or "os addons extras updates"
dirdistrossubsetplatf="x86_64"          #ex: "i386" or "i386 x86_64"
#####################################
# Configuration -end
#####################################

```

And finally lets run the script again.

```
# ./createlocalrepo.sh
Program started on 2016-06-24/00:55:33
Using Remote Repo: //mirror.cisp.com/CentOS
localrepo directory set:
/share
âââ 6.8
âÂ Â  âââ extras
âÂ Â      âââ x86_64
âââ 7.2.1511
    âââ extras
        âââ x86_64

6 directories, 0 files
2016-06-24/00:55:33: rsyncing //mirror.cisp.com/CentOS/6.8/extras/x86_64 /share/6.8/extras
2016-06-24/00:55:33: rsyncing running in background.
nohup: appending output to ânohup.outâ
2016-06-24/00:55:33: rsyncing //mirror.cisp.com/CentOS/7.2.1511/extras/x86_64 /share/7.2.1511/extras
2016-06-24/00:55:33: rsyncing running in background.
Script Finished. Please check outputfile: /tmp/localrepo.2016-06-24-00:55:33
[root@test localrepo]# nohup: appending output to ânohup.outâ
```

Just check everything is running fine.

```
# ps -ef | grep rsync
root      4110     1  0 00:55 pts/0    00:00:00 rsync -a --delete --delete-excluded --exclude local* --exclude isos rsync://mirror.cisp.com/CentOS/7.2.1511/extras/x86_64 /share/7.2.1511/extras
root      4111  4110  0 00:55 pts/0    00:00:00 rsync -a --delete --delete-excluded --exclude local* --exclude isos rsync://mirror.cisp.com/CentOS/7.2.1511/extras/x86_64 /share/7.2.1511/extras
root      4115  2852  0 00:57 pts/0    00:00:00 grep --color=auto rsync


# ls -lrthR /share/*/extras/x86_64
/share/6.8/extras/x86_64:
total 4.0K
drwxrwxr-x 2 501 501    6 Jun 16 09:01 drpms
drwxrwxr-x 2 501 501    6 Jun 16 09:01 repodata
drwxrwxr-x 2 501 501 4.0K Jun 24 00:55 Packages

/share/6.8/extras/x86_64/drpms:
total 0

/share/6.8/extras/x86_64/repodata:
total 0

/share/6.8/extras/x86_64/Packages:
total 1.2M
-rw-rw-r-- 1 501 501 4.0K Dec 19  2011 centos-release-cr-6-0.el6.centos.x86_64.rpm
-rw-rw-r-- 1 501 501 239K Jan 25  2012 jfsutils-1.1.13-9.el6.x86_64.rpm
-rw-rw-r-- 1 501 501 251K Nov 29  2012 bakefile-0.2.8-3.el6.centos.x86_64.rpm
-rw-rw-r-- 1 501 501  15K Sep  2  2014 epel-release-6-8.noarch.rpm
-rw-rw-r-- 1 501 501 432K Nov  3  2014 cloud-init-0.7.5-10.el6.centos.2.x86_64.rpm
-rw-rw-r-- 1 501 501 4.9K May 20  2015 centos-release-openstack-juno-2.el6.noarch.rpm
-rw-rw-r-- 1 501 501 4.4K Oct 22  2015 centos-release-virt-common-1-1.el6.centos.noarch.rpm
-rw-rw-r-- 1 501 501 4.4K Nov 13  2015 centos-release-gluster37-1.0-4.el6.centos.noarch.rpm
-rw-rw-r-- 1 501 501  12K Dec 17  2015 centos-release-scl-rh-1-1.el6.centos.noarch.rpm
-rw-rw-r-- 1 501 501  12K Dec 17  2015 centos-release-scl-6-6.el6.centos.noarch.rpm
-rw-rw-r-- 1 501 501 4.4K Jan 13 10:46 centos-release-storage-common-1-2.el6.centos.noarch.rpm
-rw-rw-r-- 1 501 501 4.0K Jan 13 10:46 centos-release-gluster36-1.0-3.el6.centos.noarch.rpm
-rw-rw-r-- 1 501 501  12K Mar 24 15:17 centos-release-scl-2-1.el6.centos.noarch.rpm
-rw-rw-r-- 1 501 501  12K Mar 24 15:18 centos-release-scl-rh-2-1.el6.centos.noarch.rpm
-rw-rw-r-- 1 501 501 6.7K Apr  1 07:20 centos-release-xen-common-8-1.el6.x86_64.rpm
-rw-rw-r-- 1 501 501 6.2K Apr  1 07:20 centos-release-xen-8-2.el6.x86_64.rpm
-rw-rw-r-- 1 501 501 6.1K Apr  1 07:20 centos-release-xen-8-1.el6.x86_64.rpm
-rw-rw-r-- 1 501 501 6.4K Apr  1 07:20 centos-release-xen-46-8-2.el6.x86_64.rpm
-rw-rw-r-- 1 501 501 6.4K Apr  1 07:20 centos-release-xen-44-8-2.el6.x86_64.rpm
-rw-rw-r-- 1 501 501 6.3K Apr  1 07:20 centos-release-xen-44-8-1.el6.x86_64.rpm
-rw-rw-r-- 1 501 501 6.8K Apr  1 07:20 centos-release-xen-common-8-2.el6.x86_64.rpm
-rw-rw-r-- 1 501 501 6.3K Apr  1 07:20 centos-release-xen-46-8-1.el6.x86_64.rpm
-rw-rw-r-- 1 501 501  13K Apr  6 10:28 centos-release-scl-7-2.el6.centos.noarch.rpm
-rw-rw-r-- 1 501 501  12K May 23 11:05 centos-release-scl-rh-2-2.el6.centos.noarch.rpm
-rw-rw-r-- 1 501 501  13K May 23 11:06 centos-release-scl-7-3.el6.centos.noarch.rpm
-rw-rw-r-- 1 501 501  13K Jun 16 08:59 centos-release-scl-rh-2-3.el6.centos.noarch.rpm

/share/7.2.1511/extras/x86_64:
total 4.0K
drwxrwxr-x 2 501 501    6 Jun  9 12:50 drpms
drwxrwxr-x 2 501 501    6 Jun  9 12:50 repodata
drwxrwxr-x 2 501 501 4.0K Jun 24 00:55 Packages

/share/7.2.1511/extras/x86_64/drpms:
total 0

/share/7.2.1511/extras/x86_64/repodata:
total 0

/share/7.2.1511/extras/x86_64/Packages:
total 2.8M
-rw-rw-r-- 1 501 501 1.9M Mar 28  2015 cadvisor-0.4.1-0.3.git6906a8ce.el7.x86_64.rpm
-rw-rw-r-- 1 501 501 5.0K May 20  2015 centos-release-openstack-kilo-2.el7.noarch.rpm
-rw-rw-r-- 1 501 501 4.5K Sep  3  2015 centos-release-virt-common-1-1.el7.centos.noarch.rpm
-rw-rw-r-- 1 501 501  11K Oct  8  2015 centos-release-qemu-ev-1.0-1.el7.noarch.rpm
-rw-rw-r-- 1 501 501  11K Oct  8  2015 centos-release-ovirt35-1.0-2.el7.noarch.rpm
-rw-rw-r-- 1 501 501 5.3K Oct 16  2015 centos-release-openstack-kilo-1-2.el7.noarch.rpm
-rw-rw-r-- 1 501 501 5.1K Oct 21  2015 centos-release-openstack-liberty-1-4.el7.noarch.rpm
-rw-rw-r-- 1 501 501  12K Oct 23  2015 centos-release-scl-1-1.el7.centos.noarch.rpm
-rw-rw-r-- 1 501 501  12K Oct 23  2015 centos-release-scl-rh-1-1.el7.centos.noarch.rpm
-rw-rw-r-- 1 501 501  86K Nov  5  2015 atomic-1.6-6.gitca1e384.el7.x86_64.rpm
-rw-rw-r-- 1 501 501 4.5K Nov 13  2015 centos-release-gluster37-1.0-4.el7.centos.noarch.rpm
-rw-rw-r-- 1 501 501 4.6K Nov 13  2015 centos-release-storage-common-1-2.el7.centos.noarch.rpm
-rw-rw-r-- 1 501 501 4.1K Nov 20  2015 centos-release-gluster36-1.0-3.el7.centos.noarch.rpm
-rw-rw-r-- 1 501 501  12K Dec  2  2015 centos-release-ovirt36-1.0-3.el7.centos.noarch.rpm
-rw-rw-r-- 1 501 501  18K Dec  2  2015 centos-packager-0.5.2-1.el7.centos.noarch.rpm
-rw-rw-r-- 1 501 501 6.5K Dec 21  2015 centos-release-xen-7-11.el7.x86_64.rpm
-rw-rw-r-- 1 501 501 4.6K Feb 24 15:09 centos-release-ceph-hammer-1.0-5.el7.centos.noarch.rpm
-rw-rw-r-- 1 501 501  12K Mar 24 15:22 centos-release-scl-2-1.el7.centos.noarch.rpm
-rw-rw-r-- 1 501 501  12K Mar 24 15:22 centos-release-scl-rh-2-1.el7.centos.noarch.rpm
-rw-rw-r-- 1 501 501 561K Apr  1 06:02 atomic-1.9-4.gitff44c6a.el7.x86_64.rpm
-rw-rw-r-- 1 501 501 6.3K Apr  1 06:02 centos-release-xen-46-8-1.el7.x86_64.rpm
-rw-rw-r-- 1 501 501 6.1K Apr  1 06:02 centos-release-xen-8-1.el7.x86_64.rpm
-rw-rw-r-- 1 501 501 6.7K Apr  1 06:02 centos-release-xen-common-8-1.el7.x86_64.rpm
-rw-rw-r-- 1 501 501 5.2K Apr 11 12:40 centos-release-openstack-mitaka-1-2.el7.centos.noarch.rpm
-rw-rw-r-- 1 501 501  12K May 23 11:17 centos-release-scl-2-2.el7.centos.noarch.rpm
-rw-rw-r-- 1 501 501  12K May 23 11:17 centos-release-scl-rh-2-2.el7.centos.noarch.rpm
-rw-rw-r-- 1 501 501  11K May 26 08:55 centos-release-openshift-origin-1-1.el7.centos.noarch.rpm
-rw-rw-r-- 1 501 501  12K May 26 08:55 centos-release-paas-common-1-1.el7.centos.noarch.rpm

```
