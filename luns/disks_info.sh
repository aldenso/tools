#!/bin/bash
#==============================================================================
# Author: Aldo Sotolongo
# Email:  aldenso@gmail.com
# Description: Script to generate files with important info related to disks
# for RED HAT and Oracle Linux, useful when working with FC luns and Oracle
# Databases.
#==============================================================================
# Notes:
# lssci version >= 0.27 supports --size (-s) and --scsi_id (-i)

LSBLKFILE="lsblkfile.txt"
BLKIDFILE="blkidfile.txt"
LSSCSIFILE="lsscsifile.txt"

CheckSOVersion() {
    python -c 'import yum, pprint; yb = yum.YumBase(); print yb.conf.yumvar["releasever"]' | tail -1
}

CheckLSSCSI() {
    if command -v lsscsi > /dev/null
    then 
        echo "lsscsi is installed"
    else
        echo "lsscsi not installed"; exit 1
    fi
}


CreateFiles() {
    echo "Gathering info from disks (lsblk, blkid and lsscsi)"
    version=$(CheckSOVersion)
    if [ "$version" == "7Server" ]
    then
        lsblk -l -o NAME,KNAME,TYPE,HCTL,VENDOR,MODEL,SIZE,LABEL,UUID,SERIAL,STATE| grep -E \
            "part|disk|NAME" | grep -v fd > $LSBLKFILE
    else
        lsblk -l -o NAME,KNAME,TYPE,MODEL,SIZE,LABEL,UUID,STATE| grep -E "part|disk|NAME" \
            grep -v fd > $LSBLKFILE
    fi

    blkid| grep -E -v "/dev/mapper|xfs" | sort > $BLKIDFILE 2>/dev/null

    CheckLSSCSI
    # unbuffered lsscsi version to be able to handle the ouput, and compare to a float
    lsscsiversion=$(script -c "lsscsi -V" | awk '{print $2}'| head -1)
    var=$(echo "$lsscsiversion >= 0.27" | bc -l)
    if [ "$var" -eq 1 ]
    then
        lsscsi -is| grep disk > $LSSCSIFILE
    else
        lsscsi |grep disk > $LSSCSIFILE
    fi
}

###################################################################################################
CreateFiles
echo "Done"