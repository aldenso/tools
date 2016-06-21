Solaris tools
=============

##### zfs_snapshots_backups.sh:

Script to backup zpools (useful to recover zones or ldoms with lots of zones with dedicated pools) using snapshots and gzip to save some space, is not fast, but you save a lot of space (compression are something better than 10 to 1, but depends on the data), the script uses a Backup filesystem (NFS on 10GB or 40GB network), creates a dir tree based on the hostname and pool names, takes also the important data from zfs, disk and pool (necessary for disaster recovery).

**Note**: make sure you have enough space to launch the backups (snapshots creation and backup filesystem)

Output sample:
```
# ./zfs_snapshots_backups.sh
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
```

```bash
$ ls -lrthR /backups/snaps/$(uname -n)/$(date +%d_%m_%y)
/backups/snaps/sol11/20_06_16:
total 3
drwxr-xr-x   2 root     root           8 Jun 20 16:23 zonepool

/backups/snaps/sol11/20_06_16/zonepool:
total 478472
-rw-r--r--   1 root     root        1.0K Jun 20 16:23 zonepool.pool_properties
-rw-r--r--   1 root     root         966 Jun 20 16:23 zonepool.zfs_pool_list
-rw-r--r--   1 root     root         89K Jun 20 16:23 zonepool.zfs_properties
-rw-r--r--   1 root     root         208 Jun 20 16:23 zonepool.pool_status
-rw-r--r--   1 root     root         513 Jun 20 16:23 zonepool_c7t8d0
-rw-r--r--   1 root     root        233M Jun 20 16:24 zonepool.pool.snap.gz
```
