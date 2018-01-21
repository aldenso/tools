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

if [ "$EUID" -ne 0 ]
then
    echo "You need root privileges"; exit 1
fi

DATE=$(date +%d%m%y_%H%M%S)
LSBLKFILE="lsblkfile_$DATE.txt"
BLKIDFILE="blkidfile_$DATE.txt"
LSSCSIFILE="lsscsifile_$DATE.txt"
MULTIPATHFILE="multipathfile_$DATE.txt"
ASMLISTFILE="asmlistfile_$DATE.txt"
ASMMULTIPATHFILE="asmmultipathfile_$DATE.txt"
ASMDEVSFILE="asmdevsfile_$DATE.txt"

continue="NO"
scriptfile="typescript.temp"

CheckSOVersion() {
    python -c 'import yum; yb = yum.YumBase(); print yb.conf.yumvar["releasever"]' | tail -1
}

CheckLSSCSI() {
    if command -v lsscsi > /dev/null
    then 
        echo "lsscsi is installed"; continue="YES"
    else
        echo "lsscsi not installed"; continue="NO"
    fi
}

CheckMultipath() {
    if command -v multipath > /dev/null
    then
        echo "Multipath is installed"; continue="YES"
    else
        echo "Multipath not installed"; continue="NO"
    fi
}

CheckASM() {
    if command -v oracleasm > /dev/null
    then
        echo "Oracle ASM is installed"; continue="YES"
    else
        echo "Oracla ASM not installed"; continue="NO"
    fi
}


CreateFiles() {
    echo "Gathering info from disks (lsblk, blkid, lsscsi, multipath and ASM)"
    version=$(CheckSOVersion)
    if [ "$version" == "7Server" ]
    then
        lsblk -l -o NAME,KNAME,TYPE,HCTL,VENDOR,MODEL,SIZE,LABEL,UUID,SERIAL,STATE| grep -E \
            "part|disk|NAME" | grep -v fd > "$LSBLKFILE"
    else
        lsblk -l -o NAME,KNAME,TYPE,MODEL,SIZE,LABEL,UUID,STATE| grep -E "part|disk|NAME" \
            | grep -v fd > "$LSBLKFILE"
    fi

    blkid | sort > "$BLKIDFILE" 2>/dev/null

    CheckLSSCSI
    if [ "$continue" == "YES" ]
    then
        # unbuffered lsscsi version to be able to handle the ouput, and compare to a float
        lsscsiversion=$(script -c "lsscsi -V" $scriptfile | grep version | awk '{print $2}'| head -1)
        rm $scriptfile
        var=$(echo "$lsscsiversion >= 0.27" | bc -l)
        if [ "$var" -eq 1 ]
        then
            lsscsi -is| grep disk > "$LSSCSIFILE"
        else
            lsscsi |grep disk > "$LSSCSIFILE"
        fi
    fi

    CheckMultipath
    if [ "$continue" == "YES" ]
    then
        multipath -ll > "$MULTIPATHFILE"
    fi

    CheckASM
    if [ "$continue" == "YES" ]
    then
        oracleasm listdisks > "$ASMLISTFILE"
        if [ -f "$MULTIPATHFILE" ]
        then
            disks=$(grep "dm-" "$MULTIPATHFILE" | awk '{print $1}')
            for disk in $disks
            do
                oracleasm querydisk /dev/mapper/"$disk" >> "$ASMMULTIPATHFILE" 2>&1
            done
        fi
        parts=$(grep part "$LSBLKFILE" | grep -v "dm-" | awk '{print $1}')
        for part in $parts
        do
            oracleasm querydisk /dev/"$part" >> "$ASMDEVSFILE" 2>&1
        done
    fi
}

###################################################################################################
CreateFiles
echo "Done"
