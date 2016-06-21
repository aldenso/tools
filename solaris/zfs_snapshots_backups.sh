#!/bin/bash
# @Author: Aldo Sotolongo
# @Date:   2016-06-20T19:11:53-04:30
# @Email:  aldenso@gmail.com
# @Last modified by:   Aldo Sotolongo
# @Last modified time: 2016-06-20T21:00:48-04:30
# Description: zpools backups using zfs snapshots and gzip to save some space,
# you need to have remote filesystem mounted.

BACKUPDIR="/backups"
DATE=$(date +%d_%m_%y)
POOLEXCLUDE="" #Ex. POOLEXCLUDE="rpool bigpool"
HASH="#########################################################################"

# Check if the backups nfs is mounted.
if $(mount | grep -w "$BACKUPDIR" > /dev/null 2>&1 );
then
  # List all zfs pools
  # if you don't want to backup rpool then remove the comment on the next line and comment the one after.
  # pools=$(zpool list | awk '{print $1}' | egrep -v "NAME|rpool")
  pools=$(zpool list | awk '{print $1}' | egrep -v "NAME")

  #Pool exclusion
  for EXCLUDE in $POOLEXCLUDE
  do
    pools=$(echo $pools | sed "s/$EXCLUDE//g")
  done

  for pool in $pools;
  do
    # Create the destiny dirs if they don't exist.
    test ! -d "$BACKUPDIR"/snaps/"$(uname -n)"/"$DATE"/"$pool" && mkdir -p \
    "$BACKUPDIR"/snaps/"$(uname -n)"/"$DATE"/"$pool"

    # zpool pool_properties.
    echo $HASH
    echo "Get $pool properties"
    echo $HASH
    zpool get all "$pool" > "$BACKUPDIR"/snaps/"$(uname -n)"/"$DATE"/"$pool"/"$pool".pool_properties

    # zfs list in pool.
    echo $HASH
    echo "Get zfs list in $pool"
    echo $HASH
    zfs list -r "$pool" > "$BACKUPDIR"/snaps/"$(uname -n)"/"$DATE"/"$pool"/"$pool".zfs_pool_list

    # properties for zfs in pool.
    echo $HASH
    echo "Get zfs properties in $pool"
    echo $HASH
    zfs list -r "$pool" | awk '{print $1}' | grep -v NAME | xargs zfs get all > \
     "$BACKUPDIR"/snaps/"$(uname -n)"/"$DATE"/"$pool"/"$pool".zfs_properties

     # pool status.
     echo $HASH
     echo "Get $pool status"
     echo $HASH
     zpool status "$pool" > "$BACKUPDIR"/snaps/"$(uname -n)"/"$DATE"/"$pool"/"$pool".pool_status

    # disks vtoc for pool.
    echo $HASH
    echo "Get VTOC from disks in $pool"
    echo $HASH
    disks=$(zpool status "$pool" | grep "c.t." | awk '{print $1}')
    for disk in $disks
    do
      prtvtoc /dev/rdsk/"$disk" > "$BACKUPDIR"/snaps/"$(uname -n)"/"$DATE"/"$pool"/"$pool"_"$disk"
    done

    # create zpool snapshot.
    echo $HASH
    echo "Creating snapshot $pool@$pool.snap"
    echo $HASH
    zfs snapshot -r "$pool"@"$pool".pool.snap

    # Optional, you can remove the next block, but I don't need dump and swap
    # to be in the backup, plus you can save a lot of space.
    if [ "$pool" == "rpool" ]
    then
      echo $HASH
      echo "Removing dump and swap from rpool snapshot"
      echo $HASH
    	zfs destroy "$pool"/dump@"$pool".pool.snap
    	zfs destroy "$pool"/swap@"$pool".pool.snap
    fi

    # Send the snapshot stream to the backup directory.
    echo $HASH
    echo "Sending $pool@$pool.pool.snap stream"
    echo $HASH
    zfs send -Rv "$pool"@"$pool".pool.snap | gzip > \
    "$BACKUPDIR"/snaps/"$(uname -n)"/"$DATE"/"$pool"/"$pool".pool.snap.gz

    # delete the snapshot.
    echo $HASH
    echo "Deleting snapshot."
    echo $HASH
    zfs destroy -r "$pool"@"$pool".pool.snap
  done

else
  echo "Filesystem $BACKUPDIR is not mounted."
fi
exit
