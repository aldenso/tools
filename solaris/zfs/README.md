Solaris tools
=============

##### zfs_snapshots_backups.sh:
(useful to recover zones or ldoms with lots of zones with dedicated pools)

Script to backup zpools using snapshots and gzip to save some space, is not fast, but you save a lot of space (compression can be really good, but depends on the data), the script uses a Backup filesystem (NFS on 10GB or 40GB network), creates a directory tree based on the hostname and pool names, takes also the important data from zfs, disk and pool (necessary for disaster recovery).

**Note**: make sure you have enough space to launch the backups (snapshots creation and backup filesystem)

Output sample:
```
# ./zfs_snapshots_backups.sh
#########################################################################
Started at 20/06/16 17:18:49
#########################################################################
#########################################################################
Get rpool properties
#########################################################################
#########################################################################
Get zfs list in rpool
#########################################################################
#########################################################################
Get zfs properties in rpool
#########################################################################
#########################################################################
Get rpool status
#########################################################################
#########################################################################
Get VTOC from disks in rpool
#########################################################################
#########################################################################
Creating snapshot rpool@rpool.snap
#########################################################################
#########################################################################
Removing dump and swap from rpool snapshot
#########################################################################
#########################################################################
Sending rpool@rpool.pool.snap stream
#########################################################################
sending from @ to rpool@rpool.pool.snap
sending from @ to rpool/ROOT@rpool.pool.snap
sending from @ to rpool/ROOT/solaris@install
sending from @install to rpool/ROOT/solaris@2014-07-05-22:13:41
sending from @2014-07-05-22:13:41 to rpool/ROOT/solaris@rpool.pool.snap
sending from @ to rpool/ROOT/solaris/var@install
sending from @install to rpool/ROOT/solaris/var@2014-07-05-22:13:41
sending from @2014-07-05-22:13:41 to rpool/ROOT/solaris/var@rpool.pool.snap
WARNING: could not send rpool/dump@rpool.pool.snap: does not exist
sending from @ to rpool/export@rpool.pool.snap
sending from @ to rpool/export/home@rpool.pool.snap
sending from @ to rpool/export/home/prueba@rpool.pool.snap
sending from @ to rpool/export/home/sstudent@rpool.pool.snap
sending from @ to rpool/export/home/aldo@rpool.pool.snap
sending from @ to rpool/export/home/docs@rpool.pool.snap
sending from @ to rpool/VARSHARE@rpool.pool.snap
sending from @ to rpool/zones@rpool.pool.snap
sending from @ to rpool/zones/choczone@rpool.pool.snap
sending from @ to rpool/zones/choczone/rpool@rpool.pool.snap
sending from @ to rpool/zones/choczone/rpool/ROOT@rpool.pool.snap
sending from @ to rpool/zones/choczone/rpool/ROOT/solaris@install
sending from @install to rpool/zones/choczone/rpool/ROOT/solaris@rpool.pool.snap
sending from @ to rpool/zones/choczone/rpool/ROOT/solaris/var@install
sending from @install to rpool/zones/choczone/rpool/ROOT/solaris/var@rpool.pool.snap
sending from @ to rpool/zones/choczone/rpool/VARSHARE@rpool.pool.snap
sending from @ to rpool/zones/choczone/rpool/export@rpool.pool.snap
sending from @ to rpool/zones/choczone/rpool/export/home@rpool.pool.snap
sending from @ to rpool/zones/choczone/rpool/export/home/oraclech@rpool.pool.snap
sending from @ to rpool/zones/grandmazone@rpool.pool.snap
sending from @ to rpool/zones/grandmazone/rpool@rpool.pool.snap
sending from @ to rpool/zones/grandmazone/rpool/export@rpool.pool.snap
sending from @ to rpool/zones/grandmazone/rpool/export/home@rpool.pool.snap
sending from @ to rpool/zones/grandmazone/rpool/export/home/oraclegm@rpool.pool.snap
sending from @ to rpool/zones/grandmazone/rpool/VARSHARE@rpool.pool.snap
sending from @ to rpool/zones/grandmazone/rpool/ROOT@rpool.pool.snap
sending from @ to rpool/zones/grandmazone/rpool/ROOT/solaris@install
sending from @install to rpool/zones/grandmazone/rpool/ROOT/solaris@rpool.pool.snap
sending from @ to rpool/zones/grandmazone/rpool/ROOT/solaris/var@install
sending from @install to rpool/zones/grandmazone/rpool/ROOT/solaris/var@rpool.pool.snap
WARNING: could not send rpool/swap@rpool.pool.snap: does not exist
sending from @ to rpool/ROOT/bewithdns@rpool.pool.snap
sending from @ to rpool/ROOT/bewithdns/var@rpool.pool.snap
#########################################################################
Deleting snapshot.
#########################################################################
#########################################################################
Finished rpool at 20/06/16 17:29:11
#########################################################################
#########################################################################
Get zonepool properties
#########################################################################
#########################################################################
Get zfs list in zonepool
#########################################################################
#########################################################################
Get zfs properties in zonepool
#########################################################################
#########################################################################
Get zonepool status
#########################################################################
#########################################################################
Get VTOC from disks in zonepool
#########################################################################
#########################################################################
Creating snapshot zonepool@zonepool.snap
#########################################################################
#########################################################################
Sending zonepool@zonepool.pool.snap stream
#########################################################################
sending from @ to zonepool@zonepool.pool.snap
sending from @ to zonepool/zoneftd@zonepool.pool.snap
sending from @ to zonepool/zoneftd/rpool@zonepool.pool.snap
sending from @ to zonepool/zoneftd/rpool/ROOT@zonepool.pool.snap
sending from @ to zonepool/zoneftd/rpool/ROOT/solaris@install
sending from @install to zonepool/zoneftd/rpool/ROOT/solaris@2015-12-19-20:27:04
sending from @2015-12-19-20:27:04 to zonepool/zoneftd/rpool/ROOT/solaris@zonepool.pool.snap
sending from @ to zonepool/zoneftd/rpool/ROOT/solaris/var@install
sending from @install to zonepool/zoneftd/rpool/ROOT/solaris/var@2015-12-19-20:27:04
sending from @2015-12-19-20:27:04 to zonepool/zoneftd/rpool/ROOT/solaris/var@zonepool.pool.snap
sending from @ to zonepool/zoneftd/rpool/VARSHARE@zonepool.pool.snap
sending from @ to zonepool/zoneftd/rpool/export@zonepool.pool.snap
sending from @ to zonepool/zoneftd/rpool/export/home@zonepool.pool.snap
sending from @ to zonepool/zoneftd/rpool/export/home/aldo@zonepool.pool.snap
sending from @ to zonepool/zoneftd/rpool/ROOT/backup@zonepool.pool.snap
sending from @ to zonepool/zoneftd/rpool/ROOT/backup/var@zonepool.pool.snap
#########################################################################
Deleting snapshot.
#########################################################################
#########################################################################
Finished zonepool at 20/06/16 17:30:59
#########################################################################
```

```bash
$ ls -lrthR /backups/snaps/$(uname -n)/$(date +%d_%m_%y)
/backups/snaps/sol11/20_06_16:
total 6
drwxr-xr-x   2 root     root           8 Jun 20 17:18 rpool
drwxr-xr-x   2 root     root           8 Jun 20 17:29 zonepool

/backups/snaps/sol11/20_06_16/rpool:
total 3059275
-rw-r--r--   1 root     root         989 Jun 20 17:18 rpool.pool_properties
-rw-r--r--   1 root     root        2.9K Jun 20 17:18 rpool.zfs_pool_list
-rw-r--r--   1 root     root        231K Jun 20 17:18 rpool.zfs_properties
-rw-r--r--   1 root     root         205 Jun 20 17:18 rpool.pool_status
-rw-r--r--   1 root     root         566 Jun 20 17:18 rpool_c7t0d0
-rw-r--r--   1 root     root        1.5G Jun 20 17:29 rpool.pool.snap.gz

/backups/snaps/sol11/20_06_16/zonepool:
total 478484
-rw-r--r--   1 root     root        1.0K Jun 20 17:29 zonepool.pool_properties
-rw-r--r--   1 root     root         966 Jun 20 17:29 zonepool.zfs_pool_list
-rw-r--r--   1 root     root         89K Jun 20 17:29 zonepool.zfs_properties
-rw-r--r--   1 root     root         208 Jun 20 17:29 zonepool.pool_status
-rw-r--r--   1 root     root         513 Jun 20 17:29 zonepool_c7t8d0
-rw-r--r--   1 root     root        233M Jun 20 17:30 zonepool.pool.snap.gz

zpool list
NAME       SIZE  ALLOC   FREE  CAP  DEDUP  HEALTH  ALTROOT
rpool     15.6G  6.44G  9.19G  41%  1.00x  ONLINE  -
zonepool  11.9G   438M  11.5G   3%  1.00x  ONLINE  -

```
